from datetime import datetime, timedelta


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
