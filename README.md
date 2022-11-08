# InControl2ConfigDownloader

This is a Python3 script that willd download the most recent configurations for every device in a Peplink InControl2 organization. It will not check if a configuration has already been saved, but it will just download the most current config again. 

Using a .env file, please add `incontrol_client_id` and `incontrol_client_secret` from making a client at [https://incontrol2.peplink.com/r/user/edit](https://incontrol2.peplink.com/r/user). 

TODO: 
- Not hardcode the save path
- Dynamic orginization/group/device selection
- Add token refresh instead of just getting a new token
- Error checking for each request by using response codes