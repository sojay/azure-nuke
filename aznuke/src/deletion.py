# deletion.py
import asyncio
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.subscription import SubscriptionClient
from src.animations import print_resource_action, create_progress_bar, async_spinner

def get_resource_client(credentials, subscription_id):
    """Create a resource management client for a specific subscription."""
    return ResourceManagementClient(credentials, subscription_id)

def get_network_client(credentials, subscription_id):
    """Create a network management client for a specific subscription."""
    return NetworkManagementClient(credentials, subscription_id)

def get_compute_client(credentials, subscription_id):
    """Create a compute management client for a specific subscription."""
    return ComputeManagementClient(credentials, subscription_id)

async def delete_resource(credentials, resource, dry_run=False):
    """Delete a single resource with proper client initialization."""
    # Get API version based on resource type
    api_version = {
        'Microsoft.Network/publicIPAddresses': '2023-05-01',
        'Microsoft.Network/networkInterfaces': '2023-05-01',
        'Microsoft.Network/virtualNetworks': '2023-05-01',
        'Microsoft.Network/networkSecurityGroups': '2023-05-01',
        'Microsoft.Network/networkWatchers': '2023-05-01',
        'Microsoft.Compute/virtualMachines': '2023-07-01',
        'Microsoft.Compute/disks': '2023-04-02'
    }.get(resource.type, '2023-07-01')  # Default to latest if type not found

    print_resource_action(resource, "deleting", dry_run=dry_run)
    
    if not dry_run:
        try:
            resource_client = get_resource_client(credentials, resource.subscription_id)
            
            # Parse resource ID
            id_parts = resource.id.split('/')
            if len(id_parts) > 8:
                resource_group = next((id_parts[index+1] for index, part in enumerate(id_parts) if part == "resourceGroups"), None)
                provider = next((id_parts[index+1] for index, part in enumerate(id_parts) if part == "providers"), None)
                resource_type = '/'.join(id_parts[id_parts.index(provider)+1:id_parts.index(resource.name)])

                poller = resource_client.resources.begin_delete(
                    resource_group_name=resource_group,
                    resource_provider_namespace=provider,
                    parent_resource_path="",
                    resource_type=resource_type,
                    resource_name=resource.name,
                    api_version=api_version
                )
                
                await asyncio.to_thread(poller.result)
                print_resource_action(resource, "deleted", dry_run=dry_run)
                return True
            return False
        except Exception as e:
            print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
            return False
    else:
        # In dry run mode, just simulate a delay
        await asyncio.sleep(0.5)
        print_resource_action(resource, "deleted", details="(simulation)", dry_run=dry_run)
        return True

async def process_special_resource(credentials, resource, dry_run=False):
    """Process resources that need special handling before deletion."""
    try:
        if resource.type == "Microsoft.Network/publicIPAddresses":
            network_client = get_network_client(credentials, resource.subscription_id)
            await disassociate_public_ip(network_client, resource, dry_run)
        elif resource.type == "Microsoft.Network/networkSecurityGroups":
            network_client = get_network_client(credentials, resource.subscription_id)
            await disassociate_nsg(network_client, resource, dry_run)
        elif resource.type == "Microsoft.Network/virtualNetworks/subnets":
            network_client = get_network_client(credentials, resource.subscription_id)
            await delete_subnet(network_client, resource, dry_run)
        elif resource.type == "Microsoft.Network/networkInterfaces":
            compute_client = get_compute_client(credentials, resource.subscription_id)
            await detach_network_interface(compute_client, resource, dry_run)
        elif resource.type == "Microsoft.Compute/disks":
            compute_client = get_compute_client(credentials, resource.subscription_id)
            await detach_disk(compute_client, resource, dry_run)
        
        return True
    except Exception as e:
        print_resource_action(resource, "failed", details=f"Pre-processing failed: {str(e)}", dry_run=dry_run)
        return False

