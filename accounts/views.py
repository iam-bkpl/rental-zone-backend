from email import message
import pdb
# from os import uname
from urllib import request
from urllib.parse import urldefrag
from django.conf import UserSettingsHolder
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes  
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rooms.models import Booking, Review, Room
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# from django.conf import settings
import random
# Create your views here.

# def send_register_email(user,request):
#     current_site = get_current_site(request)
#     email_subject = 'Rental Zone Email Activation'
#     email_body = render_to_string('accounts/activateMail.html',{
#         'user':user,
#         'domain':current_site,
#         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        
#     })
# import pdb
# pdb.set_trace()
global otpNo
otpNo = 0

        
# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )
        



def registerUser(request):
    if(request.user.is_authenticated and not request.user.is_staff):
        return redirect('/')
        
    # import pdb;
    # pdb.set_trace()
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        username =  request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        email =  request.POST.get('email')
        phone =  request.POST.get('phone')
        # gender =  request.POST.get('gender')
        user_type =  request.POST.get('user_type')
        address =  request.POST.get('address')
        certificate =  request.FILES.get('certificate')
        
        
        # Check if user already exists
        if(User.objects.filter(username=username).exists()):
            messages.warning(request, "Username Taken")
            return render(request, '/accounts/register.html')
        elif(User.objects.filter(email=email).exists()):
            messages.warning(request, "Email Taken")
            return render(request, 'accounts/register.html')
        if(password != confirmPassword):
            messages.warning(request,"Password Doesn't match")
            return render(request,'/accounts/register.html')
        
        
        global userEmail
        userEmail = email
        global uname
        uname  = username
        
        user = User.objects.create_user(
            username = username,password=password,email=email,first_name=first_name,last_name=last_name)
        # user.is_active = False
        user.save()
        
        
        
        
        
        
        customUser = CustomUser(user=user,phone=phone,user_type=user_type,address=address,certificate=certificate)
        customUser.save()
        # auth_login(request, user)
        
        messages.success(request,"User successfully Created")
        
        if request.user.is_staff:
            return redirect('/accounts/dashUser')
        
        return redirect('/accounts/login.html')
        # return render(request, 'accounts/otp.html')
    
    return render(request,'accounts/register.html')


# def otp(request):
#     import pdb
#     pdb.set_trace()
#     global otpNo
#     if request.method == "POST":
#         otp = request.POST.get('otp')
#         if (int(otp)==int(otpNo)):
#             return redirect('/accounts/otp')
#         else:
#             us = User.objects.get(username = uname)
#             us.delete()
#             # us = User.objects.get(email= userEmail)
#             # us.delete()
#             return HttpResponse("Invalid OTP")
#     else:
#         no = random.randrange(1000,9999)
#         send_mail('Your Rental Zone OTP Verification','Your otp is { }'.format(no),
#                   'iam.bkpl03@gmail.com',
#                   [userEmail],
#                   fail_silently=False,
#                   )
#         msg = EmailMessage('Request Callback',
#                       'Your Rental Zone OTP Verification','Your otp is { }'.format(no), to=[userEmail])
#         msg.send()
#         return render(request,'accounts/otp.html',{})
        

