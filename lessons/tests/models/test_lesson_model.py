"""
Test cases for the lesson model.
"""
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction
from django.test import TestCase

from lessons.models import Lesson, Request, User

class LessonModelTestCase(TestCase):

    fixtures = [
        "lessons/tests/fixtures/default_user.json",
        "lessons/tests/fixtures/default_request.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.request = Request.objects.get(user = self.user)
        self.lesson = Lesson.objects.create(
            request = self.request,
            teacher = "Mr Keppens"
        )

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
        """ Valid lesson model is valid. """
        self._assert_lesson_is_valid()

    # check a invalid lesson is invalid
    def test_invalid_lesson_is_invalid(self):
        """ Invalid lesson is invalid. """
        self.lesson.teacher = ""
        self._assert_lesson_is_invalid()

    # lesson must have a request
    def test_lesson_must_have_associated_request(self):
        """ Lesson must have a request. """
        self.lesson.request = None
        self._assert_lesson_is_invalid()

    # if a lesson is deleted, the associated request should not be
    def test_deleted_lesson_does_not_delete_request(self):
        """ Deleting a lesson does not delete the request. """
        before = Request.objects.count()
        self.lesson.delete()
        after = Request.objects.count()
        self.assertEqual(before, after) ######## edit this to include false check for approved
        self.assertFalse(self.request.is_approved)

    # if a request is deleted, the lesson is deleted
    def test_deleted_request_deletes_lesson(self):
        """ Deleting a request deletes the linked lesson. """
        before = Lesson.objects.count()
        self.request.delete()
        after = Lesson.objects.count()
        self.assertEqual(after, before - 1)

    # when a lesson is made, the request field "is_approved" should be set to True
    def test_request_is_approved_when_lesson_is_made(self):
        """ Request.is_approved is true when lesson is made. """
        self.assertTrue(self.request.is_approved)

    # calculateCost should return the correct value
    def test_calculateCost_calculates_correct_value(self):
        """ Lesson calculates cost correctly. """
        cost = self.lesson.calculateCost()
        self.assertEqual(40, cost)
    
    # two lessons cannot come from the same request
    def test_lessons_must_have_unique_requests(self):
        """ Two lessons cannot have the same request. """
        before = Lesson.objects.count()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Lesson.objects.create(
                    request = self.request,
                    teacher = "Mr Kolling"
                )
        after = Lesson.objects.count()
        self.assertEqual(before, after)
    
    # test that request is approved with lesson, then delete lesson, then request is not approved
    def test_request_is_not_approved_when_lesson_deleted(self):
        """ Request becomes not approved when lesson is deleted. """
        self.assertTrue(self.request.is_approved)
        self.lesson.delete()
        self.assertFalse(self.request.is_approved)
    
    # test paying for lesson results in correct balance, and is_paid set to true
    def test_pay_lesson(self):
        self.lesson.request.user.adjust_balance(100)
        self.assertFalse(self.lesson.paid)
        self.lesson.pay_lesson("123")
        self.assertTrue(self.lesson.paid)
        self.assertEqual(self.lesson.request.user.balance, 60)
    
    def test_pay_lesson_with_insufficient_funds(self):
        self.lesson.request.user.balance = 30.50
        with self.assertRaises(ValueError):
            self.lesson.pay_lesson("123")
            self.assertFalse(self.lesson.paid)