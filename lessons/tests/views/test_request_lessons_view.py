from django.test import TestCase
from lessons.forms import RequestForm
from lessons.models import User, Request
from django.urls import reverse
from django.contrib import messages
from lessons.tests.helpers import LogInTester
from django.contrib.auth.models import AnonymousUser


class RequestViewTestCase(TestCase, LogInTester):

    fixtures = [
        "lessons/tests/fixtures/default_user.json"
    ]

    def setUp(self):
        self.url = reverse("request-lessons")
        self.user = User.objects.get(username = "@johndoe")
        self.formInput = {
            "availability": "wednesday",
            "number_of_lessons": 2,
            "interval": 7,
            "duration": 60,
            "extra_info": "I would like to learn the bababooey instrument."
        }
    
    def test_request_lessons_url(self):
        self.assertEqual(self.url, "/request-lessons/")
    
    def test_get_request_lessons_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "request-lessons.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, RequestForm))
        self.assertFalse(form.is_bound)
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 0)
        
    # A lesson request can only be made by a logged in user
    def test_successful_lesson_request_from_logged_in_user(self):
        logIn = self.client.post(reverse("log_in"), {"username": self.user.username, "password": "Password123"}, follow= True)
        before = Request.objects.count()
        response = self.client.post(self.url, self.formInput, follow= True)
        self.assertEqual(response.status_code, 200)
        after = Request.objects.count()
        self.assertEqual(after, before + 1)
        createdLessonRequest = Request.objects.get(created_by = logIn.context["user"].id)
        self.assertEqual(createdLessonRequest.created_by.username, logIn.context["user"].username)
        response_url = reverse('request-display')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'request-display.html')
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)
    
    def test_unsuccessful_lesson_request_from_not_logged_in_user(self):
        logIn = self.client.post(reverse("log_in"), {"username": self.user.username, "password": "IncorrectPassword"}, follow= True)    # user will not get logged in
        self.assertFalse(self._is_logged_in())
        before = Request.objects.count()
        self.assertIsInstance(logIn.context["user"], AnonymousUser)     # not a logged in user
        with self.assertRaises(ValueError):
            self.client.post(self.url, self.formInput, follow= True)
        after = Request.objects.count()
        self.assertEqual(after, before)
        with self.assertRaises(Request.DoesNotExist):
            Request.objects.get(created_by = logIn.context["user"].id)

    def test_unsuccessful_lesson_request(self):
        self.client.post(reverse("log_in"), {"username": self.user.username, "password": "Password123"}, follow= True)
        self.formInput["duration"] = 15
        before = Request.objects.count()
        response = self.client.post(self.url, self.formInput)
        after = Request.objects.count()
        self.assertEqual(after, before)
        form = response.context["form"]
        self.assertTrue(isinstance(form, RequestForm))
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 1)
        self.assertEqual(response_messages[0].level, messages.ERROR)
        
