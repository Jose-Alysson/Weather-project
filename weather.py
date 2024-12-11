import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
latitude = float(input("Please input the latitude: "))
longitude = float(input("Please input the longitude: "))

params = {
	"latitude": latitude,
    "longitude": longitude,
	"daily": "sunrise,sunset,temperature_2m_max",
}

#print(params)

response = requests.get(url, params=params)

data = response.json()

sunset_times = data['daily']['sunset']
sunrise_times = data['daily']['sunrise']
max_temperature_celsius = data['daily']['temperature_2m_max']

max_temperature_fahrenhait = [(temp * 1.8) + 32 for temp in max_temperature_celsius]

print("The sunset, the sunrise  and the max temperature are:")
for sunrise, sunset, max_temp_f in zip(sunrise_times, sunset_times, max_temperature_fahrenhait):
    print(f"Sunrise: {sunrise}, Sunset: {sunset}, Max Temperature: {max_temp_f:.2f}°F")

# Process first location. Add a for-loop for multiple locations or weather models
response = response[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_temperature_celsius = hourly_data.Variables(0).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)



