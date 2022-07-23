from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index , name = "index"),
    path('addRoom/',views.addRoom, name="addRoom"),
    path('roomList/',views.roomsList,name="roomList"),
    path('roomView/<int:pk>/', views.roomView,name="roomView"),
    path('deleteRoom/<int:pk>/', views.deleteRoom, name="deleteRoom"),
    path('updateRoom/<int:pk>/',views.updateRoom, name="updateRoom"),
    path('bookRoom/<int:pk>/',views.bookRoom, name="bookRoom")
    
]
