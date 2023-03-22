import os
import requests
import json

class WeatherSnatcher:
    def __init__(self):
        # get api key from environment variable
        self.my_secret = os.environ["apikey"]
        # set initial values
        self.location = None
        self.valid_location = None
        self.cels_or_fahr = None
        self.response = None
        self.weather = None
        self.f_days = None
        self.json_data = None

    # ask user for location
    def get_weather(self):
        while True:
            # get current weather, forecasted weather or both from user 
            while True:
                self.weather = input("b (C, F, or B): ")
                # convert user input to uppercase
                self.weather_upper = self.weather.upper()
                # check if valid input
                if self.weather_upper in ("C", "F", "B"):
                    break 
                else:
                    print("Invalid input. Please enter either C, F, or B.")
                    continue
            # check if the user asked for forecasted weather and if so prompt for days
            while True:
                if self.weather_upper in ("F", "B"):            
                    self.f_days = int(input("How many days of forecasted weather would you like? (1-3): "))
                    # check if valid input
                    if 1 <= self.f_days <= 3:
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 3")
                        continue
            # check if the user wants celsius or fahrenheit
            while True:
                self.cels_or_fahr = input("Celsius of Fahrenheit? (C or F): ")
                # convert user input to uppercase
                self.cels_or_fahr_upper = self.cels_or_fahr.upper()
                if self.cels_or_fahr_upper in ("C", "F"):
                    break
                else:
                    print("Invalid input. Please enter either a C of F.")
                    continue
            # get location from user
            while True:
                # check if location is valid
                self.location = input("What is your current location? (City, State OR Zip Code): ")
                self.valid_location = f"https://api.weatherapi.com/v1/forecast.json?key={self.my_secret}&q={self.location}"
                 # make request to API for forecasted weather
                self.response = requests.get(self.valid_location)
                if self.response.status_code != 200:
                    print("Invalid location. Please try again.")
                    continue
                else:
                    break
            # get forecasted weather from API
            if self.response.status_code == 200:
                if self.weather_upper in ("F", "B"):
                    self.forecasted_api_url = f"https://api.weatherapi.com/v1/forecast.json?key={self.my_secret}&q={self.location}&days={self.f_days}&aqi=no&alerts=no"
                    # Make request to API for forecasted weather
                    self.response = requests.get(self.forecasted_api_url)
                    # format json data
                    self.json_data = json.loads(self.response.text)
                    break
                else:
                    # Make request to API for current weather
                    self.current_api_url = f"http://api.weatherapi.com/v1/current.json?key={self.my_secret}&q={self.location}&aqi=no"
                    # Make request to API for forecasted weather
                    self.response = requests.get(self.current_api_url)
                    # format json data
                    self.json_data = json.loads(self.response.text)
                    break
            else:
                print(f"Request failed with status code {self.response.status_code}")
                exit
    
    # display weather
    def display_weather(self):
        # check if the api call is valid and return current weather in Celsius
        if self.response.status_code == 200 and self.cels_or_fahr_upper == "C" and self.weather_upper == "C":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_c"]))
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]))
        # check if the api call is valid and return current weather in Farhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "F" and self.weather_upper == "C":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_f"]))
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]))
        # check if the api call is valid and return forecasted weather in Celsius
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "C" and self.weather_upper == "F":
            print(f"Here is your forecasted weather for the next {self.f_days} days:")
            # Iterate over the JSON payload from API call and return each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_c = forecastday["day"]["avgtemp_c"]
                self.condition = forecastday["day"]["condition"]["text"]
                print(f"{self.date}:\n \t-Avg.Temp: {self.avgtemp_c} Celsius\n \t-Condition: {self.condition}")
        # check if the api call is valid and return forecasted weather in Fahrhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "F" and self.weather_upper == "F":
            print(f"Here is your forecasted weather for the next {self.f_days} days:")
            # Iterate over the JSON payload from API call and return each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_f = forecastday["day"]["avgtemp_f"]
                self.condition = forecastday["day"]["condition"]["text"]
                print(f"{self.date}:\n \t-Avg.Temp: {self.avgtemp_f} Fahrenhiet\n \t-Condition: {self.condition}")
        # check if the api call is valid and return current and forecasted weather in Fahrhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "F" and self.weather_upper == "B":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_f"]))
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]))
            print(f"Here is your forecasted weather for the next {self.f_days} days:")
            # Iterate over the JSON payload from API call and return each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_f = forecastday["day"]["avgtemp_f"]
                self.condition = forecastday["day"]["condition"]["text"]
                print(f"{self.date}:\n \t-Avg.Temp: {self.avgtemp_f} Fahrenhiet\n \t-Condition: {self.condition}")
        # check if the api call is valid and return current and forecasted weather in Celsius
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "C" and self.weather_upper == "B":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_c"]))
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]))
            print(f"Here is your forecasted weather for the next {self.f_days} days:")
            # Iterate over the JSON payload from API call and return each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_c = forecastday["day"]["avgtemp_c"]
                self.condition = forecastday["day"]["condition"]["text"]
                print(f"{self.date}:\n \t-Avg.Temp: {self.avgtemp_c} Celsius\n \t-Condition: {self.condition}")            
        # if the request failed print out api response
        else:
            print(f"Request failed with status code {self.response.status_code}")

# main function
def main():
    weather = WeatherSnatcher()
    weather.get_weather()
    weather.display_weather()
    del weather

if __name__ == "__main__":
    main()