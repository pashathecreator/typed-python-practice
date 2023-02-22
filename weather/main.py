from pathlib import Path
from weather_api_service import get_weather
from coordinates import get_coordinates
from weather_formatter import format_weather
from exceptions import ApiServiceError
from history.history import save_weather, PlainFileWeatherStorage, JSONFileWeatherStorage


def main():
    coordinates = get_coordinates()

    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(
            f"Не удалость получить погоду по координатам {coordinates.latitude}, {coordinates.longitude}"
        )
        exit(1)

    print(format_weather(weather))

    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / "history.json")
    )


if __name__ == '__main__':
    main()
