import os
import requests
import json

class WeatherSnatcher:
    def __init__(self):
        # GET api key from environment variable
        self.my_secret = os.environ["apikey"]
        # Set initial values
        self.location = None
        self.cels_or_fahr = None
        self.response = None
        self.weather = None
        self.f_days = None

    # Ask user for location
    def user_input(self):
        while True:
            # Get location data from user
            self.location = input("What is your current location? (City, State OR Zip Code): ")
            # Get Celsius or fahrenheit
            self.cels_or_fahr = input("Celsius of Fahrenheit? (C or F): ")
            # Get current weather, forecasted weather or both	
            self.weather = input("Would you like the Current weather, Forecasted weather or Both? (C, F, or B): ")
            # Get forecasted days
            if self.weather in ("F", "B"):
                self.f_days = int(input("How many days of forecasted weather would you like? (1-3): "))
                self.forecasted_api_url = f"https://api.weatherapi.com/v1/forecast.json?key={self.my_secret}&q={self.location}&days={self.f_days}&aqi=no&alerts=no"
                # Make request to API for forecasted weather
                self.response = requests.get(self.forecasted_api_url)
                # format json data
                self.json_data = json.loads(self.response.text)
            else:
                # Make request to API for current weather
                self.current_api_url = f"http://api.weatherapi.com/v1/current.json?key={self.my_secret}&q={self.location}&aqi=no"
                # Make request to API for forecasted weather
                self.response = requests.get(self.current_api_url)
            # Check if location is valid
            if self.response.status_code == 200:
                break
            else:
                print("Invalid location. Please try again.")
                
    # GET weather
    def get_weather(self):
        # check if the api call is valid and return current weather in Celsius
        if self.response.status_code == 200 and self.cels_or_fahr == "C" and self.weather == "C":
            print("The current temperature outside is: " + str(self.response["current"]["temp_c"]))
        # check if the api call is valid and return current weather in Farhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr == "F" and self.weather == "C":
            print("The current temperature outside is: " + str(self.response["current"]["temp_f"]))
        # check if the api call is valid and return forecasted weather in Celsius
        elif self.response.status_code == 200 and self.cels_or_fahr == "C" and self.weather == "F":
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_c = forecastday["day"]["avgtemp_c"]
                self.condition = forecastday["day"]["condition"]["text"]
                print(f"Here is your forecasted weather for the next {self.f_days} days:\n {self.date}: Avg.Temp - {self.avgtemp_c} Celsius - Condition: {self.condition}")
        else:
            print(f"Request failed with status code {self.response.status_code}")

def main():
    weather = WeatherSnatcher()
    weather.user_input()
    weather.get_weather()
    del weather

if __name__ == "__main__":
    main()