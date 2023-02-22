from datetime import datetime
from typing import NamedTuple
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
import urllib.request
from urllib.error import URLError

from coordinates import Coordinates
import config
from exceptions import ApiServiceError

Celsius = float


class Weather(NamedTuple):
    temperature: Celsius
    feels_like_temperature: Celsius
    weather_condition: str
    region: str
    sunrise: datetime
    sunset: datetime


class JsonType(Enum):
    ASTRONOMY = "astronomy"
    CURRENT = "current"


class DataFromCurrentResponse(NamedTuple):
    temperature: Celsius
    feels_like_temperature: Celsius
    weather_condition: str
    region: str


class DataFromAstronomyResponse(NamedTuple):
    sunrise: datetime
    sunset: datetime


def get_weather(coordinates: Coordinates) -> Weather:
    ssl._create_default_https_context = ssl._create_unverified_context

    current_response = _get_current_weather_api_response(coordinates.latitude, coordinates.longitude)
    astronomy_response = _get_astronomy_weather_api_response(coordinates.latitude, coordinates.longitude)

    data_from_current_response = _parse_current_weather_api_response(current_response)
    data_from_astronomy_response = _parse_astronomy_weather_api_response(astronomy_response)

    return Weather(temperature=data_from_current_response.temperature,
                   feels_like_temperature=data_from_current_response.feels_like_temperature,
                   weather_condition=data_from_current_response.weather_condition,
                   region=data_from_current_response.region,
                   sunrise=data_from_astronomy_response.sunrise,
                   sunset=data_from_astronomy_response.sunset)


def _get_current_weather_api_response(latitude: float, longitude: float) -> str:
    url = config.WEATHER_API_URL.format(json_type=JsonType.CURRENT.value, latitude=str(latitude),
                                        longitude=str(longitude))
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _get_astronomy_weather_api_response(latitude: float, longitude: float) -> str:
    url = config.WEATHER_API_URL.format(json_type=JsonType.ASTRONOMY.value, latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_current_weather_api_response(current_response: str) -> DataFromCurrentResponse:
    try:
        dict_from_current_response = json.loads(current_response)
    except JSONDecodeError:
        raise ApiServiceError

    return DataFromCurrentResponse(temperature=_parse_temperature(dict_from_current_response),
                                   feels_like_temperature=_parse_feel_like_temperature(dict_from_current_response),
                                   weather_condition=_parse_weather_condition(dict_from_current_response),
                                   region=_parse_region(dict_from_current_response)
                                   )


def _parse_temperature(dict_from_current_response):
    return dict_from_current_response["current"]["temp_c"]


def _parse_feel_like_temperature(dict_from_current_response):
    return dict_from_current_response["current"]["feelslike_c"]


def _parse_weather_condition(dict_from_current_response):
    return dict_from_current_response["current"]["condition"]["text"]


def _parse_region(dict_from_current_response):
    return dict_from_current_response["location"]["region"]


def _parse_astronomy_weather_api_response(astronomy_response: str) -> DataFromAstronomyResponse:
    try:
        dict_from_astronomy_response = json.loads(astronomy_response)
    except JSONDecodeError:
        raise ApiServiceError

    return DataFromAstronomyResponse(sunrise=_parse_sunrise(dict_from_astronomy_response),
                                     sunset=_parse_sunset(dict_from_astronomy_response))


def _parse_sunrise(dict_from_astronomy_response):
    return datetime.strptime(dict_from_astronomy_response["astronomy"]["astro"]["sunrise"], "%I:%M %p")


def _parse_sunset(dict_from_astronomy_response):
    return datetime.strptime(dict_from_astronomy_response["astronomy"]["astro"]["sunset"], "%I:%M %p")