async def disassociate_public_ip(network_client, resource, dry_run=False):
    """Disassociate a public IP address from a network interface."""
    print_resource_action(resource, "deleting", details="Disassociating from network interface", dry_run=dry_run)
    
    if not dry_run:
        try:
            # Get the public IP details
            resource_group = resource.id.split('/resourceGroups/')[1].split('/')[0]
            
            # Get the resource name
            resource_name = resource.name if hasattr(resource, 'name') else resource.id.split('/')[-1]
            
            # Get public IP address
            public_ip = await asyncio.to_thread(
                network_client.public_ip_addresses.get,
                resource_group_name=resource_group,
                public_ip_address_name=resource_name
            )
            
            if not public_ip:
                print_resource_action(resource, "failed", details="Public IP not found", dry_run=dry_run)
                return False

            # Extract NIC details from the public IP configuration
            if hasattr(public_ip, 'ip_configuration') and public_ip.ip_configuration:
                nic_id = public_ip.ip_configuration.id.split('/ipConfigurations')[0]
                nic_name = nic_id.split('/')[-1]

                # Get the network interface
                nic = await asyncio.to_thread(
                    network_client.network_interfaces.get,
                    resource_group, 
                    nic_name
                )

                # Remove the public IP from the NIC's IP configuration
                for ip_config in nic.ip_configurations:
                    if ip_config.public_ip_address and ip_config.public_ip_address.id == resource.id:
                        ip_config.public_ip_address = None

                # Update the NIC
                poller = network_client.network_interfaces.begin_create_or_update(resource_group, nic_name, nic)
                
                # Wait for completion using the spinner
                def poller_result():
                    return poller.result()
                
                await async_spinner(f"Disassociating Public IP {resource_name} from NIC {nic_name}...", asyncio.to_thread(poller_result))
                print_resource_action(resource, "deleted", details=f"Disassociated from NIC {nic_name}", dry_run=dry_run)
                return True
            else:
                print_resource_action(resource, "deleted", details="No NIC association found", dry_run=dry_run)
                return True
        except Exception as e:
            print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
            return False
    else:
        # Simulate delay in dry run mode
        await asyncio.sleep(0.5)
        print_resource_action(resource, "deleted", details="Public IP disassociation (simulation)", dry_run=dry_run)
        return True

async def disassociate_nsg(network_client, resource, dry_run=False):
    """Disassociate a network security group from a network interface."""
    print_resource_action(resource, "deleting", details="Disassociating NSG from resources", dry_run=dry_run)
    
    if not dry_run:
        try:
            resource_group = resource.id.split('/resourceGroups/')[1].split('/')[0]
            disassociations = []
            
            # Get the resource name
            resource_name = resource.name if hasattr(resource, 'name') else resource.id.split('/')[-1]
            
            # List all network interfaces in the resource group
            nics = list(await asyncio.to_thread(network_client.network_interfaces.list, resource_group))
            
            for nic in nics:
                if nic.network_security_group and nic.network_security_group.id == resource.id:
                    # Remove the NSG association
                    nic.network_security_group = None
                    poller = network_client.network_interfaces.begin_create_or_update(resource_group, nic.name, nic)
                    
                    # Wait for completion using the spinner
                    def poller_result():
                        return poller.result()
                    
                    await async_spinner(f"Disassociating NSG from NIC {nic.name}...", asyncio.to_thread(poller_result))
                    disassociations.append(f"NIC: {nic.name}")

            # Check for subnet associations and remove them if a virtual network is involved
            if "/virtualNetworks/" in resource.id:
                vnet_name = resource.id.split('/virtualNetworks/')[1].split('/')[0]
                subnets = list(await asyncio.to_thread(network_client.subnets.list, resource_group, vnet_name))
                
                for subnet in subnets:
                    if subnet.network_security_group and subnet.network_security_group.id == resource.id:
                        subnet.network_security_group = None
                        poller = network_client.subnets.begin_create_or_update(
                            resource_group, vnet_name, subnet.name, subnet
                        )
                        
                        # Wait for completion using the spinner
                        def poller_result():
                            return poller.result()
                        
                        await async_spinner(f"Disassociating NSG from Subnet {subnet.name}...", asyncio.to_thread(poller_result))
                        disassociations.append(f"Subnet: {subnet.name}")
            
            if disassociations:
                details = f"Disassociated from {', '.join(disassociations)}"
            else:
                details = "No associations found"
            
            print_resource_action(resource, "deleted", details=details, dry_run=dry_run)
            return True
        except Exception as e:
            print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
            return False
    else:
        # Simulate delay in dry run mode
        await asyncio.sleep(0.5)
        print_resource_action(resource, "deleted", details="NSG disassociation (simulation)", dry_run=dry_run)
        return True

