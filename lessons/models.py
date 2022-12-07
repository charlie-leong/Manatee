from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
AVAILABILITY = [
    ('MONDAY','Monday'),
    ('TUESDAY', 'Tuesday'),
    ('WEDNESDAY','Wednesday'),
    ('THURSDAY','Thursday'),
    ('FRIDAY','Friday'),
]
NUM_LESSONS = [
    (1, "1 lesson"), (2, "2 lessons"), (3, "3 lessons"), (4, "4 lessons")
]
LESSON_INTERVAL = [
    (1, "Every week"),
    (2, "Every 2 weeks")
]
DURATIONS = [
    (30, "30 minutes"), (45, "45 minutes"), (60, "1 hour")
]

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(
        max_length=30,
        unique=True,
        validators = [RegexValidator(
            regex= r'^@\w{3,}$',
            message = "Username must consist of  an '@' and a minimum of 3 alphanumericals!"
        )])
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)

class Request(models.Model):
    availability =models.CharField(max_length=10, choices=AVAILABILITY, default='MONDAY')
    number_of_lessons=models.PositiveIntegerField(choices= NUM_LESSONS, default=1)
    interval = models.PositiveIntegerField(choices=LESSON_INTERVAL, default=1)
    duration=models.PositiveIntegerField(choices= DURATIONS, verbose_name="Duration (mins)", default= 30)
    extra_info =models.CharField(max_length=100, verbose_name="Extra information", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default= False)

    def set_approved_to_false(self):
        self.is_approved = False
        self.save()

    def set_approved_to_true(self):
        self.is_approved = True
        self.save()

class Lesson(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
    teacher = models.CharField(max_length = 30)
    startDate = models.DateField(default=timezone.now)
    startTime = models.TimeField(default=timezone.now)
    paid = models.BooleanField(default=False)

    def calculateCost(self):
        baseCost = 20
        return baseCost * self.request.duration/60 * self.request.number_of_lessons
    
    def __str__(self):
        return f'This lesson is taught by {self.teacher}'
    
    def save(self, *args, **kwargs):
        self.request.set_approved_to_true()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.request.set_approved_to_false()
        super().delete(*args, **kwargs)

class BankTransfer(models.Model):
    user_ID=models.CharField(max_length=4)
    invoice_number=models.CharField(max_length=3)
    full_invoice_number = models.CharField(max_length=8)
    pay = models.PositiveIntegerField()
    paid = models.BooleanField()

    balance = 0
