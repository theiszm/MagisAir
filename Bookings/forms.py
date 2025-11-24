from django import forms
from .models import *

class CitySearchForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city', 'country', 'iata_code']