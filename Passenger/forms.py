from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from bootstrap_datepicker_plus.widgets import DatePickerInput
from phonenumber_field.formfields import PhoneNumberField as PhoneNumberFormField

from .models import Passenger


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class PassengerForm(ModelForm):
    """A form for updating passenger information."""

    phone_number = PhoneNumberFormField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter phone number",
                "autocomplete": "off",
                "style": "padding-left: 50px;",
            }
        ),
        required=False,
    )

    birthdate = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",   # Correct modern format placement
            }
        ),
        required=False,
    )

    class Meta:
        model = Passenger
        exclude = ['user']
