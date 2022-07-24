from django.db import models
from accounts.models import CustomUser
from django.conf import settings
# Create your models here.

PARKING_CHOICE = (
   ('yes','yes'),
   ('no','no')
)

class Room(models.Model):
   # owner = models.OneToOneField(settings.AUTH_USER_MODEL,     # primary_key=True, on_delete=models.CASCADE)
   owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
   number_of_room = models.PositiveIntegerField(default=0,null=True,blank=True)
   # available_rooms = models.PositiveIntegerField(default=0)
   room_price = models.PositiveIntegerField(default=0,null=True,blank=True)
   area_of_room = models.CharField(max_length=45,null=True,blank=True)
   floor = models.CharField(max_length=45,null=True,blank=True)
   # room_type = models.CharField(max_length=45)
   parking = models.BooleanField(default=False,null=True,blank=True)
   address = models.CharField(max_length=100,null=True,blank=True)
   city = models.CharField(max_length=25,null=True,blank=True)
   state = models.CharField(max_length=25,null=True,blank=True)
   country = models.CharField(max_length=25,null=True,blank=True)
   image1 =  models.ImageField(upload_to='rooms/', null=True, blank=True )
   image2 = models.ImageField(upload_to='rooms/', null=True, blank=True)
   image3 = models.ImageField(upload_to='rooms/', null=True, blank=True)
   image4 = models.ImageField(upload_to='rooms/', null=True, blank=True)
   description = models.TextField(null=True, blank=True)
   map_link= models.TextField(null=True, blank=True)
   
#    def __str__(self):
#         return self.address 
     
     
PAYMENT_METHOD = (
    ('online', 'Online Pay'),
    ('offline', 'Offline Pay')
)
BOOK_STATUS = (
    ('booked', 'booked'),
    ('pending', 'pending'),
    ('cancel', 'cancel')
)


class Booking(models.Model):
   customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,related_name='customer_booking')
   room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_booking')
   number_of_rooms = models.PositiveIntegerField(default=0)
   book_date =  models.DateTimeField(auto_now_add = True)
   checkin_date = models.DateTimeField(blank=True, null=True)
   checkout_date = models.DateTimeField(blank=True, null=True)
   payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD, default='offline', null=True,blank=True)
   amount = models.PositiveIntegerField(default=0)
   paid = models.BooleanField(default=False)
   book_status = models.CharField(max_length=15, choices=BOOK_STATUS, default="pending")
   
   def __str__ (self):
       return self.book_status
   
   
# RATE_CHOICES = [
#     (1,'1'),
#     (2,'2'),
#     (3,'3'),
#     (4,'4'),
#     (5,'5'),
#     (6,'6'),
#     (7,'7'),
#     (8,'8'),
#     (9,'9'),
#     (10,'10'),
# ]
  

# class Review(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now=True)
#     text = models.TextField(max_length=3000,blank=True)
#     rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)