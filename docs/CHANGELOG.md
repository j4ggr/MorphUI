# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

__Types of changes__:

- _Added_ for new features.
- _Changed_ for changes in existing functionality.
- _Deprecated_ for soon-to-be removed features.
- _Removed_ for now removed features.
- _Fixed_ for any bug fixes.
- _Security_ in case of vulnerabilities.

## [0.13.1] - 2026-03-26

### Changed

- Changed `MorphDialog` `default_config` `auto_size` to `(False, True)`.

### Fixed

- Fixed `MorphAutoSizingBehavior` initialization by deferring `refresh_auto_sizing()` to the next frame via `Clock.schedule_once`, preventing layout timing issues on widget construction.

### Refactored

- Consolidated pressed-state management, ripple trigger, and `on_press`/`on_release` dispatch into `_do_press(pos)` and `_do_release()` in `MorphButtonBehavior`, removing redundant `Clock.schedule_once` call for `on_release` in `on_touch_up`.
- Removed `MorphToggleButtonBehavior._do_press` override (no longer needed); added `super()._do_release()` call in `MorphToggleButtonBehavior._do_release`.
- Simplified `trigger_action` to delegate directly to `_do_press`/`_do_release`.

## [0.13.0] - 2026-03-25

### Added

- Added `MorphLinearProgress` widget: horizontal progress indicator with determinate and indeterminate modes, rounded caps, split-track gap animation, and `default_config` sizing (`size_hint=(1, None)`, `height=dp(8)`).
- Added `MorphCircularProgress` widget: circular arc progress indicator with determinate and indeterminate modes; indeterminate mode rotates the canvas group with a sinusoidal speed pulse and animates the arc span between 1/6 and 5/6 of the circle (Material Design comet effect).
- Added `MorphWavyLinearProgress` widget: extends `MorphLinearProgress` with a continuous sine-wave polyline stroke; phase is tied to absolute x coordinate so indicator and track share one seamless wave pattern.
- Added `MorphWavyCircularProgress` widget: extends `MorphCircularProgress` with a radial sine-wave stroke; wave count is derived from the circumference (`_CIRCULAR_WAVE_COUNT = 9`) so all 9 cycles connect seamlessly at 360° regardless of widget size.
- Added `_WavePhaseAnimMixin`: mixin class providing `wave_speed` and `_wave_phase` properties and a per-frame `Clock` event that produces a travelling-wave animation on all wavy progress widgets.
- Added `_display_value` internal property to `_MorphProgressBase` that drives all canvas rendering and is smoothly animated by `on_value`.
- Added `value_animation_duration` (default `0.2` s) and `value_animation_transition` (default `'out_quad'`) properties to `_MorphProgressBase` for configuring the automatic value transition animation.
- Added `redraw()` public method to `_MorphProgressBase` for triggering an immediate canvas and color refresh from external code.
- Added `indeterminate_duration` property to `_MorphProgressBase` (default `1.33` s, matching the Material Design specification).
- Added 4-phase Material Design indeterminate animation to `MorphLinearProgress`: bar grows from 1/7 to 5/6 of the track width while accelerating, then pauses before repeating; driven by an animatable `_ind_speed` property.
- Added `MorphSimpleTooltip` subclass of `MorphTooltip` encapsulating a single text label.
- Added `MorphRichTooltip` subclass with `heading` (bold title) and `supporting` (detail text) string properties; the supporting label is added and removed from the widget tree dynamically.
- Added `MorphTooltipLabel` and `MorphTooltipHeadingLabel` to `uix/label.py`.
- Added `update_tooltip_text(text)` interface method on `MorphTooltip`, overridden in `MorphSimpleTooltip` and `MorphRichTooltip`.
- Added `linspace` generator to `morphui/utils/helpers.py` (pure-Python, no NumPy dependency).

### Changed

- Changed `value` property on `_MorphProgressBase` from a direct render trigger to a target property; setting it now starts an animated transition of `_display_value` rather than updating the canvas immediately.
- Changed `MorphCircularProgress` canvas to use `Line.circle` primitive for arc tessellation, removing manual point generation.
- Changed `MorphCircularProgress._refresh_canvas` to use a `PushMatrix`/`Rotate`/`PopMatrix` wrapper so only `Rotate.angle` is updated per frame during indeterminate mode (no geometry recalculation per frame).
- Changed `MorphTooltipBehavior.update_tooltip_text` to delegate to `tooltip.update_tooltip_text()` instead of walking the tooltip's children list.
- Changed `MorphDatePickerCalendarView` to store `selected_dates: ListProperty` (plain `datetime.date` values) instead of `selected_day_buttons` (widget references) so selection state survives month navigation.

