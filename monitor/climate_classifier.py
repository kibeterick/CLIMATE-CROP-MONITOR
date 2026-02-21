"""
Climate Classification and Agricultural Suitability Analysis
"""
from decimal import Decimal


class ClimateClassifier:
    """Classify climate zones and provide agricultural recommendations"""
    
    @staticmethod
    def classify_climate(temperature, rainfall_annual, humidity=None):
        """
        Classify climate based on temperature and rainfall
        Uses simplified Köppen climate classification
        """
        temp = float(temperature)
        rainfall = float(rainfall_annual)
        
        # Desert/Arid Climate
        if rainfall < 250:
            climate_type = 'Desert (Arid)'
            climate_code = 'BW'
            description = 'Very dry climate with minimal rainfall. Extreme temperatures.'
            suitability = 'poor'
            
        # Semi-Arid/Steppe
        elif rainfall < 500:
            climate_type = 'Semi-Arid (Steppe)'
            climate_code = 'BS'
            description = 'Dry climate with limited rainfall. Suitable for drought-resistant crops.'
            suitability = 'limited'
            
        # Tropical
        elif temp > 18 and rainfall > 1500:
            climate_type = 'Tropical Rainforest'
            climate_code = 'Af'
            description = 'Hot and wet year-round. High rainfall and humidity.'
            suitability = 'excellent'
            
        elif temp > 18 and rainfall > 750:
            climate_type = 'Tropical Savanna'
            climate_code = 'Aw'
            description = 'Warm with distinct wet and dry seasons.'
            suitability = 'good'
            
        # Temperate
        elif 10 < temp <= 18 and rainfall > 500:
            climate_type = 'Temperate'
            climate_code = 'C'
            description = 'Moderate temperatures with adequate rainfall.'
            suitability = 'excellent'
            
        # Highland/Mountain
        elif temp < 10 and rainfall > 500:
            climate_type = 'Highland'
            climate_code = 'H'
            description = 'Cool temperatures, suitable for specific crops like tea and coffee.'
            suitability = 'good'
            
        else:
            climate_type = 'Subtropical'
            climate_code = 'Cfa'
            description = 'Warm summers, mild winters, good rainfall distribution.'
            suitability = 'excellent'
        
        return {
            'climate_type': climate_type,
            'climate_code': climate_code,
            'description': description,
            'suitability': suitability,
            'is_desert': climate_code in ['BW', 'BS'],
            'temperature': temp,
            'rainfall': rainfall
        }
    
    @staticmethod
    def get_suitable_crops(climate_type, is_desert=False, temperature=20, rainfall=800):
        """Get crops suitable for the climate with temperature and rainfall considerations"""
        
        temp = float(temperature)
        rain = float(rainfall)
        
        if is_desert or 'Desert' in climate_type or 'Arid' in climate_type:
            return {
                'suitable': ['Date Palm', 'Cactus Pear', 'Aloe Vera', 'Drought-resistant Millet'],
                'possible': ['Sorghum (with irrigation)', 'Pearl Millet (with irrigation)', 'Chickpeas (with irrigation)'],
                'not_suitable': ['Rice', 'Tea', 'Coffee', 'Banana', 'Most vegetables', 'Maize'],
                'irrigation': 'Essential - Drip irrigation highly recommended',
                'warning': '⚠️ DESERT CLIMATE: Agriculture very challenging without irrigation'
            }
        
        elif 'Semi-Arid' in climate_type or 'Steppe' in climate_type:
            return {
                'suitable': ['Sorghum', 'Pearl Millet', 'Cowpeas', 'Pigeon Peas', 'Cassava'],
                'possible': ['Maize (with irrigation)', 'Sunflower', 'Groundnuts'],
                'not_suitable': ['Rice', 'Tea', 'Coffee', 'Water-intensive crops'],
                'irrigation': 'Highly recommended - Drip or sprinkler systems',
                'warning': '⚠️ Limited rainfall - Choose drought-resistant varieties'
            }
        
        elif 'Tropical Rainforest' in climate_type:
            return {
                'suitable': ['Banana', 'Pineapple', 'Cassava', 'Yams', 'Cocoa', 'Oil Palm', 'Rubber'],
                'possible': ['Rice', 'Sugarcane', 'Coconut', 'Papaya', 'Mango'],
                'not_suitable': ['Wheat', 'Barley', 'Temperate fruits', 'Potatoes'],
                'irrigation': 'Minimal - Natural rainfall usually sufficient',
                'warning': None
            }
        
        elif 'Tropical Savanna' in climate_type:
            return {
                'suitable': ['Maize', 'Beans', 'Cassava', 'Sweet Potato', 'Sorghum', 'Millet'],
                'possible': ['Rice (in wet season)', 'Sugarcane', 'Cotton', 'Groundnuts', 'Sunflower'],
                'not_suitable': ['Wheat', 'Barley', 'Tea', 'Coffee (unless highland)'],
                'irrigation': 'Needed during dry season - Supplemental irrigation recommended',
                'warning': None
            }
        
        elif 'Highland' in climate_type:
            # Highland crops vary by temperature
            if temp < 12:
                suitable = ['Tea', 'Pyrethrum', 'Wheat', 'Barley', 'Irish Potato', 'Cabbage', 'Carrots']
                possible = ['Coffee (Arabica)', 'Maize', 'Beans']
            else:
                suitable = ['Coffee (Arabica)', 'Tea', 'Irish Potato', 'Cabbage', 'Carrots', 'Onions']
                possible = ['Maize', 'Beans', 'Wheat', 'Tomatoes']
            
            return {
                'suitable': suitable,
                'possible': possible,
                'not_suitable': ['Tropical fruits', 'Cotton', 'Cassava', 'Banana'],
                'irrigation': 'Usually adequate rainfall, supplemental may be needed in dry season',
                'warning': None
            }
        
        elif 'Temperate' in climate_type:
            return {
                'suitable': ['Maize', 'Wheat', 'Beans', 'Tomato', 'Potato', 'Cabbage', 'Lettuce', 'Carrots'],
                'possible': ['Coffee (lower altitudes)', 'Apples', 'Grapes', 'Strawberries'],
                'not_suitable': ['Tropical crops requiring high heat', 'Banana', 'Cassava'],
                'irrigation': 'Supplemental irrigation recommended during dry periods',
                'warning': None
            }
        
        elif 'Subtropical' in climate_type:
            # Subtropical varies by rainfall
            if rain > 1000:
                suitable = ['Maize', 'Rice', 'Sugarcane', 'Citrus fruits', 'Avocado', 'Mango']
                possible = ['Coffee', 'Tea', 'Banana', 'Pineapple']
            else:
                suitable = ['Maize', 'Beans', 'Tomato', 'Citrus fruits', 'Avocado']
                possible = ['Wheat', 'Sunflower', 'Groundnuts']
            
            return {
                'suitable': suitable,
                'possible': possible,
                'not_suitable': ['Crops requiring extreme cold or heat'],
                'irrigation': 'Supplemental irrigation recommended' if rain < 800 else 'May need irrigation in dry season',
                'warning': None
            }
        
        else:
            return {
                'suitable': ['Maize', 'Beans', 'Vegetables'],
                'possible': ['Various crops depending on specific conditions'],
                'not_suitable': [],
                'irrigation': 'Assess based on rainfall patterns',
                'warning': None
            }
    
    @staticmethod
    def analyze_location_climate(latitude, longitude, weather_data):
        """
        Comprehensive climate analysis for a location
        """
        # Get temperature and humidity
        temperature = float(weather_data.get('temperature', 20))
        humidity = float(weather_data.get('humidity', 60))
        
        # Estimate annual rainfall based on location and current conditions
        # Use latitude and current weather to make better estimates
        lat = abs(float(latitude))
        current_rainfall = float(weather_data.get('rainfall', 0))
        
        # Kenya-specific rainfall estimation based on regions
        # Coastal/Lake regions (Kisumu, Mombasa): 1000-1800mm
        # Highland regions (Kericho, Nairobi): 900-1500mm  
        # Arid/Semi-arid (Mandera, Turkana): 200-500mm
        # Rift Valley: 600-1000mm
        
        # Use latitude to help estimate climate zone
        if lat < 23.5:  # Tropical zone
            if humidity > 70 and temperature > 22:
                # Hot and humid - likely coastal or lake region (Kisumu, Mombasa)
                estimated_annual_rainfall = 1200 + (humidity - 70) * 20
            elif temperature < 18 and humidity > 60:
                # Cool and humid - likely highland (Kericho, Nyandarua)
                estimated_annual_rainfall = 1100 + (humidity - 60) * 15
            elif humidity < 40 and temperature > 28:
                # Hot and dry - likely arid region (Mandera, Turkana)
                estimated_annual_rainfall = 250 + (humidity * 5)
            elif humidity < 50 and temperature > 25:
                # Warm and dry - semi-arid (Machakos, Kitui)
                estimated_annual_rainfall = 400 + (humidity * 8)
            else:
                # Moderate tropical conditions
                estimated_annual_rainfall = 800 + (humidity * 10)
        elif lat < 50:  # Temperate zone (Europe, parts of Asia)
            if temperature < 15:
                # Cool temperate (UK, Ireland, Northern Europe)
                estimated_annual_rainfall = 700 + (humidity * 8)
            else:
                # Warm temperate
                estimated_annual_rainfall = 600 + (humidity * 10)
        else:  # Cold zones
            estimated_annual_rainfall = 400 + (humidity * 6)
        
        # Adjust based on current rainfall if significant
        if current_rainfall > 5:
            estimated_annual_rainfall = max(estimated_annual_rainfall, 900)
        
        # Classify climate
        climate = ClimateClassifier.classify_climate(
            temperature, 
            estimated_annual_rainfall,
            humidity
        )
        
        # Get suitable crops with temperature and rainfall data
        crops = ClimateClassifier.get_suitable_crops(
            climate['climate_type'],
            climate['is_desert'],
            temperature,
            estimated_annual_rainfall
        )
        
        # Agricultural recommendations based on specific conditions
        recommendations = []
        
        # Location-specific insights
        location_insight = ""
        if lat < 23.5:  # Tropical/Subtropical regions
            if humidity > 70 and temperature > 22:
                location_insight = "🌊 Lake/Coastal Climate (like Kisumu, Mombasa)"
            elif temperature < 18 and humidity > 60:
                location_insight = "⛰️ Highland Climate (like Kericho, Nyandarua)"
            elif humidity < 40 and temperature > 28:
                location_insight = "🏜️ Arid Climate (like Mandera, Turkana)"
            elif humidity < 50 and temperature > 25:
                location_insight = "🌾 Semi-Arid Climate (like Machakos, Kitui)"
            else:
                location_insight = "🌤️ Tropical/Subtropical Climate"
        elif lat < 50:  # Temperate regions
            if temperature < 15:
                location_insight = "🌧️ Cool Temperate Climate (like UK, Ireland, Northern Europe)"
            else:
                location_insight = "🌤️ Warm Temperate Climate (like Mediterranean)"
        else:  # Cold regions
            location_insight = "❄️ Cold Climate (like Scandinavia, Canada)"
        
        if location_insight:
            recommendations.append(location_insight)
        
        if climate['is_desert']:
            recommendations.append("🏜️ DESERT/ARID CLIMATE DETECTED")
            recommendations.append("• Drip irrigation is ESSENTIAL for any agriculture")
            recommendations.append("• Consider greenhouse farming to conserve water")
            recommendations.append("• Use mulching to reduce water evaporation")
            recommendations.append("• Plant drought-resistant varieties only")
            recommendations.append("• Harvest rainwater when available")
            recommendations.append("• Focus on livestock (camels, goats) as alternative")
        else:
            if climate['suitability'] == 'excellent':
                recommendations.append("✅ Excellent climate for agriculture!")
            elif climate['suitability'] == 'good':
                recommendations.append("✓ Good climate for agriculture with proper management")
            else:
                recommendations.append("⚠️ Limited agricultural potential - special measures needed")
            
            # Rainfall-based recommendations
            if climate['rainfall'] < 400:
                recommendations.append("• CRITICAL: Install irrigation system immediately")
                recommendations.append("• Choose only drought-resistant crops")
            elif climate['rainfall'] < 600:
                recommendations.append("• Irrigation system highly recommended")
                recommendations.append("• Plant early to maximize rainfall")
            elif climate['rainfall'] < 800:
                recommendations.append("• Supplemental irrigation needed during dry season")
            
            # Temperature-based recommendations
            if temperature > 30:
                recommendations.append("• Provide shade for sensitive crops")
                recommendations.append("• Increase watering frequency")
                recommendations.append("• Mulch to keep soil cool")
            elif temperature < 15:
                recommendations.append("• Consider cold-hardy varieties")
                recommendations.append("• Use mulching for temperature regulation")
                recommendations.append("• Protect crops from frost")
            
            # Humidity-based recommendations
            if humidity > 75:
                recommendations.append("• Watch for fungal diseases in high humidity")
                recommendations.append("• Ensure good air circulation")
            elif humidity < 40:
                recommendations.append("• Increase irrigation frequency")
                recommendations.append("• Use mulch to retain soil moisture")
        
        # Water management advice
        if climate['rainfall'] < 400:
            water_status = 'Critical - Irrigation Essential for Survival'
        elif climate['rainfall'] < 600:
            water_status = 'Very Low - Irrigation Required'
        elif climate['rainfall'] < 800:
            water_status = 'Low - Supplemental Irrigation Needed'
        elif climate['rainfall'] < 1200:
            water_status = 'Adequate - Seasonal Irrigation May Be Needed'
        else:
            water_status = 'Abundant - Good Natural Water Supply'
        
        return {
            'climate': climate,
            'suitable_crops': crops,
            'recommendations': recommendations,
            'water_status': water_status,
            'agricultural_potential': climate['suitability'],
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        }
    
    @staticmethod
    def get_climate_zone_by_coordinates(latitude):
        """Determine general climate zone by latitude"""
        lat = abs(float(latitude))
        
        if lat < 23.5:
            return 'Tropical Zone', 'Hot year-round, high rainfall potential'
        elif lat < 35:
            return 'Subtropical Zone', 'Warm summers, mild winters'
        elif lat < 66.5:
            return 'Temperate Zone', 'Four distinct seasons'
        else:
            return 'Polar Zone', 'Very cold, limited agriculture'
