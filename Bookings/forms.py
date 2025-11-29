from django import forms
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['passenger', 'flight']


class FlightSearchForm(forms.Form):
    origin = forms.ModelChoiceField(
        label="Origin city",
        queryset=City.objects.all().order_by("city"),
    )

    destination = forms.ModelChoiceField(
        label="Destination city",
        queryset=City.objects.all().order_by("city"),
    )

    departure_date = forms.DateField(
        label="Departure date",
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",  # NEW correct way
            },
            attrs={
                "placeholder": "Select date",
                "class": "form-control",
            },
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get("origin")
        destination = cleaned_data.get("destination")

        if origin and destination and origin == destination:
            self.add_error("destination", "Origin and destination must be different.")

        return cleaned_data
