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
from .models import Room,Booking
from accounts.models import CustomUser

# Create your views here.

# Main page
def index(request):
    roomList = Room.objects.all()
    return render(request,'index.html')

# List of room 
def roomsList(request):
    roomList = Room.objects.all()
   
    context = {'roomList':roomList}
    return render(request, 'rooms/roomList.html',context)

# Single room 
def roomView(request,pk):
    user=request.user
    room = Room.objects.get(id=pk)
    recently_viewed_rooms = None
    session = request.session
    if( 'recently_viewed' in session ):
        if room.id in session['recently_viewed']:
            session['recently_viewed'].remove(room.id)
        
        recent_room = Room.objects.filter(pk__in = session['recently_viewed'])
        recently_viewed_rooms = sorted(
            recent_room, key=lambda x: session['recently_viewed'].index(x.id)
        )
        session['recently_viewed'].insert(0,room.id)
        if len(session['recently_viewed'])> 5:
            session['recently_viewed'].pop()
    else:
        session['recently_viewed'] = [room.id]
        
    session.modified = True
    
    
    
    
    # session handeling
    
    
    
    if(not user.is_superuser):
        # user = request.user
        context = {'recently_viewed_rooms':recently_viewed_rooms}
        if(user.is_authenticated):
            user = CustomUser.objects.get(user = request.user)  
            context.update({'room':room,'user':user})
        else:
            context.update({'room':room})
            
        return render(request,'rooms/roomView.html',context)
    else:
        # return HttpResponse("You are super admin")
        return render(request,'accounts/login.html')



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
    if(request.user.is_authenticated):
        owner = request.user
        room = Room.objects.get(id=pk)
        room.delete()
        roomList = Room.objects.all()
        context = {'roomList':roomList}
        messages.success(request,"Room Deleted Successfully")
        return render(request, 'rooms/roomList.html',context)
    else:
        return redirect('/')
        
def updateRoom(request,pk):

    # import pdb
    # pdb.set_trace() 
    if(request.user.is_authenticated):
        user = request.user.customuser
        userType = user.user_type
        room = Room.objects.get(id=pk)
        if request.method == "GET":
            if(request.user.is_authenticated and userType == "room_owner"):
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
                context = {'room':room}
                return render(request,'rooms/roomView.html',context)
        
        
        return render(request,"rooms/updateRoom.html")
    else:
        return redirect('/')



def bookRoom(request,pk):
    room = Room.objects.get(id=pk)
    user = request.user.customuser
    if request.method == "POST" and user.user_type == "customer":
        number_of_rooms = request.POST.get('number_of_rooms')
        book_date = request.POST.get('book_date')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        paid = request.POST.get('paid')
        if paid == 'paid':
            paid = True

        
        bookRoomObj = Booking(
            customer = user, room = room, number_of_rooms=number_of_rooms,
            book_date=book_date, checkin_date=checkin_date, checkout_date=checkout_date, payment_method=payment_method, amount=amount,paid=paid
        )
        bookRoomObj.save()
        messages.success(request,"Room Book Request Sent Successfully")
        context = {'userInfo':user}
        return render(request,'accounts/userProfile.html',context)
    context= {'room':room}
    return render(request,'rooms/bookRoom.html',context)