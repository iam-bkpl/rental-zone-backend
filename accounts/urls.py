from django.contrib import admin
from django.urls import path
from accounts import views
# from rooms import views

urlpatterns = [
    # path('',views.index),
    path('register/',views.registerUser, name="registerUser"),
    path('login/',views.login, name='login'),
    path('logout/',views.logout,name="logout"),
    
    
    # user profile
    path('userProfile/',views.userProfile, name="userProfile"),
    path('deleteProfile/<int:pk>',views.deleteProfile, name="deleteProfile"),
    path('editProfile/<int:pk>',views.editProfile, name="editProfile"),
    path('updateProfile/<int:pk>',views.updateProfile, name="updateProfile"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('dashRoom/',views.dashRoom,name="dashRoom"),
    path('dashUser/',views.dashUser,name="dashUser"),
    path('dashBooking/',views.dashBooking,name="dashBooking"),
    path('dashReview/',views.dashReview,name="dashReview"),
    
    
]
