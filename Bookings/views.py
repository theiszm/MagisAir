from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.db import connection

# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")

def search_flights(request):
    form = FlightSearchForm(request.GET or None)
    flights = []

    if form.is_valid():
        origin_iata = form.cleaned_data["origin"].iata_code
        dest_iata = form.cleaned_data["destination"].iata_code
        date = form.cleaned_data["departure_date"]

        sql = """
        SELECT
            Bookings_flight.flight_code,
            origin_city.city,
            destination_city.city,
            TIME(Bookings_flight.departure),
            TIME(Bookings_flight.arrival),
            CAST(
                (JULIANDAY(Bookings_flight.arrival)
                 - JULIANDAY(Bookings_flight.departure)) * 1440
                AS INTEGER
            )
        FROM Bookings_flight
        JOIN Bookings_route
            ON Bookings_flight.route_id = Bookings_route.id
        JOIN Bookings_city origin_city
            ON Bookings_route.origin_id = origin_city.id
        JOIN Bookings_city destination_city
            ON Bookings_route.destination_id = destination_city.id
        WHERE origin_city.iata_code = %s
          AND destination_city.iata_code = %s
          AND DATE(Bookings_flight.departure) = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [origin_iata, dest_iata, date])
            rows = cursor.fetchall()

        # map the tuple rows into a clean list of dictionaries
        for row in rows:
            flights.append({
                "flight_code": row[0],
                "origin_city": row[1],
                "destination_city": row[2],
                "departure_time": row[3],
                "arrival_time": row[4],
                "duration_minutes": row[5],
            })

    return render(request, "booksearch.html", {
        "form": form,
        "flights": flights,
    })

#class CitySearchView(TemplateView):
#   model = City
#   template_name = 'booksearch.html'

class CitySearchResultsView(ListView):
    model = Flight
    template_name = 'searchresult.html'
    
class DestinationFlightsView(DetailView):
    model = City
    template_name = 'cityflightcheck.html'

class FlightBookingView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking.html'
    success_url = reverse_lazy('bookings:mybookedflights')

class MyBookedFlightsView(ListView):
    model = Booking
    template_name = 'mybookedflights.html'

    def get_queryset(self):
        return Booking.objects.filter(passenger__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        passenger = Passenger.objects.filter(user=self.request.user).first()
        context['passenger'] = passenger
        return context
    
class MyBookedFlightDetailView(DetailView):
    model = Booking
    template_name = 'mybookedflight.html'

    def get_queryset(self):
        return Booking.objects.filter(passenger__user=self.request.user)