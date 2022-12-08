from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

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
    number_of_lessons=models.PositiveIntegerField(choices= NUM_LESSONS, default=1)
    interval = models.PositiveIntegerField(validators=[MinValueValidator(2, "Cannot request lessons for a period shorter than 2 days."), MaxValueValidator(14, "Cannot request lessons for a period longer than 14 days.")])  # whats the minimum? whats the maximum?
    duration=models.PositiveIntegerField(choices= DURATIONS, verbose_name="Duration (mins)", default= 30)
    extra_info =models.CharField(max_length=100, verbose_name="Extra information", blank=True)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default= False)


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    # username = models.CharField(
    #     max_length=30,
    #     unique=True,
    #     validators = [RegexValidator(
    #         regex= r'^@\w{3,}$',
    #         message = "Username must consist of  an '@' and a minimum of 3 alphanumericals!"
    #     )])
    username = None
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)  # check if need to edit
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
   
class BankTransfer(models.Model):
    user_ID=models.CharField(max_length=4)
    invoice_number=models.CharField(max_length=3)
    full_invoice_number = models.CharField(max_length=8)
    pay = models.PositiveIntegerField()
    paid = models.BooleanField()
    balance = 0
   
class Lesson(models.Model):
    assigned_student_id = models.CharField(max_length = 10)
    assigned_teacher_id = models.CharField(max_length = 10)
    number_of_lessons = models.PositiveIntegerField(default=1)
    week_interval = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField(default=60)
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


# basically defining model manager for no username 
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, first_name, last_name):  # check if add id field
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    ## Here goes the model definition from before. ##

    objects = UserManager() ## This is the new line in the User model. ##

