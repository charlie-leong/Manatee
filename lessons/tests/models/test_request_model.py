from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Request, User


class RequestModelTestCase(TestCase):

    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/default_request.json",
        ]

    def setUp(self):
        self.user = User.objects.get(username = "@johndoe")
        self.request = Request.objects.get(user = self.user)

    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except (ValidationError):
            self.fail("Request should be valid")
    
    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()
    
    def test_is_valid_request(self):
        self._assert_request_is_valid()
    
    def test_invalid_availability(self):
        self.request.availability = "invalid weekday"
        self._assert_request_is_invalid()
    
    def test_greater_than_max_num_of_lessons(self):
        self.request.number_of_lessons = 99
        self._assert_request_is_invalid()
    
    def test_less_than_min_num_of_lessons(self):
        self.request.number_of_lessons = 0
        self._assert_request_is_invalid()
    
    def test_greater_than_max_interval(self):
        self.request.interval = 21
        self._assert_request_is_invalid()
    
    def test_less_than_min_interval(self):
        self.request.interval = 1
        self._assert_request_is_invalid()

    def test_invalid_duration(self):
        self.request.duration = 32
        self._assert_request_is_invalid()
    
    def test_greater_than_max_extra_info(self):
        string = "senirAndHowardAreEpicLecturers"
        for _ in range(10):
            self.request.extra_info += string
        self._assert_request_is_invalid()

    def test_invalid_is_approved(self):
        self.request.is_approved = None
        self._assert_request_is_invalid()

    def test_invalid_user_field(self):
        self.request.user = None
        self._assert_request_is_invalid()

    def test_cascade_on_delete_created_by(self):
        user = User.objects.get(id = self.user.id)
        id = user.id
        user.delete()
        with self.assertRaises(Request.DoesNotExist):
            Request.objects.get(user = id)
        
    def test_is_not_approved_without_lesson(self):
        self.assertFalse(self.request.is_approved)