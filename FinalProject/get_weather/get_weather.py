from datetime import datetime, timedelta
from flask import jsonify
import json, os, requests


def get_weather_info(location_key, date):
    within_4_days = check_if_within_4_days(date)
    if(within_4_days is not None):
        aw_api_key = os.getenv("aw_api_key")
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={aw_api_key}"
        wresponse = requests.get(url)
        wresponse.raise_for_status()

        wresponse = json.loads(wresponse.content)
        wresponse = wresponse['DailyForecasts']

        weather_info = get_available_days_weather(wresponse, within_4_days)
        return weather_info
    else:
        return jsonify({})
    

def get_available_days_weather(wresponse, within_4_days):    
    weather_info = {}
    # format the weather info based on what day it is and then return it
    while within_4_days < 5:
        weather_info[within_4_days] = wresponse[within_4_days]
        within_4_days+=1

    return weather_info



def check_if_within_4_days(date):
    """Checks if the given date is within 4 days of today's date.

    Args:
        date_string: A datetime.date string.

    Returns:
        number of days away from today, none if false
    """
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    today = datetime.today().date()
    delta = abs(date_obj - today)
    if(delta<=timedelta(days=4)):
        return delta.days
    else:
        return None