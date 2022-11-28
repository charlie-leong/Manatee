from django.test import TestCase
from lessons.forms import RequestForm
from lessons.models import User, Request
from django.urls import reverse
from django.contrib import messages


class RequestViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("request-lessons")
        self.user = User.objects.create_user(
            "@johndoe",
            first_name = "John",
            last_name = "Doe",
            email = "johndoe@example.org",
            password = "Password123"
        )
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
        
    def test_unsuccessful_lesson_request(self):
        self.formInput["duration"] = 15
        before = Request.objects.count()
        response = self.client.post(self.url, self.formInput)
        after = Request.objects.count()
        self.assertEqual(after, before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "request-lessons.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, RequestForm))
        response_messages = list(response.context["messages"])
        self.assertEqual(len(response_messages), 1)
        self.assertEqual(response_messages[0].level, messages.ERROR)
    
    def test_successful_lesson_request(self):
        before = Request.objects.count()
        response = self.client.post(self.url, self.formInput, follow= True)
        self.assertEqual(response.status_code, 200)
        after = Request.objects.count()
        self.assertEqual(after, before + 1)
        response_url = reverse('request-display')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'request-display.html')
        response_messages = list(response.context['messages'])
        self.assertEqual(len(response_messages), 0)