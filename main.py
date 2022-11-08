# Written By Tyler Zars (11/8/22)

# Requests and parsing
import requests
import json

# ENV Vars
import os
from dotenv import load_dotenv, set_key

# Get ENV Vars for OAuth2
load_dotenv()
incontrol_client_id = os.getenv('incontrol_client_id')
incontrol_client_secret = os.getenv('incontrol_client_secret')

# Make tokens dict
tokens = {}

# Get filepath
file_path = input("Enter the full (non-relative) filepath to the directory that files should be saved too (EX: /Users/tylerzars/Desktop/Ross/PyIncontrolConfig/Testing/): ")

# Read in .env vars
if os.getenv('access_token') != None:
    tokens["access_token"] = os.getenv('access_token')
    tokens["refresh_token"] = os.getenv('refresh_token')
else:
    # Get OAuth2 Token
    url = 'https://api.ic.peplink.com/api/oauth2/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    token_req_payload = {'grant_type': 'client_credentials'}

    # Send post & get back access token
    token_response = requests.post(url, data=token_req_payload, verify=True, allow_redirects=False, auth=(incontrol_client_id, incontrol_client_secret))
    tokens = json.loads(token_response.text)

    # Set .env
    set_key("access_token", tokens["access_token"])
    set_key("refresh_token", tokens["refresh_token"])

    #print(tokens)



# Get orginization id
org_id_request = "https://api.ic.peplink.com/rest/o?access_token=" + tokens['access_token']
org_id_response = (requests.get(org_id_request)).json()

# Loop through all orginizations available
counter = 0
for org in org_id_response["data"]:
    print("[{}]: {} with Orginization ID \"{}\"".format(counter, org["name"], org["id"]))
    counter += 1

# Allow user to select and validate user input
try: 
    user_org_select = int(input("Select or via number in brackets (EX: [1] = 1): "))
    print("Currently selected \"{}\" with org_id code \"{}\"".format(org_id_response["data"][user_org_select]["name"], org_id_response["data"][user_org_select]["id"]))
    org_id = org_id_response["data"][user_org_select]["id"]
except: 
    print("Invalid Orginization ID!")
    exit()

# Get Groups
groups_request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g" + "?access_token=" + tokens['access_token']
groups_response = (requests.get(groups_request)).json()

all_group_id = []
for response in groups_response["data"]:
    all_group_id.append(response["id"])
    #print(response["id"])

print(f"All groups: {all_group_id}")

# Get devices & build dict of them
groups_and_devices_dict = {}
for group in all_group_id: 
    devices_request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d" + "?access_token=" + tokens['access_token']
    devices_response = (requests.get(devices_request)).json()
    #print(devices_response)
    
    devices_list = []
    for response in devices_response["data"]:
        devices_list.append(response["id"])
        #print("{} with devices {}".format(group, response["id"]))

    groups_and_devices_dict[group] = devices_list

print(groups_and_devices_dict)

# Build another dict with devices and list of configs
groups_and_devices_configs_dict = {}
for group in all_group_id: 

    for device in groups_and_devices_dict[group]:
        #print(device)
        configs_request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d/" + str(device) + "/config_backup" +"?access_token=" + tokens['access_token']
        
        device_configs_response = (requests.get(configs_request)).json()
        #print(devices_response)

        # Grab most recent config date
        config_id_response = device_configs_response["data"][-1]
        # Grab most recent config time
        #print(config_id_response["file_list"][-1])

        config_id = config_id_response["file_list"][-1]["id"]

        # Filename for save config
        device_name_request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d/" + str(device) + "?access_token=" + tokens['access_token']
        device_name_response = (requests.get(device_name_request)).json()["data"]["name"]
        file_name = device_name_response + "-"
        file_name += config_id_response["date"].strip("-") + "_"
        file_name += config_id_response["file_list"][-1]["time"].replace(":","_")

        # Save config
        save_config_request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d/" + str(device) + "/config_backup/" + str(config_id) + "?access_token=" + tokens['access_token']
        config_download = (requests.get(save_config_request))
        #print(config_download.content) # See raw hex recieved

        # Add file to filepath for saving
        file_path_save = file_path + file_name + ".conf"
        open(file_path_save, 'wb').write(config_download.content)

        # Print overview of loop
        print("Saved config for {} as {}.conf".format(device_name_response, file_name))

        

