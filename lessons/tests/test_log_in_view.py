from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm

class LogInViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse("log_in")

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