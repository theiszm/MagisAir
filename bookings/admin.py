from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Passenger)
admin.site.register(City)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Booking)