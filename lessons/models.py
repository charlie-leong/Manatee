from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Request(models.Model):
    availability =models.CharField(max_length=10)
    numLessons=models.CharField(max_length=10)
    interval = models.CharField(max_length=10)
    duration=models.CharField(max_length=10)
    extra =models.CharField(max_length=10)

    
