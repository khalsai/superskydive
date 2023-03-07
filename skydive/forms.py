from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password_repeat = forms.CharField(widget=forms.PasswordInput())
    phone_number = forms.CharField(widget=forms.NumberInput(), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "password_repeat")


