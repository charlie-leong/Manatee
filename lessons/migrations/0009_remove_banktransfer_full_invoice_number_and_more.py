# Generated by Django 4.1.3 on 2022-12-12 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_alter_banktransfer_invoice_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banktransfer',
            name='full_invoice_number',
        ),
        migrations.AlterField(
            model_name='banktransfer',
            name='invoice_number',
            field=models.CharField(error_messages={'unique': 'Invoice numbers must be unique'}, max_length=8, unique=True),
        ),
    ]
