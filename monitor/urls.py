from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='monitor/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('farms/', views.farm_list, name='farm_list'),
    path('farms/create/', views.farm_create, name='farm_create'),
    path('farms/<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('farms/<int:farm_id>/weather-update/', views.weather_update, name='weather_update'),
    
    path('farms/<int:farm_id>/crops/create/', views.crop_create, name='crop_create'),
    path('crops/<int:crop_id>/', views.crop_detail, name='crop_detail'),
    
    path('alerts/', views.alerts_list, name='alerts_list'),
    path('alerts/<int:alert_id>/mark-read/', views.alert_mark_read, name='alert_mark_read'),
    
    # Export and batch operations
    path('export/crops/', views.export_crops, name='export_crops'),
    path('export/weather/<int:farm_id>/', views.export_weather, name='export_weather'),
    path('batch/update-weather/', views.batch_update_weather, name='batch_update_weather'),
    path('batch/update-stages/', views.batch_update_crop_stages, name='batch_update_crop_stages'),
    
    # Statistics
    path('farms/<int:farm_id>/statistics/', views.farm_statistics, name='farm_statistics'),
    
    # Location-based weather
    path('weather/current-location/', views.current_location_weather, name='current_location_weather'),
    path('weather/search/', views.search_location_weather, name='search_location_weather'),
    
    # Soil measurements
    path('farms/<int:farm_id>/soil/create/', views.soil_measurement_create, name='soil_measurement_create'),
    path('soil/<int:measurement_id>/', views.soil_measurement_detail, name='soil_measurement_detail'),
    path('farms/<int:farm_id>/soil/', views.soil_measurements_list, name='soil_measurements_list'),
]
