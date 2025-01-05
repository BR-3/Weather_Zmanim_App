from flask import g
import os, requests
from get_api_response.get_weather.weather_helper_methods import check_if_within_4_days, format_weather_response, get_available_days_weather

def check_if_get_weather(location_key, date):
    """ Checks if should get weather based on user's preferences if the user is signed in,
    if not signed in will call the get_weather_info method
    Args:
        location_key (str): accuweather location key
        date (str): date in 'yyyy-mm-dd' format"""
    if not g.preferences or g.preferences['show_weather'] == True:
       return get_weather_info(location_key, date)
    else:
        return {}


def get_weather_info(location_key, date):
    """
    Fetches weather information for a given location key and date.

    Args:
        location_key (str): AccuWeather location key.
        date (str): Date in 'YYYY-MM-DD' format.

    Returns:
        json: Weather information for the relevant days, or an empty json if unavailable.
    """
    within_4_days = check_if_within_4_days(date)

    if within_4_days is None:
        return {}
    
    aw_api_key = os.getenv("aw_api_key")
    if not aw_api_key:
        raise EnvironmentError("API key not found in environment variables")

    url = f"https://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={aw_api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw_weather_info = response.json()

        if 'DailyForecasts' not in raw_weather_info:
            print("Unexpected API response structure")
            return {}

        weather_info = get_available_days_weather(raw_weather_info['DailyForecasts'], within_4_days)
        weather_info = format_weather_response(weather_info)
        return weather_info
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}
    

