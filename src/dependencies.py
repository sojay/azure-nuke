# dependencies.py
def build_dependency_graph(resources):
    """Build a graph of resource dependencies."""
    dependency_graph = {}
    
    # Initialize the graph
    for resource in resources:
        dependency_graph[resource.id] = []
    
    # This is a simplified approach. In a real implementation,
    # you would need to query Azure's API for specific dependency information
    # or infer dependencies based on resource types and properties.
    
    # For example, a VM depends on its NIC, which depends on its subnet, etc.
    
    return dependency_graph

def sort_by_dependencies(resources, dependency_graph):
    """Sort resources based on their dependencies (topological sort)."""
    # This is a simplified version. A real implementation would use
    # a proper topological sort algorithm.
    
    # For now, we'll use a basic approach that prioritizes known
    # resource types in a reasonable order
    
    # Common deletion order (from leaf to root):
    # 1. Virtual Machines
    # 2. Disks
    # 3. NICs
    # 4. Public IPs
    # 5. NSGs
    # 6. Virtual Networks
    # 7. Resource Groups
    
    type_order = {
        'Microsoft.Compute/virtualMachines': 1,
        'Microsoft.Compute/disks': 2,
        'Microsoft.Network/networkInterfaces': 3,
        'Microsoft.Network/publicIPAddresses': 4,
        'Microsoft.Network/networkSecurityGroups': 5,
        'Microsoft.Network/virtualNetworks': 6,
        'Microsoft.Resources/resourceGroups': 7,
    }
    
    # Default priority for unknown types
    default_priority = 0
    
    return sorted(resources, key=lambda r: type_order.get(r.type, default_priority))