from django import forms
from django.core.validators import RegexValidator

from .models import Request
# Create your forms here.

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields=['availability', 'number_of_lessons', 'interval', 'duration', 'extra']
        #widgets = {'number_of_lessons':forms.NumberInput(),'interval':forms.NumberInput(),'duration':forms.NumberInput()}

    def clean(self):
        pass
