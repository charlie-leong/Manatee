# Generated by Django 4.1.3 on 2022-12-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_alter_banktransfer_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransfer',
            name='invoice_number',
            field=models.CharField(error_messages={'unique': 'Invoice numbers must be unique'}, max_length=3, unique=True),
        ),
    ]
