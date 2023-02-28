import os
import requests
from pprint import pprint

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
    pprint(response.json()["current"]['temp_f'])
else:
    print(f'Request failed with status code {response.status_code}')
