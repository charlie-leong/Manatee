"""
Test cases for the user model.
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import User

# Create your tests here.
class UserModelTestCase(TestCase):

    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/other_users.json"
        ]

    def setUp(self):
        self.user = User.objects.get(username = "@johndoe")
    
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user should be valid")
    
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_valid_user(self):
        self._assert_user_is_valid()
    
    def test_invalid_user(self):
        self.user.username = "invalid_username"
        self._assert_user_is_invalid()
    
    def test_no_blank_username(self):
        self.user.username = ""
        self._assert_user_is_invalid()

    def test_unique_username(self):
        self.second_user = User.objects.get(username = "@janedoe")
        self.user.username = self.second_user.username
        self._assert_user_is_invalid()
    
    # test that subtracting a value larger than the balance is not allowed
    def test_subtracting_amount_bigger_than_balance(self):
        with self.assertRaises(ValueError):
            self.user.adjust_balance(-101.01)
    
    def test_subtract_from_balance(self):
        self.user.adjust_balance(10.1)
        self.assertEqual(self.user.balance, 110.1)