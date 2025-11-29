from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
import string
import random

from Passenger.models import Passenger

class City(models.Model):
    """ A model for a specific destination for the airline. """
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    # IATA airport code (e.g., MNL, HKG)
    iata_code = models.CharField(
        "IATA code",  
        max_length=3,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}$',
                message="IATA code must be exactly three uppercase letters (A–Z)."
            ),
        ]
    )
    
    class Meta:
        verbose_name_plural = "Cities"

    def get_absolute_url(self):
        return reverse('bookings:cityflights', args=[self.pk])
        
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
    flight_code = models.CharField(  
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^MA \d{3}$',
                message="Flight code must be in format 'MA 800' (MA + space + 3 digits)."
            )
        ],
        unique=True,
        verbose_name="Flight Code",
        help_text="Format: MA 800"
    )
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
    )
    base_fare = models.PositiveIntegerField()
    
    @property
    def duration(self):
        d = self.arrival - self.departure
        hours = d.seconds // 3600
        mins = (d.seconds % 3600) // 60
        return f"{hours} hr {mins} min"

    def __str__(self):
        return f"{self.flight_code} — {self.route}"
    
def generate_booking_ref():
        letters = string.ascii_uppercase
        digits = string.digits
        combination = letters + digits
        return ''.join(random.choices(combination, k=6))
    
class Booking(models.Model):
    booking_ref = models.CharField(
        max_length=6,
        unique=True,
        editable=False,
        null=True,
        blank=True,
    )
    created_at = models.DateField(auto_created=True, auto_now_add=True)
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name='bookings',    # passenger.bookings.all()
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='bookings',    # flight.bookings.all()
    )
    
    # each unit = 5kg extra baggage, for example
    baggage_allowance_qty = models.PositiveIntegerField(
        verbose_name="Baggage allowance",
        default=0
    )
    travel_insurance = models.BooleanField(default=False)
    
    BAGGAGE_UNIT_PRICE = 1000   # per 5kg unit
    TERMINAL_FEE_PRICE = 800    # always included, qty = 1
    INSURANCE_PRICE = 500       # if travel_insurance == True
      
    def save(self, *args, **kwargs):
        # only generate number on first creation
        if not self.booking_ref:   
            ref = generate_booking_ref()
    
            # ensure uniqueness
            while Booking.objects.filter(booking_ref=ref).exists():
                ref = generate_booking_ref()
    
            self.booking_ref = ref
            
        super().save(*args, **kwargs)
    
    @property
    def total_cost(self):
        # normalized: use flight.base_fare, not a field on Booking
        base_fare = self.flight.base_fare

        extras = 0
        extras += self.baggage_allowance_qty * self.BAGGAGE_UNIT_PRICE
        extras += self.TERMINAL_FEE_PRICE
        if self.travel_insurance:
            extras += self.INSURANCE_PRICE

        return base_fare + extras
    
    def baggage_allowance_price_product(self):
        return self.baggage_allowance_qty * self.BAGGAGE_UNIT_PRICE

    def __str__(self):
        return f"Booking #{self.booking_ref} — {self.passenger} on {self.flight}"
    
    class Meta:
        unique_together = ('passenger', 'flight')

    def get_absolute_url(self):
        return reverse('bookings:bookingdetail', args=[self.pk])
    
    