"""
database.py

Parts C4, C5 and C6 of the D493 Weather Data project.

C4: WeatherRecord maps a table in SQLite using the SQLAlchemy ORM, and
    WeatherDatabase creates that table.
C5: WeatherDatabase.populate() saves a WeatherData object as a row.
C6: WeatherDatabase.query_record() reads the row back and
    WeatherDatabase.display_record() prints it in a formatted report.

ORM usage follows the SQLAlchemy 2.x documentation (SQLAlchemy, n.d.).
"""

from datetime import datetime

from sqlalchemy import Float, Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


# =========================================================================
# Part C4: ORM class that defines the SQLite table
# =========================================================================
class Base(DeclarativeBase):
    """Base class that all ORM table classes inherit from."""


class WeatherRecord(Base):
    """One row of five-year weather statistics for a location and date."""

    __tablename__ = "weather_data"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Location and date
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Five-year temperature statistics (F)
    avg_temperature: Mapped[float] = mapped_column(Float)
    min_temperature: Mapped[float] = mapped_column(Float)
    max_temperature: Mapped[float] = mapped_column(Float)

    # Five-year wind speed statistics (mph)
    avg_wind_speed: Mapped[float] = mapped_column(Float)
    min_wind_speed: Mapped[float] = mapped_column(Float)
    max_wind_speed: Mapped[float] = mapped_column(Float)

    # Five-year precipitation statistics (inches)
    sum_precipitation: Mapped[float] = mapped_column(Float)
    min_precipitation: Mapped[float] = mapped_column(Float)
    max_precipitation: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return (f"<WeatherRecord id={self.id} ({self.latitude}, {self.longitude}) "
                f"{self.month}/{self.day}/{self.year}>")


class WeatherDatabase:
    """Creates the SQLite table and handles saving and reading weather rows."""

    def __init__(self, db_url="sqlite:///identifier.sqlite"):
        """
        Connect to SQLite and create the weather_data table if it does not
        already exist.

        :param db_url: SQLAlchemy database URL; tests pass "sqlite:///:memory:"
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)  # C4: builds the table

    @staticmethod
    def _find(session, latitude, longitude, month, day, year):
        """Return the row matching a location and date, or None."""
        statement = select(WeatherRecord).where(
            WeatherRecord.latitude == latitude,
            WeatherRecord.longitude == longitude,
            WeatherRecord.month == month,
            WeatherRecord.day == day,
            WeatherRecord.year == year,
        )
        return session.scalars(statement).first()

    # =====================================================================
    # Part C5: populate the table with the weather data
    # =====================================================================
    def populate(self, weather):
        """
        Save a WeatherData object to the table. If a row already exists for
        the same location and date it is updated, so running the program
        again does not create duplicates.

        :param weather: a WeatherData object whose methods have been called
        :return: the primary key (id) of the saved row
        """
        with Session(self.engine) as session:
            record = self._find(session, weather.latitude, weather.longitude,
                                weather.month, weather.day, weather.year)
            if record is None:
                record = WeatherRecord()
                session.add(record)

            # Copy each instance variable from the WeatherData object.
            record.latitude = weather.latitude
            record.longitude = weather.longitude
            record.month = weather.month
            record.day = weather.day
            record.year = weather.year
            record.avg_temperature = weather.avg_temperature
            record.min_temperature = weather.min_temperature
            record.max_temperature = weather.max_temperature
            record.avg_wind_speed = weather.avg_wind_speed
            record.min_wind_speed = weather.min_wind_speed
            record.max_wind_speed = weather.max_wind_speed
            record.sum_precipitation = weather.sum_precipitation
            record.min_precipitation = weather.min_precipitation
            record.max_precipitation = weather.max_precipitation

            session.commit()  # write the row to identifier.sqlite
            return record.id
