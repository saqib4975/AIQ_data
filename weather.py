import pandas as pd
import requests
from urllib.parse import urlencode


def fetch_weather_data(city, api_key):
    """Fetches weather data from the OpenWeatherMap API for a given city,
    exposing more columns and handling nested data."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"  # Use metric units

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None


def citywise(cities):
    api_key = "c961850a61dc345e93bd9415d74b7688"
    weather_data_list = []

    for city in cities:
        weather_data = fetch_weather_data(city, api_key)
        if weather_data:
            weather_info = {
                "City": weather_data["name"],
                "Weather Condition": weather_data["weather"][0]["main"],
                "Temperature (°C)": weather_data["main"]["temp"],
                "Feels Like (°C)": weather_data["main"]["feels_like"],
                "Minimum Temperature (°C)": weather_data["main"]["temp_min"],
                "Maximum Temperature (°C)": weather_data["main"]["temp_max"],
                "Humidity (%)": weather_data["main"]["humidity"],
                "Wind Speed (m/s)": weather_data["wind"]["speed"],
                "Sunrise (Unix Timestamp)": weather_data["sys"]["sunrise"],
                "Sunset (Unix Timestamp)": weather_data["sys"]["sunset"],
            }
            weather_data_list.append(weather_info)
        else:
            print(f"Failed to retrieve weather data for {city}.")

    if weather_data_list:
        weather_df = pd.DataFrame(weather_data_list)
        print("Weather Data:")
        print(weather_df)
    else:
        print("No weather data available.")


if __name__ == "__main__":
    cities = ["Abu Dhabi", "Dubai","London","Paris","New York","Tokyo","Vilnius"]  # List of cities
    citywise(cities)


