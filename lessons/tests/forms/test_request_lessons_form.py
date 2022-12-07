from django.test import TestCase
from lessons.forms import RequestForm
from lessons.models import Request, User
from django import forms

class RequestFormTestCase(TestCase):

    def setUp(self):
        self.formInput = {
            "availability": "WEDNESDAY",
            "number_of_lessons": 2,
            "interval": 2,
            "duration": 60,
            "extra_info": "I would like to learn the bababooey instrument."
        }
    
    def test_valid_form(self):
        form = RequestForm(data = self.formInput)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = RequestForm()
        self.assertIn("availability", form.fields)
        self.assertIn("number_of_lessons", form.fields)
        self.assertIn("interval", form.fields)
        self.assertIn("duration", form.fields)
        self.assertIn("extra_info", form.fields)
        extra_info_widget = form.fields["extra_info"].widget
        self.assertIsInstance(extra_info_widget, forms.Textarea)
    
    def test_form_uses_model_validation(self):
        self.formInput["number_of_lessons"] = 7
        form = RequestForm(data = self.formInput)
        self.assertFalse(form.is_valid())
    
    def test_form_saves_correctly(self):
        # create a user to provide a value for the created_by field
        user = User.objects.create_user(
            "@johndoe",
            first_name = "John",
            last_name = "Doe",
            email = "johndoe@example.org",
            password = "Password123"
        )

        form = RequestForm(data = self.formInput)
        before = Request.objects.count()
        form.save(user)
        after = Request.objects.count()
        self.assertEqual(after, before + 1)
        request = Request.objects.get(id = 1)
        self.assertEqual(request.availability, "WEDNESDAY")
        self.assertEqual(request.number_of_lessons, 2)
        self.assertEqual(request.interval, 2)
        self.assertEqual(request.duration, 60)
        self.assertEqual(request.user.id, user.id)