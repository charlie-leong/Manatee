"""
Test cases for the Log in form.
"""
from django import forms
from django.test import TestCase

from lessons.forms import LogInForm

class LogInFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            "email" : "janedoe@exmaple.org",
            "password" : "Password123"
        }
    
    # form has necessary fields
    def test_form_has_necessary_fields(self):
        """ Form has necessary fields. """
        form = LogInForm()
        self.assertIn("email", form.fields)
        self.assertIn("password", form.fields)
        pw_widget = form.fields["password"].widget
        self.assertTrue(isinstance(pw_widget, forms.PasswordInput))

    # form accepts valid input
    def test_form_accepts_valid_input(self):
        """ Form accepts valid input. """
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form does not accept blank username
    def test_no_blank_username(self):
        """ Form doesn't accept blank email. """
        self.form_input["email"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form does not accept blank password
    def test_no_blank_password(self):
        """ Form doesn't accept blank password. """
        self.form_input["password"] = ""
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # form accepts incorrect username
    def test_form_accepts_incorrect_username(self):
        """ 
        Form accepts incorrect username (i.e. does not make obvious what the
        correct username format is.
        """
        self.form_input["username"] = "bad_username"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form accepts incorrect password
    def test_form_accepts_incorrect_password(self):
        """
        Form accepts incorrect password (i.e. does not make obvious what the
        correct password format is.
        """
        self.form_input["password"] = "nocaps123"
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())