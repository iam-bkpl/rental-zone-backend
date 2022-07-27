from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display= ('user','phone','user_type','address')


# myModules = [CustomUser,CustomUserAdmin]
# admin.site.unregister(Group)
admin.site.register(CustomUser,CustomUserAdmin)
# admin.site.register(User)
# admin.site.register(myModules)




