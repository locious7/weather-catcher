import os
import requests
from pprint import pprint


class WeatherCatcher:
    def __init__(self):
        # GET api key from environment variable
        self.my_secret = "f038b09d00d3498ab5811212232702" #os.environ['apikey']
        # Get location date from user
        self.location = input("What is your current location? (City, State): ")
        # Get celcius or fahrenheit
        self.c_or_f = input("Celcius of Fahrenheit? (C or F): ")
        # URL to use with api call request
        # This request will retrieve the current real time weather
        self.api_url = f'http://api.weatherapi.com/v1/current.json?key={self.my_secret}&q={self.location}&aqi=no'
        # make a call to the weather api using the reqests module
        self.response = requests.get(self.api_url)

    # Ask user for location
    def get_user_input(self):
        while self.location != self.response.status_code == 200:
            self.location
            return self.response

# GET weather
    def get_weather(self):
        # check if the api call is valid or not and return current temp in Celcius
        if self.response.status_code == 200 and self.c_or_f == "C":
            pprint(self.response.json()["current"]['temp_c'])
            return self.response.json()["current"]['temp_c']
        # check if the api call is valid or not and return current temp in Farhenhiet
        elif self.response.status_code == 200 and self.c_or_f == "F":
            pprint(self.response.json()["current"]['temp_f'])
            print(f'Request failed with status code {self.response.status_code}')
        else:
            print(f'Request failed with status code {self.response.status_code}')


weather = WeatherCatcher()
weather.get_user_input()
weather.get_weather()
