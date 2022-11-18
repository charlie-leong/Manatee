"""Unit tests of the sign up form."""
from django.test import TestCase
from lessons.forms import SignUpForm
from lessons.models import User

class SignUpFormTestCase(TestCase):

    def test_valid_form(self):
        form_input = {
            "first_name" : "Jane",
            "last_name" : "Doe",
            "username" : "@janedoe",
            "email" : "janedoe@example.org",
            "new_password" : "Password123",
            "password_confirmation" : "Password123",
        }
        form = SignUpForm(data=form_input)
        self.assertTrue(form.is_valid())
