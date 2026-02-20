"""Management command to update weather data for all farms"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from monitor.models import Farm, WeatherRecord
from monitor.weather_service import WeatherService
from monitor.utils import check_and_create_alerts


class Command(BaseCommand):
    help = 'Update weather data for all farms with coordinates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if recently updated',
        )

    def handle(self, *args, **options):
        force = options['force']
        farms = Farm.objects.exclude(latitude__isnull=True, longitude__isnull=True)
        
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        for farm in farms:
            # Skip if updated in last 3 hours (unless forced)
            if not force and farm.last_weather_update:
                time_since_update = timezone.now() - farm.last_weather_update
                if time_since_update < timedelta(hours=3):
                    skipped_count += 1
                    continue
            
            self.stdout.write(f'Updating weather for {farm.name}...')
            
            try:
                weather_data = WeatherService.get_weather_data(
                    farm.latitude, 
                    farm.longitude
                )
                
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
                    alerts = check_and_create_alerts(farm)
                    if alerts:
                        self.stdout.write(
                            self.style.WARNING(
                                f'  Created {len(alerts)} alert(s) for {farm.name}'
                            )
                        )
                    
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Updated {farm.name}')
                    )
                else:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Failed to fetch data for {farm.name}')
                    )
            
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error updating {farm.name}: {str(e)}')
                )
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count} farms'))
        self.stdout.write(f'Skipped: {skipped_count} farms')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {error_count} farms'))
        self.stdout.write('='*50)
