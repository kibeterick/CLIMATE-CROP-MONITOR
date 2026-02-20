"""
Advanced analytics and insights for farmers
"""
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class FarmAnalytics:
    """Advanced analytics for farm performance"""
    
    @staticmethod
    def get_crop_performance(farm):
        """Analyze crop performance metrics"""
        from .models import Crop, YieldPrediction
        
        crops = Crop.objects.filter(farm=farm)
        
        performance = {
            'total_crops': crops.count(),
            'active_crops': crops.filter(is_active=True).count(),
            'harvested_crops': crops.filter(is_active=False, actual_harvest_date__isnull=False).count(),
            'total_area': crops.aggregate(Sum('area_planted'))['area_planted__sum'] or 0,
            'crops_by_type': {},
            'crops_by_stage': {},
            'average_growth_days': 0
        }
        
        # Crops by type
        for crop_type, crop_name in Crop.CROP_TYPES:
            count = crops.filter(crop_type=crop_type).count()
            if count > 0:
                performance['crops_by_type'][crop_name] = count
        
        # Crops by growth stage
        for stage_code, stage_name in Crop.GROWTH_STAGES:
            count = crops.filter(current_stage=stage_code, is_active=True).count()
            if count > 0:
                performance['crops_by_stage'][stage_name] = count
        
        # Average growth days
        active_crops = crops.filter(is_active=True)
        if active_crops.exists():
            total_days = sum([crop.days_since_planting() for crop in active_crops])
            performance['average_growth_days'] = total_days // active_crops.count()
        
        return performance
    
    @staticmethod
    def get_weather_trends(farm, days=30):
        """Analyze weather trends"""
        from .models import WeatherRecord
        
        start_date = timezone.now().date() - timedelta(days=days)
        records = WeatherRecord.objects.filter(
            farm=farm,
            date__gte=start_date
        ).order_by('date')
        
        if not records.exists():
            return None
        
        temps = [float(r.temperature) for r in records]
        humidity = [float(r.humidity) for r in records]
        rainfall = [float(r.rainfall) for r in records]
        
        trends = {
            'avg_temperature': sum(temps) / len(temps) if temps else 0,
            'max_temperature': max(temps) if temps else 0,
            'min_temperature': min(temps) if temps else 0,
            'avg_humidity': sum(humidity) / len(humidity) if humidity else 0,
            'total_rainfall': sum(rainfall),
            'rainy_days': len([r for r in rainfall if r > 0]),
            'records_count': records.count(),
            'temperature_trend': 'stable',  # Can be 'rising', 'falling', 'stable'
            'rainfall_trend': 'normal'  # Can be 'drought', 'normal', 'heavy'
        }
        
        # Determine temperature trend
        if len(temps) >= 7:
            recent_avg = sum(temps[-7:]) / 7
            older_avg = sum(temps[:7]) / 7
            if recent_avg > older_avg + 2:
                trends['temperature_trend'] = 'rising'
            elif recent_avg < older_avg - 2:
                trends['temperature_trend'] = 'falling'
        
        # Determine rainfall trend
        if trends['total_rainfall'] < 10:
            trends['rainfall_trend'] = 'drought'
        elif trends['total_rainfall'] > 200:
            trends['rainfall_trend'] = 'heavy'
        
        return trends
    
    @staticmethod
    def get_yield_predictions_summary(farm):
        """Summarize yield predictions"""
        from .models import YieldPrediction, Crop
        
        crops = Crop.objects.filter(farm=farm, is_active=True)
        predictions = YieldPrediction.objects.filter(crop__in=crops)
        
        if not predictions.exists():
            return None
        
        total_predicted = predictions.aggregate(Sum('predicted_yield'))['predicted_yield__sum'] or 0
        avg_confidence = predictions.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
        
        return {
            'total_predicted_yield': float(total_predicted),
            'average_confidence': float(avg_confidence),
            'predictions_count': predictions.count(),
            'crops_with_predictions': crops.filter(predictions__isnull=False).distinct().count()
        }
    
    @staticmethod
    def get_alert_summary(farm):
        """Summarize alerts"""
        from .models import Alert
        
        alerts = Alert.objects.filter(farm=farm)
        
        return {
            'total_alerts': alerts.count(),
            'unread_alerts': alerts.filter(is_read=False).count(),
            'critical_alerts': alerts.filter(severity='critical').count(),
            'high_alerts': alerts.filter(severity='high').count(),
            'alerts_by_type': {
                alert_type: alerts.filter(alert_type=alert_type).count()
                for alert_type, _ in Alert.ALERT_TYPES
            }
        }
    
    @staticmethod
    def get_irrigation_recommendation(farm, crop):
        """Calculate irrigation needs based on weather and crop type"""
        from .models import WeatherRecord
        
        # Get recent weather (last 7 days)
        week_ago = timezone.now().date() - timedelta(days=7)
        recent_weather = WeatherRecord.objects.filter(
            farm=farm,
            date__gte=week_ago
        )
        
        if not recent_weather.exists():
            return None
        
        total_rainfall = sum([float(w.rainfall) for w in recent_weather])
        avg_temp = sum([float(w.temperature) for w in recent_weather]) / recent_weather.count()
        avg_humidity = sum([float(w.humidity) for w in recent_weather]) / recent_weather.count()
        
        # Crop water requirements (mm/day)
        water_needs = {
            'maize': 5.0,
            'beans': 4.0,
            'wheat': 4.5,
            'coffee': 6.0,
            'tea': 5.5,
            'potato': 5.0,
            'tomato': 6.0
        }
        
        daily_need = water_needs.get(crop.crop_type, 5.0)
        weekly_need = daily_need * 7
        
        # Adjust for temperature and humidity
        if avg_temp > 30:
            weekly_need *= 1.2
        if avg_humidity < 50:
            weekly_need *= 1.1
        
        deficit = weekly_need - total_rainfall
        
        recommendation = {
            'weekly_water_need': round(weekly_need, 2),
            'rainfall_received': round(total_rainfall, 2),
            'water_deficit': round(max(0, deficit), 2),
            'irrigation_needed': deficit > 0,
            'irrigation_amount': round(max(0, deficit), 2),
            'frequency': 'daily' if deficit > 20 else 'every 2-3 days' if deficit > 10 else 'weekly'
        }
        
        return recommendation
