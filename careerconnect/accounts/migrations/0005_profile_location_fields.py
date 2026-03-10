from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_is_recruiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='location_lat',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='location_long',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
