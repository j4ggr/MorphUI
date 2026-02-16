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