# Requests and parsing
import requests
import json
import urllib.request

# ENV Vars
import os
from dotenv import load_dotenv, set_key

# Get ENV Vars for OAuth2
load_dotenv()
incontrol_client_id = os.getenv('incontrol_client_id')
incontrol_client_secret = os.getenv('incontrol_client_secret')

# Make tokens dict
tokens = {}

# Read in env vars
if os.getenv('access_token') != None:
    tokens["access_token"] = os.getenv('access_token')
    tokens["refresh_token"] = os.getenv('refresh_token')
else:
    # Get OAuth2 Token: https://docs.informatica.com/integration-cloud/cloud-api-manager/current-version/api-manager-guide/authentication-and-authorization/oauth-2-0-authentication-and-authorization/python-3-example--invoke-a-managed-api-with-oauth-2-0-authentica.html
    url = 'https://api.ic.peplink.com/api/oauth2/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    token_req_payload = {'grant_type': 'client_credentials'}

    # Send post & get back access token
    token_response = requests.post(url, data=token_req_payload, verify=True, allow_redirects=False, auth=(incontrol_client_id, incontrol_client_secret))
    tokens = json.loads(token_response.text)

    # Set ENV
    set_key("access_token", tokens["access_token"])
    set_key("refresh_token", tokens["refresh_token"])

    #print(tokens)



# Get orginization id
request = "https://api.ic.peplink.com/rest/o?access_token=" + tokens['access_token']
org_id_response = (requests.get(request)).json()
org_id = org_id_response["data"][0]["id"]
print("Currently selected \"{}\" with org_id code \"{}\"".format(org_id_response["data"][0]["name"], org_id))


# Get groups
request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g" + "?access_token=" + tokens['access_token']
group_response = (requests.get(request)).json()

all_group_id = []
for response in group_response["data"]:
    all_group_id.append(response["id"])
    #print(response["id"])

print(all_group_id)

# Get devices & build dict of them
groups_and_devices_dict = {}
for group in all_group_id: 
    request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d" + "?access_token=" + tokens['access_token']
    devices_response = (requests.get(request)).json()
    #print(devices_response)
    
    devices_list = []
    for response in devices_response["data"]:
        #all_group_id.append(response["id"])
        devices_list.append(response["id"])
        #print("{} with devices {}".format(group, response["id"]))

    groups_and_devices_dict[group] = devices_list

print(groups_and_devices_dict)

# Build another dict with devices and list of configs
groups_and_devices_configs_dict = {}
for group in all_group_id: 

    for device in groups_and_devices_dict[group]:
        #print(device)
        request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d/" + str(device) + "/config_backup" +"?access_token=" + tokens['access_token']
        
        devices_response = (requests.get(request)).json()
        #print(devices_response)

        # Grab most recent config date
        config_id_response = devices_response["data"][-1]
        # Grab most recent config time
        #print(config_id_response["file_list"][-1])

        config_id = config_id_response["file_list"][-1]["id"]

        # Filename for save config
        device_name_request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d/" + str(device) + "?access_token=" + tokens['access_token']
        file_name = (requests.get(device_name_request)).json()["data"]["name"] + "-"
        file_name += config_id_response["date"].strip("-") + "_"
        file_name += config_id_response["file_list"][-1]["time"].replace(":","_")


        #print(file_name)

        # Save config
        request = "https://api.ic.peplink.com/rest/o/" + org_id + "/g/" + str(group) + "/d/" + str(device) + "/config_backup/" + str(config_id) + "?access_token=" + tokens['access_token']
        config_download = (requests.get(request))
        #print(config_download.content) # See raw hex recieved

        # TODO Get this path from the env file
        file_path = "/Users/tylerzars/Desktop/Ross/PyIncontrolConfig/Testing/"
        file_path += file_name + ".conf"
        open(file_path, 'wb').write(config_download.content)

        print("Saved config for {} as {}.conf".format(file_name.split("-")[0], file_name))

        

