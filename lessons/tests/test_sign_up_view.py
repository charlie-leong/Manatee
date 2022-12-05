from django.test import TestCase
from lessons.forms import SignUpForm
from django.urls import reverse
from lessons.models import User
from django.contrib.auth.hashers import check_password
from .helpers import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse("sign_up")
        self.form_input = {
            "username": "@janedoe",
            "first_name" : "Jane",
            "last_name" : "Doe",
            "email" : "janedoe@example.org",
            "new_password" : "Password123",
            "password_confirmation" : "Password123",
        }

    # test that url is correct
    def test_sign_up_url(self):
        self.assertEqual(self.url, "/sign_up/")
    
    # test that a get request to signup returns 200
    def test_get_sign_up_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sign_up.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    # test for an unsuccessful signup (bad data)
    def test_unsuccessful_sign_up(self):
        before = User.objects.count()
        self.form_input["email"] = ""
        response = self.client.post(self.url, self.form_input)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sign_up.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)

    # test for successful signup
    def test_successful_sign_up(self):
        before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after = User.objects.count()
        self.assertEqual(after, before + 1)
        response_url = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "dashboard.html")
        user = User.objects.get(email = "janedoe@example.org")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(check_password("Password123", user.password))
        self.assertTrue(self._is_logged_in())
