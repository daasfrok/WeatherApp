"""
test.py

Part D: three unit tests for the D493 Weather Data project.

The API is replaced with a mock (unittest.mock) so the tests are fast,
repeatable and do not depend on an internet connection. The database test
uses an in-memory SQLite database so identifier.sqlite is never touched.

Run with:  python -m unittest test -v
"""

import unittest
from unittest.mock import MagicMock, patch

from weather_data import WeatherData
from database import WeatherDatabase

LAT, LON, MONTH, DAY, YEAR = 30.2669, -97.7729, 4, 18, 2027


def fake_response(variable, value):
    """Build a fake requests.Response that looks like an Open-Meteo reply."""
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"daily": {"time": ["x"], variable: [value]}}
    return response


class TestWeatherProject(unittest.TestCase):

    def test_1_instance_variables(self):
        """The class stores the location/date and covers the last five years."""
        weather = WeatherData(LAT, LON, MONTH, DAY, YEAR)
        self.assertEqual(weather.latitude, LAT)
        self.assertEqual(weather.longitude, LON)
        self.assertEqual((weather.month, weather.day, weather.year), (MONTH, DAY, YEAR))
        self.assertEqual(weather.get_years(), [2022, 2023, 2024, 2025, 2026])
        self.assertIsNone(weather.avg_temperature)  # not set until the API is called

    @patch("weather_data.requests.get")
    def test_2_mean_temperature_statistics(self, mock_get):
        """get_mean_temperature() asks for Fahrenheit and computes avg/min/max."""
        temps = [70.0, 72.0, 68.0, 75.0, 65.0]
        mock_get.side_effect = [fake_response("temperature_2m_mean", t) for t in temps]

        weather = WeatherData(LAT, LON, MONTH, DAY, YEAR)
        weather.get_mean_temperature()

        self.assertEqual(mock_get.call_count, 5)  # one request per year
        self.assertEqual(mock_get.call_args.kwargs["params"]["temperature_unit"], "fahrenheit")
        self.assertEqual(weather.avg_temperature, 70.0)
        self.assertEqual(weather.min_temperature, 65.0)
        self.assertEqual(weather.max_temperature, 75.0)

    def test_3_database_populate_and_query(self):
        """A record saved to SQLite can be queried back with the same values."""
        weather = WeatherData(LAT, LON, MONTH, DAY, YEAR)
        weather.avg_temperature, weather.min_temperature, weather.max_temperature = 70.0, 65.0, 75.0
        weather.avg_wind_speed, weather.min_wind_speed, weather.max_wind_speed = 12.5, 8.0, 18.0
        weather.sum_precipitation, weather.min_precipitation, weather.max_precipitation = 1.2, 0.0, 0.8

        db = WeatherDatabase("sqlite:///:memory:")
        record_id = db.populate(weather)
        db.populate(weather)  # saving again should update, not duplicate
        record = db.query_record(LAT, LON, MONTH, DAY, YEAR)

        self.assertIsNotNone(record)
        self.assertEqual(record.id, record_id)
        self.assertEqual(record.avg_temperature, 70.0)
        self.assertEqual(record.max_wind_speed, 18.0)
        self.assertEqual(record.sum_precipitation, 1.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
