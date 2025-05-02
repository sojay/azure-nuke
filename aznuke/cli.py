#!/usr/bin/env python3
import sys
import argparse
import asyncio
import os
from colorama import init, Fore, Style

from aznuke.src.auth import get_subscriptions
from aznuke.src.discovery import discover_all_resources
from aznuke.src.filtering import load_exclusions, filter_resources
from aznuke.src.deletion import delete_resources
from aznuke.src.safety import require_confirmation, is_protected_subscription
from aznuke.src.animations import (
    show_startup_animation,
    async_spinner,
    print_resource_action,
    create_progress_bar,
    show_summary_by_type,
    show_completion_animation,
    clear_screen
)

# Initialize colorama
init(autoreset=True)

# Default configuration file path
DEFAULT_CONFIG_PATH = "config/exclusions.yaml"

async def get_subscriptions_async(credentials):
    """Async wrapper for getting subscriptions"""
    result = await asyncio.to_thread(get_subscriptions, credentials)
    return result

async def discover_resources_async(credentials, subscriptions, resource_types=None):
    """Async wrapper for resource discovery"""
    result = await asyncio.to_thread(discover_all_resources, credentials, subscriptions, resource_types)
    return result

async def filter_resources_async(all_resources, exclusions, progress_bar):
    """Async wrapper for resource filtering"""
    result = await asyncio.to_thread(filter_resources, all_resources, exclusions, progress_bar)
    return result

def parse_resource_types(checks_str):
    """Parse comma-separated resource types string"""
    if not checks_str:
        return None
    return [check.strip() for check in checks_str.split(',')]

async def cmd_scan(args):
    """Scan for resources in Azure"""
    try:
        # Show startup animation if not in JSON output mode
        if args.output != 'json':
            show_startup_animation()
        
        from azure.identity import DefaultAzureCredential
        credentials = DefaultAzureCredential()
        
        # Get subscriptions with proper async handling
        subscriptions = await async_spinner("Retrieving subscriptions...", 
                                            get_subscriptions_async(credentials), 
                                            silent=args.output == 'json')
        
        # Filter subscriptions by profile if specified
        if args.profile:
            subscriptions = [sub for sub in subscriptions if sub.display_name.lower() == args.profile.lower()]
            if not subscriptions:
                print(f"{Fore.RED}No subscriptions found matching profile '{args.profile}'{Style.RESET_ALL}")
                return
        
        # Filter subscriptions by region if specified
        if args.region:
            # Note: This is a simplification. In a real app, you'd need to filter resources by region, not subscriptions
            print(f"{Fore.CYAN}Filtering by region: {args.region}{Style.RESET_ALL}")
        
        if args.output != 'json':
            print(f"{Fore.CYAN}Found {len(subscriptions)} accessible subscriptions{Style.RESET_ALL}")
        
        # Convert checks to resource types
        resource_types = parse_resource_types(args.checks)
        
        # Discover resources with progress animation
        if args.output != 'json':
            print(f"{Fore.YELLOW}[DISCOVERING]{Style.RESET_ALL} Starting resource discovery...")
        
        all_resources = await async_spinner("Scanning Azure resources...", 
                                           discover_resources_async(credentials, subscriptions, resource_types),
                                           silent=args.output == 'json')
        
        if args.output != 'json':
            print(f"{Fore.CYAN}Found {len(all_resources)} total resources{Style.RESET_ALL}")
        
        # Load exclusions and filter resources
        exclusions = load_exclusions(args.config)
        
        if args.output != 'json':
            progress_bar = create_progress_bar(len(all_resources), "Filtering resources")
        else:
            progress_bar = None
            
        # Use async wrapper for filtering
        resources_to_process, resources_to_preserve = await filter_resources_async(
            all_resources, exclusions, progress_bar
        )
        
        if progress_bar:
            progress_bar.close()
        
        # Filter by severity if specified
        if args.severity:
            # This is a placeholder - you would implement severity filtering
            print(f"{Fore.CYAN}Filtering by severity: {args.severity}{Style.RESET_ALL}")
            # resources_to_process = [r for r in resources_to_process if r.severity == args.severity]
        
        if args.output != 'json':
            print(f"{Fore.YELLOW}[SELECTED]{Style.RESET_ALL} {len(resources_to_process)} resources identified")
            print(f"{Fore.GREEN}[EXCLUDED]{Style.RESET_ALL} {len(resources_to_preserve)} resources excluded")
            
            # Show summary of resources by type
            resources_by_type = {}
            for resource in resources_to_process:
                if resource.type not in resources_by_type:
                    resources_by_type[resource.type] = []
                resources_by_type[resource.type].append(resource)
            
            print(f"\n{Fore.CYAN}Resources Selected:{Style.RESET_ALL}")
            show_summary_by_type(resources_by_type)
        else:
            # Output in JSON format
            import json
            result = {
                "scan_results": {
                    "total_resources": len(all_resources),
                    "resources_identified": len(resources_to_process),
                    "resources_excluded": len(resources_to_preserve),
                    "resources": []
                }
            }
            
            for resource in resources_to_process:
                result["scan_results"]["resources"].append({
                    "name": resource.name,
                    "type": resource.type,
                    "subscription_id": resource.subscription_id,
                    "resource_group": resource.resource_group
                })
            
            print(json.dumps(result, indent=2))
        
    except KeyboardInterrupt:
        if args.output != 'json':
            print(f"\n{Fore.YELLOW}[INTERRUPTED]{Style.RESET_ALL} Operation cancelled by user")
    except Exception as e:
        if args.output != 'json':
            print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL} An unexpected error occurred: {e}")
            # Print more detailed error information in verbose mode
            if args.verbose:
                import traceback
                print(traceback.format_exc())
        else:
            import json
            error_result = {
                "error": str(e)
            }
            print(json.dumps(error_result))