### Refactored

- Introduced `_MorphProgressBase` as a shared base class for all progress indicators, consolidating common properties (`value`, `indeterminate`, `indicator_color`, `track_color`, `thickness`), canvas bindings, and the abstract `_setup_canvas`/`_refresh_canvas` interface.

### Fixed

- Fixed `MorphAutoSizingBehavior` text label growing horizontally beyond its container.
- Fixed `MorphDatePickerCalendarView` weekday header alignment and improved format hint UX.

## [0.12.0] - 2026-03-09

### Added

- Added `MorphMotionBaseBehavior` class holding all base properties and methods used for motion behavior classes.
- Added `MorphDialogMotionBehavior` class which extends `MorphMotionBaseBehavior` to provide motion functionality specific to dialogs.
- Added `MorphScrimLayer` class that provides a semi-transparent overlay appearing behind dialogs to focus user attention.
- Added `MorphDialog` class that provides a customizable dialog component for displaying information, prompting user input, or presenting interactive content in modal overlays.
- Added `animate_opacity` during scale in and out animations to `MorphScaleBehavior`.
- Added `__events__` properties to behavior classes instead of calling `self.register_event_type()` in `__init__`.
- Added comprehensive test suite for motion behaviors (15 tests for `MorphMotionBaseBehavior`, 13 tests for `MorphDialogMotionBehavior`, 4 tests for `MorphMenuMotionBehavior`).

### Changed

- Changed `MorphMenuMotionBehavior` to extend `MorphMotionBaseBehavior` class for better code organization.
- Changed property names in `MorphMotionBaseBehavior` by removing the `menu_` prefix since they are used for multiple behavior types, not just menus.
- Changed `MorphAutoSizingBehavior` to first set `text_size` to `(None, None)` and update texture to ensure correct dimensions before setting `text_size` to match `texture_size`.

### Removed

- Removed adding padding to `texture_size` for calculating minimum size properties in `BaseLabel` since `texture_size` already includes padding.
- Removed calling `self.register_event_type()` method in behavior `__init__` methods in favor of using `__events__` properties.

## [0.11.1] - 2026-03-03

### Added

- Added `caller_collide_point` method to MorphMenuMotionBehavior as a workaround for the fact that the native `collide_point` method does not work correctly for the caller button when the menu is open.
- Added `on_release` method to MorphDropdownSelect that toggles the dropdown menu.

### Changed

- Changed MorphDropdownMenu to no longer handle the `active` state of the caller button, simplifying state management.
- Changed MorphDropdownSelect to bind `is_open` property to setter of `active` state for better state synchronization.

## [0.11.0] - 2026-02-20

### Removed

- Removed `dismiss_allowed` property from MorphMenuMotionBehavior since the dismissing is now handled by the on_touch_up() method. If the caller has a ripple in progress or a touch collides the caller widget, it will not call dismiss.

### Changed

- Changed MorphDropdownSelect to set its active state to False when the dropdown menu is dismissed, ensuring that the button's visual state correctly reflects the menu's visibility.
- Changed MorphMenuMotionBehavior to not call dismiss in on_touch_up() method if the caller's on_touch_up() method returns True, which indicates that the touch event was handled by the caller and should not trigger dismissing the menu. This allows for more flexible interactions where the caller can choose to handle touch events without automatically dismissing the menu.

### Fixed

- Fixed property name from `label_text` to `heading_text` in MorphDockedDatePickerField to better reflect its purpose and to align with common terminology for form fields. This change also involved updating internal logic to ensure that the correct property is used for setting the heading text of the date picker field.

## [0.10.0] - 2026-02-18

### Added

- Added setting of active state to False on dropdown button when dropdown menu is dismissed to ensure visual state consistency.
- Added `_bound_leading_widget` property to MorphLeadingWidgetBehavior to store references to widgets with active property bindings.
- Added `_bound_trailing_widget` property to MorphTrailingWidgetBehavior to store references to widgets with active property bindings.
- Added unbinding of properties to previous leading/trailing widgets when they change.
- Added `refresh_widget()` function to morphui.utils.helpers that iterates through all attributes of a given widget and calls any method that starts with `'refresh_'`.
- Added visibility properties to composition behaviors.

