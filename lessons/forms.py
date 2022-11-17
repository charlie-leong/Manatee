from django.core.validators import RegexValidator
from django import forms
from .models import User

class LogInForm(forms.Form): #not associated wiht a particualr user model
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
    new_password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(),
        validators = [RegexValidator(
            regex= r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',  #?= checks if something is coming up ahead
            message = "password must have uppercase, lowercase and a number"

        )]
    )
    password_confirmation = forms.CharField(label='password confirmation', widget=forms.PasswordInput())

    # override clean function to check that password and conf are the same
    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'confirmation does not match pasword')

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
