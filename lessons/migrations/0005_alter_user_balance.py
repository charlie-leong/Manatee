# Generated by Django 4.1.3 on 2022-12-12 19:53

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_alter_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
