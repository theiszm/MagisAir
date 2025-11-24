from django import forms
from .models import *

class CitySearchForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city', 'country', 'iata_code']

class FlightSearchForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['departure_date', 'arrival_date', 'flight_code', 'route']