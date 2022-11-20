from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm
from lessons.models import User

class LogInViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse("log_in")
        User.objects.create_user(
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

    # test successful login
    def test_successful_log_in(self):
        form_input = {
            "username" : "@johndoe",
            "password" : "Password123"
        }
        response = self.client.post(self.url, form_input)
        self.assertTrue(self._is_logged_in())

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

    def _is_logged_in(self):
        return "_auth_user_id" in self.client.session.keys()