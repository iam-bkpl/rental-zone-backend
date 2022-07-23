from statistics import mode
from django.db import models
from accounts.models import CustomUser
# Create your models here.

PARKING_CHOICE = (
   ('yes','yes'),
   ('no','no')
)

class Room(models.Model):
   # owner = models.OneToOneField(settings.AUTH_USER_MODEL,     # primary_key=True, on_delete=models.CASCADE)
   owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
   number_of_room = models.PositiveIntegerField(default=0)
   # available_rooms = models.PositiveIntegerField(default=0)
   room_price = models.PositiveIntegerField(default=0)
   area_of_room = models.CharField(max_length=45)
   floor = models.CharField(max_length=45)
   # room_type = models.CharField(max_length=45)
   parking = models.BooleanField(default=False)
   address = models.CharField(max_length=100,null=False,blank=False)
   city = models.CharField(max_length=25,null=True,blank=True)
   state = models.CharField(max_length=25,null=True,blank=True)
   country = models.CharField(max_length=25,null=True,blank=True)
   image1 =  models.ImageField(upload_to='rooms/', null=True, blank=True )
   image2 = models.ImageField(upload_to='rooms/', null=True, blank=True)
   image3 = models.ImageField(upload_to='rooms/', null=True, blank=True)
   image4 = models.ImageField(upload_to='rooms/', null=True, blank=True)
   description = models.TextField(null=True, blank=True)
   map_link= models.TextField(null=True, blank=True)
   
   def __str__(self):
        return self.address 