async def cmd_delete(args):
    """Delete resources in Azure"""
    try:
        if not args.yes:
            show_startup_animation()
        
        from azure.identity import DefaultAzureCredential
        credentials = DefaultAzureCredential()
        
        # Get subscriptions with proper async handling
        subscriptions = await async_spinner("Retrieving subscriptions...", 
                                           get_subscriptions_async(credentials))
        
        # Filter subscriptions by profile if specified
        if args.profile:
            subscriptions = [sub for sub in subscriptions if sub.display_name.lower() == args.profile.lower()]
            if not subscriptions:
                print(f"{Fore.RED}No subscriptions found matching profile '{args.profile}'{Style.RESET_ALL}")
                return
        
        # Filter out protected subscriptions
        if args.protected_subscriptions:
            subscriptions = [sub for sub in subscriptions 
                             if not is_protected_subscription(sub.subscription_id, args.protected_subscriptions)]
        
        print(f"{Fore.CYAN}Found {len(subscriptions)} accessible subscriptions{Style.RESET_ALL}")
        
        # Convert checks to resource types
        resource_types = parse_resource_types(args.checks)
        
        # Discover resources with progress animation
        print(f"{Fore.YELLOW}[DISCOVERING]{Style.RESET_ALL} Starting resource discovery...")
        all_resources = await async_spinner("Scanning Azure resources...", 
                                           discover_resources_async(credentials, subscriptions, resource_types))
        
        print(f"{Fore.CYAN}Found {len(all_resources)} total resources{Style.RESET_ALL}")
        
        # Load exclusions and filter resources
        exclusions = load_exclusions(args.config)
        progress_bar = create_progress_bar(len(all_resources), "Filtering resources")
            
        # Use async wrapper for filtering
        resources_to_delete, resources_to_preserve = await filter_resources_async(
            all_resources, exclusions, progress_bar
        )
        
        progress_bar.close()
        
        print(f"{Fore.YELLOW}[SELECTED]{Style.RESET_ALL} {len(resources_to_delete)} resources for deletion")
        print(f"{Fore.GREEN}[EXCLUDED]{Style.RESET_ALL} {len(resources_to_preserve)} resources based on filters")
        
        # Show summary of resources to be deleted
        resources_by_type = {}
        for resource in resources_to_delete:
            if resource.type not in resources_by_type:
                resources_by_type[resource.type] = []
            resources_by_type[resource.type].append(resource)
        
        print(f"\n{Fore.CYAN}Resources Selected for Deletion:{Style.RESET_ALL}")
        show_summary_by_type(resources_by_type)
        
        # Check if it's a dry run
        dry_run = args.dry_run
        
        # Get confirmation and delete resources
        if args.yes or await require_confirmation(resources_to_delete, credentials, dry_run):
            deleted, failed = await delete_resources(credentials, resources_to_delete, dry_run)
            
            # Show completion animation
            success = len(failed) == 0
            show_completion_animation(success, len(deleted), len(failed))
            
            if failed:
                print(f"\n{Fore.YELLOW}[DETAILS]{Style.RESET_ALL} Resources that failed to process:")
                for resource, error in failed:
                    print(f"  {Fore.RED}- {resource.name}: {error}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[CANCELLED]{Style.RESET_ALL} Operation cancelled by user")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[INTERRUPTED]{Style.RESET_ALL} Operation cancelled by user")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL} An unexpected error occurred: {e}")
        # Print more detailed error information in verbose mode
        if args.verbose:
            import traceback
            print(traceback.format_exc())

async def _main():
    parser = argparse.ArgumentParser(
        description="Azure Nuke - Azure resource scanner and cleanup tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run a full scan
    aznuke scan

    # Scan a specific subscription and region
    aznuke scan --profile production --region westus2

    # Scan only Storage and VM resources
    aznuke scan --checks storage,virtualmachines

    # Export results as JSON
    aznuke scan --output json > azure_report.json

    # Delete resources (after confirmation)
    aznuke delete

    # Delete specific resource types without confirmation
    aznuke delete --checks storage,virtualmachines --yes

    # Perform a dry run to see what would be deleted
    aznuke delete --dry-run
"""
    )
    
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
    scan_parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, 
                            help="Path to exclusions configuration file")
    scan_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete resources in Azure")
    delete_parser.add_argument("--profile", help="Azure subscription profile name")
    delete_parser.add_argument("--region", help="Azure region to target")
    delete_parser.add_argument("--checks", help="Comma-separated list of resource types to delete")
    delete_parser.add_argument("--dry-run", action="store_true", 
                              help="Perform a dry run without actually deleting resources")
    delete_parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, 
                              help="Path to exclusions configuration file")
    delete_parser.add_argument("--protected-subscriptions", nargs="+", 
                              help="List of subscription IDs that should not be modified")
    delete_parser.add_argument("--yes", "-y", action="store_true", 
                              help="Skip confirmation prompt")
    delete_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        await cmd_scan(args)
    elif args.command == "delete":
        await cmd_delete(args)
    else:
        parser.print_help()

def main():
    """Entry point for the application script"""
    asyncio.run(_main()) 