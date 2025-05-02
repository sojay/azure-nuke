# main.py
import asyncio
import argparse
from colorama import init, Fore, Style
from azure.identity import DefaultAzureCredential
from src.auth import get_subscriptions
from src.discovery import discover_all_resources
from src.filtering import load_exclusions, filter_resources
from src.deletion import delete_resources
from src.safety import require_confirmation, is_protected_subscription
from src.animations import (
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

async def get_subscriptions_async(credentials):
    """Async wrapper for getting subscriptions"""
    # This function turns the synchronous get_subscriptions into an awaitable
    result = await asyncio.to_thread(get_subscriptions, credentials)
    return result

async def discover_resources_async(credentials, subscriptions):
    """Async wrapper for resource discovery"""
    # This function turns the synchronous discover_all_resources into an awaitable
    result = await asyncio.to_thread(discover_all_resources, credentials, subscriptions)
    return result

async def filter_resources_async(all_resources, exclusions, progress_bar):
    """Async wrapper for resource filtering"""
    # This function turns the synchronous filter_resources into an awaitable
    result = await asyncio.to_thread(filter_resources, all_resources, exclusions, progress_bar)
    return result

async def main():
    try:
        # Show startup animation
        show_startup_animation()
        
        parser = argparse.ArgumentParser(description="Azure Nuke - Delete all resources in Azure subscriptions")
        parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting resources")
        parser.add_argument("--config", default="config/exclusions.yaml", help="Path to exclusions configuration file")
        parser.add_argument("--protected-subscriptions", nargs="+", help="List of subscription IDs that should not be modified")
        args = parser.parse_args()
        
        # Get credentials
        credentials = DefaultAzureCredential()
        
        # Get subscriptions with proper async handling
        subscriptions = await async_spinner("Retrieving subscriptions...", get_subscriptions_async(credentials))
        
        # Filter out protected subscriptions
        if args.protected_subscriptions:
            subscriptions = [sub for sub in subscriptions if not is_protected_subscription(sub.subscription_id, args.protected_subscriptions)]
        
        print(f"{Fore.CYAN}Found {len(subscriptions)} accessible subscriptions{Style.RESET_ALL}")
        
        # Discover all resources with progress animation
        print(f"{Fore.YELLOW}[DISCOVERING]{Style.RESET_ALL} Starting resource discovery across all subscriptions...")
        all_resources = await async_spinner("Scanning Azure resources...", discover_resources_async(credentials, subscriptions))
        print(f"{Fore.CYAN}Found {len(all_resources)} total resources{Style.RESET_ALL}")
        
        # Load exclusions and filter resources
        exclusions = load_exclusions(args.config)
        progress_bar = create_progress_bar(len(all_resources), "Filtering resources")
        
        # Use async wrapper for filtering
        resources_to_delete, resources_to_preserve = await filter_resources_async(all_resources, exclusions, progress_bar)
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
        
        # Get confirmation and delete resources
        if await require_confirmation(resources_to_delete, credentials, args.dry_run):
            deleted, failed = await delete_resources(credentials, resources_to_delete, args.dry_run)
            
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
        # Print more detailed error information for debugging
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())