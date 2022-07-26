from django.contrib import admin
from .models import Room,Booking,Review
from accounts.models import CustomUser
# Register your models here.

from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()

class RoomAdmin(admin.ModelAdmin):
    list_display = ('owner','number_of_room','room_price','address','city')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer','room','number_of_rooms','book_status','paid')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','room','date','rate')
    
    
myModels = [Room, Booking,Review]       


admin.site.register(Room,RoomAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Review,ReviewAdmin)



class RoomAdmin(admin.AdminSite):
    site_header = "RentalAdmin Admin "
newModels = [Room,Booking,Review,CustomUser]
room_site = RoomAdmin(name="RoomAdmin")
room_site.register(newModels)


# admin.site.register(myModels)
