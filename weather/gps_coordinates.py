from dataclasses import dataclass


@dataclass
class Coordinates:
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    return Coordinates(**{"latitude": 10, "longitude": 20})
