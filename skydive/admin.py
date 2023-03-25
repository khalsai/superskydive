from django.contrib import admin

# Register your models here.

from django.db import models

from .models import Destination_desc, Destination, Booking, Passenger, Cards, Transactions, Reservation

admin.site.register(Destination)
admin.site.register(Destination_desc)
admin.site.register(Booking)
admin.site.register(Passenger)
admin.site.register(Cards)
admin.site.register(Transactions)
admin.site.register(Reservation)
