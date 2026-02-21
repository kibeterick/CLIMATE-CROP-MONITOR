from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    county = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Farm(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=200, db_index=True)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    size_acres = models.DecimalField(max_digits=10, decimal_places=2)
    soil_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_weather_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['farmer', 'name']),
        ]

    def __str__(self):
        return f"{self.name} - {self.farmer}"
    
    def get_active_crops_count(self):
        """Get count of active crops"""
        return self.crops.filter(is_active=True).count()
    
    def get_total_area_planted(self):
        """Get total area planted with active crops"""
        from django.db.models import Sum
        result = self.crops.filter(is_active=True).aggregate(Sum('area_planted'))
        return result['area_planted__sum'] or 0


class Crop(models.Model):
    CROP_TYPES = [
        ('maize', 'Maize'),
        ('beans', 'Beans'),
        ('wheat', 'Wheat'),
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('potato', 'Potato'),
        ('tomato', 'Tomato'),
    ]
    
    GROWTH_STAGES = [
        ('germination', 'Germination'),
        ('vegetative', 'Vegetative'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('maturity', 'Maturity'),
        ('harvest', 'Harvest'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    crop_type = models.CharField(max_length=50, choices=CROP_TYPES)
    variety = models.CharField(max_length=100, blank=True)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField(null=True, blank=True)
    actual_harvest_date = models.DateField(null=True, blank=True)
    area_planted = models.DecimalField(max_digits=10, decimal_places=2)
    current_stage = models.CharField(max_length=50, choices=GROWTH_STAGES, default='germination')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-planting_date']
        indexes = [
            models.Index(fields=['farm', 'is_active']),
            models.Index(fields=['crop_type', 'current_stage']),
        ]

    def __str__(self):
        return f"{self.get_crop_type_display()} at {self.farm.name}"

    def days_since_planting(self):
        return (timezone.now().date() - self.planting_date).days
    
    def get_growth_progress_percentage(self):
        """Calculate growth progress as percentage"""
        days = self.days_since_planting()
        # Estimate 120 days as full cycle for most crops
        expected_days = 120
        if self.crop_type in ['beans', 'tomato']:
            expected_days = 90
        elif self.crop_type in ['coffee', 'tea']:
            expected_days = 150
        return min(100, int((days / expected_days) * 100))
    
    def needs_attention(self):
        """Check if crop needs attention based on stage and time"""
        days = self.days_since_planting()
        if self.current_stage == 'germination' and days > 21:
            return True
        if self.current_stage == 'vegetative' and days > 70:
            return True
        return False


class WeatherRecord(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_records')
    date = models.DateField(default=timezone.now)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Weather for {self.farm.name} on {self.date}"


class YieldPrediction(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='predictions')
    predicted_yield = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    prediction_date = models.DateField(auto_now_add=True)
    actual_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prediction for {self.crop} - {self.predicted_yield} bags"


class Alert(models.Model):
    ALERT_TYPES = [
        ('weather', 'Weather Alert'),
        ('pest', 'Pest Alert'),
        ('disease', 'Disease Alert'),
        ('irrigation', 'Irrigation Alert'),
        ('harvest', 'Harvest Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.farm.name}"



class SoilMeasurement(models.Model):
    """Soil analysis and measurements for farms"""
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='soil_measurements')
    measurement_date = models.DateField(default=timezone.now)
    
    # Soil properties
    ph_level = models.DecimalField(max_digits=3, decimal_places=1, help_text="Soil pH (0-14)")
    nitrogen = models.DecimalField(max_digits=5, decimal_places=2, help_text="Nitrogen level (ppm)")
    phosphorus = models.DecimalField(max_digits=5, decimal_places=2, help_text="Phosphorus level (ppm)")
    potassium = models.DecimalField(max_digits=5, decimal_places=2, help_text="Potassium level (ppm)")
    
    # Additional measurements
    organic_matter = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Organic matter (%)")
    moisture = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Soil moisture (%)")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Soil temperature (°C)")
    
    # Analysis results
    ph_status = models.CharField(max_length=50, blank=True)
    nutrient_status = models.CharField(max_length=50, blank=True)
    overall_health = models.CharField(max_length=20, choices=[
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
    ], default='fair')
    
    # Recommendations
    recommendations = models.TextField(blank=True, help_text="Soil improvement recommendations")
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-measurement_date']
        indexes = [
            models.Index(fields=['farm', 'measurement_date']),
        ]
    
    def __str__(self):
        return f"Soil measurement for {self.farm.name} on {self.measurement_date}"
    
    def analyze(self):
        """Analyze soil measurements and generate recommendations"""
        from .soil_service import SoilAnalysisService
        
        # Analyze pH
        ph_analysis = SoilAnalysisService.analyze_soil_ph(self.ph_level)
        self.ph_status = ph_analysis['classification']
        
        # Analyze nutrients
        nutrient_analysis = SoilAnalysisService.analyze_nutrients(
            self.nitrogen, self.phosphorus, self.potassium
        )
        
        # Generate recommendations
        recs = []
        recs.extend(ph_analysis['recommendations'])
        recs.append(f"Nitrogen: {nutrient_analysis['nitrogen']['recommendation']}")
        recs.append(f"Phosphorus: {nutrient_analysis['phosphorus']['recommendation']}")
        recs.append(f"Potassium: {nutrient_analysis['potassium']['recommendation']}")
        
        if self.moisture:
            moisture_analysis = SoilAnalysisService.analyze_soil_moisture(self.moisture)
            recs.append(f"Moisture: {moisture_analysis['recommendation']}")
        
        self.recommendations = '\n'.join(recs)
        
        # Determine overall health
        if ph_analysis['status'] in ['good', 'excellent'] and \
           all(nutrient_analysis[n]['level'] in ['Medium', 'High'] for n in ['nitrogen', 'phosphorus', 'potassium']):
            self.overall_health = 'excellent'
        elif ph_analysis['status'] == 'good':
            self.overall_health = 'good'
        else:
            self.overall_health = 'fair'
        
        self.save()
