from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Request(models.Model):
    availability =models.CharField(max_length=10)
    numLessons=models.PositiveIntegerField()
    interval = models.PositiveIntegerField()
    duration=models.PositiveIntegerField()
    extra =models.CharField(max_length=10)
