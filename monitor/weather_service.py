import requests
from django.conf import settings
from decimal import Decimal


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap FREE API (Perfect for Students!)"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    ONE_CALL_URL = "https://api.openweathermap.org/data/2.5/onecall"  # FREE One Call API 2.5
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
    
    @staticmethod
    def get_weather_data(latitude, longitude):
        """Fetch current weather data using FREE One Call API 2.5"""
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == 'PUT_YOUR_FREE_API_KEY_HERE':
            # Return realistic demo data for students without API key
            return {
                'temperature': Decimal('23.5'),
                'humidity': Decimal('68.0'),
                'wind_speed': Decimal('4.2'),
                'description': 'Partly cloudy (demo data)',
                'rainfall': Decimal('0'),
                'pressure': Decimal('1013'),
                'feels_like': Decimal('24.0'),
                'uv_index': Decimal('5.0')
            }
        
        try:
            # Use FREE One Call API 2.5 (includes current, hourly, daily forecasts!)
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric',
                'exclude': 'minutely,hourly,daily,alerts'  # Only get current weather for now
            }
            
            response = requests.get(WeatherService.ONE_CALL_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current']
                
                return {
                    'temperature': Decimal(str(current['temp'])),
                    'humidity': Decimal(str(current['humidity'])),
                    'wind_speed': Decimal(str(current['wind_speed'])),
                    'description': current['weather'][0]['description'],
                    'rainfall': Decimal(str(current.get('rain', {}).get('1h', 0))),
                    'pressure': Decimal(str(current.get('pressure', 1013))),
                    'feels_like': Decimal(str(current.get('feels_like', current['temp']))),
                    'uv_index': Decimal(str(current.get('uvi', 0)))
                }
            else:
                # Fallback to basic weather API if One Call fails
                return WeatherService._get_basic_weather(latitude, longitude)
                
        except Exception as e:
            print(f"One Call API error: {e}, trying basic API...")
            return WeatherService._get_basic_weather(latitude, longitude)
    
    @staticmethod
    def _get_basic_weather(latitude, longitude):
        """Fallback to basic weather API"""
        try:
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
                'rainfall': Decimal(str(data.get('rain', {}).get('1h', 0))),
                'pressure': Decimal(str(data['main'].get('pressure', 1013))),
                'feels_like': Decimal(str(data['main'].get('feels_like', data['main']['temp']))),
                'uv_index': Decimal('0')
            }
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            # Return demo data if all APIs fail
            return {
                'temperature': Decimal('22.0'),
                'humidity': Decimal('65.0'),
                'wind_speed': Decimal('3.8'),
                'description': 'Weather data unavailable',
                'rainfall': Decimal('0'),
                'pressure': Decimal('1013'),
                'feels_like': Decimal('22.0'),
                'uv_index': Decimal('0')
            }
    
    @staticmethod
    def get_weather_by_city(city_name):
        """Fetch weather data by city name using FREE API"""
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == 'PUT_YOUR_FREE_API_KEY_HERE':
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
            # Return demo data if API fails
            return {
                'temperature': Decimal('24.0'),
                'humidity': Decimal('70.0'),
                'wind_speed': Decimal('4.5'),
                'description': f'Partly cloudy in {city_name} (demo data)',
                'rainfall': Decimal('0'),
                'latitude': -1.2921,
                'longitude': 36.8219
            }
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

    @staticmethod
    def get_extended_weather(latitude, longitude):
        """Get extended weather data using FREE One Call API 2.5 (current + hourly + daily forecasts)"""
        if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == 'PUT_YOUR_FREE_API_KEY_HERE':
            return None
        
        try:
            # Use FREE One Call API 2.5 - includes current, hourly (48h), daily (7d)!
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(WeatherService.ONE_CALL_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'current': {
                        'temperature': Decimal(str(data['current']['temp'])),
                        'feels_like': Decimal(str(data['current']['feels_like'])),
                        'humidity': Decimal(str(data['current']['humidity'])),
                        'wind_speed': Decimal(str(data['current']['wind_speed'])),
                        'description': data['current']['weather'][0]['description'],
                        'uv_index': Decimal(str(data['current'].get('uvi', 0))),
                        'pressure': Decimal(str(data['current'].get('pressure', 1013)))
                    },
                    'hourly': data.get('hourly', [])[:24],  # Next 24 hours
                    'daily': data.get('daily', [])[:7],     # Next 7 days
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error fetching extended weather data: {e}")
            return None
