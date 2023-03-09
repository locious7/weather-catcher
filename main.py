import os
import requests
from pprint import pprint

class WeatherCatcher:
  def __init__(self,my_secret,location,api_url,response)

    # GET api key from environment variable
    self.my_secret = os.environ['apikey']
    # make a call to the weather api using the reqests module
    self.response = requests.get(api_url)
    
  # Ask user for location
  def get_user_input:
    # Get location date from user
    self.location = input("What is your current location? (City, State): ")
    while self.location != response.status_code == 200:
      self.location
    return self.response
		# Get celcius or fahrenheit 
		self.c_or_f = input("Celcius of Fahrenheit? (C or F): ")
  
# GET weather
  def get_weather:
    # URL to use with api call request
    # This request will retrieve the current real time weather
    self.api_url = f'http://api.weatherapi.com/v1/current.json?key={self.my_secret}&q={self.location}&aqi=no'
    # check if the api call is valid or not and return current temp in Celcius
    if self.response.status_code == 200 and self.c_or_f == "C":
        pprint(response.json()["current"]['temp_c'])
				return response.json()["current"]['temp_c']
    else:
        print(f'Request failed with status code {response.status_code}')
	
		# check if the api call is valid or not and return current temp in Farhenhiet
    if self.response.status_code == 200 and self.c_or_f == "F":
        pprint(response.json()["current"]['temp_f'])
				return response.json()["current"]['temp_f']
    else:
        print(f'Request failed with status code {response.status_code}')
		

weather = WeatherCatcher()