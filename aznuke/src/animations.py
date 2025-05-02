# src/animations.py
import asyncio
import sys
import os
import time
from colorama import init, Fore, Style
from pyfiglet import Figlet
from tqdm import tqdm
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_startup_animation():
    """Display the startup animation with Azure Nuke logo."""
    clear_screen()
    
    # Create Azure Nuke ASCII art
    fig = Figlet(font='slant')
    azure_nuke_text = fig.renderText('Azure Nuke')
    
    # Print the ASCII art in blue
    print(Fore.BLUE + azure_nuke_text)
    print(Fore.YELLOW + "[INITIALIZING]" + Style.RESET_ALL + " Azure resource removal tool\n")
    
    # Loading animation
    print(Fore.CYAN + "Preparing environment", end='')
    for _ in range(5):
        time.sleep(0.3)
        print(".", end='', flush=True)
    print(Style.RESET_ALL + "\n")

async def async_spinner(message, coro, silent=False):
    """
    Display a spinner while awaiting a coroutine.
    
    Args:
        message (str): Message to display
        coro: The coroutine to await
        silent (bool): Whether to suppress output
    """
    if not silent:
        print(f"{message}...")
    result = await coro  # Await the coroutine
    return result

def print_resource_action(resource, action, details="", dry_run=False):
    """
    Print resource action with color coding.
    
    Args:
        resource: The resource object
        action (str): One of 'scanning', 'deleting', 'deleted', 'skipped', 'failed', 'preserved'
        details (str, optional): Additional details to display
        dry_run (bool): Whether we're in dry run mode
    """
    resource_name = getattr(resource, 'name', str(resource))
    resource_type = getattr(resource, 'type', '')
    
    dry_run_prefix = "[DRY RUN] " if dry_run else ""
    
    if action == "scanning":
        print(f"{Fore.YELLOW}[SCANNING]{Style.RESET_ALL} {resource_type}: {resource_name}", end='\r')
    elif action == "deleting":
        print(f"{Fore.YELLOW}[{dry_run_prefix}DELETING]{Style.RESET_ALL} {resource_type}: {resource_name} {details}")
    elif action == "deleted":
        print(f"{Fore.RED}[{dry_run_prefix}DELETED]{Style.RESET_ALL} {resource_type}: {resource_name} {details}")
    elif action == "preserved":
        print(f"{Fore.GREEN}[PRESERVED]{Style.RESET_ALL} {resource_type}: {resource_name} {details}")
    elif action == "failed":
        print(f"{Fore.MAGENTA}[FAILED]{Style.RESET_ALL} {resource_type}: {resource_name} {details}")
    else:
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {resource_type}: {resource_name} {details}")

def create_progress_bar(total, description="Processing"):
    """Create a tqdm progress bar that can be updated."""
    return tqdm(total=total, desc=description, bar_format='{l_bar}{bar:30}{r_bar}')

def show_summary_by_type(resources_by_type, max_display=10):
    """
    Display a colored summary of resources by type.
    
    Args:
        resources_by_type (dict): Dictionary of resources grouped by type
        max_display (int): Maximum number of resources to display per type
    """
    for resource_type, resources in resources_by_type.items():
        print(f"\n{Fore.CYAN}{resource_type}{Style.RESET_ALL} ({len(resources)}):")
        for resource in resources[:max_display]:
            subscription_name = getattr(resource, 'subscription_name', 'Unknown')
            print(f"  {Fore.WHITE}- {resource.name} {Fore.YELLOW}(Subscription: {subscription_name}){Style.RESET_ALL}")
        if len(resources) > max_display:
            print(f"  {Fore.YELLOW}... and {len(resources) - max_display} more{Style.RESET_ALL}")

def show_completion_animation(success, resources_deleted, resources_failed):
    """
    Show completion animation with statistics.
    
    Args:
        success (bool): Whether the operation was fully successful
        resources_deleted (int): Number of resources successfully deleted/processed
        resources_failed (int): Number of resources that failed to process
    """
    print("\n")
    if success:
        fig = Figlet(font='slant')
        complete_text = fig.renderText('Complete!')
        print(Fore.GREEN + complete_text)
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Operation completed successfully!")
    else:
        fig = Figlet(font='slant')
        complete_text = fig.renderText('Completed')
        print(Fore.YELLOW + complete_text)
        print(f"{Fore.YELLOW}[COMPLETE WITH ERRORS]{Style.RESET_ALL} Some operations failed")
    
    print(f"{Fore.CYAN}         Resources processed: {resources_deleted}")
    if resources_failed > 0:
        print(f"{Fore.RED}         Resources failed: {resources_failed}")
    else:
        print(f"{Fore.CYAN}         Resources failed: {resources_failed}")
    
    print(f"\n{Fore.YELLOW}[NOTE]{Style.RESET_ALL} Please check logs for details.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())