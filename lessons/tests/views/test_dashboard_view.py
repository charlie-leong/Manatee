"""
Test cases for the dashboard view.
"""
from django.test import TestCase
from django.urls import reverse

from lessons.models import User
from lessons.tests.helpers import LogInTester, reverse_with_next

class DashboardViewTestCase(TestCase, LogInTester):

    fixtures = [
        "lessons/tests/fixtures/default_user.json"
    ]

    def setUp(self):
        self.url = reverse("dashboard")
        self.user = User.objects.get(username = "@johndoe")

    # test that the url is correct
    def test_dashboard_view_has_correct_url(self):
        self.assertEqual(self.url, "/dashboard/")

    # test when a user is not logged in, they are redirected to the log in page
    def test_not_logged_in_user_redirects_to_log_in_page(self):
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # test get dashboard view
    def tests_get_dashboard_view(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")