from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'full_name']


class UserPasswordChangeForm(PasswordChangeForm):
    pass