### Changed

- Changed all composition behavior classes to inherit from EventDispatcher.
- Changed state-sensitive properties in composition behaviors from AliasProperties to StringProperty.
- Changed child widgets' state-sensitive properties to be bound to their behavior properties instead of using getter/setter methods.
- Changed MorphTextField to inherit from MorphDelegatedThemeBehavior, MorphLeadingWidgetBehavior, MorphTripleLabelBehavior, and MorphTrailingWidgetBehavior.
- Changed MorphFilterChip to no longer inherit from MorphIconBehavior due to changes in composition behaviors.
- Changed default spacing and padding of chips and their child widget classes.
- Changed defining the leading icon for recycled widgets to be done via `normal_leading_icon` instead of `leading_icon` (which only works at init).
- Improved naming in composition behaviors.

### Removed

- Removed obsolete getter and setter methods used for AliasProperties in composition behaviors.
- Removed obsolete `_update_icon` method from MorphFilterChip.
- Removed obsolete reinvented code from MorphTextField that is now covered by new behavior inheritance.

### Fixed

- Fixed bug where `label_text` was used instead of `heading_text` where needed.

## [0.9.0] - 2026-02-16

### Added

- Added `explicit_color_properties` set to MorphColorThemeBehavior for tracking user-specified colors that should not be automatically updated by theme changes.
- Added `_detect_explicit_properties()` method to MorphColorThemeBehavior to auto-detect explicitly set color properties from kwargs during initialization.
- Added `_refresh_list_views()` method to MorphDockedDatePickerMenu for refreshing list views before displaying.
- Added 'disabled' theme style to `THEME.STYLES` constant.

### Changed

- Changed MorphColorThemeBehavior to give `theme_color_bindings` precedence over `theme_style`, allowing override of predefined theme style bindings.
- Changed all widgets to use `default_config.copy() | kwargs` pattern in `__init__`, replacing clean_config usage.
- Changed MorphDockedDatePickerMenu to inherit from MorphElevationBoxLayout.
- Changed MorphDockedDatePickerMenu to return to calendar view when a month is selected in month view.
- Changed MorphDockedDatePickerMenu to reposition menu when size changes to ensure it connects to caller.
- Changed MorphDockedDatePickerMenu to return to calendar view when using arrow keys while in list view (year or month).
- Changed MorphChartToolbar to inherit from MorphToggleButtonBehavior class.
- Changed MorphChartToolbar menu toggling to use active state instead of manual open/close.
- Changed composition behaviors to call `_update_icon` within refreshing leading or trailing widget methods.
- Changed ListView classes to use f-strings for Builder.load_string and define tree using `__name__` attribute.
- Changed all THEME.STYLES to have consistent disabled colors across all styles.

### Removed

- Removed `clean_config()` function from morphui.utils.helpers, replaced with dynamic explicit property tracking system.
- Removed obsolete `_update_content_layer` override from MorphDelegatedThemeBehavior.

### Fixed

- Fixed MorphDockedDatePickerMenu where highlighting and marking selected buttons when using text input instead of clicking on a button now works correctly.
- Fixed MorphDockedDatePickerMenu where wrong item had check mark when switching to list view; list view is now refreshed before entering.
- Fixed MorphDockedDatePickerMenu to set the correct item active when changing year or month using arrow buttons.
- Fixed MorphChartToolbar where menu was closed and reopened when clicking on button while menu was already open.
- Fixed MorphContentLayerBehavior where resetting `disabled_content_color` is now done in `_update_content_layer` method instead of `refresh_content` method with outdated color.
- Fixed MorphDelegatedThemeBehavior where delegating states are now done in `_update_current_state` method override instead of using bindings which didn't work properly.

## [0.8.0] - 2026-02-12

### Added

- Added container theme style to `THEME.STYLES` constant.
- Added `_clear_active` and `set_active_by_text` methods to BaseDatePickerListView for updating each item when showing the view.
- Added getter and setter methods for `disabled_content_color` in MorphContentLayerBehavior.
- Added default `pos_hint={'center_y': 0.5}` for labels and buttons used within containers.

### Changed

