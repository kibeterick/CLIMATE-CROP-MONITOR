from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q, Count, Sum, Avg
from datetime import timedelta
from .models import Farmer, Farm, Crop, WeatherRecord, YieldPrediction, Alert
from .weather_service import WeatherService
from .prediction_service import YieldPredictionService
from .utils import (
    export_crops_to_csv, export_weather_to_csv, 
    calculate_farm_statistics, check_and_create_alerts,
    get_crop_recommendations
)


def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'monitor/home.html')


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create farmer profile
            Farmer.objects.create(
                user=user,
                county=request.POST.get('county', 'Kiambu')
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'monitor/register.html', {'form': form})


@login_required
def dashboard(request):
    """Main dashboard with enhanced statistics"""
    try:
        farmer = request.user.farmer
    except Farmer.DoesNotExist:
        farmer = Farmer.objects.create(user=request.user, county='Kiambu')
    
    farms = farmer.farms.all()
    total_farms = farms.count()
    active_crops = Crop.objects.filter(farm__farmer=farmer, is_active=True)
    total_crops = active_crops.count()
    
    # Calculate total area
    total_area = farms.aggregate(Sum('size_acres'))['size_acres__sum'] or 0
    planted_area = active_crops.aggregate(Sum('area_planted'))['area_planted__sum'] or 0
    
    # Get recent alerts
    recent_alerts = Alert.objects.filter(farm__farmer=farmer, is_read=False)[:5]
    total_unread_alerts = Alert.objects.filter(farm__farmer=farmer, is_read=False).count()
    
    # Get weather data for first farm
    current_weather = None
    if farms.exists():
        first_farm = farms.first()
        if first_farm.latitude and first_farm.longitude:
            current_weather = WeatherService.get_weather_data(
                first_farm.latitude, first_farm.longitude
            )
    
    # Crops by stage
    crops_by_stage = {}
    for stage_code, stage_name in Crop.GROWTH_STAGES:
        count = active_crops.filter(current_stage=stage_code).count()
        if count > 0:
            crops_by_stage[stage_name] = count
    
    context = {
        'farmer': farmer,
        'total_farms': total_farms,
        'total_crops': total_crops,
        'total_area': total_area,
        'planted_area': planted_area,
        'active_crops': active_crops[:5],
        'recent_alerts': recent_alerts,
        'total_unread_alerts': total_unread_alerts,
        'current_weather': current_weather,
        'crops_by_stage': crops_by_stage,
    }
    return render(request, 'monitor/dashboard.html', context)


@login_required
def farm_list(request):
    """List all farms with search and filter"""
    farmer = request.user.farmer
    farms = farmer.farms.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        farms = farms.filter(
            Q(name__icontains=search_query) | 
            Q(location__icontains=search_query) |
            Q(soil_type__icontains=search_query)
        )
    
    # Add statistics to each farm
    farms_with_stats = []
    for farm in farms:
        farm.active_crops_count = farm.get_active_crops_count()
        farm.total_area_planted = farm.get_total_area_planted()
        farms_with_stats.append(farm)
    
    context = {
        'farms': farms_with_stats,
        'search_query': search_query,
    }
    return render(request, 'monitor/farm_list.html', context)


@login_required
def farm_detail(request, farm_id):
    """Farm detail view with comprehensive statistics"""
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    crops = farm.crops.filter(is_active=True)
    weather_records = farm.weather_records.all()[:30]
    alerts = farm.alerts.all()[:10]
    
    # Calculate farm statistics
    stats = calculate_farm_statistics(farm)
    
    # Get crop recommendations
    recommendations = get_crop_recommendations(farm, weather_records)
    
    context = {
        'farm': farm,
        'crops': crops,
        'weather_records': weather_records,
        'alerts': alerts,
        'stats': stats,
        'recommendations': recommendations,
    }
    return render(request, 'monitor/farm_detail.html', context)


