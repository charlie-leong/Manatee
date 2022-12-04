from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm
from lessons.models import User
from lessons.tests.helpers import LogInTester
from django.contrib import messages

class LogInViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse("log_in")
        self.user = User.objects.create_user(
            "@johndoe",
            first_name = "John",
            last_name = "Doe",
            email = "johndoe@example.org",
            password = "Password123"
        )

    # test that url is correct
    def test_log_in_url(self):
        self.assertEqual(self.url, "/log_in/")

    # test that a get request to signup returns 200
    def test_get_log_in_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 0)

    # test unsuccessful login
    def test_unsuccessful_log_in(self):
        form_input = {
            "username" : "@johndoe",
            "password" : "Wrongpassword123"
        }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 1)
        self.assertEqual(response_messages[0].level, messages.ERROR)

    # test successful login
    def test_succesful_log_in(self):
        form_input = {
            'username': '@johndoe', 
            'password': 'Password123'
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)

    # test correct redirect after successful login
    def test_correct_redirect_after_successful_login(self):
        form_input = {
            "username" : "@johndoe",
            "password" : "Password123"
        }
        response = self.client.post(self.url, form_input, follow = True)
        response_url = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "dashboard.html")
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)

    # test successful login by inactive user
    def test_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {
            "username" : "@johndoe",
            "password" : "Password123"
        }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 1)
        self.assertEqual(response_messages[0].level, messages.ERROR)