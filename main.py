import os
import requests
from pprint import pprint


class WeatherSnatcher:
    def __init__(self):
        # GET api key from environment variable
        self.my_secret = os.environ['apikey']
        # Set initial values
        self.location = None
        self.c_or_f = None
        self.response = None
        self.weather = None
        self.f_days = None

    # Ask user for location
    def user_input(self):
        while True:
            # Get location data from user
            self.location = input("What is your current location? (City, State OR Zip Code): ")
            # Get celcius or fahrenheit
            self.c_or_f = input("Celcius of Fahrenheit? (C or F): ")
            # Get current weather, forecasted weather or both	
            self.weather = input("Would you like the Current weather, Forecasted weather or Both? (C, F, or B): ")
            # Get forecasted days
            if self.weather in ("F", "B"):
                self.f_days = int(input("How many days of forecasted weather would you like? (1-10): "))
                self.forecasted_api_url = f'https://api.weatherapi.com/v1/forecast.json?key={self.my_secret}&q={self.location}&days={self.f_days}&aqi=no&alerts=no'
                # Make request to API for forecasted weather
                self.response = requests.get(self.forecasted_api_url)
            else:
                # Make request to API for current weather
                self.current_api_url = f'http://api.weatherapi.com/v1/current.json?key={self.my_secret}&q={self.location}&aqi=no'
                # Make request to API for forecasted weather
                self.response = requests.get(self.current_api_url)
            # Check if location is valid
            if self.response.status_code == 200:
                break
            else:
                print("Invalid location. Please try again.")
                
    # GET weather
    def get_weather(self):
        # check if the api call is valid or not and return current weather temperature in Celcius
        if self.response.status_code == 200 and self.c_or_f == "C":
            print('The current temperature outside is: ' + self.response.json()["current"]['temp_c'])
        # check if the api call is valid or not and return current weather temperature in Farhenhiet
        elif self.response.status_code == 200 and self.c_or_f == "F":
            pprint('The current temperature outside is: ' + self.response.json()["current"]['temp_f'])
        else:
            print(f'Request failed with status code {self.response.status_code}')

def main():
    weather = WeatherSnatcher()
    weather.user_input()
    weather.get_weather()
    del weather

if __name__ == "__main__":
    main()