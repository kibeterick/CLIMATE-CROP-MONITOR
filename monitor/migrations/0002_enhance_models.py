# Generated migration for enhanced models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='last_weather_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='farm',
            index=models.Index(fields=['farmer', 'name'], name='monitor_far_farmer__idx'),
        ),
        migrations.AlterField(
            model_name='farm',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AddIndex(
            model_name='crop',
            index=models.Index(fields=['farm', 'is_active'], name='monitor_cro_farm_id_idx'),
        ),
        migrations.AddIndex(
            model_name='crop',
            index=models.Index(fields=['crop_type', 'current_stage'], name='monitor_cro_crop_ty_idx'),
        ),
        migrations.AlterModelOptions(
            name='crop',
            options={'ordering': ['-planting_date']},
        ),
        migrations.AlterModelOptions(
            name='farm',
            options={'ordering': ['-created_at']},
        ),
    ]
