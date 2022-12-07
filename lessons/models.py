from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    availability =models.CharField(max_length=10, choices=AVAILABILITY, default='monday')
    number_of_lessons=models.PositiveIntegerField(choices= NUM_LESSONS, default=1)
    interval = models.PositiveIntegerField(validators=[MinValueValidator(2, "Cannot request lessons for a period shorter than 2 days."), MaxValueValidator(14, "Cannot request lessons for a period longer than 14 days.")])  # whats the minimum? whats the maximum?
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
