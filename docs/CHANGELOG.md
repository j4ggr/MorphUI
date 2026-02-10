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