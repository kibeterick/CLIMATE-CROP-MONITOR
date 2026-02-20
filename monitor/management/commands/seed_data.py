from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from monitor.models import Farmer, Farm, Crop, WeatherRecord, Alert
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create test user
        user, created = User.objects.get_or_create(
            username='testfarmer',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'Farmer'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: testfarmer'))

        # Create farmer profile
        farmer, created = Farmer.objects.get_or_create(
            user=user,
            defaults={
                'county': 'Kiambu',
                'phone_number': '+254712345678'
            }
        )

        # Create farms
        farm1, created = Farm.objects.get_or_create(
            farmer=farmer,
            name='Green Valley Farm',
            defaults={
                'location': 'Kiambu',
                'latitude': Decimal('-1.1743'),
                'longitude': Decimal('36.9366'),
                'size_acres': Decimal('10.5'),
                'soil_type': 'Loam'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created farm: {farm1.name}'))

        farm2, created = Farm.objects.get_or_create(
            farmer=farmer,
            name='Sunrise Farm',
            defaults={
                'location': 'Nakuru',
                'latitude': Decimal('-0.3031'),
                'longitude': Decimal('36.0800'),
                'size_acres': Decimal('15.0'),
                'soil_type': 'Clay'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created farm: {farm2.name}'))

        # Create crops
        today = date.today()
        
        crop1, created = Crop.objects.get_or_create(
            farm=farm1,
            crop_type='maize',
            planting_date=today - timedelta(days=45),
            defaults={
                'variety': 'H614',
                'area_planted': Decimal('5.0'),
                'current_stage': 'vegetative'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created crop: Maize'))

        crop2, created = Crop.objects.get_or_create(
            farm=farm1,
            crop_type='beans',
            planting_date=today - timedelta(days=30),
            defaults={
                'variety': 'KAT B1',
                'area_planted': Decimal('3.0'),
                'current_stage': 'vegetative'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created crop: Beans'))

        crop3, created = Crop.objects.get_or_create(
            farm=farm2,
            crop_type='wheat',
            planting_date=today - timedelta(days=60),
            defaults={
                'variety': 'Kenya Fahari',
                'area_planted': Decimal('8.0'),
                'current_stage': 'flowering'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created crop: Wheat'))

        # Create weather records
        for i in range(7):
            record_date = today - timedelta(days=i)
            WeatherRecord.objects.get_or_create(
                farm=farm1,
                date=record_date,
                defaults={
                    'temperature': Decimal('22.5') + Decimal(str(i * 0.5)),
                    'humidity': Decimal('65.0') + Decimal(str(i * 2)),
                    'rainfall': Decimal('2.5') if i % 2 == 0 else Decimal('0'),
                    'wind_speed': Decimal('3.2'),
                    'description': 'Partly cloudy'
                }
            )

        self.stdout.write(self.style.SUCCESS('Created weather records'))

        # Create alerts
        Alert.objects.get_or_create(
            farm=farm1,
            alert_type='weather',
            severity='medium',
            title='Moderate Temperature',
            defaults={
                'message': 'Temperature is within optimal range for maize growth.',
                'is_read': False
            }
        )

        Alert.objects.get_or_create(
            farm=farm2,
            alert_type='irrigation',
            severity='high',
            title='Low Rainfall Alert',
            defaults={
                'message': 'No significant rainfall in the past 5 days. Consider irrigation.',
                'is_read': False
            }
        )

        self.stdout.write(self.style.SUCCESS('Created alerts'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
        self.stdout.write(self.style.WARNING('Test credentials: username=testfarmer, password=testpass123'))
