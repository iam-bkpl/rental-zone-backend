from django.contrib import admin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display= ('user','phone','user_type','address')


# myModules = [CustomUser,CustomUserAdmin]
admin.site.register(CustomUser,CustomUserAdmin)
# admin.site.register(myModules)




