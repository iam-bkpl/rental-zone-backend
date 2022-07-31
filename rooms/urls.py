from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index , name = "index"),
    path('addRoom/',views.addRoom, name="addRoom"),
    path('roomList/',views.roomsList,name="roomList"),
    path('roomView/<int:pk>/', views.roomView,name="roomView"),
    path('deleteRoom/<int:pk>/', views.deleteRoom, name="deleteRoom"),
    path('editRoom/<int:pk>/',views.editRoom,name="editRoom"),
    path('updateRoom/<int:pk>',views.updateRoom, name="updateRoom"),
    path('bookRoom/<int:pk>/',views.bookRoom, name="bookRoom"),
    path('editBookStatus/<int:pk>/',views.editBookStatus,name="editBookStatus"),
    path('updateBookStatus/<int:pk>/',views.updateBookStatus,name="updateBookStatus"),
    path('rateRoomView/<int:pk>/',views.rateRoomView,name="rateRoomView" ),
    path('deleteReview/<int:pk>/',views.deleteReview,name="deleteReview"),
    # path('rateRoom/<int:pk>/',views.rateRoom,name="rateRoom"),
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)