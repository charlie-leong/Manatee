from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
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

DURATION_OPTIONS = (
    (30, '30'),
    (45, '45'),
    (60, '60'),
    (90, '90')
)

class Request(models.Model):
    availability =models.CharField(max_length=10, choices=AVAILABILITY, default='monday')
    number_of_lessons=models.PositiveIntegerField(default=1)
    interval = models.PositiveIntegerField()
    duration=models.PositiveIntegerField(choices=DURATION_OPTIONS, default=60)
    extra =models.CharField(max_length=10, blank=True)

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
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
    balance = 0
   
class Lesson(models.Model):
    assigned_student_id = models.CharField(max_length = 10)
    assigned_teacher_id = models.CharField(max_length = 10)
    number_of_lessons = models.PositiveIntegerField()
    week_interval = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    paid = False

    def togglePaid():
        if(paid == False):
            paid = False
            return paid
        paid = True
        return paid
    
    def calculateCost():
        baseCost = 20
        return baseCost * duration/60 * number_of_lessons

