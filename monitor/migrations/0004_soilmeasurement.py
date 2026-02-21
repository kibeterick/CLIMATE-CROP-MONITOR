# Generated migration for SoilMeasurement model

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_rename_monitor_cro_farm_id_idx_monitor_cro_farm_id_f3056d_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoilMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_date', models.DateField(default=django.utils.timezone.now)),
                ('ph_level', models.DecimalField(decimal_places=1, help_text='Soil pH (0-14)', max_digits=3)),
                ('nitrogen', models.DecimalField(decimal_places=2, help_text='Nitrogen level (ppm)', max_digits=5)),
                ('phosphorus', models.DecimalField(decimal_places=2, help_text='Phosphorus level (ppm)', max_digits=5)),
                ('potassium', models.DecimalField(decimal_places=2, help_text='Potassium level (ppm)', max_digits=5)),
                ('organic_matter', models.DecimalField(blank=True, decimal_places=2, help_text='Organic matter (%)', max_digits=5, null=True)),
                ('moisture', models.DecimalField(blank=True, decimal_places=2, help_text='Soil moisture (%)', max_digits=5, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, help_text='Soil temperature (°C)', max_digits=5, null=True)),
                ('ph_status', models.CharField(blank=True, max_length=50)),
                ('nutrient_status', models.CharField(blank=True, max_length=50)),
                ('overall_health', models.CharField(choices=[('poor', 'Poor'), ('fair', 'Fair'), ('good', 'Good'), ('excellent', 'Excellent')], default='fair', max_length=20)),
                ('recommendations', models.TextField(blank=True, help_text='Soil improvement recommendations')),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soil_measurements', to='monitor.farm')),
            ],
            options={
                'ordering': ['-measurement_date'],
                'indexes': [
                    models.Index(fields=['farm', 'measurement_date'], name='monitor_soi_farm_id_f3056d_idx'),
                ],
            },
        ),
    ]
