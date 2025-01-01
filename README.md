# Weather and Zmanim App
This application combines weather data and Jewish prayer times (Zmanim) into an easy-to-use platform. Built with Flask, it allows users to search for weather conditions and detailed Zmanim for any location by entering a zip code or city name.

# Key Features
## 1. Weather Information
Provides current weather conditions, including temperature, humidity, wind speed, and precipitation data.
Displays a 5-day forecast for the selected location, offering insights into upcoming weather patterns.
Weather data is retrieved from the AccuWeather API, ensuring reliable and accurate results.

## 2. Zmanim (Jewish Prayer Times)
Calculates precise Zmanim based on the user's location and date.
Includes major Zmanim such as sunrise, sunset, sof zman krias shema, and sof zman tefillah.
Powered by the Hebcal API to ensure accurate times according to Halachic standards.

## 3. Search by Location and Date
Users can search for a location by entering a zip code or city name.
Select a specific date to view Zmanim and weather data for that day, or default to the current day.

## 4. User-Friendly Interface
A clean and intuitive design allows users to switch between weather and Zmanim data seamlessly.
The information is presented in an easy-to-read format, ensuring a smooth user experience.

## 5. Real-Time Updates
Data is fetched dynamically based on user input, ensuring that the information displayed is up-to-date.

## 6. Integration with Twilio (Optional)
Users can opt to receive notifications for specific Zmanim through SMS. This feature is powered by Twilio, allowing reminders to be sent directly to their phones.
User Accounts: Enable users to save preferred locations and receive customized notifications.
