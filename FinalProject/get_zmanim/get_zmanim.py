from datetime import datetime
import requests


def get_zmanim_info(date, zip_code):

    date = format_date_string(date)

    url = f"https://db.ou.org/zmanim/getCalendarData.php?mode=day&dateBegin={date}&zipCode={zip_code}"
        
    # fetch data from the zmanim api
    zresponse = requests.get(url)
    zresponse.raise_for_status()

    #convert to json
    zresponse = zresponse.json()

    # fixing the day of week
    day = int(zresponse['dayOfWeek'])
    zresponse['dayOfWeek'] = get_day_of_week(day)

    # fixing english date
    e_date = zresponse['engDateString']
    zresponse['engDateString'] = format_date(e_date)

    return zresponse


def get_day_of_week(day_num): 
    """
        this method takes an integer representing a day of the week and returns
        the corresponding day.
        Day 1 is Monday and so on.
        Args:
            day_num: integer representing day of week (from zmanim api results)
        Returns:
            string for the day of the week
    """
    if day_num == 1:
        return 'Monday'
    elif day_num == 2:
        return 'Tuesday'
    elif day_num ==3:
        return 'Wednesday'
    elif day_num == 4:
        return 'Thursday'
    elif day_num == 5:
        return 'Friday'
    elif day_num == 6:
        return 'Shabbos'
    elif day_num == 7:
        return 'Sunday'
    
def format_date(date):
    """
    Formats a date string in the format 'MM/DD/YYYY' to 'DD Month YYYY'.

    Args:
        date: The date string to format.

    Returns:
        The formatted date string.
    """

    date_obj = datetime.strptime(date, '%m/%d/%Y')
    formatted_date = date_obj.strftime('%d %B %Y')
    return formatted_date


def format_date_string(date_string):
    """
    this method converts a python date string to a more readable format (which will be used for zmanim api)
    Args:
        date_string: date in format yyyy-mm-dd
    Returns:
        the date formated as mm/dd/yyyy
    """
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    formatted_date = date_object.strftime("%m/%d/%Y")
    return formatted_date