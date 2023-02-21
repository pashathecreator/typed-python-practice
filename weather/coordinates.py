from typing import NamedTuple
import socket
import geocoder


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    latitude_and_longitude = geocoder.ip(get_my_ip()).latlng
    return Coordinates(latitude=latitude_and_longitude[0], longitude=latitude_and_longitude[1])


ip_address = str


def get_my_ip() -> ip_address:
    host_name = socket.gethostname()
    return socket.gethostbyname(host_name)
