from calendar import Calendar
from calendar import day_abbr
from calendar import month_name
from textwrap import dedent

from typing import Any
from typing import List
from typing import Dict
from datetime import date

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

from morphui.uix.list import BaseListView
from morphui.uix.list import MorphListLayout # noqa F401
from morphui.uix.list import MorphToggleListItemFlat
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.button import MorphSimpleIconButton
from morphui.uix.button import MorphDatePickerDayButton
from morphui.uix.button import MorphTextIconToggleButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.textfield import MorphTextField
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.gridlayout import MorphGridLayout
from morphui.uix.screenmanager import MorphScreen
from morphui.uix.screenmanager import MorphScreenManager

from morphui.utils.helpers import clamp


__all__ = [
    'MorphDatePickerYearView',
    'MorphDatePickerMonthView',
    'MorphDatePickerCalendarView',
    'MorphDockedDatePickerMenu',
    'MorphDockedDatePickerField',]


class _ListItemLeadingWidget(MorphLeadingIconLabel):

    default_config: Dict[str, Any] = (
        MorphLeadingIconLabel.default_config.copy() | dict(
            auto_size=(False, True),
            size_hint_x=(None),
            width=(dp(24)),))
    
class _ListItemLabelWidget(MorphSimpleLabel):

    default_config: Dict[str, Any] = (
        MorphSimpleLabel.default_config.copy() | dict(
            auto_size=(True, True),))
    
class _ListItemTrailingWidget(MorphSimpleIconLabel):

    default_config: Dict[str, Any] = (
        MorphSimpleIconLabel.default_config.copy() | dict(
            auto_size=(False, True),
            size_hint_x=(1),))

class _ToggleListItemFlat(
        MorphToggleListItemFlat):
    
    default_child_widgets = (
        MorphToggleListItemFlat.default_child_widgets | {
        'leading_widget': _ListItemLeadingWidget,
        'label_widget': _ListItemLabelWidget,
        'trailing_widget': _ListItemTrailingWidget,})


class BaseDatePickerListView(
        BaseListView):
    """Base class for date picker list views.

    This class serves as a foundation for specific date picker views
    such as year and month views.
    """
    
    Builder.load_string(dedent('''
        <BaseDatePickerListView>:
            viewclass: '_ToggleListItemFlat'
            MorphListLayout:
        '''))

    default_data: Dict[str, Any] = DictProperty(
        MorphToggleListItemFlat.default_config.copy() | {
        'normal_leading_icon': 'blank',
        'active_leading_icon': 'check',
        'label_text': '',
        'visible_edges': [],})


class MorphDatePickerYearView(
        BaseDatePickerListView):
    """A year view for the date picker component.

    This view displays a grid of years for selection within the
    date picker.
    """

    year_start: int = NumericProperty(1970)
    """The starting year for the year view.

    This property defines the first year displayed in the year view.

    :attr:`year_start` is a :class:`kivy.properties.NumericProperty` and
    defaults to `1970`.
    """

    year_end: int = NumericProperty(2100)
    """The ending year for the year view.

    This property defines the last year displayed in the year view.

    :attr:`year_end` is a :class:`kivy.properties.NumericProperty` and
    defaults to `2100`.
    """

    current_year: int = NumericProperty(date.today().year)
    """The currently selected year.

    :attr:`current_year` is a :class:`kivy.properties.NumericProperty` and
    defaults to `2024`.
    """

    def _get_default_scroll_y(self) -> float:
        """Calculate the default scroll position for the year view.

        This method computes the initial scroll position based on the
        current year, ensuring that the current year is visible when
        the view is first displayed.
        """
        total_years = self.year_end - self.year_start + 1
        if total_years <= 0:
            return 1.0
        position = (self.current_year - self.year_start) / total_years
        return 1.0 - position
    
    def _set_default_scroll_y(self, value: float) -> None:
        """Set the scroll position for the year view.

        Parameters
        ----------
        value : float
            The scroll position to set (0.0 to 1.0).
        """
        self.scroll_y = clamp(value, 0.0, 1.0)

    default_scroll_y: float = AliasProperty(
        _get_default_scroll_y,
        _set_default_scroll_y,
        bind=[
            'year_start',
            'year_end',
            'current_year'],)
    """The default scroll position for the year view (read-only).

    This property is automatically calculated based on the 
    :attr:`year_start`, :attr:`year_end`, and :attr:`current_year`
    properties to ensure that the current year is visible when the
    view is first displayed.

    :attr:`default_scroll_y` is a
    :class:`kivy.properties.AliasProperty` that is read-only and bound
    to the relevant year properties.
    """
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.bind( # type: ignore
            year_start=self._populate_years,
            year_end=self._populate_years,
            default_scroll_y=lambda _, value: self._set_default_scroll_y(value),)
        self.default_scroll_y = self.default_scroll_y
        self._populate_years()

    def _populate_years(self, *args) -> None:
        """Populate the year view with years from :attr:`year_start` to 
        :attr:`year_end`.
        
        This method generates the list of years to be displayed in the
        year view based on the specified start and end years.
        """
        years = [
            {   
                'label_text': str(y),
                'active': y == self.current_year,
                'group': 'year_list_items'}
            for y in range(self.year_start, self.year_end + 1)]
        self.items = years


