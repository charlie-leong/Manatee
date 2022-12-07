from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from django.db.utils import IntegrityError

import random
from datetime import date, timedelta, time

from lessons.models import User, Request, Lesson, AVAILABILITY, DURATIONS, NUM_LESSONS, LESSON_INTERVAL

class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        # print("The seed command has not been implemented yet!")
        # print("TO DO: Create a seed command following the instructions of the assignment carefully.")
        self.create_superuser()
        self.create_admin()
        self.create_regular_user()
        self.generate_students()
        self.generate_requests()
        self.generate_lessons()

    def generate_students(self):
        for i in range(100):
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
                    password = password
                )
            except IntegrityError:
                continue
    
    def generate_requests(self):
        pks = User.objects.values_list("pk", flat=True)
        for i in range(75):
            random_pk = random.choice(pks)
            user = User.objects.get(pk = random_pk)
            Request.objects.create(
                user = user, 
                availability = random.choice(AVAILABILITY)[0],
                number_of_lessons = random.choice(NUM_LESSONS)[0],
                interval = random.choice(LESSON_INTERVAL)[0],
                duration = random.choice(DURATIONS)[0]
            )
    
    def generate_lessons(self):
        pks = Request.objects.values_list("pk", flat = True)
        for i in range(60):
            random_pk = random.choice(pks)
            request = Request.objects.get(pk = random_pk)
            try:
                Lesson.objects.create(
                    request = request,
                    teacher = f'Mr {self.faker.last_name()}',
                    startDate = self.generate_random_date(),
                    startTime = self.generate_random_time()
                )
            except IntegrityError:
                continue

    def generate_random_date(self):
        random_month = random.randrange(9, 13)
        random_day = random.randrange(1, 29)
        return date(2022, random_month, random_day)

    def generate_random_time(self):
        random_hour = random.randrange(9, 16)
        random_minute = random.choice([0, 30])
        return time(random_hour, random_minute, 0)

    def create_superuser(self):
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
        try:
            User.objects.create_user(
                "@johndoe",
                first_name = "John",
                last_name = "Doe",
                email = "john.doe@example.org",
                password = "Password123"
            )
        except IntegrityError:
            pass

    def createThreeUsers(self):
        if not User.objects.filter(username = "@johndoe").exists():
            User.objects.create_user(
                "@johndoe",
                first_name = "John",
                last_name = "Doe",
                email = "john.doe@example.org",
                password = "Password123"
            )
        
        if not User.objects.filter(username = "@petrapickles").exists():
            User.objects.create_user(
                "@petrapickles",
                first_name = "Petra",
                last_name = "Pickles",
                email = "petra.pickles@example.org",
                password = "Password123",
                is_staff = True
            )

        if not User.objects.filter(username = "@martymajor").exists():
            User.objects.create_superuser(
                "@martymajor",
                first_name = "Marty",
                last_name = "Major",
                email = "marty.major@example.org",
                password = "Password123"
            )