- Changed buttons to use 'container' as `theme_style`.
- Changed MorphContentLayerBehavior's `disabled_content_color` to an AliasProperty to handle kivy native disabled colors.
- Changed MorphListItemFlat to also call refreshing state and interaction in `refresh_view_attrs` method.
- Changed MorphTextField where setting y position for leading and trailing widget is obsolete since widgets are centered by pos_hint.
- Changed MorphDropdownList to remove obsolete checking for children length within `set_focus_by_text` method.

### Removed

- Removed obsolete `get_resolved_content_color` method from MorphContentLayerBehavior since `_get_content_color` method exists for the `content_color` AliasProperty.

### Fixed

- Fixed MorphContentLayerBehavior where resetting `disabled_content_color` was done in `refresh_content` method with outdated color. Now resetting is done in `_update_content_layer` method.
- Fixed MorphDropdownMenu where dropdown reopened when clicking a caller. Now it checks if a ripple is in progress and only sets caller active state to False if no ripple is in progress.

## [0.7.0] - 2026-02-11

### Added

- Added `hex_colormap` as DictProperty to ThemeManager to store registered seed colors.
- Added `available_seed_colors` as AliasProperty to ThemeManager that is bound to changes of hex_colormap.
- Added `colormap` as read-only property to ThemeManager to return a RGBA colormap derived from hex_colormap.
- Added `leading_scale_enabled` BooleanProperty to MorphLeadingWidgetBehavior as flag, whether scale animations are enabled for the leading widget.
- Added `on_pre_open` method to chart in which the flag `dismiss_allowed` is set to True.
- Added refreshing view from data in `on_pre_open` and in `on_pre_dismiss` to MorphDropdownMenu to ensure the view is up to date after a selection.

### Changed

- Changed ThemeManager's `is_dark_mode` to an AliasProperty so we can react to that when theme style changes (e.g. a theme toggle button can get active and normal state based on is_dark_mode status).
- Changed storing registered colors in ThemeManager to be handled locally instead of storing to kivy global colormap.
- Changed default theme_color_bindings for buttons.
- Changed predefined theme styles.
- Changed default border width to dp(0.5).
- Changed layer.py color retrieval to use a consistent method: tries to get the color for current state; if a specific color for the state is not set, it falls back to the normal color; if that is also not set it returns the transparent color.

## [0.6.0] - 2026-02-10

### Added

- Added MorphDropdownButton class (a simple dropdown select button that can be used to trigger a dropdown menu).
- Added MorphSimpleBoxLayout class that is basic kivy BoxLayout with support for auto_sizing.
- Added MorphTripleLabelBehavior class for managing heading, supporting and tertiary label widgets.
- Added MorphHeadingLabel, MorphSupportingLabel and MorphTertiaryLabel classes.
- Added MorphListItem which provides a more complex layout than MorphListItemFlat with heading, supporting and tertiary labels.
- Added MorphToggleListItem that extends MorphListItem with toggling its active state.
- Added tests for MorphTripleLabelBehavior class.

### Changed

- Changed MorphDropdownList to set focus to lowest child at `on_arrow_up_press` method if none has focus.
- Changed Container classes to inherit from the new MorphSimpleBoxLayout.
- Changed attribute name from `default_child_widgets` to `default_child_classes` in Container.
- Changed MorphMenuMotionBehavior, moved presetting size from `_adjust_and_reposition` method into `_adjust_to_fit_window` method.
- Changed touch behavior, removed overlapping transition part for ripple in and out.

### Fixed

- Fixed MorphMenuMotionBehavior where presetting size before adjusting to window did not consider adjusting size to caller when `same_width_as_caller` was set to True.

## [0.5.0] - 2026-02-05

### Added

- Added MorphScrollView class to scrollview.py module.
- Added MorphTabNavigationManagerBehavior and MorphTabNavigableBehavior for managing tab navigation between widgets.
- Added `is_empty` property to MorphDataViewTable to indicate when table has no data to show.
- Added attributes for top left and lower left widgets in MorphDataViewTable.
- Added `available_texts` property to BaseListView.
- Added `_clear_hover` method to MorphDropdownList.
- Added `_set_focus_by_text` method to MorphDropdownList.
- Added tests for refactored KeyPressBehavior.
- Added tests for MorphTabNavigableBehavior class.
- Added tests for MorphTabNavigationManagerBehavior.

### Changed

