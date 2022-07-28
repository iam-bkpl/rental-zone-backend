from audioop import reverse
from doctest import REPORT_UDIFF
from email import message
from itertools import count
from os import stat
import pdb
import re
from types import TracebackType
from unittest import loader
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from matplotlib.style import available
from numpy import number
from accounts import models
from accounts.views import userProfile
from rooms.forms import RoomForm,RateForm
from .models import Review, Room,Booking
from accounts.models import CustomUser
import datetime
# Create your views here.

# Main page
def index(request):
    roomList = Room.objects.all()
    return render(request,'index.html')

# List of room 
def roomsList(request):
    roomList = Room.objects.all()
    # reviews = Review.objects.filter(room=room)
    # reviews_avg = reviews.aggregate(Avg('rate'))
    # reviews_count = reviews.count()
    
    context = {'roomList':roomList}
    # context.update({'reviews':reviews,'reviews_avg':reviews_avg,'reviews_count':reviews_count})
    return render(request, 'rooms/roomList.html',context)

# Single room 
def roomView(request,pk):
    # import  pdb
    # pdb.set_trace()
    user=request.user
    room = Room.objects.get(id=pk)
    reviews = Review.objects.filter(room=room)
    reviews_avg = reviews.aggregate(Avg('rate'))
    reviews_count = reviews.count()
    context =  {'room':room}
    
    recently_viewed_rooms = None
    session = request.session
    context = {'reviews':reviews,'reviews_avg':reviews_avg,'reviews_count':reviews_count}
    
    if( 'recently_viewed' in session ):
        if room.id in session['recently_viewed']:
            session['recently_viewed'].remove(room.id)
        
        recent_room = Room.objects.filter(pk__in = session['recently_viewed'])
        recently_viewed_rooms = sorted(
            recent_room, key=lambda x: session['recently_viewed'].index(x.id)
        )
        session['recently_viewed'].insert(0,room.id)
        if len(session['recently_viewed'])> 3:
            session['recently_viewed'].pop()
    else:
        session['recently_viewed'] = [room.id]
        
    
    # sessionRoomId = request.session.get('recently_viewed')
    # sessionRoomObj = Room.objects.filter(id=sessionRoomId)
    # context.update({'sessionRoomObj': sessionRoomObj})
        
    session.modified = True 
    # session handeling
    if(not user.is_superuser):
        # user = request.user
        context.update({'recently_viewed_rooms':recently_viewed_rooms})
        if(user.is_authenticated):
            user = CustomUser.objects.get(user = request.user)  
            context.update({'room':room,'user':user})
        else:
            context.update({'room':room})
            
        return render(request,'rooms/roomView.html',context)
    else:
        # return HttpResponse("You are super admin")
        # return render(request,'accounts/login.html')
        room = Room.objects.get(id=pk)
        context =  {'room':room}
        return render(request,'rooms/roomView.html',context)



# def addRoom(request):
#     if request.method == "POST":
#           form = RoomForm(request.POST)
#           if form.is_valid():  
#             try:  
#                 form.save()  
#                 messages(request,"Room Added Successfully")
#                 return redirect('/')
                
#             except:  
#                 return messages(request,"Error while adding form")  
#     else:  
#         form = RoomForm()  
#     return render(request,'rooms/addRoom.html',{'form':form})  


# Add Room
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
                available_rooms = number_of_room
                room_price = request.POST.get('room_price')
                area_of_room = request.POST.get('area_of_room')
                floor = request.POST.get('floor')
                # room_type = request.POST.get('room_type')
                parking = request.POST.get('parking')
                if parking == 'yes':
                    parking = True
                else:
                    parking = False
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
                
                newRoomObj = Room(owner=user,available_rooms= available_rooms , number_of_room=number_of_room,room_price=room_price,area_of_room=area_of_room,floor=floor,parking=parking,address=address,city=city,state=state,country=country,image1=image1,image2=image2,image3=image3,image4=image4,description=description,map_link=map_link)

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
        
        if request.user.is_staff:
            return redirect('/accounts/dashRoom')
        
        return render(request, 'rooms/roomList.html',context)
    else:
        return redirect('/')
       
       
def editRoom(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'rooms/editRoom.html',context)
    

 
def updateRoom(request,pk):
    # import pdb
    # pdb.set_trace() 
    if(request.user.is_authenticated):
        user = request.user.customuser
        userType = user.user_type
        room = Room.objects.get(id=pk)
        roomObj = Room.objects.get(id=pk)
        
        if request.method == "POST":
            if(userType == "room_owner" or request.user.is_staff):
            # userInfo = CustomUser.objects.get(user_id = user.id)
                number_of_room = request.POST.get('number_of_room') 
                available_rooms = request.POST.get('available_rooms')
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
                
                if int(number_of_room) < int(room.available_rooms):
                    messages.success(request,"Please Select less than"+str(room.number_of_room))
                    context= {'room':room}
                    return render(request,'rooms/roomView.html',context)
        
                roomObj.number_of_room = number_of_room
                roomObj.available_rooms = available_rooms
                roomObj.room_price = room_price
                roomObj.area_of_room = area_of_room
                roomObj.floor = floor
                roomObj.parking = parking
                roomObj.address = address
                roomObj.city = city
                roomObj.state = state
                roomObj.country = country
                roomObj.image1 = image1
                roomObj.image2 = image2
                roomObj.image3 = image3
                roomObj.image4 = image4
                roomObj.description = description
                roomObj.map_link = map_link
                roomObj.save()
                
                # newRoomObj = Room(id=pk, owner=user,number_of_room=number_of_room,room_price=room_price,area_of_room=area_of_room,floor=floor,parking=parking,address=address,city=city,state=state,country=country,image1=image1,image2=image2,image3=image3,image4=image4,description=description,map_link=map_link)

                # newRoomObj.save()
                # import pdb
                # pdb.set_trace()
                checkUser = request.user
                if request.user.is_staff:
                    return redirect('/accounts/dashRoom')
                
                context = {'room':roomObj}
                messages.success(request,"Room Updated")
                return render(request,'rooms/roomView.html',context)
            else:
                room = Room.objects.get(id=pk)
                context = {'room':roomObj}
                return render(request,'rooms/roomList.html',context)
        room = Room.objects.get(id=pk)
        context = {'room':room}
        return render(request,"rooms/roomView.html",context)
    return render(request,"rooms/roomList.html")
    


