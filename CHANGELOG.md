# Changelog

All notable changes to Azure Nuke will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Homebrew support for macOS and Linux
- Cross-platform binary support (Darwin AMD64/ARM64, Linux AMD64/ARM64, Windows AMD64)
- GitHub Pages documentation site
- Comprehensive documentation with MkDocs
- PyInstaller spec for building standalone executables
- Automated release workflows
- Build and release scripts

### Changed
- Improved installation documentation
- Updated project structure for better packaging

## [0.1.3] - 2024-01-20

### Added
- Comprehensive scanning of Azure resources across subscriptions
- Safe deletion with confirmation prompts and dry-run mode
- Flexible filtering by resource type, region, and more
- Exclusion system to protect critical infrastructure
- Beautiful ASCII art banners for a better command-line experience
- Color-coded output for easy identification of actions and results
- Support for multiple Azure resource types (Storage, Compute, Network, KeyVault, Monitor)
- Asynchronous operations for better performance
- Detailed logging and error handling

### Fixed
- Initial release bug fixes and improvements

## [0.1.2] - 2024-01-15

### Added
- Basic resource discovery functionality
- Command-line interface with scan and delete commands
- Configuration file support for exclusions

## [0.1.1] - 2024-01-10

### Added
- Initial project structure
- Basic Azure authentication

## [0.1.0] - 2024-01-05

### Added
- Initial release of Azure Nuke
- Basic functionality for Azure resource management 