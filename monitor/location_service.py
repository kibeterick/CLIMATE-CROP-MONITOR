"""
Location and Geolocation Services
"""
import requests
from django.conf import settings
from decimal import Decimal


class LocationService:
    """Handle location detection and geocoding"""
    
    GEOCODING_URL = "https://nominatim.openstreetmap.org/search"
    REVERSE_GEOCODING_URL = "https://nominatim.openstreetmap.org/reverse"
    
    @staticmethod
    def get_location_from_coordinates(latitude, longitude):
        """Get location name from coordinates (reverse geocoding)"""
        try:
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'ClimateMonitor/2.0'
            }
            
            response = requests.get(
                LocationService.REVERSE_GEOCODING_URL,
                params=params,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                # Build location string
                location_parts = []
                if address.get('city'):
                    location_parts.append(address['city'])
                elif address.get('town'):
                    location_parts.append(address['town'])
                elif address.get('village'):
                    location_parts.append(address['village'])
                
                if address.get('county'):
                    location_parts.append(address['county'])
                elif address.get('state'):
                    location_parts.append(address['state'])
                
                if address.get('country'):
                    location_parts.append(address['country'])
                
                location_name = ', '.join(location_parts) if location_parts else data.get('display_name', 'Unknown Location')
                
                return {
                    'location': location_name,
                    'city': address.get('city') or address.get('town') or address.get('village', ''),
                    'county': address.get('county') or address.get('state', ''),
                    'country': address.get('country', ''),
                    'latitude': latitude,
                    'longitude': longitude
                }
            
            return None
            
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None
    
    @staticmethod
    def search_location(location_name):
        """Search for location and get coordinates (geocoding)"""
        try:
            params = {
                'q': location_name,
                'format': 'json',
                'limit': 5,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'ClimateMonitor/2.0'
            }
            
            response = requests.get(
                LocationService.GEOCODING_URL,
                params=params,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json()
                
                if results:
                    locations = []
                    for result in results:
                        address = result.get('address', {})
                        locations.append({
                            'display_name': result.get('display_name', ''),
                            'latitude': float(result.get('lat', 0)),
                            'longitude': float(result.get('lon', 0)),
                            'city': address.get('city') or address.get('town') or address.get('village', ''),
                            'county': address.get('county') or address.get('state', ''),
                            'country': address.get('country', ''),
                            'type': result.get('type', '')
                        })
                    
                    return locations
            
            return []
            
        except Exception as e:
            print(f"Geocoding error: {e}")
            return []
    
    @staticmethod
    def get_current_location_weather(latitude, longitude):
        """Get weather for current location"""
        from .weather_service import WeatherService
        
        # Get location name
        location_info = LocationService.get_location_from_coordinates(latitude, longitude)
        
        # Get weather data
        weather_data = WeatherService.get_weather_data(latitude, longitude)
        
        if location_info and weather_data:
            return {
                'location': location_info,
                'weather': weather_data
            }
        
        return None
    
    @staticmethod
    def search_location_weather(location_name):
        """Search location and get its weather"""
        from .weather_service import WeatherService
        
        # Search for location
        locations = LocationService.search_location(location_name)
        
        if not locations:
            return None
        
        # Get weather for first result
        first_location = locations[0]
        weather_data = WeatherService.get_weather_data(
            first_location['latitude'],
            first_location['longitude']
        )
        
        return {
            'location': first_location,
            'weather': weather_data,
            'all_results': locations
        }
