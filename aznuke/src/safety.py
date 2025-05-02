# safety.py
from src.deletion import delete_resources

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
    
    for resource_type, resources in resources_by_type.items():
        print(f"\n{resource_type} ({len(resources)}):")
        for resource in resources[:10]:  # Show only the first 10 resources of each type
            print(f"  - {resource.name} (Subscription: {resource.subscription_name})")
        if len(resources) > 10:
            print(f"  ... and {len(resources) - 10} more")
    
    if dry_run:
        print("\nDRY RUN MODE: No resources will be deleted.")
        return True
    
    confirmation = input("Type 'DELETE' to confirm deletion: ").strip().lower()
    if confirmation == "delete":
        print("Proceeding with the deletion process...")
        # Call your deletion logic here
        await delete_resources(credentials, resources_to_delete, dry_run=False)
    else:
        print("Deletion process aborted.")
        return False