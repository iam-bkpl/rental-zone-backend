from django.contrib import admin
from django.urls import path
from accounts import views
# from rooms import views

urlpatterns = [
    path('admin/',admin.site.urls),
    # path('',views.index),
    path('register/',views.registerUser, name="registerUser"),
    path('login/',views.login, name='login'),
    path('logout/',views.logout,name="logout"),
    
    # user profile
    path('userProfile/',views.userProfile, name="userProfile"),
    path('deleteProfile/',views.deleteProfile, name="deleteProfile"),
    path('updateProfile/',views.updateProfile, name="updateProfile")
]
