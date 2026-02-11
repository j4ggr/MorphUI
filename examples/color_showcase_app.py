from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window

from morphui.app import MorphApp
from morphui.uix.label import MorphLabel
from morphui.uix.button import MorphIconButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.behaviors import MorphScaleBehavior
from morphui.uix.behaviors import MorphToggleButtonBehavior
from morphui.theme.palette import create_color_property_mapping


SUBBOX_WIDTH = 250
COLUMN_SPACING = 8
ROW_SPACING = COLUMN_SPACING * 2

COLORS = create_color_property_mapping()

class ThemeToggleButton(
        MorphScaleBehavior,
        MorphToggleButtonBehavior,
        MorphIconButton):

    def __init__(self, **kwargs) -> None:
        kwargs = dict(
            on_release=self.theme_manager.toggle_theme_mode,
            normal_icon='brightness-3',
            active_icon='brightness-5',
            identity='theme_toggle_button',
            ) | kwargs
        super().__init__(**kwargs)
        self.theme_manager.bind(is_dark_mode=self.setter('active'))
        self.active = self.theme_manager.is_dark_mode


class ColorLabel(MorphLabel):
    default_config = dict(
        size_hint_y=None,
        auto_width=False,
        auto_height=True,
        padding=[4, 8],)


class ColorShowcaseApp(MorphApp):
    """Example application showcasing MorphUI color themes."""
    
    def build(self) -> MorphBoxLayout:
        """Build the main application interface."""
        self.theme_manager.register_seed_color('morphui_teal', '#00b8c2')
        self.theme_manager.register_seed_color('morphui_gold', '#fbc12d')
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_gold'
        self.theme_manager.color_scheme = 'RAINBOW'
        
        self.layout = MorphBoxLayout(
            MorphBoxLayout(
                ThemeToggleButton(),
                Widget(),
                identity='navigation_box',
                orientation='vertical',
                auto_width=True,
                spacing=4,
                padding=[8, 4],),
            MorphBoxLayout(
                MorphBoxLayout(
                    create_category_box('primary'),
                    create_category_box('secondary'),
                    create_category_box('tertiary'),
                    create_category_box('error'),
                    identity='category_box',
                    orientation='horizontal',
                    spacing=COLUMN_SPACING,
                    auto_size=True,),
                MorphBoxLayout(
                    create_fixed_box('primary'),
                    create_fixed_box('secondary'),
                    create_fixed_box('tertiary'),
                    identity='fixed_box',
                    orientation='horizontal',
                    spacing=COLUMN_SPACING,
                    auto_size=True,),
                MorphBoxLayout(
                    create_surface_box(),
                    create_inverse_box(),
                    identity='inverse_box',
                    orientation='horizontal',
                    spacing=COLUMN_SPACING,
                    auto_size=True,),
                # Widget(),
                identity='output_box',
                orientation='vertical',
                spacing=ROW_SPACING,
                auto_size=True,),
            identity='main_layout',
            orientation='horizontal',
            theme_color_bindings={
                'normal_surface_color': 'background_color',},
            padding=[0, 16, 16, 16],
            auto_size=True,)
        
        Clock.schedule_once(self.set_window_size, 0.1)
        
        return self.layout
    
    def set_window_size(self, *args) -> None:
        """Set initial focus to the theme toggle button."""
        Window.size = (
            self.layout.minimum_width + 30,
            self.layout.minimum_height)
    

def create_category_box(category_name) -> MorphBoxLayout:
    """Create a box layout for a color category."""
    box = MorphBoxLayout(
        ColorLabel(
            text=f'{category_name.capitalize()}',
            theme_color_bindings={
                'normal_surface_color': f'{category_name}_color',
                'normal_content_color': f'content_{category_name}_color'},),
        ColorLabel(
            text=f'Content {category_name}',
            theme_color_bindings={
                'normal_surface_color': f'content_{category_name}_color',
                'normal_content_color': f'{category_name}_color'},),
        ColorLabel(
            text=f'{category_name.capitalize()} Container',
            theme_color_bindings={
                'normal_surface_color': f'{category_name}_container_color',
                'normal_content_color': f'content_{category_name}_container_color'},),
        ColorLabel(
            text=f'Content {category_name} Container',
            theme_color_bindings={
                'normal_surface_color': f'content_{category_name}_container_color',
                'normal_content_color': f'{category_name}_container_color'},),
        orientation='vertical',
        size_hint= (None, None),
        auto_height=True,
        width=SUBBOX_WIDTH,)
    return box