def login(request):
    if(request.user.is_authenticated):
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
             auth_login(request, user)
             userInfo = CustomUser.objects.filter(user_id=user.id).get()
             request.session['userdata']=userInfo.id
             messages.info(request, "Logged in successfully")
             return redirect('/')
    
        messages.info(request,"User name and PAssword doesn't exit")
        return render(request,'accounts/login.html')
    return render(request,'accounts/login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

            # import pdb
            # pdb.set_trace()

def userProfile(request):
    # import pdb
    # pdb.set_trace()
    if(request.user.is_authenticated and not request.user.is_superuser):
        customuser = request.user.customuser   
        # getUser = User.objects.get(id=user.id)
        # print(getUser.id)
        # userInfo = CustomUser.objects.get(user_id=user.id)
        # userInfo = CustomUser.objects.get(user_id=getUser.id)
        if(customuser.user_type=="customer"):
                # request.userdata = userInfo
                userInfo = customuser
                
                context = {'userInfo':customuser, 'role':"Customer"}
                return render(request,'accounts/userProfile.html',context)
        
        elif(customuser.user_type =="room_owner"):
            # userInfo =  request.userdata 
          
            # import pdb
            # pdb.set_trace() 
            rooms = customuser.room_set.all()
            
            
        
            # roomInfo = Room.objects.get(owner=customuser)
            # rooms = Room.objects.filter(owner=customuser).all()
            # context = {'roomInfo':roomInfo,'userId':userInfo.id}
            bookedRoom = Booking.objects.exclude(customer__isnull = True)
            context = {'rooms':rooms,'userInfo':customuser, 'role':"Owner",
                       'bookedRoom':bookedRoom
                       }
            return render(request,'accounts/userProfile.html',context)
        
        elif(customuser.user_type =="rentalAdmin"):    
            # userInfo = request.user
            userRole = request.user.customuser.user_type
            context = {'userInfo':customuser, 'role':userRole}
            return render(request,'accounts/userProfile.html',context)
        else:    
            return HttpResponse("Not a Valid User")
    else:
        return redirect('/')

def editProfile(request,pk):
    if(request.user.is_authenticated):
        user = User.objects.get(id=pk)
        customuser = user.customuser
        
        context = {'userInfo':user,'customuser':customuser}
        return render(request,"accounts/editProfile.html",context)

    return redirect('/')

def updateProfile(request,pk):
    if(not request.user.is_authenticated):
        return redirect('/')
    
    # import pdb;
    # pdb.set_trace()
    if request.method == "POST":
        
        userObj = User.objects.get(id=pk)
        customUserObj = userObj.customuser
        
        first_name = request.POST.get('first_name',userObj.first_name)
        last_name =  request.POST.get('last_name',userObj.last_name)
        username =  request.POST.get('username',userObj.username)     
        # password = request.POST.get('password',userObj.password)
        # confirmPassword = request.POST.get('confirmPassword')
        email =  request.POST.get('email',userObj.email)
        phone =  request.POST.get('phone',customUserObj.phone)
        # gender =  request.POST.get('gender')
        # user_type =  request.POST.get('user_type',customUserObj.user_type)
        address =  request.POST.get('address',customUserObj.address)
        # certificate =  request.FILES.get('certificate',customUserObj.certificate)

        # Check if user already exists
        # if(User.objects.filter(username=username).exists()):
        #     messages.warning(request, "Username Taken")
        #     return render(request, '/accounts/register.html')
        # elif(User.objects.filter(email=email).exists()):
        #     messages.warning(request, "Email Taken")
        #     return render(request, 'accounts/register.html')
        # user = User.objects.create_user(
        #     username = username,password=password,email=email,first_name=first_name,last_name=last_name)
        # customUser = CustomUser(user=user,phone=phone,user_type=user_type,address=address,certificate=certificate)
        # userObj.username = username
        # userObj.password = password
        userObj.email = email
        userObj.first_name = first_name
        userObj.last_name = last_name
        
        userObj.save()
        
        customUserObj.user = userObj
        customUserObj.phone = phone
        # customUserObj.user_type = user_type
        customUserObj.address = address
        # customUserObj.certificate = certificate
        
        customUserObj.save()
        # auth_login(request, userObj)
        messages.success(request,"User detail Updated")
        # return redirect('accounts/login.html')
        
        # import pdb
        # pdb.set_trace()
        
        if request.user.is_staff:
            return redirect('/accounts/dashUser')
        
        return render(request, 'accounts/userProfile.html')
    
    return render(request,'accounts/userProfile.html')



def deleteProfile(request,pk):
    if(request.user.is_authenticated):
        # user = User.objects.get(id=pk)
        user = request.user
        user.is_active = False
        user.save()
        # user.delete()
        messages.success(request,"User Deleted Successfully")
        # auth_logout(request)
        logout(request)
            
    return render(request,'index.html')
    # return HttpResponse("Delete Page")
    
    
    
def dashUser(request):
    # customuser = CustomUser.objects.all()
    user = User.objects.all()
    
    context = {'users':user,}
    return render(request,'dashboard/dashUser.html',context)

def dashboard(request):
    user = User.objects.all()
    rooms = Room.objects.all()
    bookings = Booking.objects.all()
    reivews = Review.objects.all()
    
    context = {'users':user,'rooms':rooms,'bookings':bookings,'reviews':reivews}
    return render(request,'dashboard/dashboard.html',context)



def dashRoom(request):
    rooms = Room.objects.all()
    
    context = {'rooms':rooms}
    return render(request,'dashboard/dashRoom.html',context)

def dashBooking(request):
    bookings = Booking.objects.all()
    
    context = {'bookings':bookings}
    return render(request,'dashboard/dashBooking.html',context)


def dashReview(request):
    rooms = Room.objects.all()
    reviews = Review.objects.all()
    context = {'rooms':rooms,'reviews':reviews}
    return render(request,'dashboard/dashReview.html',context)

