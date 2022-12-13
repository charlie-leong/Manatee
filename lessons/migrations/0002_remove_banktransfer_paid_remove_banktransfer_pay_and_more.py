# Generated by Django 4.1.3 on 2022-12-12 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banktransfer',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='banktransfer',
            name='pay',
        ),
        migrations.RemoveField(
            model_name='banktransfer',
            name='user_ID',
        ),
        migrations.AddField(
            model_name='banktransfer',
            name='cost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='banktransfer',
            name='lesson',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banktransfer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='request',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]