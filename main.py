"""
main.py

Entry point for the D493 Weather Data project.

C3: creates a WeatherData object and calls its three API methods.
C5: saves the results to the SQLite table.
C6: queries the table and prints the stored record.

Run with:  python main.py
"""

from weather_data import WeatherData
from database import WeatherDatabase

# -------------------------------------------------------------------------
# Event settings: change these to use a different location or date.
# -------------------------------------------------------------------------
LOCATION_NAME = "Zilker Park, Austin, Texas"
LATITUDE = 30.2669
LONGITUDE = -97.7729
EVENT_MONTH = 4      # April
EVENT_DAY = 18
EVENT_YEAR = 2027    # data is pulled for 2022-2026
DATABASE_URL = "sqlite:///identifier.sqlite"


def main():
    # =====================================================================
    # Part C3: create an instance of the C1 class and call the C2 methods
    # =====================================================================
    weather = WeatherData(LATITUDE, LONGITUDE, EVENT_MONTH, EVENT_DAY, EVENT_YEAR)
    years = weather.get_years()
    print(f"Pulling weather for {LOCATION_NAME} on "
          f"{EVENT_MONTH:02d}/{EVENT_DAY:02d} for {years[0]}-{years[-1]}...\n")

    temps = weather.get_mean_temperature()
    winds = weather.get_max_wind_speed()
    precip = weather.get_precipitation_sum()

    # Show the raw yearly values returned by the API.
    print(f"{'Year':<8}{'Mean Temp (F)':>15}{'Max Wind (mph)':>16}{'Precip (in)':>13}")
    for yr, t, w, p in zip(years, temps, winds, precip):
        print(f"{yr:<8}{t:>15.2f}{w:>16.2f}{p:>13.2f}")
    print()

    # =====================================================================
    # Part C5: populate the SQLite table with the weather data
    # =====================================================================
    db = WeatherDatabase(DATABASE_URL)
    record_id = db.populate(weather)
    print(f"Saved to identifier.sqlite (record id {record_id}).\n")


if __name__ == "__main__":
    main()
