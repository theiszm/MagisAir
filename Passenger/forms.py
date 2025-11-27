from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import *

class SignupForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username', 'email']

class PassengerForm(ModelForm):
    """A form for updating passenger information. """
    class Meta:
        model = Passenger
        exclude=['user']
        widgets = {
            "birthdate": DatePickerInput(
                options={
                    "format": "YYYY-MM-DD",
                },
                attrs={
                    "class": "form-control",
                }
            )
        }

        
