from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('destsearch', views.CitySearchView.as_view(), name='destsearch'),
    path('destsearchresult', views.CitySearchResultsView.as_view(), name='destsearchresult'),
    path('cityflights/<int:pk>/', views.DestinationFlightsView.as_view(), name='cityflights'),
]

app_name = 'bookings'