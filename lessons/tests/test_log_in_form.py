from django.test import TestCase
from lessons.forms import LogInForm
from django import forms

class LogInFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            "email" : "janedoe@example.org",
            "password" : "Password123"
        }
    
    # form has necessary fields
    def test_form_has_necessary_fields(self):
        form = LogInForm()
        self.assertIn("email", form.fields)
        self.assertIn("password", form.fields)
        pw_widget = form.fields["password"].widget
        self.assertTrue(isinstance(pw_widget, forms.PasswordInput))

    # form accepts valid input
    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form does not accept blank email
    def test_no_blank_email(self):
        self.form_input["email"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form does not accept blank password
    def test_no_blank_password(self):
        self.form_input["password"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form accepts incorrect email
    def test_form_accepts_incorrect_email(self):
        self.form_input["email"] = "bad_email"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form accepts incorrect password
    def test_form_accepts_incorrect_password(self):
        self.form_input["password"] = "nocaps123"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())