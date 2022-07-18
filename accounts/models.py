from pyexpat import model
from django.db import models
from django.forms import modelformset_factory

# Create your models here.

USER_TYPE = (
    ('customer', 'Customer'),
    ('room_owner', 'Room Owner')
)

class Customer(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address =  models.CharField(max_length=50, null=False)
    email = models.EmailField()