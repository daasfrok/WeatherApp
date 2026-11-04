# D493 Weather Data Project

A Python program that collects five years of historical weather for an event
location and date, stores the results in a local SQLite database through the
SQLAlchemy ORM, and queries the stored record to confirm it was saved
correctly. The event planning team uses this data to choose tents, canopies
and other coverings.

## Chosen event

| Setting   | Value                          |
|-----------|--------------------------------|
| Location  | Zilker Park, Austin, Texas     |
| Latitude  | 30.2669                        |
| Longitude | -97.7729                       |
| Date      | April 18, 2027                 |
| Data years| 2022, 2023, 2024, 2025, 2026   |

To use another location or date, change the constants at the top of `main.py`
(`LOCATION_NAME`, `LATITUDE`, `LONGITUDE`, `EVENT_MONTH`, `EVENT_DAY`,
`EVENT_YEAR`). The program always uses the five years before `EVENT_YEAR`.

## Project files

| File              | Purpose                                                        |
|-------------------|----------------------------------------------------------------|
| `weather_data.py` | `WeatherData` class (C1) and the three API methods (C2)        |
| `database.py`     | `WeatherRecord` ORM table and `WeatherDatabase` class (C4–C6)  |
| `main.py`         | Runs the program: creates the object, saves, queries (C3, C5, C6) |
| `test.py`         | Three unit tests (D)                                           |
| `requirements.txt`| Required packages and versions (E)                             |

## Requirements

- Python 3.10 or newer (built and tested on Python 3.13)
- Internet connection (to reach the Open-Meteo API)
- Packages in `requirements.txt`

## Commands

Install the packages (from the project folder):

```
pip install -r requirements.txt
```

Run the program:

```
python main.py
```

Run the unit tests:

```
python -m unittest test -v
```

(`python test.py` also works.)

## Inputs

- The event settings in `main.py` (latitude, longitude, month, day, year).
- Daily weather from the Open-Meteo Historical Weather API
  (`https://archive-api.open-meteo.com/v1/archive`), requested with:
  - `temperature_2m_mean` in Fahrenheit
  - `wind_speed_10m_max` in miles per hour
  - `precipitation_sum` in inches

No API key is needed.

## Outputs

1. **Console – yearly values:** a table of the mean temperature, maximum wind
   speed and precipitation for each of the five years.
2. **Database file – `identifier.sqlite`:** a SQLite file in the project folder with a
   table named `weather_data`. Its columns are: `id` (primary key),
   `latitude`, `longitude`, `month`, `day`, `year`, `avg_temperature`,
   `min_temperature`, `max_temperature`, `avg_wind_speed`, `min_wind_speed`,
   `max_wind_speed`, `sum_precipitation`, `min_precipitation`,
   `max_precipitation`. Running the program again updates the existing row
   instead of adding a duplicate.
3. **Console – formatted report:** the record read back from `identifier.sqlite`,
   showing the five-year average/sum, minimum and maximum for each measure,
   plus the time the report was generated.

Test output: three tests reported as `ok`, followed by `OK`. The tests mock
the API and use an in-memory database, so they do not need internet access and
do not change `identifier.sqlite`.

## How the statistics are calculated

- Temperature: average, minimum and maximum of the five daily mean temperatures.
- Wind speed: average, minimum and maximum of the five daily maximum wind speeds.
- Precipitation: sum, minimum and maximum of the five daily precipitation totals.

Values are rounded to two decimal places.

## References

Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J.,
Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C.,
Dee, D., & Thépaut, J.-N. (2023). *ERA5 hourly data on single levels from 1940 to
present* [Data set]. ECMWF. https://doi.org/10.24381/cds.adbb2d47

Python Software Foundation. (n.d.). *unittest — Unit testing framework*.
https://docs.python.org/3/library/unittest.html

SQLAlchemy. (n.d.). *SQLAlchemy 2.0 documentation: ORM quick start*.
https://docs.sqlalchemy.org/en/20/orm/quickstart.html

Zippenfenig, P. (2023). *Open-Meteo.com Weather API* [Computer software]. Zenodo.
https://doi.org/10.5281/ZENODO.7970649