class MorphDatePickerMonthView(
        BaseDatePickerListView):
    """A month view for the date picker component.

    This view displays a grid of months for selection within the
    date picker.
    """

    current_month: int = NumericProperty(date.today().month)
    """The currently selected month.

    This property defines the month that is currently selected in the
    month view.

    :attr:`current_month` is a :class:`kivy.properties.NumericProperty`
    and defaults to current month.
    """

    month_names: List[str] = ListProperty(
        [month_name[i] for i in range(1, 13)])
    """List of month names to display in the month view.

    :attr:`month_names` is a :class:`kivy.properties.ListProperty` and
    defaults to the full names of the months from January to December.
    """

    current_month_name: str = AliasProperty(
        lambda self: self.month_names[self.current_month - 1],
        bind=[
            'current_month',
            'month_names'],)
    """The name of the currently selected month (read-only).

    :attr:`current_month_name` is a 
    :class:`kivy.properties.AliasProperty` that derives its value from 
    :attr:`current_month` and :attr:`month_names`.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind( # type: ignore
            month_names=self._populate_months,)
        self._populate_months()

    def _populate_months(self) -> None:
        """Populate the month view with months January to December.

        This method generates the list of months to be displayed in the
        month view.
        """
        months = [
            {
                'label_text': self.month_names[i],
                'active': (i + 1) == self.current_month,
                'group': 'month_list_items',}
            for i in range(12)]
        self.items = months


class MorphDatePickerCalendarView(
        MorphBoxLayout):
    """A calendar view for the date picker component.

    This view displays a calendar grid for a specific month and year,
    allowing date selection.
    """

    weekday_headers: List[str] = ListProperty(list(day_abbr))
    """List of weekday abbreviations to display as headers.

    :attr:`weekday_headers` is a :class:`kivy.properties.ListProperty`
    and defaults to the abbreviated names of the weekdays from
    Monday to Sunday.
    """

    date_values: List[date | None] = ListProperty([])
    """List of date values to display in the calendar grid.

    :attr:`date_values` is a :class:`kivy.properties.ListProperty` and
    defaults to an empty list.
    """

    default_config: Dict[str, Any] = dict(
        orientation='vertical',
        auto_size=(True, True),
        theme_color_bindings=dict(
            normal_surface_color='transparent_color',),)

    def __init__(self, **kwargs) -> None:
        super().__init__(
            MorphBoxLayout(
                *[
                    MorphSimpleLabel(
                        typography_size='large',
                        halign='center',
                        valign='middle',)
                    for _ in range(7)],
                theme_color_bindings=dict(
                    normal_surface_color='transparent_color',),
                height=dp(42),
                size_hint=(1, None),
                identity='weekday_header_layout',),
            MorphGridLayout(
                cols=7,
                auto_size=(True, True),
                identity='date_grid_layout',),
            **kwargs)
        self.bind(
            weekday_headers=self._populate_weekday_headers,
            date_values=self._populate_date_values,)
        self._populate_weekday_headers()
        self._populate_date_values()

    def _populate_weekday_headers(self, *args) -> None:
        """Populate the weekday header layout with abbreviations.

        This method updates the labels in the weekday header layout
        based on the :attr:`weekday_headers` property.
        """
        header_layout = self.identities.weekday_header_layout
        for i, label in enumerate(header_layout.children[::-1]):
            label.text = self.weekday_headers[i]
    
    def _populate_date_values(self, *args) -> None:
        """Populate the date grid layout with date values.

        This method updates the buttons in the date grid layout based
        on the :attr:`date_values` property.
        """
        date_grid = self.identities.date_grid_layout
        date_grid.clear_widgets()
        for date_value in self.date_values:
            date_grid.add_widget(
                MorphDatePickerDayButton(
                    typography_size='large',
                    disabled= date_value is None,
                    date_value=date_value,))


class MorphDockedDatePickerMenu(
        MorphSizeBoundsBehavior,
        MorphElevationBehavior,
        MorphMenuMotionBehavior,
        MorphBoxLayout):
    
    calendar: Calendar = Calendar(firstweekday=0)
    """The calendar instance used for date calculations.

    :attr:`calendar` is a standard Python :class:`calendar.Calendar`
    instance initialized with the first weekday set to Monday.
    """

    current_year: int = NumericProperty(date.today().year)
    """The currently selected year.

    :attr:`current_year` is a :class:`kivy.properties.NumericProperty` and
    defaults to `2024`.
    """

    current_month: int = NumericProperty(date.today().month)
    """The currently selected month.

    This property defines the month that is currently selected in the
    month view.

    :attr:`current_month` is a :class:`kivy.properties.NumericProperty`
    and defaults to current month.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_container_high_color',),
        orientation='vertical',
        size_hint=(None, None),
        padding=dp(4),
        spacing=dp(8),
        radius=[dp(8)],)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        kw_header_button = dict(
            theme_color_bindings=dict(
                normal_surface_color='transparent_color',
                normal_content_color='content_surface_color',
                disabled_content_color='content_surface_variant_color',
                hovered_content_color='content_surface_variant_color',),
            auto_size=(True, True),
            disabled_state_opacity=0.0,
            round_sides=True,)
            
        self.add_widgets(
            MorphBoxLayout(
                MorphSimpleIconButton(
                    icon='arrow-left',
                    on_release=lambda x: self._change_month(-1),
                    identity='prev_month_button',
                    **kw_header_button),
                MorphTextIconToggleButton(
                    on_release=lambda x: self.change_view(x, 'month_view_screen'),
                    identity='month_button',
                    **kw_header_button),
                MorphSimpleIconButton(
                    icon='arrow-right',
                    on_release=lambda x: self._change_month(1),
                    identity='next_month_button',
                    **kw_header_button,),
                Widget(),
                MorphSimpleIconButton(
                    icon='arrow-left',
                    on_release=lambda x: self._change_year(-1),
                    identity='prev_year_button',
                    **kw_header_button),
                MorphTextIconToggleButton(
                    on_release=lambda x: self.change_view(x, 'year_view_screen'),
                    identity='year_button',
                    **kw_header_button),
                MorphSimpleIconButton(
                    icon='arrow-right',
                    on_release=lambda x: self._change_year(1),
                    identity='next_year_button',
                    **kw_header_button),
                identity='header_layout',
                size_hint=(1, None),
                auto_size=(False, True),
                height=dp(48),),
            MorphScreenManager(
                MorphScreen(
                    MorphDatePickerCalendarView(
                        identity='calendar_view',),
                    name='calendar_view_screen',),
                MorphScreen(
                    MorphDatePickerMonthView(
                        item_release_callback=self._on_month_selected,
                        identity='month_view',),
                    name='month_view_screen',),
                MorphScreen(
                    MorphDatePickerYearView(
                        item_release_callback=self._on_year_selected,
                        identity='year_view',),
                    name='year_view_screen',),
                identity='screen_manager',))
        self.bind(
            current_year=self._update_calendar,
            current_month=self._update_calendar,)
        self.identities.calendar_view.bind(
            width=self._update_size,
            height=self._update_size,)
        self._update_calendar()
        self._update_size()

    def _update_calendar(self, *args) -> None:
        """Update the calendar view based on the current year and month.

        This method generates the list of date values to be displayed
        in the calendar view based on the selected year and month.
        """
        date_values = [
            dv if dv.month == self.current_month else None
            for dv in 
            self.calendar.itermonthdates(self.current_year, self.current_month)]
        self.identities.calendar_view.date_values = date_values
        
        self.identities.month_view.current_month = self.current_month
        self.identities.year_view.current_year = self.current_year

        self.identities.month_button.label_text = (
            self.identities.month_view.current_month_name)
        self.identities.year_button.label_text = str(self.current_year)

    def _update_size(self, *args) -> None:
        """Update the size of the date picker menu based on the calendar
        view.

        This method adjusts the width and height of the date picker menu
        to match the size of the calendar view.
        """
        self.width = (
            self.identities.calendar_view.width
            + self.padding[0]
            + self.padding[2])
        self.height = (
            self.identities.weekday_header_layout.height
            + self.identities.date_grid_layout.height
            + self.identities.header_layout.height
            + self.padding[1]
            + self.padding[3]
            + self.spacing * 2)
    
    def change_view(
            self, button: MorphTextIconToggleButton, screen_name: str) -> None:
        """Navigate to the month selection view."""
        if screen_name == 'calendar_view_screen' or not button.active:
            self.identities.screen_manager.transition.direction = 'right'
            self.identities.screen_manager.current = 'calendar_view_screen'
        else:
            self.identities.screen_manager.transition.direction = 'left'
            self.identities.screen_manager.current = screen_name
        
        kind = 'month' if 'year' in button.identity else 'year'
        for other_button in self.identities.header_layout.children:
            identity = getattr(other_button, 'identity', '')
            if kind in identity:
                other_button.disabled = button.active
    
    def _on_year_selected(
            self, item: MorphToggleListItemFlat, index: int) -> None:
        """Handle the selection of a year from the year view.
        This method updates the current year based on the selected
        year item and navigates back to the calendar view.

        Parameters
        ----------
        item : MorphToggleListItemFlat
            The selected year item.
        index : int
            The index of the selected year item.
        """
        self._change_year(int(item.label_text) - self.current_year)
        self.identities.year_button.trigger_action()
    
    def _change_year(self, delta: int) -> None:
        """Change the current year by the specified delta.

        Parameters
        ----------
        delta : int
            The amount to change the current year by (positive or
            negative).
        """
        self.current_year += delta

    def _on_month_selected(
            self, item: MorphToggleListItemFlat, index: int) -> None:
        """Handle the selection of a month from the month view.
        This method updates the current month based on the selected
        month item and navigates back to the calendar view.

        Parameters
        ----------
        item : MorphToggleListItemFlat
            The selected month item.
        index : int
            The index of the selected month item.
        """
        self.current_month = (
            self.identities.month_view.month_names.index(item.label_text)
            + 1)
        self.identities.month_button.trigger_action()
    
    def _change_month(self, delta: int) -> None:
        """Change the current month by the specified delta.

        Parameters
        ----------
        delta : int
            The amount to change the current month by (positive or
            negative).
        """
        new_month = self.current_month + delta
        if new_month < 1:
            self.current_month = 12
            self._change_year(-1)
        elif new_month > 12:
            self.current_month = 1
            self._change_year(1)
        else:
            self.current_month = new_month
    

