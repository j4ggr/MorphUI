from typing import Any
from typing import Dict

from kivy.metrics import dp
from kivy.properties import AliasProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

from morphui.utils import clean_config
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphSimpleIconButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.behaviors import MorphIdentificationBehavior
from morphui.uix.behaviors import MorphRoundSidesBehavior


__all__ = [
    'MorphDataViewNavigationButton',
    'MorphDataViewNavigationPageLabel',
    'MorphDataViewNavigation',]


class MorphDataViewNavigationButton(
        MorphIdentificationBehavior,
        MorphRoundSidesBehavior,
        MorphSimpleIconButton):
    """A button used in the data view navigation component."""

    page_offset: float = NumericProperty(0)
    """The page offset to apply when this button is pressed.

    This property determines how many pages to move forward or backward
    in the data view when the button is activated. Positive values move
    forward, while negative values move backward.
    - A value of `0` indicates no movement. 
    - A value of `float('inf')` indicates moving to the last page.
    - A value of `-float('inf')` indicates moving to the first page.

    :attr:`page_offset` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """

    default_config: Dict[str, Any] = (
        MorphSimpleIconButton.default_config.copy() | dict(
        theme_color_bindings={
            'normal_surface_color':'transparent_color',
            'disabled_border_color':'transparent_color',
            'normal_content_color':'content_surface_color',
            'hovered_content_color':'content_surface_variant_color'},
        disabled_state_opacity=0.0,
        round_sides=True,))


class MorphDataViewNavigationPageLabel(MorphSimpleLabel):
    """A label used in the data view navigation component."""
    
    current_page: int = NumericProperty(0)
    """The current page number displayed by the label.

    :attr:`current_page` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """

    total_pages: int = NumericProperty(0)
    """The total number of pages displayed by the label.

    :attr:`total_pages` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """
    
    format_string: str = AliasProperty(
        lambda self: f'{self.current_page} / {self.total_pages}',
        None,
        bind=['current_page', 'total_pages'])
    """The formatted string displaying the current and total pages.

    This property generates a string in the format
    "current_page / total_pages" to represent the pagination status.

    :attr:`format_string` is an :class:`~kivy.properties.AliasProperty`
    and is bound to changes in `current_page` and `total_pages`.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_content_color='content_surface_color',),
        typography_role='Label',
        typography_size='medium',
        typography_weight='Regular',
        pos_hint={'center_y': 0.5},
        halign='left',
        valign='center',
        auto_size=True,
        padding=[dp(2), dp(0)],)
    """Default configuration for the MorphDataViewNavigationPageLabel."""

    def __init__(self, **kwargs) -> None:
        """Initialize the page label with default configuration."""
        super().__init__(**kwargs)
        self.bind(format_string=self.setter('text'))
        self.text = self.format_string


class MorphDataViewNavigation(
        MorphBoxLayout):
    """A navigation component for data views.
    
    This widget provides controls for navigating through pages of data,
    including buttons to go to the first, previous, next, and last 
    pages. It also includes a label to display the current page and
    total number of pages, as well as a button to toggle between
    repository data and metadata.
    """

    current_page: int = NumericProperty(0)
    """The current page number in the navigation.

    This property tracks the current page being viewed in the data view.
    
    :attr:`current_page` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """

    total_pages: int = NumericProperty(0)
    """The total number of pages available in the data view.

    This property indicates the total number of pages that can be
    navigated through in the data view.

    :attr:`total_pages` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0`.
    """

    default_config = dict(
        orientation='horizontal',
        size_hint=(1, None),
        auto_size=(False, True),
        spacing=dp(0),
        padding=dp(0),
        theme_color_bindings={
            'normal_surface_color': 'transparent_color',  
        },)
    """Default configuration for the MorphDataViewNavigation."""

    def __init__(self, **kwargs) -> None:
        """Initialize the navigation component."""
        config = clean_config(self.default_config, kwargs)
        self.first_page_button = MorphDataViewNavigationButton(
            identity='first_page_button',
            icon='chevron-double-left',
            page_offset= -float('inf'),
            on_release=lambda btn: self.navigate_by_offset(btn.page_offset),)
        self.previous_page_button = MorphDataViewNavigationButton(
            identity='previous_page_button',
            icon='chevron-left',
            page_offset= -1,
            on_release=lambda btn: self.navigate_by_offset(btn.page_offset),)
        self.page_label = MorphDataViewNavigationPageLabel(
            identity='page_label',)
        self.next_page_button = MorphDataViewNavigationButton(
            identity='next_page_button',
            icon='chevron-right',
            page_offset=1,
            on_release=lambda btn: self.navigate_by_offset(btn.page_offset),)
        self.last_page_button = MorphDataViewNavigationButton(
            identity='last_page_button',
            icon='chevron-double-right',
            page_offset=float('inf'),
            on_release=lambda btn: self.navigate_by_offset(btn.page_offset),)
        super().__init__(
            Widget(),  # Spacer
            self.first_page_button,
            self.previous_page_button,
            self.page_label,
            self.next_page_button,
            self.last_page_button,
            **config)
        self.bind(
            current_page=self.page_label.setter('current_page'),
            total_pages=self.page_label.setter('total_pages'),)
        self.page_label.current_page = self.current_page
        self.page_label.total_pages = self.total_pages

    def navigate_by_offset(self, offset: float) -> None:
        """Navigate to a page by applying an offset to the current page.

        This method updates the `current_page` property based on
        the provided offset value. It ensures that the new page
        number remains within valid bounds (0 to total_pages - 1).

        Parameters
        ----------
        offset : float
            The page offset to apply. Positive values move forward,
            negative values move backward. Special values `float('inf')`
            and `-float('inf')` navigate to the last and first pages,
            respectively.
        """
        if offset == float('inf'):
            new_page = self.total_pages
        elif offset == -float('inf'):
            new_page = 1
        else:
            new_page = self.current_page + int(offset)
        
        new_page = max(1, min(new_page, self.total_pages))
        self.current_page = new_page
    
    def on_total_pages(self, instance: Any, total_pages: int) -> None:
        """Event handler called when the total number of pages changes.

        This method ensures that the `current_page` remains valid
        when the `total_pages` property is updated.
        """
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages

        disabled = total_pages <= 1
        self.first_page_button.disabled = disabled
        self.previous_page_button.disabled = disabled
        self.page_label.disabled = disabled
        self.next_page_button.disabled = disabled
        self.last_page_button.disabled = disabled
