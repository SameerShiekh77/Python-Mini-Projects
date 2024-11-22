from azure.identity import AzureCliCredential  # or use DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
import guacamole
import os
import paramiko

 # Define necessary parameters
subscription_id = ""
resource_group_name = ""
location = "westus2"
vm_name = ""
username= ""
password = ""


# Replace with your resource group and image gallery details
image_gallery_name = ""
image_name = ""
image_version = "1.0.0"  # Replace with your image version if applicable


# 18.04-LTS
# 20.185.189.139
# Authenticate with Azure using Azure CLI credentials (or DefaultAzureCredential)
credential = AzureCliCredential()  # or use DefaultAzureCredential() if you've set env variables

# Initialize clients
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)



# Fetch the image ID from the shared image gallery
image = compute_client.gallery_images.get(
    resource_group_name=resource_group_name,
    gallery_name=image_gallery_name,
    gallery_image_name=image_name,
)
image_id = image.id  # Image ID to use in the VM creation parameters



def launch_spot_vm(subscription_id,resource_group_name,location,vm_name,username,password):
   
   
    # Step 1: Create or check resource group
    resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": location}
    )

    # Step 2: Configure VM parameters
    vm_parameters = {
        "location": location,
        "hardware_profile": {"vm_size": "Standard_DS1_v2"},
        "storage_profile": {
            "image_reference": {
                "id":image_id
            }
        },
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": username,
            "admin_password": password  # Use a secure password or SSH keys
        },
        "network_profile": {
            "network_interfaces": [{
                "id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/{vm_name}NIC"
            }]
        },
        
        "security_profile": {
            "security_type": "TrustedLaunch"
        },
        "priority": "Spot",
        "eviction_policy": "Deallocate"  # Option for Azure Spot
    }

    # Step 3: Create Virtual Network, Subnet, Public IP, and Network Interface
    from azure.mgmt.network import NetworkManagementClient

    network_client = NetworkManagementClient(credential, subscription_id)

    # Create a virtual network
    vnet_params = {
        "location": location,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]}
    }
    vnet = network_client.virtual_networks.begin_create_or_update(resource_group_name, f"{vm_name}VNet", vnet_params).result()

    # Create a subnet
    subnet_params = {"address_prefix": "10.0.0.0/24"}
    subnet = network_client.subnets.begin_create_or_update(resource_group_name, f"{vm_name}VNet", f"{vm_name}Subnet", subnet_params).result()

    # Create a public IP address
    public_ip_params = {
        "location": location,
        "public_ip_allocation_method": "Dynamic"
    }
    public_ip = network_client.public_ip_addresses.begin_create_or_update(resource_group_name, f"{vm_name}PublicIP", public_ip_params).result()

    # Create a network interface
    nic_params = {
        "location": location,
        "ip_configurations": [{
            "name": f"{vm_name}IPConfig",
            "public_ip_address": public_ip,
            "subnet": {"id": subnet.id}
        }]
    }
    nic = network_client.network_interfaces.begin_create_or_update(resource_group_name, f"{vm_name}NIC", nic_params).result()

    # Update network interface ID in VM parameters
    vm_parameters["network_profile"]["network_interfaces"][0]["id"] = nic.id

    # Step 4: Create the VM
    async_vm_creation = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name, vm_name, vm_parameters
    )
    vm = async_vm_creation.result()  # Wait for the VM to be created
    print(f"vm: {vm}")
    print(f"VM {vm_name} created successfully with ID: {vm.id}")
    
    # After VM creation, fetch the NIC to retrieve the public IP address
    nic_name = f"{vm_name}NIC"  # Name of the network interface

    # Retrieve the network interface details
    nic = network_client.network_interfaces.get(resource_group_name, nic_name)

    # Get the ID of the public IP address from the NIC's IP configuration
    public_ip_id = nic.ip_configurations[0].public_ip_address.id

    # Fetch the public IP address resource
    public_ip = network_client.public_ip_addresses.get(
        resource_group_name, public_ip_id.split('/')[-1]
    )

    # Print the public IP address
    print(f"Public IP address of VM '{vm_name}': {public_ip.ip_address}")
    host_public_ip = public_ip.ip_address


# spot the vm

def stop_vm(vm_name):

    # Stop (power off) the VM
    print(f"Stopping VM '{vm_name}' in resource group '{resource_group_name}'...")
    async_vm_stop = compute_client.virtual_machines.begin_power_off(resource_group_name, vm_name)
    async_vm_stop.wait()  # Wait for the operation to complete
    
    '''
    This stops (powers off) the VM but does not deallocate it. Powering off stops the VM’s CPU but does not release associated resources (like the IP address). If you want to deallocate the VM to release resources, use begin_deallocate instead:
    '''
    async_vm_deallocate = compute_client.virtual_machines.begin_deallocate(resource_group_name, vm_name)
    async_vm_deallocate.wait()
    print(f"VM '{vm_name}' has been stopped and deallocated.")


    print(f"VM '{vm_name}' has been stopped.")



# delete the vm
def delete_vm(vm_name):

    # Delete the VM
    print(f"Deleting VM '{vm_name}' in resource group '{resource_group_name}'...")
    async_vm_delete = compute_client.virtual_machines.begin_delete(resource_group_name, vm_name)
    async_vm_delete.wait()  # Wait for the delete operation to complete

    print(f"VM '{vm_name}' has been deleted.")
    

    

def create_guacamole_admin_session():
    return guacamole.session(
        ",
        "postgresql",
        "",
        ""
    )


def create_guacamole_connection(ip):
    # create guacamole session using admin api credentials
    guacamole_session = create_guacamole_admin_session()
    # create guacamole connection
    guacamole_connection = guacamole_session.manage_connection(
        request="post",
        type="vnc",
        name="Muhammad Sameer | TESTING | 234",
        parent_identifier=2,
        parameters={
            "hostname": ip,
            "port": "5901",
            "username": "",
            "password": "",
            "enable-sftp": "false",
        },
        attributes={
            "max-connections": "1",
            "max-connections-per-user": "1"
        })
    guacamole_connection_id = guacamole_connection.json().get("identifier")
    print(f"guacamole_connection.json(): {guacamole_connection.json()}")
    # give access of the connection to the user
    user_connection = guacamole_session.update_user_connection(
        username="muhammadsameer.css@gmail.com", connectionid=guacamole_connection_id)
    # update the instance with the connection id
    print(f"user_connection: {user_connection}")



def delete_guacamole_session(id):

    guacamole_session = create_guacamole_admin_session()
    guacamole_session.delete_connection(id)

# launch_spot_vm(subscription_id,resource_group_name,location,vm_name,username,password)
# create_guacamole_connection('')
# delete_guacamole_session('4581')
# stop_vm(vm_name)
# delete_vm(vm_name)


