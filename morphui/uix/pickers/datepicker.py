from calendar import Calendar
from calendar import day_abbr
from calendar import month_name
from textwrap import dedent

from typing import Any
from typing import List
from typing import Dict
from typing import Literal

from datetime import date
from dateutil.parser import parse as parse_date

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import OptionProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

from morphui.uix.list import BaseListView
from morphui.uix.list import MorphListLayout
from morphui.uix.list import MorphToggleListItemFlat
from morphui.uix.label import MorphSimpleLabel
from morphui.uix.label import MorphSimpleIconLabel
from morphui.uix.label import MorphLeadingIconLabel
from morphui.uix.button import MorphSimpleIconButton
from morphui.uix.button import MorphDatePickerDayButton
from morphui.uix.button import MorphTextIconToggleButton
from morphui.uix.boxlayout import MorphBoxLayout
from morphui.uix.boxlayout import MorphElevationBoxLayout
from morphui.uix.textfield import MorphTextField
from morphui.uix.textfield import MorphTextFieldFilled
from morphui.uix.textfield import MorphTextFieldRounded
from morphui.uix.textfield import MorphTextFieldOutlined
from morphui.uix.behaviors import MorphRoundSidesBehavior
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
    'MorphDockedDatePickerField',
    'MorphDockedDatePickerFieldOutlined',
    'MorphDockedDatePickerFieldRounded',
    'MorphDockedDatePickerFieldFilled',]


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
    
    default_child_classes = (
        MorphToggleListItemFlat.default_child_classes | {
        'leading_widget': _ListItemLeadingWidget,
        'label_widget': _ListItemLabelWidget,
        'trailing_widget': _ListItemTrailingWidget,})


