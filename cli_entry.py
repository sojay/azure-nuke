#!/usr/bin/env python3
"""Standalone entry point for Azure Nuke CLI."""

import sys
import os
import asyncio
from colorama import init, Fore, Style

# Handle bundled executable path resolution
if getattr(sys, 'frozen', False):
    # Running in a bundle (PyInstaller)
    application_path = os.path.dirname(sys.executable)
    bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    config_path = os.path.join(bundle_dir, 'config', 'exclusions.yaml')
    if not os.path.exists(config_path):
        config_path = os.path.join(bundle_dir, 'aznuke', 'config', 'exclusions.yaml')
else:
    # Running as a normal Python script
    application_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(application_path, 'config', 'exclusions.yaml')
    if not os.path.exists(config_path):
        config_path = os.path.join(application_path, 'aznuke', 'config', 'exclusions.yaml')

# Add the current directory to the path
sys.path.insert(0, application_path)

# Initialize colorama
init(autoreset=True)

# Get version dynamically
try:
    from aznuke import __version__
    version_string = f'Azure Nuke {__version__}'
except ImportError:
    version_string = 'Azure Nuke (version unknown)'

async def _main():
    try:
        from aznuke.cli import create_parser, dispatch_command

        parser = create_parser(default_config_path=config_path, version_string=version_string)
        args = parser.parse_args()
        await dispatch_command(args, parser)
    except ImportError as e:
        print(f"{Fore.RED}Error: Could not import Azure Nuke modules: {e}{Style.RESET_ALL}")
        print("Make sure Azure Nuke is properly installed.")
        if "-v" in sys.argv or "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if "-v" in sys.argv or "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def main():
    """Entry point for the application script"""
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
