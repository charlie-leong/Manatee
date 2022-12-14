"""
Test cases for the transaction view.
"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from ..helpers import LogInTester


class TransactionViewTestCase(TestCase, LogInTester):

    fixtures = [
        "lessons/tests/fixtures/default_user.json"
    ]

    def setUp(self):
        self.url = reverse("transfer-display")
        self.user = User.objects.get(username = "@johndoe")

    # test that the url is correct
    def test_transaction_view_has_correct_url(self):
        self.assertEqual(self.url, "/transfer-display/")

    # testing the transaction view page.
    def test_transaction_view(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transfer-display.html")


        


    