"""Example application demonstrating the MorphDialog widget with various
configurations and use cases.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))

from kivy.metrics import dp

from morphui.app import MorphApp
from morphui.uix.label import MorphLabel
from morphui.uix.label import MorphHeadingLabel
from morphui.uix.button import MorphButton
from morphui.uix.button import MorphIconButton
from morphui.uix.dialog import MorphDialog
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.gridlayout import MorphGridLayout
from morphui.uix.floatlayout import MorphFloatLayout


class DialogExampleApp(MorphApp):

    def build(self) -> MorphFloatLayout:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_teal'

        # Create buttons to demonstrate different dialog types
        main_layout = MorphFloatLayout(
            MorphGridLayout(
                MorphButton(
                    text="Simple Dialog",
                    on_release=self.show_simple_dialog),
                MorphButton(
                    text="Confirmation Dialog",
                    on_release=self.show_confirmation_dialog),
                MorphButton(
                    text="Alert Dialog",
                    on_release=self.show_alert_dialog),
                MorphButton(
                    text="Custom Dialog",
                    on_release=self.show_custom_dialog),
                MorphButton(
                    text="No Backdrop Dismiss",
                    on_release=self.show_no_backdrop_dialog),
                MorphButton(
                    text="Large Content Dialog",
                    on_release=self.show_large_content_dialog),
                cols=2,
                spacing=dp(10),
                padding=dp(20),
                auto_size=(True, True),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}),
            theme_color_bindings={
                'normal_surface_color': 'surface_color'})
        
        return main_layout

    def show_simple_dialog(self, *args) -> None:
        """Show a simple dialog with a title and message."""
        dialog = MorphDialog(
            MorphHeadingLabel(
                text="Simple Dialog",),
            MorphLabel(
                text="This is a simple dialog with a title and message.\nClick outside to dismiss.",
                auto_size=True,),)
        dialog.open()

    def show_confirmation_dialog(self, *args) -> None:
        """Show a confirmation dialog with action buttons."""
        dialog = MorphDialog(
            MorphHeadingLabel(
                text="Confirm Action",),
            MorphLabel(
                text="Are you sure you want to proceed with this action?",
                auto_size=True,),
            MorphBoxLayout(
                MorphButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()),
                MorphButton(
                    text="Confirm",
                    on_release=lambda x: (
                        print("Action confirmed!"),
                        dialog.dismiss())),
                orientation='horizontal',
                spacing=dp(10),
                size_hint=(1, None),
                auto_size=(False, True)),)
        dialog.open()

    def show_alert_dialog(self, *args) -> None:
        """Show an alert dialog with an icon."""
        dialog = MorphDialog(
            MorphBoxLayout(
                MorphIconButton(
                    icon='alert-circle',
                    theme_color_bindings={
                        'icon_color': 'error_color'}),
                MorphHeadingLabel(
                    text="Alert!",),
                orientation='horizontal',
                spacing=dp(10),
                size_hint=(1, None),
                auto_size=(False, True)),
            MorphLabel(
                text="This is an alert message. Something requires your attention.",
                auto_size=(True, True),),
            MorphButton(
                text="OK",
                on_release=lambda x: dialog.dismiss(),),)
        dialog.open()

    def show_custom_dialog(self, *args) -> None:
        """Show a dialog with custom styling."""
        dialog = MorphDialog(
            MorphHeadingLabel(
                text="Custom Styled Dialog",),
            MorphLabel(
                text="This dialog has custom colors and styling.",
                auto_size=True,),
            MorphButton(
                text="Close",
                on_release=lambda x: dialog.dismiss(),),
            theme_color_bindings={
                'normal_surface_color': 'primary_container_color',
                'normal_text_color': 'on_primary_container_color'})
        # Custom scrim color (more transparent)
        dialog.scrim_color = [0, 0, 0, 0.3]
        dialog.open()

    def show_no_backdrop_dialog(self, *args) -> None:
        """Show a dialog that doesn't dismiss when clicking outside."""
        dialog = MorphDialog(
            MorphHeadingLabel(
                text="No Backdrop Dismiss",),
            MorphLabel(
                text="This dialog won't close when you click outside. You must click the Close button.",
                auto_size=(True, True)),
            MorphButton(
                text="Close",
                on_release=lambda x: dialog.dismiss(),),
            backdrop_dismiss=False)
        dialog.open()

    def show_large_content_dialog(self, *args) -> None:
        """Show a dialog with larger content area."""
        # Create multiple lines of text
        lines = [
            "This is a dialog with more content.",
            "",
            "It demonstrates how the dialog handles",
            "larger amounts of text and content.",
            "",
            "The dialog will automatically constrain",
            "itself within the window bounds while",
            "respecting the configured margins.",
            "",
            "You can scroll if needed, and the dialog",
            "will maintain its size limits.",
        ]
        
        dialog = MorphDialog(
            MorphHeadingLabel(
                text="Large Content Dialog",),
            MorphLabel(
                text="\n".join(lines),
                auto_size=True,),
            MorphBoxLayout(
                MorphButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()),
                MorphButton(
                    text="Accept",
                    on_release=lambda x: (
                        print("Accepted!"),
                        dialog.dismiss())),
                orientation='horizontal',
                spacing=dp(10),
                size_hint=(1, None),
                auto_size=(False, True)),)
        dialog.open()


if __name__ == '__main__':
    DialogExampleApp().run()
