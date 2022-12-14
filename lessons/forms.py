"""
All of the forms of the lesson application.
"""
from django import forms
from django.core.validators import RegexValidator
from lessons.models import BankTransfer, Request, User
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RequestForm(forms.ModelForm):
    """ Form that will let users create a Request object. """
    class Meta:
        model = Request
        fields=['availability', 'number_of_lessons', 'duration', 'interval', 'extra_info']
        widgets = {'extra_info': forms.Textarea()}

    def save(self, user):
        super().save(commit=False)
        request = Request.objects.create(
            availability = self.cleaned_data.get("availability"),
            number_of_lessons = self.cleaned_data.get("number_of_lessons"),
            interval = self.cleaned_data.get("interval"),
            duration = self.cleaned_data.get("duration"),
            extra_info = self.cleaned_data.get("extra_info"),
            user = user
        )
        return request


class LogInForm(forms.Form): #not associated with a particular user model
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    """ Form that users will use to sign up. """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators = [RegexValidator(
            regex= r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',  #?= checks if something is coming up ahead
            message = "Password must have uppercase, lowercase and a number!"

        )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    # override clean function to check that password and conf are the same
    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match pasword!')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            password = self.cleaned_data.get('new_password'),
        )
        return user


class BankTransferForm(forms.ModelForm):
    class Meta:
        model = BankTransfer
        fields=['invoice_number']
    
    invoice_number = forms.CharField(max_length=3)

    def save(self, user_, lesson_):
        super().save(commit=False)
        invoice = BankTransfer.objects.create(
            user = user_,
            lesson = lesson_,
            invoice_number = f'{user_.id}-{self.cleaned_data.get("invoice_number")}',
            cost = lesson_.calculateCost()
        )
        return invoice



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')