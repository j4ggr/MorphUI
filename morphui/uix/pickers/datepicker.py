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
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from morphui.uix.list import BaseListView
from morphui.uix.list import MorphListLayout # noqa F401
from morphui.uix.list import MorphListItemFlat
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.button import MorphTextIconButton
from morphui.uix.button import MorphDatePickerDayButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.textfield import MorphTextField
from morphui.uix.behaviors import MorphElevationBehavior
from morphui.uix.behaviors import MorphMenuMotionBehavior
from morphui.uix.behaviors import MorphSizeBoundsBehavior
from morphui.uix.gridlayout import MorphGridLayout
from morphui.uix.screenmanager import MorphScreen
from morphui.uix.screenmanager import MorphScreenManager


__all__ = [
    'MorphDatePickerYearView',
    'MorphDatePickerMonthView',
    'MorphDatePickerCalendarView',
    'MorphDockedDatePickerMenu',
    'MorphDockedDatePickerField',]


class BaseDatePickerListView(
        BaseListView):
    
    Builder.load_string(dedent('''
        <MorphDatePickerYearView>:
            viewclass: 'MorphListItemFlat'
            MorphListLayout:
                normal_surface_color: [0, 0, 0, 0]
        '''))

    default_data: Dict[str, Any] = DictProperty(
        MorphListItemFlat.default_config.copy() | {
        'normal_leading_icon': '',
        'active_leading_icon': 'check',
        'label_text': '',})
    
    default_config: Dict[str, Any] = (
        BaseListView.default_config.copy() | dict(
            size_hint=(None, None),))


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
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.bind( # type: ignore
            year_start=self._populate_years,
            year_end=self._populate_years,)
        
        self._populate_years()

    def _populate_years(self, *args) -> None:
        """Populate the year view with years from :attr:`year_start` to 
        :attr:`year_end`.
        
        This method generates the list of years to be displayed in the
        year view based on the specified start and end years.
        """
        years = [
            {'label_text': str(y), 'active': y == self.current_year,}
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
        bind=['current_month'])
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
            {'label_text': self.month_names[i], 'active': (i + 1) == self.current_month,}
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
                    normal_surface_color='primary_color',),
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
        padding=dp(4),
        spacing=dp(8),)
    
    def __init__(self, **kwargs) -> None:
        self.screen_manager = MorphScreenManager(
            MorphScreen(
                MorphDatePickerCalendarView(
                    identity='calendar_view',),
                name='calendar_view_screen',),
            MorphScreen(
                MorphDatePickerMonthView(
                    identity='month_view',),
                name='month_view_screen',),
            MorphScreen(
                MorphDatePickerYearView(
                    identity='year_view',),
                name='year_view_screen',),
            identity='screen_manager',)
        super().__init__(**kwargs)
        self.add_widget(
            MorphBoxLayout(
                MorphTextIconButton(
                    on_release=lambda x: self._go_to_month_view(),
                    normal_icon='menu-down',
                    active_icon='menu-up',
                    identity='month_button',),
                MorphTextIconButton(
                    normal_icon='menu-down',
                    active_icon='menu-up',
                    on_release=lambda x: self._go_to_year_view(),
                    identity='year_button',),))
        self.add_widget(self.screen_manager)
        self.screen_manager.current = 'calendar_view_screen'
        self.bind(
            current_year=self._update_calendar,
            current_month=self._update_calendar,)
        self._update_calendar()

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
        

        self.identities.month_button.label_text = (
            self.identities.month_view.current_month_name)
        self.identities.year_button.label_text = str(self.current_year)
    
    def _go_to_month_view(self) -> None:
        """Navigate to the month selection view."""
        self.screen_manager.current = 'month_view_screen'

    def _go_to_year_view(self) -> None:
        """Navigate to the year selection view."""
        self.screen_manager.current = 'year_view_screen'

    def _go_to_calendar_view(self) -> None:
        """Navigate to the calendar view."""
        self.screen_manager.current = 'calendar_view_screen'
    

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

    def __init__(self, **kwargs) -> None:
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
