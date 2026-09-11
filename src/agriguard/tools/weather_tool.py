"""Open-Meteo weather lookup and spray-suitability output."""
from agriguard.services import WeatherService

def get_weather(location:str,service:WeatherService|None=None)->dict:
    if not location.strip():raise ValueError('location is required')
    return (service or WeatherService()).get(location).model_dump()