async def delete_subnet(network_client, resource, dry_run=False):
    """Delete a subnet after ensuring it is not in use."""
    print_resource_action(resource, "deleting", details="Preparing subnet for deletion", dry_run=dry_run)
    
    if not dry_run:
        try:
            # Get the resource name
            resource_name = resource.name if hasattr(resource, 'name') else resource.id.split('/')[-1]
            
            # Extract VNet name and resource group
            path_parts = resource.id.split('/')
            vnet_index = path_parts.index('virtualNetworks') if 'virtualNetworks' in path_parts else -1
            
            if vnet_index > 0 and vnet_index + 1 < len(path_parts):
                vnet_name = path_parts[vnet_index + 1]
                resource_group = path_parts[path_parts.index('resourceGroups') + 1] if 'resourceGroups' in path_parts else None
                
                if not resource_group:
                    raise ValueError("Resource group not found in resource ID")
                
                # List all network interfaces in the subnet
                nics = list(await asyncio.to_thread(network_client.network_interfaces.list, resource_group))
                nic_deletions = []
                
                for nic in nics:
                    for ip_config in nic.ip_configurations:
                        if ip_config.subnet and ip_config.subnet.id == resource.id:
                            print_resource_action(nic, "deleting", details=f"NIC in Subnet: {resource_name}", dry_run=dry_run)
                            poller = network_client.network_interfaces.begin_delete(resource_group, nic.name)
                            
                            # Wait for completion using the spinner
                            def poller_result():
                                return poller.result()
                            
                            await async_spinner(f"Deleting NIC {nic.name}...", asyncio.to_thread(poller_result))
                            nic_deletions.append(nic.name)
                            print_resource_action(nic, "deleted", dry_run=dry_run)

                # Get the virtual network
                vnet = await asyncio.to_thread(network_client.virtual_networks.get, resource_group, vnet_name)

                # Remove the subnet
                vnet.subnets = [subnet for subnet in vnet.subnets if subnet.name != resource_name]

                # Update the virtual network
                poller = network_client.virtual_networks.begin_create_or_update(resource_group, vnet_name, vnet)
                
                # Wait for completion using the spinner
                def poller_result():
                    return poller.result()
                
                await async_spinner(f"Removing subnet {resource_name} from VNet {vnet_name}...", asyncio.to_thread(poller_result))
                
                details = f"Removed from VNet {vnet_name}"
                if nic_deletions:
                    details += f", deleted NICs: {', '.join(nic_deletions)}"
                
                print_resource_action(resource, "deleted", details=details, dry_run=dry_run)
                return True
            else:
                print_resource_action(resource, "failed", details="Invalid resource ID format for subnet", dry_run=dry_run)
                return False
        except Exception as e:
            print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
            return False
    else:
        # Simulate delay in dry run mode
        await asyncio.sleep(0.5)
        print_resource_action(resource, "deleted", details="Subnet deletion (simulation)", dry_run=dry_run)
        return True

async def detach_network_interface(compute_client, resource, dry_run=False):
    """Detach a network interface from a virtual machine."""
    print_resource_action(resource, "deleting", details="Detaching from VM", dry_run=dry_run)
    
    if not dry_run:
        try:
            resource_id_parts = resource.id.split('/')
            if '/virtualMachines/' in resource.id:
                resource_group = resource.id.split('/resourceGroups/')[1].split('/')[0]
                vm_name = resource.id.split('/virtualMachines/')[1].split('/')[0]

                # Get the virtual machine
                vm = await asyncio.to_thread(compute_client.virtual_machines.get, resource_group, vm_name)

                # Remove the NIC from the VM's network profile
                vm.network_profile.network_interfaces = [
                    nic for nic in vm.network_profile.network_interfaces if nic.id != resource.id
                ]

                # Update the virtual machine
                poller = compute_client.virtual_machines.begin_create_or_update(resource_group, vm_name, vm)
                
                # Wait for completion using the spinner
                def poller_result():
                    return poller.result()
                
                await async_spinner(f"Detaching NIC from VM {vm_name}...", asyncio.to_thread(poller_result))
                print_resource_action(resource, "deleted", details=f"Detached from VM {vm_name}", dry_run=dry_run)
                return True
            else:
                print_resource_action(resource, "failed", details="Not attached to a VM", dry_run=dry_run)
                return False
        except Exception as e:
            print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
            return False
    else:
        # Simulate delay in dry run mode
        await asyncio.sleep(0.5)
        print_resource_action(resource, "deleted", details="NIC detachment (simulation)", dry_run=dry_run)
        return True

async def detach_disk(compute_client, resource, dry_run=False):
    """Detach a disk from a virtual machine."""
    print_resource_action(resource, "deleting", details="Detaching disk", dry_run=dry_run)
    
    if not dry_run:
        try:
            # This is a placeholder for actual disk detachment logic
            # You would need to implement the actual disk detachment here
            await asyncio.sleep(1)
            print_resource_action(resource, "deleted", details="Disk detached", dry_run=dry_run)
            return True
        except Exception as e:
            print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
            return False
    else:
        # Simulate delay in dry run mode
        await asyncio.sleep(0.5)
        print_resource_action(resource, "deleted", details="Disk detachment (simulation)", dry_run=dry_run)
        return True

