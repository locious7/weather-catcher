# This program will get current weather conditions from the users
# desired location via their input and print the results to the screen.

import os
import requests
import json
import datetime

# define main class 
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

    # ask user for desired weather
    def get_weather_input(self):
        while True:
            # get current weather, forecasted weather or both from user 
            while True:
                self.weather = input("Would you like the Current weather, Forecasted weather or Both? (C, F, or B): ")
                # convert user input to uppercase
                self.weather_upper = self.weather.upper()
                # check if user input is a C, F or B. If so break out of while loop, if not ask user to try again
                if self.weather_upper in ("C", "F", "B"):
                    break 
                else:
                    print("Invalid input. Please enter either C, F, or B.")
                    continue
            # check if the user asked for forecasted or both weather and if so prompt for forecasted days
            while True:
                # is user input forecasted or both? if so ask how many days they want
                if self.weather_upper in ("F", "B"): 
                    try:
                        self.f_days = int(input("How many days of forecasted weather would you like? (1-3): "))
                        # check if user input is between 1-3. If so break out of while loop, if not ask user to try again
                        if 1 <= self.f_days <= 3:
                            break
                        else:
                            print("Invalid input. Please enter a number between 1 and 3")
                            continue
                    # if user entered a string send error and have them try again
                    except ValueError:
                        print("Invalid input. Please enter a number between 1 and 3")
                else:
                    break
            # check if the user wants celsius or fahrenheit
            while True:
                self.cels_or_fahr = input("Celsius of Fahrenheit? (C or F): ")
                # convert user input to uppercase
                self.cels_or_fahr_upper = self.cels_or_fahr.upper()
                # if user input is a C or F, break out of while loop, if not ask user to try again
                if self.cels_or_fahr_upper in ("C", "F"):
                    break
                else:
                    print("Invalid input. Please enter either a C of F.")
                    continue
            # get desired location from user
            while True:
                self.location = input("What is your current location? (Region, City and State or Zip Code): ")
                self.valid_location = f"https://api.weatherapi.com/v1/forecast.json?key={self.my_secret}&q={self.location}"
                 # make request to API for forecasted weather to confirm if location is valid
                self.response = requests.get(self.valid_location)
                 # check if location is not valid, if not valid ask user to try again, if valid break out of while loop 
                if self.response.status_code != 200:
                    print("Invalid location. Please try again.")
                    continue
                else:
                    break
            # get forecasted weather from API
            # if API response is successful get weather data
            if self.response.status_code == 200:
                # if user asked for forecasted weather or both make API request
                if self.weather_upper in ("F", "B"):
                    # Make request to API for forecasted weather
                    self.forecasted_api_url = f"https://api.weatherapi.com/v1/forecast.json?key={self.my_secret}&q={self.location}&days={self.f_days}&aqi=no&alerts=no"
                    # set variable for API response data
                    self.response = requests.get(self.forecasted_api_url)
                    # format json data from API response
                    self.json_data = json.loads(self.response.text)
                    break
                # if user asked for current weather make API request
                else:
                    # Make request to API for current weather
                    self.current_api_url = f"http://api.weatherapi.com/v1/current.json?key={self.my_secret}&q={self.location}&aqi=no"
                    # set variable for API response data
                    self.response = requests.get(self.current_api_url)
                    # format json data from API response
                    self.json_data = json.loads(self.response.text)
                    break
            # if API response unsuccessful print failed request with API response code and exit 
            else:
                print(f"Request failed with status code {self.response.status_code}")
                exit
    # display weather
    
    def display_weather(self):
        # print new line for better readability upon weather output
        print("\n")
        # check if the api call is successful and print current weather in Celsius
        if self.response.status_code == 200 and self.cels_or_fahr_upper == "C" and self.weather_upper == "C":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_c"]) + "º celsius")
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]))
        # check if the api call is successful and print current weather in Farhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "F" and self.weather_upper == "C":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_f"]) + "º fahrenhiet")
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]))
        # check if the api call is successful and print forecasted weather in Celsius
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "C" and self.weather_upper == "F":
            print(f"Here is your forecasted weather for the next {self.f_days} days:\n")
            # Iterate over the JSON payload from API call and return each days forecasted weather
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_c = forecastday["day"]["avgtemp_c"]
                self.condition = forecastday["day"]["condition"]["text"]
                # Convert the date string to a datetime object
                self.date_object = datetime.datetime.strptime(self.date, "%Y-%m-%d")
                # Format the datetime object as Month day, year
                self.formatted_date = self.date_object.strftime("%B %d, %Y")
                print(f"{self.formatted_date}:\n \t-Avg.Temp: {self.avgtemp_c}º Celsius\n \t-Condition: {self.condition}")
        # check if the api call is successful and print forecasted weather in Fahrhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "F" and self.weather_upper == "F":
            print(f"Here is your forecasted weather for the next {self.f_days} days:\n")
            # Iterate over the JSON payload from API call and return each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_f = forecastday["day"]["avgtemp_f"]
                self.condition = forecastday["day"]["condition"]["text"]
                # Convert the date string to a datetime object
                self.date_object = datetime.datetime.strptime(self.date, "%Y-%m-%d")
                # Format the datetime object as Month day, year
                self.formatted_date = self.date_object.strftime("%B %d, %Y")
                print(f"{self.formatted_date}:\n \t-Avg.Temp: {self.avgtemp_f}º Fahrenhiet\n \t-Condition: {self.condition}")
        # check if the api call is successful and print current and forecasted weather in Celsius
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "C" and self.weather_upper == "B":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_c"]))
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]) + "\n")
            print(f"Here is your forecasted weather for the next {self.f_days} days:")
            # Iterate over the JSON payload from API call and print each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_c = forecastday["day"]["avgtemp_c"]
                self.condition = forecastday["day"]["condition"]["text"]
                # Convert the date string to a datetime object
                self.date_object = datetime.datetime.strptime(self.date, "%Y-%m-%d")
                # Format the datetime object as Month day, year
                self.formatted_date = self.date_object.strftime("%B %d, %Y")
                print(f"{self.formatted_date}:\n \t-Avg.Temp: {self.avgtemp_c}º Celsius\n \t-Condition: {self.condition}")            
        # check if the api call is successful and print current and forecasted weather in Fahrhenhiet
        elif self.response.status_code == 200 and self.cels_or_fahr_upper == "F" and self.weather_upper == "B":
            print("The current temperature outside is: " + str(self.json_data["current"]["temp_f"]))
            print("The current condition outside is: " + str(self.json_data["current"]["condition"]["text"]) + "\n")
            print(f"Here is your forecasted weather for the next {self.f_days} days:")
            # Iterate over the JSON payload from API call and print each days forecasted weather 
            for forecastday in self.json_data["forecast"]["forecastday"]:
                self.date = forecastday["date"]
                self.avgtemp_f = forecastday["day"]["avgtemp_f"]
                self.condition = forecastday["day"]["condition"]["text"]
                # Convert the date string to a datetime object
                self.date_object = datetime.datetime.strptime(self.date, "%Y-%m-%d")
                # Format the datetime object as Month day, year
                self.formatted_date = self.date_object.strftime("%B %d, %Y")
                print(f"{self.formatted_date}:\n \t-Avg.Temp: {self.avgtemp_f}º Fahrenhiet\n \t-Condition: {self.condition}")
        # if API response unsuccessful print failed request with API response code and exit
        else:
            print(f"Request failed with status code {self.response.status_code}")

# main function
def main():
    weather = WeatherSnatcher()
    weather.get_weather_input()
    weather.display_weather()
    del weather

# call main function
if __name__ == "__main__":
    main()