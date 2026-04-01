
from kivy.app import App

from morphui.theme.manager import ThemeManager
from morphui.theme.typography import Typography

    

__all__ = [
    'MorphApp',]


class MorphApp(App):
    """Base application class for MorphUI applications.

    Subclass ``MorphApp`` instead of Kivy's ``App`` to get automatic
    access to the shared ``ThemeManager`` and ``Typography`` instances.
    Configure the theme in :meth:`build` before returning the root
    widget.

    Examples
    --------
    Minimal application:

    ```python
    from morphui.app import MorphApp
    from morphui.uix.boxlayout import MorphBoxLayout
    from morphui.uix.label import MorphLabel

    class MyApp(MorphApp):
        def build(self):
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'Blue'
            return MorphBoxLayout(
                MorphLabel(text="Hello, MorphUI!"),
            )

    if __name__ == '__main__':
        MyApp().run()
    ```

    Theme configuration:

    ```python
    class MyApp(MorphApp):
        def build(self):
            tm = self.theme_manager
            tm.theme_mode = 'Dark'
            tm.seed_color = 'Orange'
            tm.color_scheme = 'VIBRANT'
            tm.color_scheme_contrast = 0.0
            return self.create_ui()
    ```

    See Also
    --------
    ThemeManager : Manages the dynamic color palette and theme mode.
    Typography : Provides font registration and text role management.
    """

    _theme_manager: ThemeManager = ThemeManager()
    """Theme manager instance for handling theming and styles."""

    _typography: Typography = Typography()
    """Typography instance for managing fonts and text styles."""

    @property
    def theme_manager(self) -> ThemeManager:
        """Access the theme manager for theming and style management.
        (read-only).

        The :attr:`theme_manager` attribute provides access to the
        :class:`ThemeManager` instance, which handles theming and style
        management. This instance is automatically initialized as a
        class attribute.
        """
        return self._theme_manager

    @property
    def typography(self) -> Typography:
        """Access the typography system for text style management.
        (read-only).

        The :attr:`typography` attribute provides access to the
        :class:`Typography` instance, which handles font registration
        and text style management. This instance is automatically
        initialized as a class attribute.
        """
        return self._typography
