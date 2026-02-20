from django.contrib import admin
from .models import Farmer, Farm, Crop, WeatherRecord, YieldPrediction, Alert


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['user', 'county', 'phone_number', 'created_at']
    search_fields = ['user__username', 'user__email', 'county']


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'location', 'size_acres', 'created_at']
    search_fields = ['name', 'location', 'farmer__user__username']
    list_filter = ['created_at']


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'farm', 'planting_date', 'current_stage', 'is_active']
    search_fields = ['crop_type', 'variety', 'farm__name']
    list_filter = ['crop_type', 'current_stage', 'is_active', 'planting_date']


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ['farm', 'date', 'temperature', 'humidity', 'rainfall']
    search_fields = ['farm__name']
    list_filter = ['date']


@admin.register(YieldPrediction)
class YieldPredictionAdmin(admin.ModelAdmin):
    list_display = ['crop', 'predicted_yield', 'actual_yield', 'prediction_date']
    search_fields = ['crop__crop_type', 'crop__farm__name']
    list_filter = ['prediction_date']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'farm', 'alert_type', 'severity', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'farm__name']
    list_filter = ['alert_type', 'severity', 'is_read', 'created_at']
