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

# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")

class CitySearchView(TemplateView):
    model = City
    template_name = 'booksearch.html'

class CitySearchResultsView(ListView):
    model = City
    template_name = 'searchresult.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = City.objects.filter(
            Q(city__icontains=query) | Q(country__icontains=query)
        )
        return object_list
    
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