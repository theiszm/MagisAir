from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView

# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")

class TestView(CreateView):
    model = City
    form_class = DestinationForm
    template_name = 'test.html'