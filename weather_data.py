"""
weather_data.py

Parts C1 and C2 of the D493 Weather Data project.

Defines the WeatherData class, which stores a chosen event location and date
(C1) and pulls the most recent five years of historical daily weather for that
date from the Open-Meteo Historical Weather API (C2).

Data source: Open-Meteo Historical Weather API (Zippenfenig, 2023), which is
built on ECMWF ERA5 reanalysis data (Hersbach et al., 2023). Full references
are listed in README.md.
"""

import statistics
from datetime import date

import requests

# Open-Meteo Historical Weather API endpoint (Zippenfenig, 2023).
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Number of past years to collect for each statistic.
YEARS_OF_DATA = 5


class WeatherData:
    """Historical weather statistics for one location on one calendar date."""

    # =====================================================================
    # Part C1: class with instance variables for the location and date
    # =====================================================================
    def __init__(self, latitude, longitude, month, day, year):
        """
        Store the event location and date and set up empty statistics.

        :param latitude: location latitude in decimal degrees
        :param longitude: location longitude in decimal degrees
        :param month: event month (1-12)
        :param day: event day of month (1-31)
        :param year: event year; data is pulled for the five years before it
        """
        # Confirm the month/day/year form a real calendar date
        # (raises ValueError for something like February 30).
        date(year, month, day)

        # Location and date of the event
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year

        # Five-year temperature statistics (degrees Fahrenheit)
        self.avg_temperature = None
        self.min_temperature = None
        self.max_temperature = None

        # Five-year wind speed statistics (miles per hour)
        self.avg_wind_speed = None
        self.min_wind_speed = None
        self.max_wind_speed = None

        # Five-year precipitation statistics (inches)
        self.sum_precipitation = None
        self.min_precipitation = None
        self.max_precipitation = None

    # =====================================================================
    # Part C2: methods that pull daily weather data from the Weather API
    # =====================================================================
    def get_years(self):
        """Return the most recent five years before the event year, oldest first."""
        return list(range(self.year - YEARS_OF_DATA, self.year))

    def _fetch_daily_values(self, variable):
        """
        Request one daily weather variable for the chosen month/day in each
        of the five years and return the values as a list.

        Units are requested from the API directly: Fahrenheit for
        temperature, mph for wind speed and inches for precipitation.

        :param variable: Open-Meteo daily variable name
        :return: list of floats, one per year that returned data
        """
        values = []
        for data_year in self.get_years():
            # The API expects ISO 8601 dates (yyyy-mm-dd); start and end are
            # the same because we want a single day.
            day_string = f"{data_year:04d}-{self.month:02d}-{self.day:02d}"
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "start_date": day_string,
                "end_date": day_string,
                "daily": variable,
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": "auto",  # daily totals use the location's local day
            }
            response = requests.get(ARCHIVE_URL, params=params, timeout=30)
            response.raise_for_status()  # stop on HTTP errors such as 400
            data = response.json()

            # The response holds one value per requested day, so take index 0.
            value = data["daily"][variable][0]
            if value is not None:  # skip a year if the API has no value
                values.append(float(value))

        if not values:
            raise ValueError(f"No data returned from the API for '{variable}'.")
        return values

    def get_mean_temperature(self):
        """
        Pull the daily mean temperature (F) for the date in each of the last
        five years, then set the five-year average, minimum and maximum.
        """
        temps = self._fetch_daily_values("temperature_2m_mean")
        self.avg_temperature = round(statistics.mean(temps), 2)
        self.min_temperature = round(min(temps), 2)
        self.max_temperature = round(max(temps), 2)
        return temps

    def get_max_wind_speed(self):
        """
        Pull the daily maximum wind speed (mph) for the date in each of the
        last five years, then set the five-year average, minimum and maximum.
        """
        speeds = self._fetch_daily_values("wind_speed_10m_max")
        self.avg_wind_speed = round(statistics.mean(speeds), 2)
        self.min_wind_speed = round(min(speeds), 2)
        self.max_wind_speed = round(max(speeds), 2)
        return speeds

    def get_precipitation_sum(self):
        """
        Pull the daily precipitation sum (inches) for the date in each of the
        last five years, then set the five-year total, minimum and maximum.
        """
        precip = self._fetch_daily_values("precipitation_sum")
        self.sum_precipitation = round(sum(precip), 2)
        self.min_precipitation = round(min(precip), 2)
        self.max_precipitation = round(max(precip), 2)
        return precip