@login_required
def farm_create(request):
    """Create new farm"""
    if request.method == 'POST':
        farm = Farm.objects.create(
            farmer=request.user.farmer,
            name=request.POST['name'],
            location=request.POST['location'],
            size_acres=request.POST['size_acres'],
            soil_type=request.POST.get('soil_type', '')
        )
        
        # Always try to get coordinates from weather API
        try:
            weather_data = WeatherService.get_weather_by_city(request.POST['location'])
            if weather_data:
                farm.latitude = weather_data['latitude']
                farm.longitude = weather_data['longitude']
                farm.save()
                
                # Create initial weather record
                WeatherRecord.objects.create(
                    farm=farm,
                    temperature=weather_data['temperature'],
                    humidity=weather_data['humidity'],
                    rainfall=weather_data['rainfall'],
                    wind_speed=weather_data['wind_speed'],
                    description=weather_data['description']
                )
                messages.success(request, f'Farm created with weather data! Current temp: {weather_data["temperature"]}°C')
            else:
                messages.success(request, 'Farm created! Click "Update Weather" to fetch weather data.')
        except Exception as e:
            messages.success(request, 'Farm created! Click "Update Weather" to fetch weather data.')
        
        return redirect('farm_detail', farm_id=farm.id)
    
    return render(request, 'monitor/farm_form.html')


@login_required
def crop_create(request, farm_id):
    """Create new crop"""
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    
    if request.method == 'POST':
        crop = Crop.objects.create(
            farm=farm,
            crop_type=request.POST['crop_type'],
            variety=request.POST.get('variety', ''),
            planting_date=request.POST['planting_date'],
            area_planted=request.POST['area_planted']
        )
        
        messages.success(request, 'Crop registered successfully!')
        return redirect('farm_detail', farm_id=farm.id)
    
    return render(request, 'monitor/crop_form.html', {'farm': farm})


@login_required
def crop_detail(request, crop_id):
    """Crop detail view with predictions"""
    crop = get_object_or_404(Crop, id=crop_id, farm__farmer=request.user.farmer)
    
    # Update crop stage
    new_stage = YieldPredictionService.update_crop_stage(crop)
    if new_stage != crop.current_stage:
        crop.current_stage = new_stage
        crop.save()
    
    # Get weather records for the farm
    weather_records = crop.farm.weather_records.filter(
        date__gte=crop.planting_date
    )
    
    # Get or create yield prediction
    latest_prediction = crop.predictions.first()
    if not latest_prediction or (timezone.now().date() - latest_prediction.prediction_date).days > 7:
        # Generate new prediction
        prediction_data = YieldPredictionService.predict_yield(crop, weather_records)
        latest_prediction = YieldPrediction.objects.create(
            crop=crop,
            predicted_yield=prediction_data['predicted_yield'],
            confidence_score=prediction_data['confidence_score']
        )
    
    context = {
        'crop': crop,
        'latest_prediction': latest_prediction,
        'weather_records': weather_records[:10],
        'days_since_planting': crop.days_since_planting(),
    }
    return render(request, 'monitor/crop_detail.html', context)