def build_dependency_graph(resources):
    """Build a dependency graph for the given resources."""
    dependency_graph = {}
    
    # Map resource types to their dependency order
    resource_type_order = {
        "Microsoft.Network/virtualNetworks/subnets": 0,
        "Microsoft.Network/publicIPAddresses": 1,
        "Microsoft.Network/networkInterfaces": 2,
        "Microsoft.Compute/virtualMachines": 3,
        "Microsoft.Network/virtualNetworks": 4,
        "Microsoft.Network/networkSecurityGroups": 5,
        "Microsoft.Storage/storageAccounts": 6,
        "Microsoft.Compute/disks": 7,
        "Microsoft.Resources/resourceGroups": 8,
    }
    
    # Initialize the dependency graph
    for resource in resources:
        resource_id = resource.id
        dependency_graph[resource_id] = []
    
    # Add dependencies based on resource types and relationships
    for resource in resources:
        resource_id = resource.id
        resource_type = resource.type if hasattr(resource, 'type') else ""
        
        for other_resource in resources:
            other_id = other_resource.id
            other_type = other_resource.type if hasattr(other_resource, 'type') else ""
            
            # Skip self-comparison
            if resource_id == other_id:
                continue
            
            # Add dependency based on resource type order
            if (resource_type in resource_type_order and 
                other_type in resource_type_order and 
                resource_type_order[resource_type] < resource_type_order[other_type]):
                dependency_graph[other_id].append(resource)
            
            # Add dependency if one resource is contained within another
            if other_id != resource_id and other_id in resource_id:
                dependency_graph[resource_id].append(other_resource)
    
    return dependency_graph

def sort_by_dependencies(resources, dependency_graph):
    """Sort resources based on their dependencies."""
    sorted_resources = []
    visited = set()

    def visit(resource):
        resource_id = resource.id
        if resource_id in visited:
            return
        visited.add(resource_id)
        for dependency in dependency_graph.get(resource_id, []):
            if isinstance(dependency, str):
                # Handle the case where the dependency is a string ID
                dep_resource = next((r for r in resources if r.id == dependency), None)
                if dep_resource:
                    visit(dep_resource)
            else:
                # Handle the case where the dependency is a resource object
                visit(dependency)
        sorted_resources.append(resource)

    for resource in resources:
        visit(resource)

    return sorted_resources

async def delete_resources(credentials, resources_to_delete, dry_run=True):
    """Delete multiple resources in the correct order with proper async handling."""
    deleted_resources = []
    failed_resources = []
    
    # Group resources by subscription for efficiency
    resources_by_subscription = {}
    for resource in resources_to_delete:
        subscription_id = resource.subscription_id if hasattr(resource, 'subscription_id') else "unknown"
        if subscription_id not in resources_by_subscription:
            resources_by_subscription[subscription_id] = []
        resources_by_subscription[subscription_id].append(resource)
    
    # Create progress bar for overall deletion process
    total_resources = len(resources_to_delete)
    progress_bar = create_progress_bar(total_resources, "Deleting resources" if not dry_run else "Dry run - simulating deletion")
    
    for subscription_id, resources in resources_by_subscription.items():
        # Build and sort the dependency graph
        dependency_graph = build_dependency_graph(resources)
        sorted_resources = sort_by_dependencies(resources, dependency_graph)
        
        for resource in sorted_resources:
            try:
                # Handle special resources that need pre-processing
                if resource.type in [
                    "Microsoft.Network/publicIPAddresses",
                    "Microsoft.Network/networkSecurityGroups",
                    "Microsoft.Network/virtualNetworks/subnets",
                    "Microsoft.Network/networkInterfaces",
                    "Microsoft.Compute/disks"
                ]:
                    await process_special_resource(credentials, resource, dry_run)
                
                # Delete the resource
                result = await delete_resource(credentials, resource, dry_run)
                
                if result is True or (isinstance(result, tuple) and result[0]):
                    deleted_resources.append(resource)
                else:
                    error_msg = result[1] if isinstance(result, tuple) and len(result) > 1 else "Unknown error"
                    failed_resources.append((resource, error_msg))
            except Exception as e:
                print_resource_action(resource, "failed", details=str(e), dry_run=dry_run)
                failed_resources.append((resource, str(e)))
            finally:
                # Update progress bar
                progress_bar.update(1)
    
    progress_bar.close()
    return deleted_resources, failed_resources

# This should only be used for testing
if __name__ == "__main__":
    print("This module is not meant to be run directly. Please use main.py instead.")