- Changed MorphStateBehavior's `update_available_states` method to bind and unbind only available states.
- Changed default `disabled_state_opacity` to 0.0 in MorphInteractionLayerBehavior.
- Changed all properties named `interaction_layer_` to `interaction_` in InteractionLayer.
- Changed property name from `delegate_to_children` to `delegated_children` in MorphDelegatedThemeBehavior.
- Changed method name from `_update_delegated_children` to `_setup_child_delegation` in MorphDelegatedThemeBehavior.
- Changed MorphDataViewTable to remove edges of top_left widget when table is empty.
- Changed MorphDropdownMenu to set current focus of current text at `on_pre_open` method.
- Changed MorphDropdownMenu to clear focus and hover state for all items at `on_dismiss` method.
- Changed MorphTabNavigableBehavior to automatically remove tabs in text property.
- Changed `return None` to `return` for early exit at functions and methods where no return value is expected.
- Removed tab handling from MorphKeyPressBehavior and moved to MorphTabNavigationManagerBehavior.
- Removed random added imports.

### Fixed

- Fixed delegating content in MorphDelegatedThemeBehavior which did not work correctly.
- Fixed MRO error by removing redundant base classes from MorphDataViewNavigationButton.
- Fixed MorphPlotWidget where calling home of navigation during double tap failed if there is no navigation.
- Fixed MorphTextField trying to recalculate layout when widget is on a Screen of ScreenManager and was never visible.
- Fixed MorphDropDownMenu where listview registered key presses even when it was not open.
- Fixed Composition behavior where getting and setting icons failed for recycled widgets, using wrong icons for setting new ones.

## [0.4.0] - 2026-01-29

### Added

- Added key press behavior to MorphDropdownList to allow navigation and selection using keyboard arrows and enter key.
- Added focus state flag to MorphListItemFlat to visually indicate when an item is focused.
- Added MorphKeyPressBehavior inheritance to BaseListView.
- Added overloads for clamp function in helpers module.
- Added default item_release_callback for MorphDropdownFilterField, setting on_item_release method as the default.

### Fixed

- Fixed an issue where the filter_value property in Dropdown was set to wrong child widget, preventing filtering from working.
- Fixed MorphTooltip not dismissing anymore after introduction of MorphMenuBehavior.

### Changed

- Changed binding of hovering flag to dismiss_allowed flag for Tooltip.
- Changed binding of focus flag to dismiss_allowed flag for Dropdown.

### Removed

- Removed on_open override in Dropdown to keep it available for further customization.

## [0.3.1] - 2026-01-21

### Added

- Added active state to OverlayState.
- Added active_overlay_edge_color property to MorphOverlayLayerBehavior.

### Fixed

- Fixed an issue where the datepicker menu would not dismiss correctly when the text field lost focus.
- Fixed overlay layer not updating correctly on state change in MorphOverlayLayerBehavior.
- Fixed MorphMenuMotionBehavior to schedule calling dismiss in on_touch_up() method to ensure it registers allowing_dismiss when clicking outside of caller and menu.

### Changed

- Changed MorphMenuMotionBehavior to set dismiss_allowed to False before opening.
- Changed MorphMenuMotionBehavior to dispatch on_open after animation.
- Changed MorphMenuMotionBehavior to dispatch on_dismiss after animation.

### Removed

- Removed override of on_touch_down() method from MorphMenuMotionBehavior.

## [0.3.0] - 2026-01-19

### Added

- The module datepicker.py was added to MorphUI which provides a date picker widget with single and range selection modes.
- The MorphScreenManager was added to MorphUI which extends the Kivy ScreenManager with MorphUI theming and transitions.
- The MorphDelegatedThemeBehavior was added to MorphUI which allows delegating theming properties to a target widget.
- The MorphHighlightLayerBehavior was added to MorphUI which provides a highlight layer for widgets.

### Changed

- The default configuration for some buttons and labels was changed.

### Fixed

- Fixed missing inheritance of MorphContentLayerBehavior for MorphSimpleiconButton
- Storing original size and size_hint was a list instead of a tuple which leads to unpredictable behaviors when using MorphSizeBoundsBehavior.
  
## [0.2.0] - 2026-01-06

### Added

- Added themeing support for MorphUI widgets.
- Added uix folder for MorphUI widgets.
- Added utility functions for MorphUI.
- Added dataviews for MorphUI.
- Added visualizations for MorphUI.