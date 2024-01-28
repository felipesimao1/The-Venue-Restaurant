from django.contrib import admin

# Register your models here.

from .models import Client, Reservation

admin.site.register(Client)
admin.site.register(Reservation)