def create_fixed_box(category_name) -> MorphBoxLayout:
    """Create a box layout for a fixed color category."""
    box = MorphBoxLayout(
        MorphBoxLayout(
            ColorLabel(
                text=f'{category_name.capitalize()} Fixed',
                theme_color_bindings={
                    'normal_surface_color': f'{category_name}_fixed_color',
                    'normal_content_color': f'content_{category_name}_fixed_color'},),
            ColorLabel(
                text=f'{category_name.capitalize()} Fixed Dim',
                theme_color_bindings={
                    'normal_surface_color': f'{category_name}_fixed_dim_color',
                    'normal_content_color': f'content_{category_name}_fixed_color'},),
            orientation='horizontal',
            auto_height=True,),
        ColorLabel(
            text=f'Content {category_name} Fixed',
            theme_color_bindings={
                'normal_surface_color': f'content_{category_name}_fixed_color',
                'normal_content_color': f'{category_name}_fixed_color'},),
        ColorLabel(
            text=f'Content {category_name} Fixed Variant',
            theme_color_bindings={
                'normal_surface_color': f'content_{category_name}_fixed_variant_color',
                'normal_content_color': f'{category_name}_fixed_color'},),
        orientation='vertical',
        size_hint= (None, None),
        auto_height=True,
        width=SUBBOX_WIDTH,)
    return box

def create_surface_box() -> MorphBoxLayout:
    """Create a box layout for surface colors."""
    box = MorphBoxLayout(
        MorphBoxLayout(
            ColorLabel(
                text='Surface Dim',
                theme_color_bindings={
                    'normal_surface_color': 'surface_dim_color',
                    'normal_content_color': 'content_surface_color'},),
            ColorLabel(
                text='Surface',
                theme_color_bindings={
                    'normal_surface_color': 'surface_color',
                    'normal_content_color': 'content_surface_color'},),
            ColorLabel(
                text='Surface Bright',
                theme_color_bindings={
                    'normal_surface_color': 'surface_bright_color',
                    'normal_content_color': 'content_surface_color'},),
            orientation='horizontal',
            auto_height=True,),

        MorphBoxLayout(
            ColorLabel(
                text='Surface Container Lowest',
                theme_color_bindings={
                    'normal_surface_color': 'surface_container_lowest_color',
                    'normal_content_color': 'content_surface_color'},),
            ColorLabel(
                text='Surface Container Low',
                theme_color_bindings={
                    'normal_surface_color': 'surface_container_low_color',
                    'normal_content_color': 'content_surface_color'},),
            ColorLabel(
                text='Surface Container',
                theme_color_bindings={
                    'normal_surface_color': 'surface_container_color',
                    'normal_content_color': 'content_surface_color'},),
            ColorLabel(
                text='Surface Container High',
                theme_color_bindings={
                    'normal_surface_color': 'surface_container_high_color',
                    'normal_content_color': 'content_surface_color'},),
            ColorLabel(
                text='Surface Container Highest',
                theme_color_bindings={
                    'normal_surface_color': 'surface_container_highest_color',
                    'normal_content_color': 'content_surface_color'},),
            orientation='horizontal',
            auto_height=True,),

        MorphBoxLayout(
            ColorLabel(
                text='Content Surface',
                theme_color_bindings={
                    'normal_surface_color': 'content_surface_color',
                    'normal_content_color': 'surface_color'},),
            ColorLabel(
                text='Content Surface Variant',
                theme_color_bindings={
                    'normal_surface_color': 'content_surface_variant_color',
                    'normal_content_color': 'surface_color'},),
            ColorLabel(
                text='Outline',
                theme_color_bindings={
                    'normal_surface_color': 'outline_color',
                    'normal_content_color': 'surface_color'},),
            ColorLabel(
                text='Outline Variant',
                theme_color_bindings={
                    'normal_surface_color': 'outline_variant_color',
                    'normal_content_color': 'content_surface_color'},),
            orientation='horizontal',
            auto_height=True,),
        orientation='vertical',
        size_hint= (None, None),
        auto_height=True,
        width= 3 * SUBBOX_WIDTH + 2 * COLUMN_SPACING,)
    return box

def create_inverse_box() -> MorphBoxLayout:
    """Create a box layout for inverse colors."""
    box = MorphBoxLayout(
        ColorLabel(
            text='Inverse Surface',
            theme_color_bindings={
                'normal_surface_color': 'inverse_surface_color',
                'normal_content_color': 'inverse_content_surface_color'},),
        ColorLabel(
            text='Content Inverse Surface',
            theme_color_bindings={
                'normal_surface_color': 'inverse_content_surface_color',
                'normal_content_color': 'inverse_surface_color'},),
        ColorLabel(
            text='Inverse Primary',
            theme_color_bindings={
                'normal_surface_color': 'inverse_primary_color',
                'normal_content_color': 'inverse_surface_color'},),
        MorphBoxLayout(
            ColorLabel(
                text='Scrim',
                normal_content_color='white',
                theme_color_bindings={
                    'normal_surface_color': 'scrim_color',},),
            ColorLabel(
                text='Shadow',
                normal_content_color='white',
                theme_color_bindings={
                    'normal_surface_color': 'shadow_color',},),
            orientation='horizontal',
            auto_height=True,),
        orientation='vertical',
        size_hint= (None, None),
        auto_height=True,
        width=SUBBOX_WIDTH,)
    return box

if __name__ == '__main__':
    ColorShowcaseApp().run()
