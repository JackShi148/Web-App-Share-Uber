from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from user.forms import *

from .forms import RideInfoForm, RideShareForm, SharerInfoForm
from .models import Ride

@login_required
def request_ride_page(request):
    cur_user = request.user
    if request.method == "POST":
        form = RideInfoForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            arrival_time = form.cleaned_data['arrival_time']
            party_size = form.cleaned_data['party_size']
            vehicle_type = form.cleaned_data['vehicle_type']
            sharable = form.cleaned_data['sharable']
            special_request = form.cleaned_data['special_request']
            if vehicle_type == 'Sedan':
                seats = 4
            elif vehicle_type == "SUV":
                seats = 6
            elif vehicle_type == "Coupe":
                seats = 3
            elif vehicle_type == "Van":
                seats = 10
            if party_size > seats:
                messages.info(request, f'Your party size is more than the largest load!')
                return redirect('request_ride')
            available_seats = seats - party_size
            ride = Ride(
                owner = cur_user,
                destination = destination,
                arrival_time = arrival_time,
                vehicle_type = vehicle_type,
                owner_seats = party_size,
                sharable = sharable,
                available_seats=available_seats,
            )
            ride.special_requirements = special_request
            ride.save()
            return redirect('view_ride')
        else:
            return render(request, 'ride/request_ride.html', {'form':form})
    form = RideInfoForm()
    return render(request, 'ride/request_ride.html', {'form':form})

@login_required
def view_ride_page(request):
    cur_user = request.user
    all_ride_info = Ride.objects.filter(owner=cur_user).exclude(status='Completed').order_by('status')
    all_share_ride_info = Ride.objects.filter(sharer__icontains=cur_user).exclude(status='Completed').order_by('status')
    # all_driver_ride_info = Ride.objects.filter(driver__icontains=cur_user).exclude(status='Completed').order_by('status')
    all_driver_ride_info = Ride.objects.filter(driver=cur_user).exclude(status='Completed').order_by('status')

    des_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        des_dict["destination__icontains"] = search_data
    all_ride_info = all_ride_info.filter(**des_dict).order_by('status')
    all_share_ride_info = all_share_ride_info.filter(**des_dict).order_by('status')
    all_driver_ride_info = all_driver_ride_info.filter(**des_dict).order_by('status')
    
    is_driver = hasattr(cur_user, 'driverinfo')
    
    return render(request, 'ride/view_ride.html', {'all_ride_info':all_ride_info, 'all_share_ride_info':all_share_ride_info, 'search_data':search_data, 
                                                   'all_driver_ride_info': all_driver_ride_info, 'is_driver':is_driver})

@login_required
def owner_edit_ride_page(request, nid):
    cur_user = request.user
    if request.method == 'POST':
        form = RideInfoForm(request.POST)
        if form.is_valid():
            ride = Ride.objects.filter(id=nid, status='Open').first()
            ride.destination = form.cleaned_data['destination']
            ride.arrival_time = form.cleaned_data['arrival_time']
            owner_seats = form.cleaned_data['party_size']
            ride.vehicle_type = form.cleaned_data['vehicle_type']
            ride.sharable = form.cleaned_data['sharable']
            special_request = form.cleaned_data['special_request']
            ride.special_requirements = special_request
            if ride.vehicle_type == 'Sedan':
                seats = 4
            elif ride.vehicle_type == "SUV":
                seats = 6
            elif ride.vehicle_type == "Coupe":
                seats = 2
            elif ride.vehicle_type == "Van":
                seats = 10
            if owner_seats > ride.available_seats + ride.owner_seats:
                messages.info(request, f'Your party size is more than the largest load!')
                return redirect('/user/'+ str(nid) + '/owner_edit_ride/')
            ride.owner_seats = owner_seats
            ride.available_seats = seats - ride.owner_seats - ride.sharer_seats
            ride.save()
            return redirect('view_ride')
        else:
            ride = Ride.objects.filter(id=nid, status='Open').first()
            return render(request, 'ride/ride_edit.html', {'ride':ride, 'form':form})

    ride = Ride.objects.filter(id=nid, status='Open').first()
    # 只能修改Open状态的ride
    if ride:
        if ride.sharer:
            messages.info(request, f'You cannot edit a ride with sharers!')
            return redirect('view_ride')
        form = RideInfoForm()
        return render(request, 'ride/ride_edit.html', {'ride':ride, 'form':form})
    else: 
        messages.info(request, f'You cannot edit a confirmed ride, the Driver is in the route!')
        return redirect('view_ride')

