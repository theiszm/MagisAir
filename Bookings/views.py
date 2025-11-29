from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.db import IntegrityError, transaction, connection


def index(request):
    return HttpResponse("Hello, world!")

@login_required(login_url='login')
def search_flights(request):
    form = FlightSearchForm(request.GET or None)
    flights = []

    if form.is_valid():
        origin_iata = form.cleaned_data["origin"].iata_code
        dest_iata = form.cleaned_data["destination"].iata_code
        date = form.cleaned_data["departure_date"]

        sql = """
        SELECT
			Bookings_flight.id, 
            Bookings_flight.flight_code,
            origin_city.city,
            destination_city.city,
            DATE(Bookings_flight.departure),
            TIME(Bookings_flight.departure),
            TIME(Bookings_flight.arrival),
            Bookings_flight.base_fare,
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
				"id": row[0],               
                "flight_code": row[1],
                "origin_city": row[2],
                "destination_city": row[3],
                "departure_date": row[4],
                "departure_time": row[5],
                "arrival_time": row[6],
                "base_fare": row[7],
                "duration_minutes": row[8],
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

class FlightBookingView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking.html'

    def get_initial(self):
        initial = super().get_initial()
        flight_id = self.request.GET.get("flight_id")
        if flight_id:
            initial["flight"] = flight_id
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the selected flight from the ?flight_id=... query param
        flight_id = self.request.GET.get("flight_id")
        if flight_id:
            flight = Flight.objects.select_related(
                "route__origin",
                "route__destination",
            ).get(pk=flight_id)
            context["flight"] = flight

        # Get the logged-in passenger
        passenger = Passenger.objects.filter(user=self.request.user).first()
        context["passenger"] = passenger

        return context

    def form_valid(self, form):
        # Attach passenger + flight to instance
        passenger = Passenger.objects.get(user=self.request.user)
        flight_id = self.request.GET.get("flight_id")

        if not flight_id:
            form.add_error(None, "No flight selected.")
            return self.form_invalid(form)

        form.instance.passenger = passenger
        form.instance.flight_id = flight_id

        try:
            # Try saving inside an atomic block so IntegrityError is catchable
            with transaction.atomic():
                response = super().form_valid(form)
        except IntegrityError as e:
            # ❗ Here we convert the DB error into a form error
            form.add_error(
                None,
                "Booking with this Flight and Passenger already exists."
            )
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        return reverse_lazy(
            'bookings:bookingdetail',
            kwargs={'pk': self.object.pk}
        )


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
    
class ShowItineraryView(DetailView):
    model = Booking
    template_name = 'itinerary.html'

    def get_queryset(self):
        return Booking.objects.filter(passenger__user=self.request.user)