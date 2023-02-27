from django import forms
from django.forms.fields import DateTimeField
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Ride

class RideInfoForm(forms.Form):
    destination = forms.CharField(label='Destination', max_length=100, 
        widget = forms.TextInput(attrs={'placeholder':'destination', 'class':'form-control'}), required=True)

    arrival_time = DateTimeField(
        label="Arrival time",
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class':'form-control'})
        )

    party_size = forms.IntegerField(label='Party size', required=True,
        widget = forms.NumberInput(attrs={'placeholder':'party size', 'class':'form-control'}), 
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    vehicle_type = forms.ChoiceField(label='Vehicle type',
            widget= forms.Select(attrs={'placeholder':'vehicle type', 'class':'form-control'}), 
            choices=(("Sedan", "Sedan"),
                    ("SUV", "SUV"),
                    ("Coupe", "Coupe"),
                    ("Van", "Van")),
            )

    sharable = forms.BooleanField(label="Sharable or not", required=False)

    special_request = forms.CharField(label='Special Request', max_length=100, 
        widget = forms.TextInput(attrs={'placeholder':'special request', 'class':'form-control'}), 
        required=False)

class RideShareForm(forms.Form):
    destination = forms.CharField(label='Destination', max_length=100, 
        widget = forms.TextInput(attrs={'placeholder':'destination', 'class':'form-control'}), required=True)

    earliest_arrival = DateTimeField(
        label="Earliest arrival time",
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class':'form-control'})
        )
    latest_arrival = DateTimeField(
        label="Latest arrival time",
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class':'form-control'})
        )
    party_size = forms.IntegerField(label='Party size', required=True,
        widget = forms.NumberInput(attrs={'placeholder':'party size', 'class':'form-control'}), 
        validators=[MinValueValidator(1), MaxValueValidator(10)])

class SharerInfoForm(forms.Form):
    sharer = forms.CharField(label='Your Username', max_length=100, 
        widget = forms.TextInput(attrs={'placeholder':'Your Username', 'class':'form-control'}), required=True)

    destination = forms.CharField(label='Destination', max_length=100, 
        widget = forms.TextInput(attrs={'placeholder':'destination', 'class':'form-control'}), required=False)

    arrival_time = DateTimeField(
        label="Arrival time",
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', 'class':'form-control'}),
        required=False
        )

    party_size = forms.IntegerField(label='Party size', required=True,
        widget = forms.NumberInput(attrs={'placeholder':'party size', 'class':'form-control'}), 
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    vehicle_type = forms.ChoiceField(label='Vehicle type',
            widget= forms.Select(attrs={'placeholder':'vehicle type', 'class':'form-control'}), 
            choices=(("Sedan", "Sedan"),
                    ("SUV", "SUV"),
                    ("Coupe", "Coupe"),
                    ("Van", "Van")),
                    required=False
            )

    special_request = forms.CharField(label='Special Request', max_length=100, 
        widget = forms.TextInput(attrs={'placeholder':'special request', 'class':'form-control'}), 
        required=False)