@login_required
def owner_delete_ride_page(request, nid):
    ride = Ride.objects.filter(id=nid).first()
    if ride.status == 'Confirmed':
        messages.info(request, f'You cannot delete a confirmed ride, the Driver is in the route!')
        return redirect('view_ride')
    elif ride.sharer:
        messages.info(request, f'You cannot cancel a ride with sharers!')
        return redirect('view_ride')
    Ride.objects.filter(id=nid).delete()
    return redirect('view_ride')

@login_required
def sharer_join_ride_page(request):
    cur_user = request.user

    if request.method == 'POST':
        form = RideShareForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            earliest_arrival = form.cleaned_data['earliest_arrival']
            latest_arrival = form.cleaned_data['latest_arrival']
            sharer_seats = form.cleaned_data['party_size']

            shared_rides = Ride.objects.filter(sharable=True, status='Open')
            available_rides = shared_rides.exclude(owner=cur_user)
            available_rides = available_rides.exclude(sharer=cur_user.username)
            available_rides = available_rides.filter(available_seats__gte=sharer_seats, destination__icontains=destination)

            for ride in available_rides:
                if ride.arrival_time > latest_arrival:
                    available_rides = available_rides.exclude(id=ride.id)

                elif ride.arrival_time < earliest_arrival:
                    available_rides = available_rides.exclude(id=ride.id)
            return render(request, 'ride/view_available_ride.html', {'available_rides': available_rides})
        else:
            return render(request, 'ride/request_join_ride.html', {'form':form})

    form = RideShareForm()
    return render(request, 'ride/request_join_ride.html', {'form':form})

@login_required
def join_specific_ride_page(request, nid):
    cur_user = request.user
    join_ride = Ride.objects.filter(id=nid).first()
    if request.method == 'POST':
        form = SharerInfoForm(request.POST)
        if form.is_valid():
            sharer_seats = form.cleaned_data['party_size']
            if sharer_seats > join_ride.available_seats:
                messages.info(request, f'Your party size is more than the largest load!')
                return redirect('/user/'+ str(nid) + '/join_specific_ride/')

            if join_ride.sharer:
                join_ride.sharer = join_ride.sharer + "\n" + form.cleaned_data['sharer']
            else:
                join_ride.sharer = form.cleaned_data['sharer']
            join_ride.sharer_seats = sharer_seats
            join_ride.available_seats = join_ride.available_seats - sharer_seats
            
            join_ride.save()
            return redirect('view_ride')

        else:
            return render(request, 'ride/join_specific_ride.html', {'join_ride':join_ride, 'form':form, 'cur_user':cur_user})

    form = SharerInfoForm()
    return render(request, 'ride/join_specific_ride.html', {'join_ride':join_ride, 'form':form, 'cur_user':cur_user})


@login_required
def sharer_edit_ride_page(request, nid):
    cur_user = request.user
    join_ride = Ride.objects.filter(id=nid, status='Open').first()
    if request.method == 'POST':
        form = SharerInfoForm(request.POST)
        if form.is_valid():
            sharer_seats = form.cleaned_data['party_size']
            if join_ride.vehicle_type == 'Sedan':
                seats = 4
            elif join_ride.vehicle_type == "SUV":
                seats = 6
            elif join_ride.vehicle_type == "Coupe":
                seats = 2
            elif join_ride.vehicle_type == "Van":
                seats = 10
            if sharer_seats > join_ride.available_seats + join_ride.sharer_seats:
                messages.info(request, f'Your party size is more than the largest load!')
                return redirect('/user/'+ str(nid) + '/sharer_edit_ride/')
            join_ride.sharer_seats = sharer_seats
            join_ride.available_seats = seats - join_ride.owner_seats - join_ride.sharer_seats
            
            join_ride.save()
            return redirect('view_ride')
        else:
            return render(request, 'ride/sharer_ride_edit.html', {'ride':join_ride, 'form':form, 'cur_user':cur_user})

    # 只能修改Open状态的ride
    if join_ride:
        form = SharerInfoForm()
        return render(request, 'ride/sharer_ride_edit.html', {'ride':join_ride, 'form':form, 'cur_user':cur_user})
    else: 
        messages.info(request, f'You cannot edit a confirmed ride, the Driver is in the route!')
        return redirect('view_ride')

