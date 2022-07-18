#!/usr/bin/env python3
'''
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''
import requests
import json, csv
import os
from pprint import pprint
from dotenv import load_dotenv

# get environmental variables from the .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
ORG_NAME = os.getenv('ORG_NAME')
NET_NAME = os.getenv('NET_NAME')
SERIAL = os.getenv('SERIAL')

base_url = "https://api.meraki.com/api/v1"
headers = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# get org id
orgs_endpoint = "/organizations"
orgs = json.loads(requests.get(base_url+orgs_endpoint, headers=headers).text)
for org in orgs:
    if org["name"] == ORG_NAME:
        org_id = org["id"]

# get network id
networks_endpoint = "/organizations/{}/networks".format(org_id)
nets = json.loads(requests.get(base_url+networks_endpoint, headers=headers).text)
for net in nets:
    if net["name"] == NET_NAME:
        net_id = net["id"]

# url endpoints
acl_endpoint = "/networks/{}/switch/accessControlLists".format(net_id)
l3_interface_endpoint = "/devices/{}/switch/routing/interfaces".format(SERIAL)
dhcp_l3_interface_endpoint = l3_interface_endpoint + '/{}/dhcp'
ssid_endpoint = "/networks/" + net_id + "/wireless/ssids/{}"

# get layer 3 interface information from csv file
interfaces_file = open("l3_interfaces.csv", "r")
csv_reader = csv.DictReader(interfaces_file)

# get ssids from json file
ssid_file = open("ssids.json", "r")
ssid_body = json.load(ssid_file)
ssid_file.close()

# configure each interface from each line of the interfaces csv file
for row in csv_reader:
    name = row["name"]
    vlan_num = row["vlan_num"]
    subnet = row["subnet"]
    ip_addr = row["ip_address"]
    snooping_answer = row["igmp_snooping"]
    relay_answer = row["dhcp_relay"]
    ssid_num = row["ssid_num"]

    if snooping_answer.lower() == 'true':
        enable_snooping = True
    else:
        enable_snooping = False

    if relay_answer.lower() == 'true':
        enable_relay = True
    else:
        enable_relay = False

    if int(ssid_num) != -1:
        enable_ssid = True
    else:
        enable_ssid = False

    l3_body = {
        "name": name,
        "vlanId": vlan_num,
        "subnet": subnet,
        "interfaceIp": ip_addr
    }

    if enable_snooping:
        l3_body["multicastRouting"] = "IGMP snooping querier"

    # API call to create layer 3 interfaces
    l3_response = requests.post(base_url+l3_interface_endpoint, headers=headers, data=json.dumps(l3_body))
    pprint("L3 interface with VLAN {} created with reponse: {}".format(vlan_num, l3_response.text))
    l3_interface = json.loads(l3_response.text)
    interface_id = l3_interface["interfaceId"]

    if enable_relay: # dhcp relay needs to be configured
        dhcp_body = {
            "dhcpMode": "dhcpRelay",
            "dhcpRelayServerIps": [] # provide dhcp relay server ips
        }
        # API call to add DHCP relay to vlan
        dhcp_response = requests.put(base_url+dhcp_l3_interface_endpoint.format(interface_id), headers=headers, data=json.dumps(dhcp_body))
        pprint("VLAN {} updated to have DHCP relay with response {}".format(vlan_num, dhcp_response.text))

    if enable_ssid: # ssid is associated with this vlan
        # API call to create SSID
        ssid_response = requests.put(base_url+ssid_endpoint.format(ssid_num), headers=headers, data=json.dumps(ssid_body))
        pprint("SSID {} updated with response {}".format(ssid_num, ssid_response.text))

interfaces_file.close()

acl_answer = input("L3 interfaces have been configured. Would you like to add an ACL for this switch? (y/n) ")
if acl_answer.lower() == 'y':
    # create acl from information in json file
    f = open('acls.json')
    acl_body = json.load(f)
    acl_response = requests.put(base_url+acl_endpoint, headers=headers, data=json.dumps(acl_body))
    pprint("ACL for network {} updated with response {}".format(NET_NAME, acl_response.text))
    f.close()
