"""
This is the seeder for the application. It should generate a predetermined
student, admin and superuser. It will then generate around 100 additional
students, around 70 requests, and around 60 lessons (fulfilled requests).
"""
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker

from datetime import date, timedelta, time
import random

from lessons.models import BankTransfer, User, Request, Lesson, AVAILABILITY, DURATIONS, NUM_LESSONS, LESSON_INTERVAL

class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        """ Runs database seeding. """
        self.create_superuser()
        self.create_admin()
        self.create_regular_user()
        self.generate_students()
        self.generate_requests()
        self.generate_lessons()
        self.generate_bank_transfers()

    def generate_students(self):
        """ Generates around 100 students. """
        for i in range(100):
            print(f'Seeding user {i}',  end='\r')
            try:
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                username = f'@{first_name.lower()}{last_name.lower()}'
                email = f'{first_name.lower()}.{last_name.lower()}@example.org'
                password = "Password123"
                User.objects.create_user(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password,
                    balance = random.randint(10, 500)
                )
            # if a duplicate name combo is used, do not create user
            except IntegrityError:
                continue
        print("Students complete")
    
    def generate_requests(self):
        """ Generates around 70 requests. """
        pks = User.objects.filter(is_staff = False).values_list("pk", flat=True)
        for i in range(75):
            print(f'Seeding request {i}',  end='\r')
            random_pk = random.choice(pks)
            user = User.objects.get(pk = random_pk)
            Request.objects.create(
                user = user, 
                availability = random.choice(AVAILABILITY)[0],
                number_of_lessons = random.choice(NUM_LESSONS)[0],
                interval = random.choice(LESSON_INTERVAL)[0],
                duration = random.choice(DURATIONS)[0],
            )
        print("Requests complete")

    def generate_lessons(self):
        """ Generates around 60 lessons. """
        for i in range(60):
            pks = Request.objects.filter(is_approved = False).values_list("pk", flat = True)
            random_pk = random.choice(pks)
            request = Request.objects.get(pk = random_pk)
            print(f'Seeding lesson {i}',  end='\r')
            try:
                Lesson.objects.create(
                    request = request,
                    teacher = f'Mr {self.faker.last_name()}',
                    startDate = self.generate_random_date(),
                    startTime = self.generate_random_time()
                )
            # if a request already has a lesson, do not create another lesson
            except IntegrityError:
                continue
        print("Lessons complete")
    
    def generate_bank_transfers(self):
        """Generates around 40 bank transfers (paid lessons)."""
        for i in range(40):
            pks = Lesson.objects.filter(paid = False).values_list("pk", flat = True)
            random_pk = random.choice(pks)
            lesson = Lesson.objects.get(pk = random_pk)
            print(f'Seeding bank transfer {i}',  end='\r')
            try:
                lesson.pay_lesson(random.randint(0, 999))
            except:
                continue
        print("Bank transfers complete")

    def generate_random_date(self):
        """ Generates random date. """
        random_month = random.randrange(9, 13)
        random_day = random.randrange(1, 29)
        return date(2022, random_month, random_day)

    def generate_random_time(self):
        """ Generates random time. """
        random_hour = random.randrange(9, 16)
        random_minute = random.choice([0, 30])
        return time(random_hour, random_minute, 0)

    def create_superuser(self):
        """ Creates pre-determined superuser. """
        try:
            User.objects.create_superuser(
                "@martymajor",
                first_name = "Marty",
                last_name = "Major",
                email = "marty.major@example.org",
                password = "Password123"
            )
        except IntegrityError:
            pass
    
    def create_admin(self):
        """ Creates pre-determined admin. """
        try:
            User.objects.create_user(
                "@petrapickles",
                first_name = "Petra",
                last_name = "Pickles",
                email = "petra.pickles@example.org",
                password = "Password123",
                is_staff = True
            )
        except IntegrityError:
            pass
    
    def create_regular_user(self):
        """ Creates a pre-determined student with a request and lesson. """
        try:
            user = User.objects.create_user(
                "@johndoe",
                first_name = "John",
                last_name = "Doe",
                email = "john.doe@example.org",
                password = "Password123"
            )

            request = Request.objects.create(
                user = user,
                availability = "THURSDAY",
                number_of_lessons = 3,
                interval = 1,
                duration = 45
            )

            lesson = Lesson.objects.create(
                request = request,
                teacher = "Mr Keppens",
                startDate = date(2022, 9, 3),
                startTime = time(11, 30, 0)
            )

            lesson.pay_lesson(random.randint(0, 999))
        except IntegrityError:
            pass