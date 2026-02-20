import requests
from django.conf import settings
from decimal import Decimal


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap FREE API (Perfect for Students!)"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    
    @staticmethod
    def get_weather_data(latitude, longitude):
        """Fetch current weather data using FREE OpenWeatherMap API"""
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == 'PUT_YOUR_API_KEY_HERE':
            # Return realistic demo data for students without API key
            return {
                'temperature': Decimal('23.5'),
                'humidity': Decimal('68.0'),
                'wind_speed': Decimal('4.2'),
                'description': 'Partly cloudy (demo data - add your free API key for real data)',
                'rainfall': Decimal('0')
            }
        
        try:
            # Use FREE Current Weather API (no subscription needed!)
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': Decimal(str(data['main']['temp'])),
                'humidity': Decimal(str(data['main']['humidity'])),
                'wind_speed': Decimal(str(data['wind']['speed'])),
                'description': data['weather'][0]['description'],
                'rainfall': Decimal(str(data.get('rain', {}).get('1h', 0)))
            }
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            # Return demo data if API fails
            return {
                'temperature': Decimal('22.0'),
                'humidity': Decimal('65.0'),
                'wind_speed': Decimal('3.8'),
                'description': f'Weather data unavailable (API error)',
                'rainfall': Decimal('0')
            }
    
    @staticmethod
    def get_weather_by_city(city_name):
        """Fetch weather data by city name using FREE API"""
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == 'PUT_YOUR_API_KEY_HERE':
            # Return demo data with approximate coordinates for Kenya
            return {
                'temperature': Decimal('24.0'),
                'humidity': Decimal('70.0'),
                'wind_speed': Decimal('4.5'),
                'description': f'Partly cloudy in {city_name} (demo data)',
                'rainfall': Decimal('0'),
                'latitude': -1.2921,  # Nairobi coordinates
                'longitude': 36.8219
            }
        
        try:
            # Use FREE Current Weather API
            params = {
                'q': city_name,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': Decimal(str(data['main']['temp'])),
                'humidity': Decimal(str(data['main']['humidity'])),
                'wind_speed': Decimal(str(data['wind']['speed'])),
                'description': data['weather'][0]['description'],
                'rainfall': Decimal(str(data.get('rain', {}).get('1h', 0))),
                'latitude': data['coord']['lat'],
                'longitude': data['coord']['lon']
            }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
        
        try:
            params = {
                'q': city_name,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': Decimal(str(data['main']['temp'])),
                'humidity': Decimal(str(data['main']['humidity'])),
                'wind_speed': Decimal(str(data['wind']['speed'])),
                'description': data['weather'][0]['description'],
                'rainfall': Decimal('0'),
                'latitude': data['coord']['lat'],
                'longitude': data['coord']['lon']
            }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    @staticmethod
    def get_5day_forecast(latitude, longitude):
        """Get 5-day weather forecast using FREE OpenWeatherMap API"""
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == 'PUT_YOUR_API_KEY_HERE':
            return None
        
        try:
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(WeatherService.FORECAST_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process forecast data (returns 40 entries, 3-hour intervals for 5 days)
            forecast_list = []
            for item in data['list'][:40]:  # 5 days * 8 entries per day
                forecast_list.append({
                    'datetime': item['dt_txt'],
                    'temperature': Decimal(str(item['main']['temp'])),
                    'humidity': Decimal(str(item['main']['humidity'])),
                    'description': item['weather'][0]['description'],
                    'rainfall': Decimal(str(item.get('rain', {}).get('3h', 0)))
                })
            
            return forecast_list
            
        except Exception as e:
            print(f"Error fetching forecast data: {e}")
            return None