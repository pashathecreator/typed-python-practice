from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    return (f"{weather.region}, температура {weather.temperature}°C. "
            f"Чувствуется как {weather.feels_like_temperature}°C\n"
            f"{weather.weather_condition}\n"
            f"Восход: {weather.sunrise.time()}\n"
            f"Закат: {weather.sunset.time()}")
