from django.test import TestCase
from lessons.models import User, Request
from django.urls import reverse
from lessons.tests.helpers import LogInTester

"""
delete request view has no template and is only an endpoint for the HTTP request
"""
class DeleteRequestTestCase(TestCase, LogInTester):
    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/default_request.json",
        "lessons/tests/fixtures/other_users.json",
        "lessons/tests/fixtures/other_requests.json"
    ]

    def setUp(self):
        self.requestToBeDeleted = Request.objects.get(id = 1)
        self.url = reverse("delete-request", args=[self.requestToBeDeleted.id])
        self.user = User.objects.get(username = "@johndoe")

    def test_delete_request_url(self):
        self.assertEqual(self.url, f"/delete-request/{self.requestToBeDeleted.id}")
    
    def test_successful_delete_request_from_logged_in_user(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        before = Request.objects.count()
        response = self.client.post(self.url, follow= True)
        self.assertEqual(response.status_code, 200)
        after = Request.objects.count()
        self.assertEqual(before - 1, after)
        with self.assertRaises(Request.DoesNotExist):
            Request.objects.get(id = self.requestToBeDeleted.id)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_unsuccessful_delete_request_from_not_logged_in_user(self):
        self.assertFalse(self._is_logged_in())
        before = Request.objects.count()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        after = Request.objects.count()
        self.assertEqual(before, after)


    def test_unauthorised_request_delete_from_logged_in_user(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        notCurrUserReq = Request.objects.get(id = 2)
        before = Request.objects.count()
        response = self.client.post(reverse("delete-request", args=[notCurrUserReq.id]))
        self.assertEqual(response.status_code, 403)
        after = Request.objects.count()
        self.assertEqual(before, after)
