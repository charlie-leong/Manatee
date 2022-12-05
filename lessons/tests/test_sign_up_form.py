"""Unit tests of the sign up form."""
from django.test import TestCase
from lessons.forms import SignUpForm
from lessons.models import User
from django import forms
from django.contrib.auth.hashers import check_password

class SignUpFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            "first_name" : "Jane",
            "last_name" : "Doe",
            "email" : "janedoe@example.org",
            "new_password" : "Password123",
            "password_confirmation" : "Password123",
        }

    def test_valid_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    #form has necessary fields
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("new_password", form.fields)
        pw_field_widget = form.fields["new_password"].widget
        self.assertTrue(isinstance(pw_field_widget, forms.PasswordInput))
        self.assertIn("password_confirmation", form.fields)
        pc_field_widget = form.fields["password_confirmation"].widget
        self.assertTrue(isinstance(pc_field_widget, forms.PasswordInput))

    #form uses model validation
    def test_form_uses_user_validation(self):
        self.form_input["email"] = "janedoe@example.org"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #new password is correct format
    def test_password_has_uppercase_char(self):
        self.form_input["new_password"] = "password123"
        self.form_input["password_confirmation"] = "password123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_has_lowercase_char(self):
        self.form_input["new_password"] = "PASSWORD123"
        self.form_input["password_confirmation"] = "PASSWORD123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_has_number(self):
        self.form_input["new_password"] = "Password"
        self.form_input["password_confirmation"] = "Password"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #passwords are identical
    def test_form_passwords_are_identical(self):
        self.form_input["new_password"] = "Wrongpassword123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # test that form saves correctly
    def test_form_saves_correctly(self):
        form = SignUpForm(data = self.form_input)
        before = User.objects.count()
        form.save()
        after = User.objects.count()
        self.assertEqual(after, before + 1)
        user = User.objects.get(email = "janedoe@example.org")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(check_password("Password123", user.password))