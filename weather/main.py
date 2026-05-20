import os
from dotenv import load_dotenv
import requests
from pydantic import BaseModel
import json


load_dotenv()  
api_key = os.getenv("API_KEY")

class Location(BaseModel):
    name: str
    country: str

class CurrentWeather(BaseModel):
    temp_c: float
    humidity: int
    wind_kph: float

class WeatherResponse(BaseModel):
    location: Location
    current: CurrentWeather



def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve weather data. Status code:", response.status_code)
        return None
    

def validate_data(data):
    validated = WeatherResponse(**data)
    return validated


def save_report(validated_data):
    cleaned_data = validated_data.model_dump()

    with open("weather_report.json", "w") as f:
        json.dump(cleaned_data, f, indent=4)

    print("Weather report saved to weather_report.json")

def main():
    print("Welcome to the Weather App!")
    city = input("Enter the city name: ")

    print("Fetching weather data...")
    data = get_weather(city)
    validate_data(data)
    save_report(validate_data(data))

if __name__ == "__main__":
    main()
