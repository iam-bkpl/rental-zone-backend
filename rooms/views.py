from itertools import count
from os import stat
from types import TracebackType
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages

from accounts import models
from .models import Room
from accounts.models import CustomUser
# Create your views here.

# Main page
def index(request):
    roomList = Room.objects.all()
    print(roomList)
    
    return render(request,'index.html')

# List of room 
def roomsList(request):
    roomList = Room.objects.all()
   
    context = {'roomList':roomList}
    return render(request, 'rooms/roomList.html',context)

# Single room 
def roomView(request,pk):
    room = Room.objects.get(id=pk)
    # user = request.user
    user = CustomUser.objects.get(user = request.user)
    context = {'room':room,'user':user}
    return render(request,'rooms/roomView.html',context)





#Add Room
def addRoom(request):
    # import pdb
    # pdb.set_trace()
    user = request.user.customuser
    userType = user.user_type
    owner = "room_owner"
    if request.method == "POST":
        if(request.user.is_authenticated and userType == owner):
            # userInfo = CustomUser.objects.get(user_id = user.id)
                number_of_room = request.POST.get('number_of_room')
                # available_rooms = request.POST.get('available_rooms')
                room_price = request.POST.get('room_price')
                area_of_room = request.POST.get('area_of_room')
                floor = request.POST.get('floor')
                # room_type = request.POST.get('room_type')
                parking = request.POST.get('parking')
                if parking == 'yes':
                    parking = True
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                country = request.POST.get('country')
                image1 = request.FILES.get('image1')
                image2 = request.FILES.get('image2')
                image3 = request.FILES.get('image3')
                image4 = request.FILES.get('image4')
                description = request.POST.get('description')
                map_link = request.POST.get('map_link')
                
                newRoomObj = Room(owner=user,number_of_room=number_of_room,room_price=room_price,area_of_room=area_of_room,floor=floor,parking=parking,address=address,city=city,state=state,country=country,image1=image1,image2=image2,image3=image3,image4=image4,description=description,map_link=map_link)
                
                newRoomObj.save()
                messages.success(request,"Home Saved Successfully")
                return render(request,'accounts/userProfile.html')
        else :
                return render(request,'accounts/userProfile.html')
        # return render(request,'accounts/userProfile.html')
    return render(request,'rooms/addRoom.html')
            

def deleteRoom(request,pk):
    ownwer = request.user
    room = Room.objects.get(id=pk)
    room.delete()
    roomList = Room.objects.all()
    context = {'roomList':roomList}
    messages.success(request,"Room Deleted Successfully")
    return render(request, 'rooms/roomList.html',context)

    
def updateRoom(request,pk):
    print("Update Room")
    return HttpResponse("Update The room")