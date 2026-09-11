"""Open-Meteo geocoding and forecast client using the standard library."""

from urllib.parse import urlencode
from urllib.request import urlopen
import json
from agriguard.models import WeatherResult

class WeatherService:
    def __init__(self,timeout:float=7): self.timeout=timeout
    def _json(self,url:str)->dict:
        with urlopen(url,timeout=self.timeout) as res:return json.loads(res.read().decode())
    def get(self,location:str)->WeatherResult:
        try:
            geo=self._json('https://geocoding-api.open-meteo.com/v1/search?'+urlencode({'name':location,'count':1,'language':'en','format':'json'}))
            if not geo.get('results'):raise ValueError('Location could not be resolved')
            place=geo['results'][0]; params={'latitude':place['latitude'],'longitude':place['longitude'],'current':'temperature_2m,relative_humidity_2m,wind_speed_10m','hourly':'precipitation_probability','forecast_days':1,'timezone':'auto'}
            fc=self._json('https://api.open-meteo.com/v1/forecast?'+urlencode(params))
            current=fc.get('current',{}); rains=fc.get('hourly',{}).get('precipitation_probability',[])[:12]
            rain=float(max([x for x in rains if x is not None],default=0)); wind=float(current.get('wind_speed_10m',0))
            if rain>=60 or wind>=25: status,reason='unsuitable',f'Rain probability {rain:.0f}% or wind {wind:.0f} km/h is unsafe for immediate spraying.'
            elif rain>=35 or wind>=18: status,reason='caution',f'Rain probability {rain:.0f}% or wind {wind:.0f} km/h requires caution.'
            else: status,reason='suitable',f'Forecast rain probability {rain:.0f}% and wind {wind:.0f} km/h are within prototype limits.'
            return WeatherResult(location=place.get('name',location),temperature_c=current.get('temperature_2m'),rain_probability=rain,wind_speed_kmph=wind,humidity_percent=current.get('relative_humidity_2m'),spray_status=status,reason=reason)
        except Exception as exc:
            return WeatherResult(location=location,spray_status='unavailable',reason=f'Weather lookup unavailable: {type(exc).__name__}')