@login_required
def weather_update(request, farm_id):
    """Fetch and update weather data for a farm"""
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    
    # Try to get coordinates if not set
    if not farm.latitude or not farm.longitude:
        weather_data = WeatherService.get_weather_by_city(farm.location)
        if weather_data:
            farm.latitude = weather_data['latitude']
            farm.longitude = weather_data['longitude']
            farm.save()
    
    if farm.latitude and farm.longitude:
        weather_data = WeatherService.get_weather_data(farm.latitude, farm.longitude)
        
        if weather_data:
            weather_record = WeatherRecord.objects.create(
                farm=farm,
                temperature=weather_data['temperature'],
                humidity=weather_data['humidity'],
                rainfall=weather_data['rainfall'],
                wind_speed=weather_data['wind_speed'],
                description=weather_data['description']
            )
            
            farm.last_weather_update = timezone.now()
            farm.save(update_fields=['last_weather_update'])
            
            # Check for weather alerts
            if weather_data['temperature'] > 35:
                Alert.objects.create(
                    farm=farm,
                    alert_type='weather',
                    severity='high',
                    title='High Temperature Alert',
                    message=f'Temperature is {weather_data["temperature"]}°C. Consider irrigation.'
                )
            elif weather_data['temperature'] < 10:
                Alert.objects.create(
                    farm=farm,
                    alert_type='weather',
                    severity='medium',
                    title='Low Temperature Alert',
                    message=f'Temperature is {weather_data["temperature"]}°C. Protect sensitive crops.'
                )
            
            messages.success(request, f'Weather updated! Temp: {weather_data["temperature"]}°C, Humidity: {weather_data["humidity"]}%')
        else:
            messages.error(request, 'Failed to fetch weather data. Using demo data.')
    else:
        messages.warning(request, f'Could not find coordinates for {farm.location}. Please update farm location.')
    
    return redirect('farm_detail', farm_id=farm.id)


@login_required
def alerts_list(request):
    """List all alerts"""
    farmer = request.user.farmer
    alerts = Alert.objects.filter(farm__farmer=farmer)
    return render(request, 'monitor/alerts_list.html', {'alerts': alerts})


@login_required
def alert_mark_read(request, alert_id):
    """Mark alert as read"""
    alert = get_object_or_404(Alert, id=alert_id, farm__farmer=request.user.farmer)
    alert.is_read = True
    alert.save()
    return redirect('alerts_list')


@login_required
def export_crops(request):
    """Export crops data to CSV"""
    farmer = request.user.farmer
    crops = Crop.objects.filter(farm__farmer=farmer)
    
    csv_data = export_crops_to_csv(crops)
    
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="crops_export_{timezone.now().strftime("%Y%m%d")}.csv"'
    return response


@login_required
def export_weather(request, farm_id):
    """Export weather data for a farm to CSV"""
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    weather_records = farm.weather_records.all()
    
    csv_data = export_weather_to_csv(weather_records)
    
    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="weather_{farm.name}_{timezone.now().strftime("%Y%m%d")}.csv"'
    return response


@login_required
def batch_update_weather(request):
    """Update weather for all farms"""
    farmer = request.user.farmer
    farms = farmer.farms.exclude(latitude__isnull=True, longitude__isnull=True)
    
    updated_count = 0
    for farm in farms:
        weather_data = WeatherService.get_weather_data(farm.latitude, farm.longitude)
        if weather_data:
            WeatherRecord.objects.create(
                farm=farm,
                temperature=weather_data['temperature'],
                humidity=weather_data['humidity'],
                rainfall=weather_data['rainfall'],
                wind_speed=weather_data['wind_speed'],
                description=weather_data['description']
            )
            farm.last_weather_update = timezone.now()
            farm.save(update_fields=['last_weather_update'])
            
            # Check and create alerts
            check_and_create_alerts(farm)
            updated_count += 1
    
    messages.success(request, f'Weather updated for {updated_count} farm(s)!')
    return redirect('dashboard')


@login_required
def batch_update_crop_stages(request):
    """Update growth stages for all active crops"""
    farmer = request.user.farmer
    crops = Crop.objects.filter(farm__farmer=farmer, is_active=True)
    
    updated_count = 0
    for crop in crops:
        new_stage = YieldPredictionService.update_crop_stage(crop)
        if new_stage != crop.current_stage:
            crop.current_stage = new_stage
            crop.save(update_fields=['current_stage'])
            updated_count += 1
    
    messages.success(request, f'Updated growth stages for {updated_count} crop(s)!')
    return redirect('dashboard')


