
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Request(models.Model):
    availability =models.TextField()
    numLessons=models.TextField()
    interval = models.TextField()
    duration=models.TextField()
    extra =models.TextField()

    
