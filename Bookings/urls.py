from django.urls import path
from . import views

urlpatterns = [
	path('', views.search_flights, name='home'),
    path('destsearch', views.search_flights, name='destsearch'),
    path('destsearchresult', views.CitySearchResultsView.as_view(), name='destsearchresult'),
    path('cityflights/<int:pk>/', views.DestinationFlightsView.as_view(), name='cityflights'),
    path('booking', views.FlightBookingView.as_view(), name='booking'),
    path('mybookedflights', views.MyBookedFlightsView.as_view(), name='mybookedflights'),
    path('mybookedflights/<int:pk>/', views.MyBookedFlightDetailView.as_view(), name='bookingdetail'),
]

app_name = 'bookings'
