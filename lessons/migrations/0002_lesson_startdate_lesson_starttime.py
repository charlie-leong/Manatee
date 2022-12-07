# Generated by Django 4.1.3 on 2022-12-07 17:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='startDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='lesson',
            name='startTime',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
