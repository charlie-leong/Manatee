from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
AVAILABILITY = (
    ('monday','MONDAY'),
    ('tuesday', 'TUESDAY'),
    ('wednesday','WEDNESDAY'),
    ('thursday','THURSDAY'),
    ('friday','FRIDAY'),
)

DURATIONS = ((30, 30), (45, 45), (60, 60))
NUM_LESSONS = ((1, 1), (2, 2), (3, 3), (4, 4))      # assuming that a request will request 4 lessons at most

class Request(models.Model):
    availability =models.CharField(max_length=10, choices=AVAILABILITY, default='monday')
    # number_of_lessons=models.PositiveIntegerField(default=1)
    number_of_lessons=models.PositiveIntegerField(choices= NUM_LESSONS, default=1)
    interval = models.PositiveIntegerField(validators=[MinValueValidator(2, "Cannot request lessons for a period shorter than 2 days."), MaxValueValidator(14, "Cannot request lessons for a period longer than 14 days.")])  # whats the minimum? whats the maximum?
    duration=models.PositiveIntegerField(choices= DURATIONS, verbose_name="Duration (mins)", default= 30)
    extra_info =models.CharField(max_length=100, verbose_name="Extra information", blank=True)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default= False)

class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators = [RegexValidator(
            regex= r'^@\w{3,}$',
            message = "username must consist of @ and min 3 alphanumericals"
        )])
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
   
