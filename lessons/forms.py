from django import forms
from django.core.validators import RegexValidator
from .models import Request
# Create your forms here.

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields=['availability', 'numLessons', 'interval', 'duration', 'extra']
        widgets = {'numLessons':forms.NumberInput(),'interval':forms.NumberInput(),'duration':forms.NumberInput()}

    def clean(self):
        pass
