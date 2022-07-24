from urllib.parse import urldefrag
from django.conf import UserSettingsHolder
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from rooms.models import Booking, Room
# Create your views here.

def registerUser(request):
    if(request.user.is_authenticated):
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
        
        user = User.objects.create_user(
            username = username,password=password,email=email,first_name=first_name,last_name=last_name)
        user.save()
        customUser = CustomUser(user=user,phone=phone,user_type=user_type,address=address,certificate=certificate)
        customUser.save()
        auth_login(request, user)
        messages.success(request,"User successfully Created")
        # return redirect('accounts/login.html')
        return render(request, 'accounts/login.html')
    
    return render(request,'accounts/register.html')

def login(request):
    if(request.user.is_authenticated and not request.user.is_authenticated):
        return redirect('/')
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
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
        else:
            return HttpResponse("Login to View your Profile")
    else:
        return redirect('/')

def editProfile(request,pk):
    if(request.user.is_authenticated and not request.user.is_superuser):
        user = User.objects.get(id=pk)
        customuser = user.customuser
        
        context = {'userInfo':user,'customuser':customuser}
        return render(request,"accounts/editProfile.html",context)

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
        userObj.username = username
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
        auth_login(request, userObj)
        messages.success(request,"User detail Updated")
        # return redirect('accounts/login.html')
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
    