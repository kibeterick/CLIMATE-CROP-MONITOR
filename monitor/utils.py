"""Utility functions for the monitor app"""
import csv
from io import StringIO
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta


def export_crops_to_csv(crops):
    """Export crops data to CSV format"""
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Crop Type', 'Variety', 'Farm', 'Planting Date', 
        'Growth Stage', 'Area (acres)', 'Days Since Planting', 'Status'
    ])
    
    # Write data
    for crop in crops:
        writer.writerow([
            crop.get_crop_type_display(),
            crop.variety or 'N/A',
            crop.farm.name,
            crop.planting_date,
            crop.get_current_stage_display(),
            crop.area_planted,
            crop.days_since_planting(),
            'Active' if crop.is_active else 'Inactive'
        ])
    
    return output.getvalue()


def export_weather_to_csv(weather_records):
    """Export weather records to CSV format"""
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Date', 'Farm', 'Temperature (°C)', 'Humidity (%)', 
        'Rainfall (mm)', 'Wind Speed (m/s)', 'Description'
    ])
    
    # Write data
    for record in weather_records:
        writer.writerow([
            record.date,
            record.farm.name,
            record.temperature,
            record.humidity,
            record.rainfall,
            record.wind_speed or 'N/A',
            record.description
        ])
    
    return output.getvalue()


def calculate_farm_statistics(farm):
    """Calculate comprehensive statistics for a farm"""
    from django.db.models import Avg, Sum, Count
    from .models import Crop, WeatherRecord, YieldPrediction
    
    active_crops = farm.crops.filter(is_active=True)
    
    stats = {
        'total_crops': active_crops.count(),
        'total_area_planted': active_crops.aggregate(Sum('area_planted'))['area_planted__sum'] or 0,
        'crops_by_stage': {},
        'crops_by_type': {},
        'weather_summary': {},
        'predicted_total_yield': 0,
    }
    
    # Crops by stage
    for stage_code, stage_name in Crop.GROWTH_STAGES:
        count = active_crops.filter(current_stage=stage_code).count()
        if count > 0:
            stats['crops_by_stage'][stage_name] = count
    
    # Crops by type
    for crop_code, crop_name in Crop.CROP_TYPES:
        count = active_crops.filter(crop_type=crop_code).count()
        if count > 0:
            stats['crops_by_type'][crop_name] = count
    
    # Weather summary (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_weather = farm.weather_records.filter(date__gte=thirty_days_ago)
    
    if recent_weather.exists():
        weather_agg = recent_weather.aggregate(
            avg_temp=Avg('temperature'),
            avg_humidity=Avg('humidity'),
            total_rainfall=Sum('rainfall')
        )
        stats['weather_summary'] = {
            'avg_temperature': round(float(weather_agg['avg_temp'] or 0), 1),
            'avg_humidity': round(float(weather_agg['avg_humidity'] or 0), 1),
            'total_rainfall': round(float(weather_agg['total_rainfall'] or 0), 1),
            'days_recorded': recent_weather.count()
        }
    
    # Total predicted yield
    for crop in active_crops:
        latest_prediction = crop.predictions.first()
        if latest_prediction:
            stats['predicted_total_yield'] += float(latest_prediction.predicted_yield)
    
    stats['predicted_total_yield'] = round(stats['predicted_total_yield'], 2)
    
    return stats


def check_and_create_alerts(farm):
    """Check conditions and create alerts if needed"""
    from .models import Alert, WeatherRecord
    
    alerts_created = []
    
    # Get latest weather
    latest_weather = farm.weather_records.first()
    if not latest_weather:
        return alerts_created
    
    # Check for extreme temperature
    if latest_weather.temperature > 35:
        alert, created = Alert.objects.get_or_create(
            farm=farm,
            alert_type='weather',
            title='High Temperature Alert',
            defaults={
                'severity': 'high',
                'message': f'Temperature is {latest_weather.temperature}°C. Consider irrigation and shade for sensitive crops.'
            }
        )
        if created:
            alerts_created.append(alert)
    
    elif latest_weather.temperature < 10:
        alert, created = Alert.objects.get_or_create(
            farm=farm,
            alert_type='weather',
            title='Low Temperature Alert',
            defaults={
                'severity': 'medium',
                'message': f'Temperature is {latest_weather.temperature}°C. Protect sensitive crops from cold.'
            }
        )
        if created:
            alerts_created.append(alert)
    
    # Check for low humidity
    if latest_weather.humidity < 40:
        alert, created = Alert.objects.get_or_create(
            farm=farm,
            alert_type='irrigation',
            title='Low Humidity Alert',
            defaults={
                'severity': 'medium',
                'message': f'Humidity is {latest_weather.humidity}%. Increase irrigation frequency.'
            }
        )
        if created:
            alerts_created.append(alert)
    
    # Check crops needing attention
    from .models import Crop
    for crop in farm.crops.filter(is_active=True):
        if crop.needs_attention():
            alert, created = Alert.objects.get_or_create(
                farm=farm,
                alert_type='harvest',
                title=f'{crop.get_crop_type_display()} Needs Attention',
                defaults={
                    'severity': 'medium',
                    'message': f'{crop.get_crop_type_display()} at {crop.current_stage} stage for {crop.days_since_planting()} days. Check growth progress.'
                }
            )
            if created:
                alerts_created.append(alert)
    
    return alerts_created


def get_crop_recommendations(farm, weather_records):
    """Recommend crops based on current weather patterns"""
    from django.db.models import Avg
    
    if not weather_records.exists():
        return []
    
    # Calculate average conditions
    weather_agg = weather_records.aggregate(
        avg_temp=Avg('temperature'),
        avg_humidity=Avg('humidity')
    )
    
    avg_temp = float(weather_agg['avg_temp'] or 20)
    avg_humidity = float(weather_agg['avg_humidity'] or 60)
    
    recommendations = []
    
    # Temperature-based recommendations
    if 18 <= avg_temp <= 30:
        recommendations.append({
            'crop': 'Maize',
            'reason': 'Optimal temperature range (18-30°C)',
            'confidence': 'High'
        })
    
    if 15 <= avg_temp <= 27:
        recommendations.append({
            'crop': 'Beans',
            'reason': 'Suitable temperature range (15-27°C)',
            'confidence': 'High'
        })
    
    if 18 <= avg_temp <= 27:
        recommendations.append({
            'crop': 'Tomato',
            'reason': 'Ideal temperature range (18-27°C)',
            'confidence': 'High'
        })
    
    if 15 <= avg_temp <= 24:
        recommendations.append({
            'crop': 'Coffee',
            'reason': 'Perfect temperature for coffee (15-24°C)',
            'confidence': 'High'
        })
    
    # Humidity considerations
    if avg_humidity > 70:
        recommendations.append({
            'crop': 'Tea',
            'reason': 'High humidity suitable for tea cultivation',
            'confidence': 'Medium'
        })
    
    return recommendations[:5]  # Return top 5 recommendations
