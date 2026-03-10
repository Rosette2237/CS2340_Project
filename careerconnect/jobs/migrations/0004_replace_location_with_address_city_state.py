from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_job_location_lat_alter_job_location_long'),
    ]

    operations = [
        # Remove the old single text location field
        migrations.RemoveField(
            model_name='job',
            name='location',
        ),
        # Add structured address fields
        migrations.AddField(
            model_name='job',
            name='address',
            field=models.CharField(blank=True, max_length=300, help_text='Street address (optional)'),
        ),
        migrations.AddField(
            model_name='job',
            name='city',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='state',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        # Make lat/long optional (auto-populated via geocoding)
        migrations.AlterField(
            model_name='job',
            name='location_lat',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location_long',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True),
        ),
    ]