class BaseDatePickerListView(
        BaseListView):
    """Base class for date picker list views.

    This class serves as a foundation for specific date picker views
    such as year and month views.
    """
    
    Builder.load_string(dedent(f'''
        <BaseDatePickerListView>:
            viewclass: '{_ToggleListItemFlat.__name__}'
            {MorphListLayout.__name__}:
        '''))

    default_data: Dict[str, Any] = DictProperty(
        MorphToggleListItemFlat.default_config.copy() | {
        'normal_leading_icon': 'blank',
        'active_leading_icon': 'check',
        'label_text': '',
        'visible_edges': [],})
    
    def _clear_active(self) -> None:
        """Clear the active state of all items in the list view."""
        for child in self.layout_manager.children:
            child.active = False
            child.leading_widget._update_icon()

    def set_active_by_text(self, text: str) -> None:
        """Set the active item based on the label text.

        This method iterates through the list items and sets the active
        state of the item whose label text matches the provided text.

        Parameters
        ----------
        text : str
            The label text of the item to set as active.
        """
        self._clear_active()
        for child in self.layout_manager.children:
            if getattr(child, 'label_text', '') == text:
                child.active = True
                self.refresh_from_viewport()
                return


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

    kind: Literal['range', 'single'] = StringProperty('single')
    """The selection mode of the calendar view.

    This property defines whether the calendar allows single date
    selection or range selection.

    :attr:`kind` is a :class:`kivy.properties.StringProperty` and
    defaults to `'single'`.
    """

    selected_dates: List[date] = ListProperty([])
    """List of currently selected dates.

    This property holds the list of :class:`datetime.date` values that
    are currently selected in the calendar view.

    :attr:`selected_dates` is a :class:`kivy.properties.ListProperty`
    and defaults to an empty list.
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
        self._updating_buttons = False
        super().__init__(
            MorphBoxLayout(
                *[
                    MorphSimpleLabel(
                        typography_size='large',
                        halign='center',
                        valign='middle',
                        auto_size=False,)
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
            date_values=self._populate_date_values,
            selected_dates=self._apply_selection_to_buttons,)
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
        for child in date_grid.children[:]:
            child.unbind(active=self._on_day_button_active)
        date_grid.clear_widgets()
        for date_value in self.date_values:
            day_button = MorphDatePickerDayButton(
                typography_size='large',
                is_today=date_value == date.today(),
                disabled=date_value is None,
                date_value=date_value,)
            day_button.bind(active=self._on_day_button_active)
            date_grid.add_widget(day_button)
        self._apply_selection_to_buttons()
    
    def _on_day_button_active(
            self, instance: MorphDatePickerDayButton, active: bool) -> None:
        """Handle changes to the active state of day buttons.

        This method is called when a day button's active state
        changes. It updates :attr:`selected_dates` based on which
        date was activated or deactivated.

        Parameters
        ----------
        instance : MorphDatePickerDayButton
            The day button instance whose state changed.
        active : bool
            The new active state of the button.
        """
        if self._updating_buttons:
            return

        dv = instance.date_value
        if dv is None:
            return

        if self.kind == 'single':
            self.selected_dates = [dv] if active else []
            return

        # range mode
        dates = list(self.selected_dates)
        if active:
            match len(dates):
                case 0:
                    self.selected_dates = [dv]
                case 1:
                    if dv < dates[0]:
                        self.selected_dates = [dv, dates[0]]
                    else:
                        self.selected_dates = [dates[0], dv]
                case 2:
                    delta_first = abs((dv - dates[0]).days)
                    delta_second = abs((dv - dates[1]).days)
                    if delta_first <= delta_second:
                        self.selected_dates = sorted([dv, dates[1]])
                    else:
                        self.selected_dates = sorted([dates[0], dv])
        else:
            if dv in dates:
                dates.remove(dv)
                self.selected_dates = dates
        
    def _apply_selection_to_buttons(self, *args) -> None:
        """Apply the current :attr:`selected_dates` state to all day
        buttons in the grid.

        This method iterates all day buttons and sets their ``active``,
        ``is_start_day``, ``is_end_day``, and ``is_in_range`` properties
        to reflect the current :attr:`selected_dates`.
        """
        self._updating_buttons = True
        try:
            date_grid = self.identities.date_grid_layout
            dates = self.selected_dates
            start = dates[0] if len(dates) >= 1 else None
            end = dates[1] if len(dates) == 2 else None
            for btn in date_grid.children:
                dv = btn.date_value
                is_selected = dv is not None and dv in dates
                is_start = (
                    self.kind == 'range'
                    and dv is not None
                    and dv == start)
                is_end = (
                    self.kind == 'range'
                    and dv is not None
                    and dv == end)
                is_in_range = (
                    self.kind == 'range'
                    and start is not None
                    and end is not None
                    and dv is not None
                    and start <= dv <= end)
                btn.active = is_selected
                # Set range flags after active (active triggers _reset_flags)
                btn.is_start_day = is_start
                btn.is_end_day = is_end
                btn.is_in_range = is_in_range
        finally:
            self._updating_buttons = False
    
    def clear_selection(self) -> None:
        """Clear the current date selection in the calendar view.

        This method resets the selection state, removing any selected
        dates.
        """
        self.selected_dates = []


class MorphDockedDatePickerMenu(
        MorphSizeBoundsBehavior,
        MorphMenuMotionBehavior,
        MorphElevationBoxLayout,):
    
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

    kind: Literal['range', 'single'] = StringProperty('single')
    """The selection mode of the date picker menu.

    This property defines whether the date picker allows single date
    selection or range selection.

    :attr:`kind` is a :class:`kivy.properties.StringProperty` and
    defaults to `'single'`.
    """
    
    default_config: Dict[str, Any] = dict(
        theme_color_bindings=dict(
            normal_surface_color='surface_container_color',),
        orientation='vertical',
        size_hint=(None, None),
        padding=dp(4),
        spacing=dp(8),
        radius=[dp(8)],
        elevation=2,)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        kw_header_button = dict(
            theme_color_bindings=dict(
                normal_surface_color='transparent_color',
                normal_content_color='content_surface_color',
                disabled_content_color='outline_color',
                hovered_content_color='inverse_surface_color',),
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
                        kind=self.kind,
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
            kind=self.identities.calendar_view.setter('kind'),
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
        self.pos = self._resolve_pos()
    
    def change_view(
            self, button: MorphTextIconToggleButton, screen_name: str) -> None:
        """Navigate to the month selection view."""
        if screen_name == 'calendar_view_screen' or not button.active:
            self.identities.screen_manager.transition.direction = 'right'
            self.identities.screen_manager.current = 'calendar_view_screen'
        else:
            self._refresh_list_views()
            self.identities.screen_manager.transition.direction = 'left'
            self.identities.screen_manager.current = screen_name
        
        kind = 'month' if 'year' in button.identity else 'year'
        for other_button in self.identities.header_layout.children:
            identity = getattr(other_button, 'identity', '')
            if kind in identity:
                other_button.disabled = button.active
    
    def _refresh_list_views(self, *args) -> None:
        """Refresh the month and year list views to reflect the current
        selection.

        This method updates the active state of the items in the month
        and year list views based on the currently selected month and
        year.
        """
        self.identities.month_view.set_active_by_text(
            self.identities.month_view.current_month_name)
        self.identities.year_view.set_active_by_text(
            str(self.current_year))
    
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
        for data in self.identities.year_view.data:
            if data.get('label_text') == item.label_text:
                data['active'] = True
            else:
                data['active'] = False

        self._change_year(int(item.label_text) - self.current_year)
    
    def _change_year(self, delta: int) -> None:
        """Change the current year by the specified delta.

        Parameters
        ----------
        delta : int
            The amount to change the current year by (positive or
            negative).
        """
        self.current_year += delta
        if self.identities.year_button.active:
            self.identities.year_button.trigger_action()

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
        delta = (
            self.identities.month_view.month_names.index(item.label_text)
            - self.current_month
            + 1)
        self._change_month(delta)
    
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
            
        if self.identities.month_button.active:
            self.identities.month_button.trigger_action()
    

class MorphDockedDatePickerField(MorphTextField):
    """A date picker text field designed to be used with a docked
    layout such as MorphDockedDatePicker.

    This text field integrates with a docked date picker layout to
    provide date selection functionality.

    Examples
    --------
    Single date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerField
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerField(
                    kind='single',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout

    if __name__ == "__main__":
        MyApp().run()
    ```

    Range date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerField
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerField(
                    kind='range',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout

    if __name__ == "__main__":
        MyApp().run()
    ```
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

    kind: Literal['range', 'single'] = StringProperty('single')
    """The selection mode of the date picker menu.

    This property defines whether the date picker allows single date
    selection or range selection.

    :attr:`kind` is a :class:`kivy.properties.StringProperty` and
    defaults to `'single'`.
    """

    date_format: Literal['iso', 'us', 'eu'] = OptionProperty(
        'eu', options=['iso', 'us', 'eu'] )
    """The date format used for displaying selected dates.

    This property defines the format in which selected dates are
    displayed in the text field. Possible values include 'iso' 
    (YYYY-MM-DD), 'us' (MM/DD/YYYY), and 'eu' (DD.MM.YYYY).

    :attr:`date_format` is a :class:`kivy.properties.OptionProperty` and
    defaults to `'eu'`.
    """

    range_sep: str = StringProperty(' - ')
    """Separator used between start and end dates in range selection.

    This property defines the string used to separate the start and
    end dates when the date picker is in range selection mode.

    :attr:`range_sep` is a :class:`kivy.properties.StringProperty` and
    defaults to `' - '`.
    """

    _format_strings: Dict[str, str] = dict(
        iso=r'%Y-%m-%d',
        us=r'%m/%d/%Y',
        eu=r'%d.%m.%Y',)
    """Mapping of date formats to strftime/strptime format strings.
    
    This dictionary maps the date format options to their corresponding
    strftime/strptime format strings for date parsing and formatting:
    - 'iso': '%Y-%m-%d'
    - 'us': '%m/%d/%Y'
    - 'eu': '%d.%m.%Y'
    """

    def __init__(self, **kwargs) -> None:
        kwargs['picker_menu'] = MorphDockedDatePickerMenu(caller=self)
        kwargs['trailing_icon'] = kwargs.get(
            'trailing_icon', self.normal_trailing_icon)
        super().__init__(**kwargs)
        self.bind(
            kind=self._on_kind_changed,
            text=self._on_text_changed,
            focus=self._on_focus_changed,
            date_format=self._update_format_error_texts,
            range_sep=self._update_format_error_texts,
            normal_trailing_icon=self.trailing_widget.setter('normal_icon'),
            focus_trailing_icon=self.trailing_widget.setter('focus_icon'),)
        self.calendar_view.bind(
            selected_dates=self._set_text_by_selected_dates)
        self.trailing_widget.normal_icon = self.normal_trailing_icon
        self.trailing_widget.focus_icon = self.focus_trailing_icon
        self.trailing_widget.bind(
            on_release=self._on_trailing_release)
        self._on_kind_changed(self, self.kind)
        self._on_text_changed(self, self.text)
        self._on_focus_changed(self, self.focus)
        self._update_format_error_texts()
        self.refresh_textfield_content()

    @property
    def calendar_view(self) -> MorphDatePickerCalendarView:
        """Get the calendar view from the associated date picker menu.

        This property provides access to the
        :class:`~morphui.uix.pickers.MorphDatePickerCalendarView`
        instance within the associated date picker menu.

        :return: The calendar view instance.
        :rtype: MorphDatePickerCalendarView
        """
        return self.picker_menu.identities.calendar_view
    
    @property
    def format_string(self) -> str:
        """Get the strftime/strptime format string based on the
        selected date format.

        This property retrieves the appropriate format string for
        date parsing and formatting based on the current value of
        the :attr:`date_format` property.

        :return: The corresponding format string.
        :rtype: str
        """
        return self._format_strings[self.date_format]

    def _get_date_string(self, date_value: date | None) -> str:
        """Format a date value as a string based on the selected
        date format.

        This method converts a :class:`datetime.date` object into a
        string representation according to the specified date format.

        Parameters
        ----------
        date_value : date | None
            The date value to format.

        :return: The formatted date string.
        :rtype: str
        """
        if date_value is None:
            return ''
        return date_value.strftime(self.format_string)

    def _on_kind_changed(
            self,
            instance: 'MorphDockedDatePickerField',
            kind: Literal['range', 'single']) -> None:
        """Handle changes to the kind property.

        This method is called whenever the kind property changes.
        It updates the kind of the associated date picker menu.
        """
        self.picker_menu.kind = kind
        self.validator = 'daterange' if kind == 'range' else 'date'
        self._update_format_error_texts()

    def _update_format_error_texts(self, *args) -> None:
        """Update supporting_error_texts with the expected format hint.

        The hint is shown under the field only when the user has typed
        something invalid, replacing any previous format-based hint.
        """
        input_format = {
            'iso': 'YYYY-MM-DD',
            'us': 'MM/DD/YYYY',
            'eu': 'DD.MM.YYYY',}[self.date_format]
        if self.kind == 'range':
            hint = f'{input_format}{self.range_sep}{input_format}'
            self.supporting_error_texts = {'daterange': hint}
        else:
            self.supporting_error_texts = {'date': input_format}

    def _on_text_changed(
            self,
            instance: 'MorphDockedDatePickerField',
            text: str
            ) -> None:
        """Handle changes to the text property.

        This method is called whenever the text in the text field
        changes. It can be used to validate or format the date input.
        """
        if not self.focus:
            return

        if self.error and not text:
            self.calendar_view.clear_selection()
            return

        texts = [t.strip() for t in text.split(self.range_sep)]
        parsed_dates = [
            d for d in
            (self._parse_date_text(t) for t in texts if len(t) >= 10)
            if d is not None]

        if len(parsed_dates) >= 2 and parsed_dates[0] > parsed_dates[1]:
            self.text = f'{texts[1]}{self.range_sep}{texts[0]}'
            return

        if parsed_dates:
            last_date = parsed_dates[-1]
            self.picker_menu.current_year = last_date.year
            self.picker_menu.current_month = last_date.month

        if self.kind == 'single':
            self.calendar_view.selected_dates = parsed_dates[:1]
        else:
            self.calendar_view.selected_dates = sorted(parsed_dates[:2])

    def _set_text_by_selected_dates(self, *args) -> None:
        """Set the text field's text based on selected dates.

        This method updates the text field's content to reflect the
        currently selected dates in the calendar view. It formats the
        dates according to the specified date format and selection mode.
        """
        if self.focus:
            return

        selected = self.calendar_view.selected_dates
        if not selected:
            return

        date_string = self._get_date_string(selected[0])
        if len(selected) == 2 and self.kind == 'range':
            date_string = self.range_sep.join((
                date_string,
                self._get_date_string(selected[1])))
        self.text = date_string

    def _on_focus_changed(
            self,
            instance: 'MorphDockedDatePickerField',
            focus: bool
            ) -> None:
        """Handle changes to the focus property.

        This method is called whenever the focus state of the text
        field changes. It opens the date picker menu when the field
        gains focus and closes it when the field loses focus.
        """
        self.trailing_widget.focus = focus
        if focus:
            self.picker_menu.open()

    def _parse_date_text(self, text: str) -> date | None:
        """Parse the date from the text field.

        This method attempts to parse a date from the text field's
        content. If the text is a valid date format, it returns a
        :class:`datetime.date` object; otherwise, it returns `None`.
        """
        try:
            parsed_date = parse_date(
                text,
                dayfirst= self.date_format == 'eu',
                yearfirst= self.date_format == 'iso',
                ).date()
            return parsed_date
        except (ValueError, TypeError):
            return None

    def _on_trailing_release(self, instance) -> None:
        """Handle the release event of the trailing icon button.

        This method toggles the focus state of the text field when
        the trailing icon button is released, effectively opening or
        closing the date picker menu.
        """
        if not self.picker_menu.is_open:
            self.focus = True
        else:
            self.picker_menu.dismiss()


class MorphDockedDatePickerFieldOutlined(
        MorphDockedDatePickerField):
    """An outlined variant of the MorphDockedDatePickerField.

    This class extends the MorphDockedDatePickerField to provide an
    outlined style for the date picker text field.

    Examples
    --------
    Single date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerFieldOutlined
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerFieldOutlined(
                    kind='single',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout
    
    if __name__ == "__main__":
        MyApp().run()
    ```

    range date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerFieldOutlined
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerFieldOutlined(
                    kind='range',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout
    if __name__ == "__main__":
        MyApp().run()
    ```
    """

    default_config: Dict[str, Any] = (
        MorphTextFieldOutlined.default_config.copy() | dict())


class MorphDockedDatePickerFieldRounded(
        MorphRoundSidesBehavior,
        MorphDockedDatePickerField):
    """A rounded variant of the MorphDockedDatePickerField.

    This class extends the MorphDockedDatePickerField to provide a
    rounded style for the date picker text field.

    Examples
    --------
    Single date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerFieldRounded
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerFieldRounded(
                    kind='single',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout

    if __name__ == "__main__":
        MyApp().run()
    ```

    Range date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerFieldRounded
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerFieldRounded(
                    kind='range',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout

    if __name__ == "__main__":
        MyApp().run()
    ```
    """

    default_config: Dict[str, Any] = (
        MorphTextFieldRounded.default_config.copy() | dict())
    
    
class MorphDockedDatePickerFieldFilled(
        MorphDockedDatePickerField):
    """A filled variant of the MorphDockedDatePickerField.

    This class extends the MorphDockedDatePickerField to provide a
    filled style for the date picker text field.

    Examples
    --------
    Single date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerFieldFilled
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerFieldFilled(
                    kind='single',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.6,))

            return self.layout

    if __name__ == "__main__":
        MyApp().run()
    ```

    Range date selection:
    ```python
    from morphui.app import MorphApp
    from morphui.uix.pickers import MorphDockedDatePickerFieldFilled
    from morphui.uix.floatlayout import MorphFloatLayout

    class MyApp(MorphApp):

        def build(self) -> MorphFloatLayout:
            self.theme_manager.theme_mode = 'Dark'
            self.theme_manager.seed_color = 'morphui_teal'

            self.layout = MorphFloatLayout(
                MorphDockedDatePickerFieldFilled(
                    kind='range',
                    identity='date_picker_field',
                    pos_hint={'center_x': 0.5, 'center_y': 0.8},
                    size_hint_x= 0.,))

            return self.layout

    if __name__ == "__main__":
        MyApp().run()
    ```
    """

    default_config: Dict[str, Any] = (
        MorphTextFieldFilled.default_config.copy() | dict())
    