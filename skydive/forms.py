from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'search_input search_input_3'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'search_input search_input_3'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'search_input search_input_3'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'search_input search_input_3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'search_input search_input_3'}))
    password_repeat = forms.CharField(label='Confirm Password',
                                      widget=forms.PasswordInput(attrs={'class': 'search_input search_input_3'}))
    phone_number = forms.CharField(required='False', widget=forms.NumberInput(attrs={'class': 'search_input '
                                                                                              'search_input_3'}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "password_repeat")

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = '__all__'