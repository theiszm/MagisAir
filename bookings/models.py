from django.db import models
from django.urls import reverse
from User_Management.models import *
from django.core.validators import RegexValidator

# Create your models here.

iata_validator = RegexValidator(
    regex=r'^[A-Z]{3}$',
    message="IATA code must be exactly three uppercase letters (A–Z)."
)

class Passenger(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    phonenumber = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Enter phone number in this format: +631234567890. This accepts up to 15 digits."
            ),
        ]
    )

    def __str__(self):
        return self.name

class City(models.Model):
    """ A model for a specific destination for the airline. """
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    # IATA airport code (e.g., MNL, HKG)
    iata_code = models.CharField(
        "IATA code",  
        max_length=3,
        validators=[iata_validator],
        help_text="Enter exactly three letters."
    )
    
    class Meta:
        verbose_name_plural = "Cities"
        
    def save(self, *args, **kwargs):
        """ Save IATA codes in uppercase letters."""
        if self.iata_code:
            self.iata_code = self.iata_code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city} ({self.iata_code}), {self.country}"
    
class Route(models.Model):
    """ Lists all the routes that the airline is able to fly from and to. """
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name="origins")
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name="destinations")

    class Meta:
        unique_together = ('origin', 'destination')

    def __str__(self):
        return f"{self.origin} -> {self.destination}"
    
class Flight(models.Model):
    departuredate = models.DateField()
    departuretime = models.TimeField()
    arrivaldate = models.DateField()
    arrivaltime = models.TimeField()
    flightcost = models.PositiveIntegerField()
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    bookdate = models.DateField(auto_created=True, auto_now_add=True)
    bookcost = models.PositiveIntegerField()
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
    
    
