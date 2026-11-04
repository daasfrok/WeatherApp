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
