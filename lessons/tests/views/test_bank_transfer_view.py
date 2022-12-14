"""
Test cases for bank transfer view.
"""
from django.test import TestCase

from lessons.models import Lesson, Request, User

class BankTransferViewTestCase(TestCase):
    
    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/default_request.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username = "@johndoe")
        self.request = Request.objects.get(user = self.user)
        self.lesson = Lesson.objects.create(
            request = self.request,
            teacher = "Mr Keppens"
        )