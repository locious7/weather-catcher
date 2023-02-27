import os
import json
import requests

# GET api key from environment variable
my_secret = os.environ['apikey']

# Ask user for location
location = input("What is your current location? (City, State): ")

# URL to use with api call request
# This request will retrieve the current real time weather
api_url = f'http://api.weatherapi.com/v1/current.json?key={my_secret}&q={location}&aqi=no'

# make a call to the weather api using the reqests module
response = requests.get(api_url)

# check if the api call is valid or not
if response.status_code == 200:
    pretty_json = json.dumps(response.json, indent=4, sort_keys=True, ensure_ascii=False)
    print(pretty_json)
else:
    print(f'Request failed with status code {response.status_code}')


