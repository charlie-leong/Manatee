"""
Test cases for log in view.
"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse

from lessons.forms import LogInForm
from lessons.models import User
from lessons.tests.helpers import LogInTester, reverse_with_next


class LogInViewTestCase(TestCase, LogInTester):

    fixtures = ["lessons/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse("log_in")
        self.user = User.objects.get(username = "@johndoe")

    # test that url is correct
    def test_log_in_url(self):
        self.assertEqual(self.url, "/log_in/")

    # test that a get request to login returns 200
    def test_get_log_in_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        next_url = response.context["next"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next_url)
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 0)
    
    # test that a get request that is redirected to login then redirects correctly
    def test_get_log_in_after_redirect(self):
        destination_url = reverse("dashboard")
        self.url = reverse_with_next("log_in", destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        next = response.context["next"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 0)

    # test unsuccessful login
    def test_unsuccessful_log_in(self):
        form_input = {
            "email" : self.user.email,
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
            'email': self.user.email, 
            'password': 'Password123'
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)
    
    # test successful login with redirect
    def test_succesful_log_in_with_redirect(self):
        redirect_url = reverse("dashboard")
        form_input = {
            'email': self.user.email, 
            'password': 'Password123',
            "next_url" : redirect_url
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)

    # test correct redirect after successful login
    def test_correct_redirect_after_successful_login(self):
        form_input = {
            "email" : self.user.email,
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
            "email" : self.user.email,
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

    def test_post_log_in_with_incorrect_credentials_and_redirect(self):
        redirect_url = reverse('dashboard')
        form_input = { 'email': 'johndoe@example.org', 'password': 'WrongPassword123', 'next': redirect_url }
        response = self.client.post(self.url, form_input)
        next = response.context['next']
        self.assertEqual(next, redirect_url)

    # test get log in redirects to dashboard if user is already logged in
    def test_get_log_in_redirects_to_dashboard_if_user_is_logged_in(self):
        redirect_url = reverse("dashboard")
        self.client.login(email = self.user.email, password = "Password123")
        response = self.client.get(self.url, follow = True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)  
        self.assertTemplateUsed(response, "dashboard.html")

    # test post log in redirects to dashboard if user is already logged in
    def test_post_log_in_redirects_to_dashboard_if_user_is_logged_in(self):
        redirect_url = reverse("dashboard")
        form_input = {
            "email" : self.user.email,
            "password" : "WrongPassword123"
        }
        self.client.login(email = self.user.email, password = "Password123")
        response = self.client.post(self.url, form_input, follow = True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)  
        self.assertTemplateUsed(response, "dashboard.html")