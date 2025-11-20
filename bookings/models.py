from django.db import models
from django.urls import reverse
from User_Management.models import Profile
from django.core.validators import RegexValidator

# Create your models here.

class Passenger(models.Model):
    lastName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phonenumber = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Enter phone number in this format: +631234567890. This accepts up to 15 digits."
            ),
        ]
    )
    birthdate = models.DateField()

    GENDER_CHOICES = [
        ("1", "Bisexual"),
        ("2", "Female"),
        ("3", "Male"),
        ("4", "Pansexual"),
        ("5", "Others"),
    ]

    gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default="5"
    )

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    bookdate = models.DateField(auto_created=True, auto_now_add=True)
    bookcost = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Flight(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departuredate = models.DateField()
    departuretime = models.TimeField()
    arrivaldate = models.DateField()
    arrivaltime = models.TimeField()
    flightcost = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
