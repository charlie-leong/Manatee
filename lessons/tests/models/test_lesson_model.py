from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

from lessons.models import Lesson, User, Request

class LessonModelTestCase(TestCase):

    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/default_request.json",
        "lessons/tests/fixtures/default_lesson.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.request = Request.objects.get(user = self.user)
        self.lesson = Lesson.objects.get(request = self.request)

    def _assert_lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except (ValidationError):
            self.fail("Test lesson should be valid")
    
    def _assert_lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()

    # check a valid lesson is valid
    def test_valid_lesson_is_valid(self):
        self._assert_lesson_is_valid()

    # check a invalid lesson is invalid
    def test_invalid_lesson_is_invalid(self):
        self.lesson.teacher = ""
        self._assert_lesson_is_invalid()

    # lesson must have a request
    def test_lesson_must_have_associated_request(self):
        self.lesson.request = None
        self._assert_lesson_is_invalid()

    # if a lesson is deleted, the associated request should not be
    def test_deleted_lesson_does_not_delete_request(self):
        before = Request.objects.count()
        self.lesson.delete()
        after = Request.objects.count()
        self.assertEqual(before, after)

    # if a request is deleted, the lesson is deleted
    def test_deleted_request_deletes_lesson(self):
        before = Lesson.objects.count()
        self.request.delete()
        after = Lesson.objects.count()
        self.assertEqual(after, before - 1)

    # when a lesson is made, the request field "is_approved" should be set to True
    def test_request_is_approved_when_lesson_is_made(self):
        pass

    # calculateCost should return the correct value
    def test_calculateCost_calculates_correct_value(self):
        cost = self.lesson.calculateCost()
        self.assertEqual(40, cost)
    
    # two lessons cannot come from the same request
    def test_lessons_must_have_unique_requests(self):
        before = Lesson.objects.count()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Lesson.objects.create(
                    request = self.request,
                    teacher = "Mr Kolling"
                )
        after = Lesson.objects.count()
        self.assertEqual(before, after)