# safety.py
from src.deletion import delete_resources
from aznuke.src.animations import show_warning_banner, show_summary_by_type

def is_protected_subscription(subscription_id, protected_ids):
    """Check if a subscription is protected from deletion."""
    return subscription_id in protected_ids

async def require_confirmation(resources_to_delete, credentials, dry_run=False):
    """Require user confirmation before deletion."""
    if not resources_to_delete:
        print("No resources to delete.")
        return False
    
    print(f"\nFound {len(resources_to_delete)} resources to delete:")
    
    # Group by type for better readability
    resources_by_type = {}
    for resource in resources_to_delete:
        if resource.type not in resources_by_type:
            resources_by_type[resource.type] = []
        resources_by_type[resource.type].append(resource)
    
    # Display summary using the summary function
    show_summary_by_type(resources_by_type)
    
    if dry_run:
        print("\nDRY RUN MODE: No resources will be deleted.")
        return True
    
    # Show warning banner
    show_warning_banner()
    
    confirmation = input("Type 'DELETE' to confirm deletion: ").strip().lower()
    if confirmation == "delete":
        print("Proceeding with the deletion process...")
        # Call your deletion logic here
        await delete_resources(credentials, resources_to_delete, dry_run=False)
    else:
        print("Deletion process aborted.")
        return False