@login_required
def sharer_delete_ride_page(request, nid):
    ride = Ride.objects.filter(id=nid).first()
    if ride.status == 'Confirmed':
        messages.info(request, f'You cannot delete a confirmed ride, the Driver is in the route!')
        return redirect('view_ride')
    ride.sharer = ''
    ride.available_seats = ride.available_seats + ride.sharer_seats
    ride.sharer_seats = 0
    ride.save()
    return redirect('view_ride')

@login_required
def view_history_rides_page(request):
    cur_user = request.user
    all_ride_info = Ride.objects.filter(owner=cur_user, status='Completed')
    all_share_ride_info = Ride.objects.filter(sharer__icontains=cur_user, status='Completed')
    des_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        des_dict["destination__icontains"] = search_data
    all_ride_info = all_ride_info.filter(**des_dict).order_by('status')
    all_share_ride_info = all_share_ride_info.filter(**des_dict).order_by('status')
    return render(request, 'ride/view_history_ride.html', {'all_ride_info':all_ride_info, 'all_share_ride_info':all_share_ride_info, 'search_data':search_data})

@login_required
def view_as_driver(request):
    cur_user = request.user
    if hasattr(cur_user, 'driverinfo') == False:
        return redirect('register_driver')
    else:
        return redirect('driver_search&confirm_ride')
    
@login_required
def driver_search_confirm_ride(request):
    cur_user = request.user
    confirmable_rides = Ride.objects.exclude(owner=cur_user)
    confirmable_rides = confirmable_rides.exclude(sharer=cur_user.username)
    
    # to be solved: special requirements
    confirmable_rides = confirmable_rides.filter(vehicle_type=cur_user.driverinfo.car_type).exclude(status='Confirmed')
    confirmable_rides = confirmable_rides.exclude(status='Completed')
    
    # for ride in confirmable_rides:
    #     if ride.special_requirements == '' and cur_user.driverinfo.special_info == '':
    #         continue
    #     else:
    #         if ride.special_requirements != cur_user.driverinfo.special_info:
    #             confirmable_rides = confirmable_rides.exclude(id=ride.id)
        
    for ride in confirmable_rides:
        if ride.owner_seats+ride.sharer_seats > cur_user.driverinfo.max_pgers:
            confirmable_rides = confirmable_rides.exclude(id=ride.id)
    
    return render(request, 'ride/view_available_ride_as_driver.html', {'available_rides': confirmable_rides})

@login_required
def confirm_specific_ride_as_driver(request, nid):
    # cur_user is a driver
    cur_user = request.user
    confirm_ride = Ride.objects.filter(id=nid).first()
    
    confirm_ride.driver = cur_user.username
    confirm_ride.status = "Confirmed"
    confirm_ride.save()
    
    email_list = []
    email_list.append(confirm_ride.owner.email)
    sharers = confirm_ride.sharer
    sharers_list = sharers.split( )
    print(sharers_list)
    
    for s in sharers_list:
        email_address = User.objects.filter(username=s).first().email
        email_list.append(email_address)
       
    print(email_list)
    # to be implemented: get sharer email
    
    # Email content:
    subject = 'Your ride has been confirmed!'
    message = 'Here is the info of the ride\n'
    message += 'Destination: ' + confirm_ride.destination + '\n'
    message += 'Arrival time: ' + str(confirm_ride.arrival_time) + '\n'
    message += 'Driver: ' + confirm_ride.driver + '\n'
    message += 'Vehicle Plate Number: ' + cur_user.driverinfo.plateNum + '\n'
    message += 'Vehicle Type: ' + cur_user.driverinfo.car_type + '\n'

    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, email_list, fail_silently=False)
    
    return redirect('view_ride')

@login_required
def driver_complete_ride(request, nid):
    cur_user = request.user
    complete_ride = Ride.objects.filter(id=nid).first()
    
    complete_ride.status = "Completed"
    complete_ride.save()
    
    return redirect('view_ride')

    
