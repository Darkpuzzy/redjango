import requests
from pyowm.owm import OWM

API_KEY = 'aa35ea981da617f12c2326bd3707540b'


class WeatherApi:

    owm = OWM(API_KEY)
    mgr = owm.weather_manager()

    @classmethod
    def weather_today(cls, city):
        try:
            weather_today = cls.mgr.weather_at_place(city)
            weather = weather_today.weather
            response = {
                'date': weather.reference_time('iso'),
                'temperature': weather.temperature('celsius')['temp'],
                'conditions': weather.detailed_status,
                'wind': str(weather.wind()['speed']) + ' m/s'
            }
            return response
        except Exception as e:
            return {'Error': e}

    @classmethod
    def weather_at_five_day(cls, city):
        try:
            list_response = []
            forecast = cls.mgr.forecast_at_place(city, '3h').forecast
            weather = forecast.weathers
            for item in weather:
                response = {
                    'date': item.reference_time('iso'),
                    'temp': item.temperature('celsius')['temp'],
                    'wind': str(item.wind()['speed']) + ' m/s',
                    'conditions': item.detailed_status
                  }
                list_response.append(response)
            return list_response
        except Exception as e:
            return {'Error': e}

    @classmethod
    def weather_at_date(cls, city, date):
        try:
            forecast = cls.mgr.forecast_at_place(city, '3h').get_weather_at(date)
            response = {
                'temperature': forecast.temperature('celsius')['temp'],
                'conditions': forecast.detailed_status,
                'wind': str(forecast.wind()['speed']) + ' m/s'
            }
            return response
        except Exception as e:
            return {'Error': f"{e}"}

