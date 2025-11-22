from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('test/', views.TestView.as_view(), name='test'),
]

app_name = 'bookings'