class MorphDockedDatePickerField(MorphTextField):
    """A date picker text field designed to be used with a docked
    layout such as MorphDockedDatePicker.

    This text field integrates with a docked date picker layout to
    provide date selection functionality.
    """

    normal_trailing_icon: str = StringProperty('calendar')
    """Icon for the normal (closed) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    normal (closed) state. Other possible values could be 'menu-down',
    'chevron-down', etc.

    :attr:`normal_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `'chevron-down'`.
    """

    focus_trailing_icon: str = StringProperty('')
    """Icon for the focused (open) state of the dropdown filter field.

    This property holds the icon name used when the dropdown is in its
    focused (open) state. Other possible values could be 'menu-up',
    'chevron-up', etc.

    :attr:`focus_trailing_icon` is a
    :class:`~kivy.properties.StringProperty` and defaults to
    `''`.
    """

    picker_menu: MorphDockedDatePickerMenu = ObjectProperty(None)
    """Reference to the associated date picker menu.

    This property holds a reference to the
    :class:`~morphui.uix.pickers.MorphDockedDatePickerMenu` instance
    that is associated with this text field. It allows the text field to
    interact with the date picker menu for date selection.

    :attr:`picker_menu` is a
    :class:`~kivy.properties.ObjectProperty` and is instantiated during
    the initialization of the text field.
    """

    def __init__(self, **kwargs) -> None:
        kwargs['picker_menu'] = MorphDockedDatePickerMenu()
        kwargs['trailing_icon'] = kwargs.get(
            'trailing_icon', self.normal_trailing_icon)
        super().__init__(**kwargs)
        self.bind(
            text=self._on_text_changed,
            focus=self._on_focus_changed,
            normal_trailing_icon=self.trailing_widget.setter('normal_icon'),
            focus_trailing_icon=self.trailing_widget.setter('focus_icon'),)
        self.trailing_widget.normal_icon = self.normal_trailing_icon
        self.trailing_widget.focus_icon = self.focus_trailing_icon
        self.trailing_widget.bind(
            on_release=self._on_trailing_release)
        self._on_text_changed(self, self.text)
        self._on_focus_changed(self, self.focus)

    def _on_text_changed(self, instance, value) -> None:
        """Handle changes to the text property.

        This method is called whenever the text in the text field
        changes. It can be used to validate or format the date input.
        """
        pass  # Implement date validation/formatting as needed

    def _on_focus_changed(self, instance, value) -> None:
        """Handle changes to the focus property.

        This method is called whenever the focus state of the text
        field changes. It can be used to open or close the date picker
        when the field gains or loses focus.
        """
        pass  # Implement focus handling as needed
