from typing import NamedTuple
import geocoder
import requests


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    latitude_and_longitude = geocoder.ip(_get_my_ip()).latlng
    return Coordinates(latitude=latitude_and_longitude[0], longitude=latitude_and_longitude[1])


ip_address = str


def _get_my_ip() -> ip_address:
    return requests.get("http://wtfismyip.com/text").text

