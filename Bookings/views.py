from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.db.models import Q

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