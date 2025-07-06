#!/usr/bin/env python3
"""Standalone entry point for Azure Nuke CLI."""

import sys
import os
import asyncio
import argparse
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

async def _main():
    parser = argparse.ArgumentParser(
        description="Azure Nuke - Azure resource scanner and cleanup tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument
    parser.add_argument('--version', action='version', version='Azure Nuke 0.1.9')
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for resources in Azure")
    scan_parser.add_argument("--profile", help="Azure subscription profile name")
    scan_parser.add_argument("--region", help="Azure region to scan")
    scan_parser.add_argument("--checks", help="Comma-separated list of resource types to scan")
    scan_parser.add_argument("--output", choices=["text", "json"], default="text", 
                            help="Output format (text or json)")
    scan_parser.add_argument("--severity", choices=["low", "medium", "high"], 
                            help="Filter results by severity")
    scan_parser.add_argument("--config", default=config_path, 
                            help="Path to exclusions configuration file")
    scan_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete resources in Azure")
    delete_parser.add_argument("--profile", help="Azure subscription profile name")
    delete_parser.add_argument("--region", help="Azure region to target")
    delete_parser.add_argument("--checks", help="Comma-separated list of resource types to delete")
    delete_parser.add_argument("--dry-run", action="store_true", 
                              help="Perform a dry run without actually deleting resources")
    delete_parser.add_argument("--config", default=config_path, 
                              help="Path to exclusions configuration file")
    delete_parser.add_argument("--protected-subscriptions", nargs="+", 
                              help="List of subscription IDs that should not be modified")
    delete_parser.add_argument("--yes", "-y", action="store_true", 
                              help="Skip confirmation prompt")
    delete_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Import the actual implementation
    try:
        from aznuke.cli import cmd_scan, cmd_delete
        
        if args.command == "scan":
            await cmd_scan(args)
        elif args.command == "delete":
            await cmd_delete(args)
        else:
            parser.print_help()
    except ImportError as e:
        print(f"{Fore.RED}Error: Could not import Azure Nuke modules: {e}{Style.RESET_ALL}")
        print("Make sure Azure Nuke is properly installed.")
        if args.verbose if hasattr(args, 'verbose') else False:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if args.verbose if hasattr(args, 'verbose') else False:
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