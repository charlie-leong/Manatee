from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User

# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "@johndoe",
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