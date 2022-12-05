from lessons.models import Lesson, User
from django.core.exceptions import ValidationError
from django.test import TestCase

class LessonModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                '@johndoe', 
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
        )
    
    def assert_lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except(ValidationError):
            self.fail("lesson should be valid")

    def assert_lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()

    
    def test_correct_student_id_length(self):
        self.lesson.assigned_student_id = "123456789"
        self.assert_lesson_is_invalid()

    def test_max_student_id_length(self):
        self.lesson.assigned_student_id = "123456789012"
        self.assert_lesson_is_invalid()
    
    def test_correct_teacher_id_length(self):
        self.lesson.assigned_teacher_id = "123456789"
        self.assert_lesson_is_invalid()

    def test_max_teacher_id_length(self):
        self.lesson.assigned_teacher_id = "123456789012"
        self.assert_lesson_is_invalid()

    def test_invalid_duration(self):
            self.lesson.duration = 47
            self.assert_lesson_is_invalid()
    
    def test_less_than_minimum_week_interval(self):
            self.lesson.interval = 1
            self.assert_lesson_is_invalid()


    def test_invalid_number_of_lessons(self):
            self.lesson.interval = 5
            self.assert_lesson_is_invalid()
