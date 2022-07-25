from django.contrib import admin
from .models import Room,Booking,Review
# Register your models here.

myModels = [Room, Booking,Review]
admin.site.register(myModels)
