from django.db import models
from django.contrib.auth.models import User


class Ride(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)    # destination
    arrival_time = models.DateTimeField(help_text='Format: 01/01/2022, 12:00')
    vehicle_choices = (
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("Coupe", "Coupe"),
        ("Van", "Van")
    )
    vehicle_type = models.CharField(max_length=10, choices=vehicle_choices)
    owner_seats = models.PositiveIntegerField(default=1)
    special_requirements = models.CharField(max_length=400, blank=True, null=True)
    sharable = models.BooleanField(default=False)

    driver = models.CharField(default='', max_length=50, blank=True, null=True)

    sharer = models.CharField(default='', max_length=50, blank=True, null=True)
    sharer_seats = models.PositiveIntegerField(default=0)

    # order status
    rideStatus_choice = (
        ("Open", "Open"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed")
    )
    status = models.CharField(
        max_length=10, choices=rideStatus_choice, default="Open")
    # owner + sharer
    available_seats = models.PositiveIntegerField(default=0) 