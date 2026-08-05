"""
Background worker observers for MorphUI.

This module provides observer helpers that bridge background workers
(callables run on a daemon thread, exposing plain ``busy``/``status``/
``progress``/``cancel`` attributes) with widgets that display that
state. Polling happens on the Kivy clock so widget updates always
occur on the main thread.

Classes
-------
ProgressObserver
    Starts a worker on a thread and mirrors its progress onto a widget.
"""
from typing import Any
from typing import Callable

from threading import Thread

from kivy.clock import Clock
from kivy.clock import ClockEvent


__all__ = [
    'ProgressObserver',]


class ProgressObserver:
    """Observer class that runs a background worker on a thread and
    updates a widget with its current status and progress.

    The observer periodically checks the worker's status and progress,
    and updates the widget accordingly. If the observer's :attr:`cancel`
    flag is set to ``True``, it requests cancellation of the worker's
    task. The observer polls until the worker finishes its task, then
    fires the applicable ``on_success``/``on_failure``/``on_completion``
    callback.

    Parameters
    ----------
    worker : Any
        The background worker whose progress is being observed. The
        worker must be callable (it is run via
        ``Thread(target=worker, ...)``) and must have the following
        attributes:
        - ``busy``: A boolean indicating whether the worker is still
          busy.
        - ``status``: A string representing the current status of the
          worker's task.
        - ``progress``: A float between 0 and 1 representing the
          current progress of the worker's task.
        - ``cancel``: A boolean that can be set to ``True`` to request
          cancellation of the worker's task.
        - ``success`` (optional): A boolean indicating whether the
          task completed successfully. If absent, completion is always
          treated as a success.
    widget : Any
        The widget that displays the progress of the worker's task. The
        widget must have the following attributes:
        - ``busy``: A boolean indicating whether the widget is in a
          busy state (e.g., showing a progress indicator).
        - ``status``: A string representing the current status to be
          displayed on the widget.
        - ``progress``: A float between 0 and 1 representing the
          current progress to be displayed on the widget.
        - ``cancel``: A boolean that can be set to ``True`` to allow
          cancellation of the worker's task from the widget.
    interval : float, optional
        The polling interval in seconds passed to
        :meth:`~kivy.clock.CyClockBase.schedule_interval`. Defaults to
        ``0.1``.
    on_success : Callable[[], None], optional
        Called once after the worker finishes if ``worker.success`` is
        truthy (or absent). Overrides the :meth:`on_success` method.
    on_failure : Callable[[], None], optional
        Called once after the worker finishes if ``worker.success`` is
        falsy. Overrides the :meth:`on_failure` method.
    on_completion : Callable[[], None], optional
        Called once after the worker finishes, regardless of success or
        failure. Overrides the :meth:`on_completion` method.

    Examples
    --------
    ```python
    from morphui.utils import ProgressObserver

    class Worker:
        busy = False
        status = ''
        progress = 0.0
        cancel = False
        success = True

        def __call__(self):
            self.busy = True
            for i in range(100):
                if self.cancel:
                    self.status = 'Cancelled'
                    self.success = False
                    break
                self.progress = i / 99
                self.status = f'Processing {i + 1}/100'
            self.busy = False

    observer = ProgressObserver(Worker(), my_widget)
    observer.start()
    ```
    """

    _required_attrs = ('busy', 'cancel', 'progress', 'status')
    """Attributes both the worker and widget are required to expose."""

    worker: Any
    """The background worker being run and observed."""

    widget: Any
    """The widget being updated with the worker's progress."""

    interval: float
    """Polling interval in seconds used for the clock event."""

    cancel: bool
    """Set to ``True`` to request cancellation of the ongoing task.

    Propagated to both :attr:`widget` and :attr:`worker` on the next
    poll.
    """

    _clock_event: ClockEvent | None
    """Handle for the :meth:`~kivy.clock.CyClockBase.schedule_interval`
    event used to poll the worker. ``None`` while not running."""

    _worker_thread: Thread | None
    """The daemon thread the worker is running on. ``None`` while not
    running."""

    def __init__(
            self,
            worker: Any,
            widget: Any,
            interval: float = 0.1,
            on_success: Callable[[], None] | None = None,
            on_failure: Callable[[], None] | None = None,
            on_completion: Callable[[], None] | None = None,
            ) -> None:
        assert all(hasattr(worker, attr) for attr in self._required_attrs), (
            f'Worker must have attributes: {", ".join(self._required_attrs)}')
        assert all(hasattr(widget, attr) for attr in self._required_attrs), (
            f'Widget must have attributes: {", ".join(self._required_attrs)}')

        self.worker = worker
        self.widget = widget
        self.interval = interval
        self.cancel = False
        self._clock_event = None
        self._worker_thread = None
        if callable(on_success):
            self.on_success = on_success
        if callable(on_failure):
            self.on_failure = on_failure
        if callable(on_completion):
            self.on_completion = on_completion

    @property
    def is_running(self) -> bool:
        """Whether the observer is currently polling the worker."""
        return self._clock_event is not None

    def start(self, **kwargs) -> None:
        """Start the worker on a daemon thread and begin polling its
        progress.

        Does nothing if the observer is already running.

        Parameters
        ----------
        **kwargs : Any
            Forwarded to the worker call.
        """
        if self.is_running:
            return

        self.cancel = False
        self.widget.busy = True
        self._worker_thread = Thread(
            target=self.worker,
            kwargs=kwargs,
            daemon=True,
            name='ProgressObserverWorker')
        self._worker_thread.start()
        self._clock_event = Clock.schedule_interval(self._poll, self.interval)

    __call__ = start

    def stop(self) -> None:
        """Stop polling the worker.

        Does nothing if the observer is not currently running. Note
        that this only stops polling; it does not itself request
        cancellation of the worker's task, use :attr:`cancel` for that.
        """
        if self._clock_event is None:
            return

        self._clock_event.cancel()
        self._clock_event = None

    def _poll(self, dt: float) -> None:
        """Poll the worker once per clock tick (called by Kivy's clock).

        Runs on the main thread, so widget property writes are safe.
        Stops the observer and fires the appropriate callbacks once the
        worker is no longer busy.

        Parameters
        ----------
        dt : float
            Time elapsed since the last call, provided by the Kivy
            clock. Unused.
        """
        if self.cancel:
            self.widget.cancel = True
            self.worker.cancel = True

        self.update_view()

        if self.worker.busy:
            return

        self.stop()
        self.widget.busy = False
        if getattr(self.worker, 'success', True):
            self.on_success()
        else:
            self.on_failure()
        self.on_completion()

    def update_view(self) -> None:
        """Update the widget's status and progress based on the
        worker's current status and progress. This method can be
        called periodically to refresh the widget's display.
        """
        self.widget.status = self.worker.status
        self.widget.progress = self.worker.progress

    def on_success(self) -> None:
        """Callback called when the worker successfully completes its
        task. This can be used to perform any necessary cleanup or
        updates to the widget after a successful completion."""

    def on_failure(self) -> None:
        """Callback called when the worker fails to complete its task.
        This can be used to perform any necessary cleanup or updates
        to the widget after a failure."""

    def on_completion(self) -> None:
        """Callback called when the worker completes its task,
        regardless of success or failure. This can be used to perform
        any necessary cleanup or updates to the widget after
        completion."""
