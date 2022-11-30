from lessons.models import Lesson, User
from django.core.exceptions import ValidationError
from django.test import TestCase

class LessonModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                "@johndoe",
                first_name = "John",
                last_name = "Doe",
                email = "johndoe@example.org",
                password = "Password123"
            )
        self.lesson = Lesson.objects.create(
            assigned_student_id = "",
            assigned_teacher_id = "",
            number_of_lessons = 2,
            week_interval = 1,
            duration = 60,
            paid = False
        )
    
    def assert_request_is_valid(self):
        try:
            self.lesson.full_clean()
        except( ValidationError):
            self.fail("lesson should be valid")

    def assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()

    
    def test_correct_student_id_length(self):
        self.lesson.assigned_student_id = "123456789"
        self.assert_request_is_invalid()

    def test_max_student_id_length(self):
        self.lesson.assigned_student_id = "123456789012"
        self.assert_request_is_invalid()
    
