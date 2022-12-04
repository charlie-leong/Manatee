from django.test import TestCase
from lessons.forms import LogInForm
from django import forms

class LogInFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            "username" : "@janedoe",
            "password" : "Password123"
        }
    
    # form has necessary fields
    def test_form_has_necessary_fields(self):
        form = LogInForm()
        self.assertIn("username", form.fields)
        self.assertIn("password", form.fields)
        pw_widget = form.fields["password"].widget
        self.assertTrue(isinstance(pw_widget, forms.PasswordInput))

    # form accepts valid input
    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form does not accept blank username
    def test_no_blank_username(self):
        self.form_input["username"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form does not accept blank password
    def test_no_blank_password(self):
        self.form_input["password"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form accepts incorrect username
    def test_form_accepts_incorrect_username(self):
        self.form_input["username"] = "bad_username"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form accepts incorrect password
    def test_form_accepts_incorrect_password(self):
        self.form_input["password"] = "nocaps123"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())