@login_required
def farm_statistics(request, farm_id):
    """Detailed statistics view for a farm"""
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    stats = calculate_farm_statistics(farm)
    
    # Get weather trends (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    weather_records = farm.weather_records.filter(date__gte=thirty_days_ago).order_by('date')
    
    context = {
        'farm': farm,
        'stats': stats,
        'weather_records': weather_records,
    }
    return render(request, 'monitor/farm_statistics.html', context)


@login_required
def current_location_weather(request):
    """Get weather for user's current location - PUBLIC ACCESS"""
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if latitude and longitude:
            from .location_service import LocationService
            from .climate_classifier import ClimateClassifier
            
            result = LocationService.get_current_location_weather(
                float(latitude),
                float(longitude)
            )
            
            if result:
                # Add climate classification
                climate_analysis = ClimateClassifier.analyze_location_climate(
                    float(latitude),
                    float(longitude),
                    result['weather']
                )
                
                context = {
                    'location': result['location'],
                    'weather': result['weather'],
                    'climate_analysis': climate_analysis,
                    'is_current_location': True
                }
                return render(request, 'monitor/location_weather.html', context)
    
    return render(request, 'monitor/location_weather.html')


def search_location_weather(request):
    """Search for a location and get its weather - PUBLIC ACCESS"""
    context = {}
    
    if request.method == 'POST':
        location_name = request.POST.get('location_search')
        
        if location_name:
            from .location_service import LocationService
            from .climate_classifier import ClimateClassifier
            
            result = LocationService.search_location_weather(location_name)
            
            if result:
                # Add climate classification
                climate_analysis = ClimateClassifier.analyze_location_climate(
                    result['location']['latitude'],
                    result['location']['longitude'],
                    result['weather']
                )
                
                context = {
                    'location': result['location'],
                    'weather': result['weather'],
                    'climate_analysis': climate_analysis,
                    'all_results': result['all_results'],
                    'search_query': location_name,
                    'is_current_location': False
                }
            else:
                messages.error(request, f'Location "{location_name}" not found. Try a different search.')
    
    return render(request, 'monitor/location_weather.html', context)



@login_required
def soil_measurement_create(request, farm_id):
    """Create new soil measurement"""
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    
    if request.method == 'POST':
        from .models import SoilMeasurement
        
        measurement = SoilMeasurement.objects.create(
            farm=farm,
            measurement_date=request.POST.get('measurement_date', timezone.now().date()),
            ph_level=request.POST['ph_level'],
            nitrogen=request.POST['nitrogen'],
            phosphorus=request.POST['phosphorus'],
            potassium=request.POST['potassium'],
            organic_matter=request.POST.get('organic_matter') or None,
            moisture=request.POST.get('moisture') or None,
            temperature=request.POST.get('temperature') or None,
            notes=request.POST.get('notes', '')
        )
        
        # Analyze the measurement
        measurement.analyze()
        
        messages.success(request, 'Soil measurement recorded and analyzed successfully!')
        return redirect('soil_measurement_detail', measurement_id=measurement.id)
    
    return render(request, 'monitor/soil_measurement_form.html', {'farm': farm})


@login_required
def soil_measurement_detail(request, measurement_id):
    """View soil measurement details"""
    from .models import SoilMeasurement
    
    measurement = get_object_or_404(
        SoilMeasurement,
        id=measurement_id,
        farm__farmer=request.user.farmer
    )
    
    context = {
        'measurement': measurement,
        'farm': measurement.farm
    }
    
    return render(request, 'monitor/soil_measurement_detail.html', context)


@login_required
def soil_measurements_list(request, farm_id):
    """List all soil measurements for a farm"""
    from .models import SoilMeasurement
    
    farm = get_object_or_404(Farm, id=farm_id, farmer=request.user.farmer)
    measurements = SoilMeasurement.objects.filter(farm=farm)
    
    context = {
        'farm': farm,
        'measurements': measurements
    }
    
    return render(request, 'monitor/soil_measurements_list.html', context)
