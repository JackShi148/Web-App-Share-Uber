from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from user.forms import *

from .models import RiderInfo, DriverInfo

@login_required
def homePage(request):
    return render(request, 'user/home.html')

def registerPage(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid(): 
            username=form.cleaned_data['username']
            # print(username)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            user = User.objects.create_user(username=username, email=email, password=password2)
            new_user = RiderInfo.objects.create(user=user, phone=phone, address=address)
            new_user.save()
            return redirect('login')
        else:
            return render(request, 'user/register.html', {'form':form})
    form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form':form})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('login')

    return render(request, 'user/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required
def profilePage(request):
    cur_user = request.user
    is_driver = hasattr(cur_user, 'driverinfo')
    return render(request, 'user/user_profile.html', {'user':cur_user, 'is_driver':is_driver})

@login_required
def user_edit_page(request):
    cur_user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            cur_user.email = form.cleaned_data['email']
            cur_user.riderinfo.phone = form.cleaned_data['phone']
            cur_user.first_name = form.cleaned_data['first_name']
            cur_user.last_name = form.cleaned_data['last_name']
            cur_user.riderinfo.address = form.cleaned_data['address']
            cur_user.save()
            cur_user.riderinfo.save()
            return redirect('user_profile')
        else:
            return render(request, 'user/user_edit.html', {'cur_user':cur_user, 'form':form})
    form = UserEditForm()
    return render(request, 'user/user_edit.html', {'cur_user':cur_user, 'form':form})

@login_required
def register_driver(request):
    cur_user = request.user
    if request.method == "POST":
        form = DriverRegistrationForm(request.POST)
        if form.is_valid(): 
            user = cur_user
            phone = form.cleaned_data['phone']
            car_type = form.cleaned_data['car_type']
            licenseNum = form.cleaned_data['licenseNum']
            plateNum = form.cleaned_data['plateNum']
            max_pgers = form.cleaned_data['max_pgers']
            special_info = form.cleaned_data['special_info']
            
            driver = DriverInfo.objects.create(user = user, phone = phone, car_type = car_type, 
                                               licenseNum=licenseNum, plateNum=plateNum, max_pgers=max_pgers,
                                               special_info=special_info)
            driver.save()
            cur_user.driverinfo = driver
            cur_user.save()
            
            return redirect('view_as_driver')
            
        else:
            return render(request, 'user/register_driver.html', {'form':form})
    form = DriverRegistrationForm()
    return render(request, 'user/register_driver.html', {'form':form})

@login_required
def edit_profile_driver_info(request):
    cur_user = request.user
    if request.method == 'POST':
        form =  DriverRegistrationForm(request.POST)
        if form.is_valid():
            cur_user.driverinfo.phone = form.cleaned_data['phone']
            cur_user.driverinfo.car_type = form.cleaned_data['car_type']
            cur_user.driverinfo.licenseNum = form.cleaned_data['licenseNum']
            cur_user.driverinfo.plateNum = form.cleaned_data['plateNum']
            cur_user.driverinfo.max_pgers = form.cleaned_data['max_pgers']
            cur_user.driverinfo.special_info = form.cleaned_data['special_info']
            
            cur_user.save()
            cur_user.driverinfo.save()
            return redirect('user_profile')
        else:
            return render(request, 'user/user_edit_driver_info.html', {'cur_user':cur_user, 'form':form})
    form = DriverRegistrationForm()
    return render(request, 'user/user_edit_driver_info.html', {'cur_user':cur_user, 'form':form})

@login_required
def unregister_driver(request):
    cur_user = request.user
    cur_user.driverinfo.delete()
    
    return redirect('user_profile')