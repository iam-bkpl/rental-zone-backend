from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

USER_TYPE = (
    ('customer', 'Customer'),
    ('room_owner', 'Room Owner')
)
USER_GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('others','others')
)

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=25, null=True,blank=True)
    # last_name = models.CharField(max_length=25, null=True,blank=True)
    # username = models.CharField(max_length=20,null=True,blank=True,unique=True)
    # email = models.EmailField(unique=True, null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    # gender = models.CharField(max_length=7,null=True,blank=True,choices=USER_GENDER)
    # user_type = models.CharField(max_length=15,null=True,blank=True, choices=USER_TYPE)
    user_type = models.CharField(max_length=15,null=True,blank=True)
    address =  models.CharField(max_length=30, null=True,blank=True)
    # verified = models.BooleanField(default=False,null=True,blank=True)
    certificate = models.ImageField(upload_to='certificate', null=True,blank=True) 
    
    def __str__(self):
        return self.user.username