def bookRoom(request,pk):
    now = datetime.datetime.now()
    # import pdb
    # pdb.set_trace()
    room = Room.objects.get(id=pk)
    user = request.user.customuser
    if request.method == "POST" and user.user_type == "customer":
        number_of_rooms = request.POST.get('number_of_rooms')
        # book_date = request.POST.get('book_date')
        checkin_date = request.POST.get('checkin_date')
        # checkout_date = request.POST.get('checkout_date')
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        paid = request.POST.get('paid')
        
        
        
        if paid == 'paid':
            paid = True
        else:
            paid = False
            
        if int(number_of_rooms) > room.available_rooms:
            messages.success(request,"Please Select less than"+str(room.available_rooms))
            context= {'room':room}
            return render(request,'rooms/bookRoom.html',context)
        else:
            room.available_rooms = int(room.available_rooms) -int(number_of_rooms)
            room.save()
            
        if checkin_date < str(now):
            messages.success(request,"Enter a valid Date")
            context= {'room':room}
            return render(request,'rooms/bookRoom.html',context)
        
        
        bookRoomObj = Booking(
            customer = user, room = room, number_of_rooms=number_of_rooms,
            checkin_date=checkin_date, payment_method=payment_method, amount=amount,paid=paid
        )
        bookRoomObj.save()
        messages.success(request,"Room Book Request Sent Successfully")
        context = {'userInfo':user}
        return render(request,'accounts/userProfile.html',context)
    context= {'room':room}
    return render(request,'rooms/bookRoom.html',context)



def editBookStatus(request,pk):
    # import pdb
    # pdb.set_trace() 
    bookedRoom = Booking.objects.get(id=pk)
    
    context = {'bookedRoom':bookedRoom}
    return render(request,"rooms/editBookStatus.html",context)

def updateBookStatus(request,pk):
    # import pdb
    # pdb.set_trace() 
    bookedRoom = Booking.objects.get(id=pk)
    if request.method == "POST":
        owner = request.user
        book_status = request.POST.get('book_status')
        bookedRoom.book_status = book_status
        bookedRoom.save()
        messages.success(request,"Booking status Changed successfully")
        # return redirect("accounts/userProfile/"+str(ownerid),context)
        return redirect('/accounts/userProfile/')
    

def rateRoomView(request,pk):
    import pdb
    # pdb.set_trace()
    user = request.user
    customUser = user.customuser
    room = Room.objects.get(id=pk)
    template = "/roomView/"+str(room.id)
    rate = Review.objects.filter()
    if request.method == "POST":
        text = request.POST.get("text")
        rate = request.POST.get("rate")
            # rate.user = user
            # rate.room = room
            # rate.text = text
            # rate.rate = rate
            
        rateObj = Review(user=customUser,room=room,text=text,rate=rate)
        rateObj.save()
        messages.success(request,"Successfully Rated")

        # user = request.user
        context = {}
        if(user.is_authenticated):
            user = CustomUser.objects.get(user = request.user)  
            context.update({'room':room,'user':user})
        else:
            return redirect('/')
            
        return render(request,'rooms/rateRoom.html',context)
    # else:
        # return HttpResponse("You are super admin")
    context=({'room':room,'user':customUser})
    return render(request,'rooms/rateRoom.html',context)
    

def deleteReview(request,pk):
    rate = Review.objects.get(id=pk)
    rate.delete()
    messages.success(request,"Review Deleted successfully")
    return redirect('/accounts/dashReview')

# def rateRoom(request,pk):
#     # import pdb
#     # pdb.set_trace()
#     room = Room.objects.get(id=pk)
#     user = request.user
#     template = "/roomView/"+str(room.id)
#     if(user.is_authentica{% static 'rooms/image1' %} ted) and user.customuser =="customer":
#         messages.success(request,"Entered")
#         if request.method == "POST":
#             text = request.POST.get("text")
#             rate = request.POST.get("rate")
#             rate.user = user
#             rate.room = room
#             rate.text = text
#             rate.rate = rate
#             rate.save()
#             messages.success(request,"Successfully Rated")
#             return redirect(template)
#     messages.success(request,"Can't rate room")
#     return redirect(template)
#         #     form = RateForm(request.POST)
#         #     if form.is_valid():
#         #         rate = form.save(commit=False)
        #         rate.user = request.user
        #         rate.room = room
        #         rate.save()
        #         template_name = "/roomView/"+str(room.id)
        #         return HttpResponseRedirect(reverse(template_name,args=[pk]))
        # else:
        #     form = RateForm()
        # roomTemplate = "/roomView"+str(pk)
        # template =  loader.get_template(roomTemplate)
        # context = {
        #     'form':form,
        #     'moive':room   
        # }
        # return HttpResponse(template.render(context,request))
        
        
    
EMAIL_USE_TLS = True  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_USER = 'iam.bkpl03@gmail.com'
EMAIL_HOST_PASSWORD = 'dufyahaiaxyodxsw'
EMAIL_PORT = 587
