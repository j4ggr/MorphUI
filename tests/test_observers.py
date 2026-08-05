import sys
import pytest

from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).parent.resolve()))

from morphui.utils.observers import ProgressObserver


class FakeWorker:
    """Minimal callable worker exposing the attributes ProgressObserver
    requires."""

    def __init__(
            self,
            busy: bool = True,
            status: str = '',
            progress: float = 0.0,
            cancel: bool = False,
            success: bool | None = None) -> None:
        self.busy = busy
        self.status = status
        self.progress = progress
        self.cancel = cancel
        if success is not None:
            self.success = success
        self.call_kwargs = None

    def __call__(self, **kwargs) -> None:
        self.call_kwargs = kwargs


class FakeWidget:
    """Minimal widget exposing the attributes ProgressObserver
    requires."""

    def __init__(self) -> None:
        self.busy = False
        self.status = ''
        self.progress = 0.0
        self.cancel = False


class TestProgressObserverInit:

    def test_missing_worker_attrs_raises(self) -> None:
        with pytest.raises(AssertionError):
            ProgressObserver(object(), FakeWidget())

    def test_missing_widget_attrs_raises(self) -> None:
        with pytest.raises(AssertionError):
            ProgressObserver(FakeWorker(), object())

    def test_defaults(self) -> None:
        observer = ProgressObserver(FakeWorker(), FakeWidget())
        assert observer.interval == 0.1
        assert observer.cancel is False
        assert observer.is_running is False

    def test_custom_callbacks_override_methods(self) -> None:
        on_success = Mock()
        on_failure = Mock()
        on_completion = Mock()
        observer = ProgressObserver(
            FakeWorker(), FakeWidget(),
            on_success=on_success,
            on_failure=on_failure,
            on_completion=on_completion)
        assert observer.on_success is on_success
        assert observer.on_failure is on_failure
        assert observer.on_completion is on_completion


class TestProgressObserverStart:

    def test_start_sets_busy_and_schedules_polling(self) -> None:
        worker = FakeWorker()
        widget = FakeWidget()
        observer = ProgressObserver(worker, widget)

        with patch('morphui.utils.observers.Thread') as mock_thread_cls, \
             patch('morphui.utils.observers.Clock.schedule_interval') as mock_schedule:
            observer.start(foo='bar')

        assert widget.busy is True
        assert observer.cancel is False
        mock_thread_cls.assert_called_once_with(
            target=worker, kwargs={'foo': 'bar'}, daemon=True,
            name='ProgressObserverWorker')
        mock_thread_cls.return_value.start.assert_called_once()
        mock_schedule.assert_called_once_with(observer._poll, observer.interval)
        assert observer.is_running is True

    def test_start_noop_when_already_running(self) -> None:
        observer = ProgressObserver(FakeWorker(), FakeWidget())
        with patch('morphui.utils.observers.Thread'), \
             patch('morphui.utils.observers.Clock.schedule_interval') as mock_schedule:
            observer.start()
            observer.start()

        mock_schedule.assert_called_once()

    def test_call_is_alias_for_start(self) -> None:
        observer = ProgressObserver(FakeWorker(), FakeWidget())
        with patch('morphui.utils.observers.Thread'), \
             patch('morphui.utils.observers.Clock.schedule_interval'):
            observer()

        assert observer.is_running is True


class TestProgressObserverStop:

    def test_stop_cancels_clock_event(self) -> None:
        observer = ProgressObserver(FakeWorker(), FakeWidget())
        mock_event = Mock()
        observer._clock_event = mock_event

        observer.stop()

        mock_event.cancel.assert_called_once()
        assert observer._clock_event is None
        assert observer.is_running is False

    def test_stop_noop_when_not_running(self) -> None:
        observer = ProgressObserver(FakeWorker(), FakeWidget())
        observer.stop()  # Should not raise.
        assert observer.is_running is False


class TestProgressObserverPoll:

    def test_poll_updates_widget_while_busy(self) -> None:
        worker = FakeWorker(busy=True, status='Working', progress=0.4)
        widget = FakeWidget()
        observer = ProgressObserver(worker, widget)
        observer._clock_event = Mock()

        observer._poll(0)

        assert widget.status == 'Working'
        assert widget.progress == 0.4
        assert observer.is_running is True

    def test_poll_propagates_cancel_flag(self) -> None:
        worker = FakeWorker(busy=True)
        widget = FakeWidget()
        observer = ProgressObserver(worker, widget)
        observer._clock_event = Mock()
        observer.cancel = True

        observer._poll(0)

        assert widget.cancel is True
        assert worker.cancel is True

    def test_poll_stops_and_calls_on_success_when_worker_finishes(self) -> None:
        worker = FakeWorker(busy=False, status='Done', progress=1.0)
        widget = FakeWidget()
        on_success = Mock()
        on_failure = Mock()
        on_completion = Mock()
        observer = ProgressObserver(
            worker, widget,
            on_success=on_success, on_failure=on_failure,
            on_completion=on_completion)
        observer._clock_event = Mock()

        observer._poll(0)

        assert widget.busy is False
        assert observer.is_running is False
        on_success.assert_called_once()
        on_failure.assert_not_called()
        on_completion.assert_called_once()

    def test_poll_calls_on_failure_when_worker_reports_failure(self) -> None:
        worker = FakeWorker(busy=False, success=False)
        widget = FakeWidget()
        on_success = Mock()
        on_failure = Mock()
        observer = ProgressObserver(
            worker, widget, on_success=on_success, on_failure=on_failure)
        observer._clock_event = Mock()

        observer._poll(0)

        on_failure.assert_called_once()
        on_success.assert_not_called()

    def test_poll_treats_missing_success_attr_as_success(self) -> None:
        worker = FakeWorker(busy=False)
        assert not hasattr(worker, 'success')
        widget = FakeWidget()
        on_success = Mock()
        observer = ProgressObserver(worker, widget, on_success=on_success)
        observer._clock_event = Mock()

        observer._poll(0)

        on_success.assert_called_once()


class TestProgressObserverUpdateView:

    def test_update_view_mirrors_worker_state(self) -> None:
        worker = FakeWorker(status='Halfway', progress=0.5)
        widget = FakeWidget()
        observer = ProgressObserver(worker, widget)

        observer.update_view()

        assert widget.status == 'Halfway'
        assert widget.progress == 0.5
