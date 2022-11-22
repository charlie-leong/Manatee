from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
AVAILABILITY = (
    ('monday','MONDAY'),
    ('tuesday', 'TUESDAY'),
    ('wednesday','WEDNESDAY'),
    ('thursday','THURSDAY'),
    ('friday','FRIDAY'),
)

class Request(models.Model):
    availability =models.CharField(max_length=10, choices=AVAILABILITY, default='monday')
    numLessons=models.PositiveIntegerField()
    interval = models.PositiveIntegerField()
    duration=models.PositiveIntegerField()
    extra =models.CharField(max_length=10, blank=True)
