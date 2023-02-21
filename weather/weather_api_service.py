from datetime import datetime
from typing import NamedTuple

from coordinates import Coordinates

Celsius = int


class Weather(NamedTuple):
    temperature: Celsius
    feels_like_temperature: Celsius
    weather_condition: str
    sunrise: datetime
    sunset: datetime
    region: str


def get_weather(coordinates: Coordinates) -> Weather:
    return Weather(
        temperature=20,
        feels_like_temperature=22,
        weather_condition="Moderate snow",
        sunrise=datetime.strptime("08:34", "%H:%M"),
        sunset=datetime.strptime("08:34", "%H:%M"),
        region="Tomsk"
    )
