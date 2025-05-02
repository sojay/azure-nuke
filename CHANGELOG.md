# Changelog

All notable changes to the Azure Nuke project will be documented in this file.

## [0.1.3] - 2025-05-02

### Changed
- Updated README with Cloudinary image hosting
- Fixed image display in PyPI documentation

## [0.1.1] - 2025-05-01

### Added
- Beautiful ASCII art banners for the main application, warnings, and completion screens
- Added show_warning_banner function to display danger alerts before resource deletion
- Updated completion screens with custom ASCII art for both successful and partial completions

### Changed
- Replaced Figlet-generated text with custom ASCII art banners
- Updated the safety confirmation UI to use the new warning banner
- Improved visual consistency across the application

## [0.1.0] - 2025-05-01

### Added
- Initial release
- Azure resource scanning functionality
- Resource deletion with safety confirmations
- Dry run mode for previewing actions
- Exclusion system via YAML configuration
- Support for filtering by resource type, region, and subscription 