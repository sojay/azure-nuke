# filtering.py
import yaml
import re
import os
import sys

def find_config_file(config_path):
    """
    Find the configuration file in various locations.
    
    Args:
        config_path: The path provided by the user
        
    Returns:
        The path to the config file or None if not found
    """
    # Check if the provided path exists
    if os.path.exists(config_path):
        return config_path
    
    # Check in the current directory
    if os.path.exists(os.path.join(os.getcwd(), config_path)):
        return os.path.join(os.getcwd(), config_path)
    
    # Check in the package directory
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(os.path.join(package_dir, config_path)):
        return os.path.join(package_dir, config_path)
    
    # Check in the config subdirectory of the package
    config_dir = os.path.join(package_dir, 'config')
    if os.path.exists(os.path.join(config_dir, os.path.basename(config_path))):
        return os.path.join(config_dir, os.path.basename(config_path))
    
    # As a last resort, look for the default exclusions file in the package
    default_path = os.path.join(package_dir, 'config', 'exclusions.yaml')
    if os.path.exists(default_path):
        print(f"Using default exclusions file from: {default_path}")
        return default_path
    
    return None

def load_exclusions(config_file):
    """Load exclusion rules from YAML configuration."""
    config_path = find_config_file(config_file)
    
    if not config_path:
        print(f"Warning: Could not find exclusions file at {config_file}. No exclusions will be applied.")
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Failed to load exclusions file: {e}")
        return {}

def should_preserve(resource, exclusions):
    """Determine if a resource should be preserved based on exclusion rules."""
    # Check if resource type is excluded
    if resource.type in exclusions.get('resource_types', []):
        return True
    
    # Check if resource name matches excluded patterns
    for pattern in exclusions.get('name_patterns', []):
        if re.match(pattern, resource.name):
            return True
    
    # Check for specific resource IDs
    if resource.id in exclusions.get('resource_ids', []):
        return True
    
    # Check for resource tags
    if hasattr(resource, 'tags') and resource.tags:
        for tag_key, tag_value in exclusions.get('tags', {}).items():
            if tag_key in resource.tags and resource.tags[tag_key] == tag_value:
                return True
    
    return False

def filter_resources(resources, exclusions, progress_bar=None):
    """Filter resources based on exclusion rules."""
    resources_to_delete = []
    resources_to_preserve = []

    for resource in resources:
        # Update progress bar if provided
        if progress_bar:
            progress_bar.update(1)

        # Check if resource should be preserved based on exclusion rules
        if should_preserve(resource, exclusions):
            resources_to_preserve.append(resource)
        else:
            resources_to_delete.append(resource)

    return resources_to_delete, resources_to_preserve