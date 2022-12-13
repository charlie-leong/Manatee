# Generated by Django 4.1.3 on 2022-12-13 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_remove_banktransfer_full_invoice_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransfer',
            name='invoice_number',
            field=models.CharField(error_messages={'unique': 'Invoice numbers must be unique'}, max_length=10, unique=True),
        ),
    ]
