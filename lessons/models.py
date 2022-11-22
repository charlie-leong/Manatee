from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

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
   
class Request(models.Model):
    availability =models.CharField(max_length=10)
    numLessons=models.CharField(max_length=10)
    interval = models.CharField(max_length=10)
    duration=models.CharField(max_length=10)
    extra =models.CharField(max_length=10)