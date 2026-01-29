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

## [0.4.0] - 2026-01-29

### Added

- Added key press behavior to MorphDropdownList to allow navigation and selection using keyboard arrows and enter key.
- Added focus state flag to MorphListItemFlat to visually indicate when an item is focused.

### Fixed

- Fixed an issue where the filter_value property in Dropdown was set to wrong child widget. So that filtering did not work at all.

### Changed

- Binding hovering flag to dismiss_allowed flag for Tooltip and Dropdown to ensure correct behavior when hovering state changes.

### Removed

- Removed on_open override in Dropdown as so stays available for further customization.

## [0.3.1] - 2026-01-21

### Fixed

- Fixed an issue where the datepicker menu would not dismiss correctly when the text field lost focus.
- Fixed overlay layer not updating correctly on state change in MorphUI.

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