from datetime import datetime
import requests


def get_zmanim_info(date, zip_code):
    date = format_date_string(date)

    url = f"https://db.ou.org/zmanim/getCalendarData.php?mode=day&dateBegin={date}&zipCode={zip_code}"

    try: 
        # fetch data from the zmanim api
        response = requests.get(url)
        response.raise_for_status()

        zmanim_info = response.json()

        # fixing the day of week
        day = int(zmanim_info['dayOfWeek'])
        zmanim_info['dayOfWeek'] = get_day_of_week(day)

        # fixing english date
        english_date = zmanim_info['engDateString']
        zmanim_info['engDateString'] = format_date(english_date)

        return zmanim_info
    except:
        print(f"Error fetching zmanim data")
        return {}


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