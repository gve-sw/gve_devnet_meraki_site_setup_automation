# GVE DevNet Meraki Site Setup
This prototype is used to automate the configuration of Meraki network switch settings. Specifically, this prototype will configure L3 interfaces for a given switch, ssids for the VLANs, and ACLs for the network.

## Contacts
* Danielle Stacy

## Solution Components
* Meraki APIs
* Python 3.9

## Prerequisites
#### Meraki API Keys
In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization). 

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).

#### Organization Name, Network Name, and Serial Number
This prototype requires retrieving the organization and network ids to make the API requests. The code itself will find the ids, but it requires the user to provide the name of the organization and network that the switch is found in. Additionally, the API calls require the serial number of the switch it will be configuring.
To find the name of the organization, follow these instructions:
1. Login to the Meraki dashboard.
2. In the left-hand menu, select the Organization dropdown menu. It should be the first item in the menu.
3. All of the organizations should now be listed in the left-hand menu. To view a summary of the organizations, select the `MSP Portal` option.
4. Note the name of the organization that the switch is located in. This name will be needed in the Installation portion of this prototype.

> For more information on MSP Portal, visit [this article](https://documentation.meraki.com/General_Administration/Inventory_and_Devices/Monitoring_and_Managing_Multiple_Organizations)

Once the organization name has been found, it is time to locate the network name. To find the name of the network, follow these instructions:
1. In the left-hand menu, select the Organization dropdown menu. It should be the first item in the menu. 
2. All of the organizations should now be listed in the left-hand menu. Select the organization name that was determined previously.
3. Now all of the networks associated with the organization should be listed on the dashboard. Note the name of the network that the switch is located in.

Finally, after the network name has been noted, the serial number of the switch is needed. To find the serial number of the network, follow these instructions:
1. Select the network that was noted previously. 
2. The dashboard should now reflect the network settings of the network selected. In the left-hand menu, the different network options should be displayed. Select the `Switch` option, then from that menu select the `Switches` option.
3. The dashboard should now display the switches in the network. Select the switch that will have Layer 3 interfaces configured on it.
4. The dashboard should now display the information specific to the switch. The location, LAN IP, serial number, L3 routing status, etc of the switch should be listed on the left side of the dashboard, next to the left-hand menu. Make note of the serial number of the switch.

## Installation/Configuration
1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_meraki_site_setup_automation`
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Add Meraki API key, organization name, network name, and serial number that were retrieved in the Prerequisites section to the environmental variables in the .env file.
```
API_KEY="API key goes here"
ORG_NAME="name of organization goes here"
NET_NAME="name of network goes here"
SERIAL="serial number of switch goes here"
```
4. In the file l3_interfaces.csv, provide the information necessary for the layer 3 interfaces you are trying to configure. This includes the name, VLAN number, the subnet with that interface (in CIDR notation), the IP address of the interface, whether you want to enable IGMP snooping (true or false), whether DHCP relay should be enabled, and the SSID number of the SSID that should be associated with the interface if it needs an SSID configured with it. If the interface does not need an SSID, give the number -1 for this field.
5. (Optional) If you are wanting to configure DHCP relay for the interface, provide a list of IP addresses for the DHCP relay servers on line 109 of setup_site.py.
6. (Optional) If you are wanting to configure SSIDs, provide the SSID information in the file ssids.json. The given ssids.json file provides a template for an SSID with auth mode 8021x-radius. You'll have to customize it to fit your specific RADIUS server configurations. To use a different auth mode, refer to the [documentation](https://developer.cisco.com/meraki/api-v1/#!update-network-wireless-ssid) for the APIs on SSIDs.
7. (Optional) If you are wanting to configure an ACL for this switch, provide the information needed for the list in the file acls.json. The current acls.json file provides a template to follow. Make sure that if you choose to configure an ACL with this option, that it remains in the format provided in the file.
8. Install the requirements with `pip3 install -r requirements.txt`

> Note: If no layer 3 interfaces have previously been configured, you will have to add a default route. For more information about configuring layer 3 interfaces with APIs, visit the [documentation](https://developer.cisco.com/meraki/api-latest/#!create-device-switch-routing-interface).


## Usage
To run the program, use the command:
```
$ python3 setup_site.py
```

Once the program has set up the layer 3 interfaces, it will prompt you to choose if you want to configure an access control list. Type y if you would like to and n if you would not.

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Output from running the code to configure layer 3 interfaces and SSIDs.
![/IMAGES/l3_interface_output.png](/IMAGES/l3_interface_output.png) 

Prompt to configure ACL and output from adding rules to the ACL.
![/IMAGES/acl_output.png](/IMAGES/acl_output.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
