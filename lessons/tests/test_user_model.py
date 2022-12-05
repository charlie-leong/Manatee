from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import User

# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name = "John",
            last_name = "Doe",
            email = "johndoe@example.org",
            password = "Password123"
        )
    
    def _asser_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user should be valid")
    
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_valid_user(self):
        self._asser_user_is_valid()
    
    def test_invalid_user(self):
        self.user.email = "invalid_email"
        self._assert_user_is_invalid()
    
    def test_no_blank_email(self):
        self.user.email = ""
        self._assert_user_is_invalid()

    def test_unique_email(self):
        self.second_user = User.objects.create_user(
            first_name = "Jane",
            last_name = "Doe",
            email = "janedoe@example.org",
            password = "Password123"
        )
        self.user.email = self.second_user.email
        self._assert_user_is_invalid()
    
    def test_unique_username(self):
        self.second_user = User.objects.create_user(
            first_name = "Jane",
            last_name = "Doe",
            email = "janedoe@example.org",
            password = "Password123"
        )
        self.user.username = self.second_user.username
        self._assert_user_is_invalid()