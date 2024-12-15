from datetime import datetime, timedelta
import os, requests

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
        return weather_info
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}
    

def get_available_days_weather(raw_weather_info, within_4_days):   
    """
    this method formats the weather info given based on what day it is and returns it

    Args:
        raw_weather_info: json data of all given weather
        within_4_days: int representing number of days between given date and 4 days from current date
    Returns:
        weather_info, the weather just for days relevant to 4 days from current date
    """ 
    weather_info = {}
    # format the weather info based on what day it is and then return it
    while within_4_days < 5:
        weather_info[within_4_days] = raw_weather_info[within_4_days]
        within_4_days+=1

    return weather_info



def check_if_within_4_days(date):
    """Checks if the given date is within 4 days of today's date and not in the past.

    Args:
        date: A datetime.date string in 'YYYY-MM-DD' format.
    Returns:
        The number of days away from today if the date is within the next 4 days; None otherwise.
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    today = datetime.today().date()
    
    if date_obj < today:
        return None
    
    delta = abs(date_obj - today)
    return delta.days if delta <= timedelta(days=4) else None
