from django.contrib import admin
from .models import Room,Booking
# Register your models here.

myModels = [Room, Booking]
admin.site.register(myModels)
