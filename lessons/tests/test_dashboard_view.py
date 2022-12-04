from re import T
from django.test import TestCase
from django.urls import reverse
from .helpers import reverse_with_next, LogInTester
from lessons.models import User

class DashboardViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse("dashboard")
        self.user = User.objects.create_user(
            "@johndoe",
            first_name = "John",
            last_name = "Doe",
            email = "johndoe@example.org",
            password = "Password123"
        )

    # test that the url is correct
    def test_dashboard_view_has_correct_url(self):
        self.assertEqual(self.url, "/dashboard/")

    # test when a user is not logged in, they are redirected to the log in page
    def test_not_logged_in_user_redirects_to_log_in_page(self):
        redirect_url = reverse_with_next("log_in", self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # test get dashboard view
    def test_get_dashboard_view(self):
        self.client.login(username="@johndoe", password="Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")