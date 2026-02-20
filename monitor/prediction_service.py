import pandas as pd
import numpy as np
from decimal import Decimal
from django.utils import timezone


class YieldPredictionService:
    """Service for predicting crop yields based on weather and crop data"""
    
    # Base yields per acre for different crops (in bags)
    BASE_YIELDS = {
        'maize': 15,
        'beans': 8,
        'wheat': 12,
        'coffee': 10,
        'tea': 20,
        'potato': 25,
        'tomato': 30,
    }
    
    # Optimal temperature ranges (min, max) in Celsius
    OPTIMAL_TEMP = {
        'maize': (18, 30),
        'beans': (15, 27),
        'wheat': (12, 25),
        'coffee': (15, 24),
        'tea': (13, 30),
        'potato': (15, 20),
        'tomato': (18, 27),
    }
    
    @staticmethod
    def predict_yield(crop, weather_records):
        """
        Predict crop yield based on historical weather data with enhanced algorithm
        
        Args:
            crop: Crop model instance
            weather_records: QuerySet of WeatherRecord instances
        
        Returns:
            dict with predicted_yield and confidence_score
        """
        if not weather_records.exists():
            # No weather data, return base yield with low confidence
            base_yield = YieldPredictionService.BASE_YIELDS.get(crop.crop_type, 10)
            return {
                'predicted_yield': Decimal(str(base_yield * float(crop.area_planted))),
                'confidence_score': Decimal('30.0'),
                'factors': {
                    'temperature': 'Unknown',
                    'rainfall': 'Unknown',
                    'humidity': 'Unknown'
                }
            }
        
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame(list(weather_records.values('temperature', 'humidity', 'rainfall')))
        
        # Calculate weather factors
        avg_temp = float(df['temperature'].mean())
        avg_humidity = float(df['humidity'].mean())
        total_rainfall = float(df['rainfall'].sum())
        temp_variance = float(df['temperature'].std())
        
        # Get base yield for crop type
        base_yield = YieldPredictionService.BASE_YIELDS.get(crop.crop_type, 10)
        
        # Calculate temperature factor with variance penalty
        optimal_range = YieldPredictionService.OPTIMAL_TEMP.get(crop.crop_type, (15, 30))
        if optimal_range[0] <= avg_temp <= optimal_range[1]:
            temp_factor = 1.0
        else:
            deviation = min(abs(avg_temp - optimal_range[0]), abs(avg_temp - optimal_range[1]))
            temp_factor = max(0.5, 1.0 - (deviation * 0.05))
        
        # Penalize high temperature variance (stress)
        if temp_variance > 5:
            temp_factor *= max(0.8, 1.0 - (temp_variance - 5) * 0.02)
        
        # Calculate rainfall factor with crop-specific requirements
        optimal_rainfall = {
            'maize': (500, 800),
            'beans': (400, 600),
            'wheat': (450, 650),
            'coffee': (1000, 1500),
            'tea': (1200, 1800),
            'potato': (500, 700),
            'tomato': (400, 600),
        }
        
        rain_range = optimal_rainfall.get(crop.crop_type, (500, 800))
        if rain_range[0] <= total_rainfall <= rain_range[1]:
            rain_factor = 1.0
        elif total_rainfall < rain_range[0]:
            rain_factor = max(0.4, total_rainfall / rain_range[0])
        else:
            rain_factor = max(0.6, 1.0 - ((total_rainfall - rain_range[1]) / rain_range[1]))
        
        # Calculate humidity factor
        if 60 <= avg_humidity <= 80:
            humidity_factor = 1.0
        elif avg_humidity < 60:
            humidity_factor = max(0.6, avg_humidity / 60)
        else:
            humidity_factor = max(0.7, 1.0 - (avg_humidity - 80) / 100)
        
        # Growth stage bonus
        stage_bonus = {
            'germination': 0.9,
            'vegetative': 1.0,
            'flowering': 1.1,
            'fruiting': 1.15,
            'maturity': 1.2,
            'harvest': 1.0
        }
        stage_multiplier = stage_bonus.get(crop.current_stage, 1.0)
        
        # Calculate final yield with weighted factors
        combined_factor = (
            (temp_factor * 0.35) + 
            (rain_factor * 0.40) + 
            (humidity_factor * 0.25)
        ) * stage_multiplier
        
        predicted_yield_per_acre = base_yield * combined_factor
        total_predicted_yield = predicted_yield_per_acre * float(crop.area_planted)
        
        # Calculate confidence score based on data availability and quality
        days_of_data = weather_records.count()
        data_quality = min(100, (days_of_data / 30) * 100)  # 30 days = 100%
        
        # Reduce confidence if factors are poor
        factor_quality = combined_factor * 100
        confidence = min(95, (data_quality * 0.6) + (factor_quality * 0.4))
        confidence = max(30, confidence)
        
        return {
            'predicted_yield': Decimal(str(round(total_predicted_yield, 2))),
            'confidence_score': Decimal(str(round(confidence, 2))),
            'factors': {
                'temperature': f'{temp_factor:.2f}',
                'rainfall': f'{rain_factor:.2f}',
                'humidity': f'{humidity_factor:.2f}',
                'stage_bonus': f'{stage_multiplier:.2f}'
            }
        }
    
    @staticmethod
    def update_crop_stage(crop):
        """Update crop growth stage based on days since planting"""
        days = crop.days_since_planting()
        
        # Simple stage progression based on days (varies by crop)
        stage_thresholds = {
            'maize': [(0, 'germination'), (14, 'vegetative'), (60, 'flowering'), 
                     (80, 'fruiting'), (100, 'maturity'), (120, 'harvest')],
            'beans': [(0, 'germination'), (10, 'vegetative'), (35, 'flowering'),
                     (50, 'fruiting'), (70, 'maturity'), (90, 'harvest')],
            'wheat': [(0, 'germination'), (21, 'vegetative'), (60, 'flowering'),
                     (80, 'fruiting'), (100, 'maturity'), (120, 'harvest')],
        }
        
        thresholds = stage_thresholds.get(crop.crop_type, stage_thresholds['maize'])
        
        for threshold_days, stage in reversed(thresholds):
            if days >= threshold_days:
                return stage
        
        return 'germination'
