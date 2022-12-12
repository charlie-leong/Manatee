from django.test import TestCase
from lessons.forms import RequestForm
from lessons.models import User, Request
from django.urls import reverse
from django.contrib import messages
from lessons.tests.helpers import LogInTester

class EditRequestTestCase(TestCase, LogInTester):
    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/default_request.json",
        "lessons/tests/fixtures/other_users.json",
        "lessons/tests/fixtures/other_requests.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username = "@johndoe")
        self.otherUser = User.objects.get(username = "@janedoe")
        self.request = Request.objects.get(user = self.user)
        self.url = reverse("edit-request", args=[self.request.id])
        self.editedFormInput = {
            "availability": "WEDNESDAY",
            "number_of_lessons": 1,
            "interval": 1,
            "duration": 30,
            "extra_info": "I would like to learn the gandalf sax instrument."
        }

    def test_edit_request_url(self):
        self.assertEqual(self.url, f"/edit-request/{self.request.id}")
    
    def test_get_edit_request_view(self):
        self.client.login(username = self.user.username, password = "Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit-request.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, RequestForm))
        self.assertFalse(form.is_bound)     # form is not bound even when pre-populated with object data
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 0)
    
    def test_successful_edit_request_from_logged_in_user(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.editedFormInput, follow= True)
        self.assertEqual(response.status_code, 200)
        updatedLessonRequest = Request.objects.get(user = self.user)
        self.assertEqual(updatedLessonRequest.user.username, self.user.username)
        self.assertEqual(updatedLessonRequest.extra_info, self.editedFormInput["extra_info"])
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)

    def test_unsuccessful_request_edit_from_not_logged_in_user(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, self.editedFormInput)
        self.assertEqual(response.status_code, 302)     # user is redirected to log-in
        self.assertNotEqual(self.request.extra_info, self.editedFormInput["extra_info"])

    def test_unauthorised_request_edit_from_logged_in_user(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        notCurrUserReq = Request.objects.get(user = self.otherUser)
        response = self.client.post(reverse("edit-request", args=[notCurrUserReq.id]), self.editedFormInput)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(self.request.extra_info, self.editedFormInput["extra_info"])

    def test_invalid_request_edit_from_logged_in_user(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        self.editedFormInput["duration"] = 90
        response = self.client.post(self.url, self.editedFormInput)
        notUpdatedLessonRequest = Request.objects.get(user = self.user)
        self.assertNotEqual(notUpdatedLessonRequest.duration, self.editedFormInput["duration"])
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 1)
        self.assertEqual(response_messages[0].level, messages.ERROR)
