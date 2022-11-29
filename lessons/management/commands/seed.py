from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User
from django.db.utils import IntegrityError

class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        # print("The seed command has not been implemented yet!")
        # print("TO DO: Create a seed command following the instructions of the assignment carefully.")
        self.createThreeUsers()
        for i in range(100):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = f'@{first_name.lower()}{last_name.lower()}'
            email = f'{first_name.lower()}.{last_name.lower()}@example.org'
            password = "Password123"
            try:
                User.objects.create_user(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password
                )
            except IntegrityError:
                continue

    
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
