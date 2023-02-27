from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RiderInfo, DriverInfo


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, error_messages={'max_length':'Length must be within 20', 'required':'username is required'}, 
        widget = forms.TextInput(attrs={'placeholder':'username', 'class':'form-control'}), label='username')

    password1 = forms.CharField(error_messages={'required':'password is required'}, 
        widget = forms.PasswordInput(attrs={'placeholder':'password', 'class':'form-control'}), label='password1')

    password2 = forms.CharField(error_messages={'required':'password is required'}, 
        widget = forms.PasswordInput(attrs={'placeholder':'password', 'class':'form-control'}), label='password2')

    email = forms.EmailField(error_messages={'required':'email is required'}, 
        widget = forms.EmailInput(attrs={'placeholder':'email', 'class':'form-control'}), label='email')

    phone = forms.IntegerField(error_messages={'required':'phone is required'}, 
        widget = forms.NumberInput(attrs={'placeholder':'phone', 'class':'form-control'}), label='phone')
        
    address = forms.CharField(max_length=50, error_messages={'max_length':'Length must be within 50'}, 
        widget = forms.TextInput(attrs={'placeholder':'address', 'class':'form-control'}), label='address', required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone', 'address']


class UserEditForm(forms.Form):
    email = forms.EmailField(error_messages={'required':'email is required'}, 
        widget = forms.EmailInput(attrs={'placeholder':'email', 'class':'form-control'}), label='email')
    phone = forms.IntegerField(error_messages={'required':'phone is required'}, 
        widget = forms.NumberInput(attrs={'placeholder':'phone', 'class':'form-control'}), label='phone')
    first_name = forms.CharField(max_length=20, error_messages={'max_length':'Length must be within 20', 'required':'fisrt name is required'}, 
        widget = forms.TextInput(attrs={'placeholder':'first name', 'class':'form-control'}), label='fisrt_name')
    last_name = forms.CharField(max_length=20, error_messages={'max_length':'Length must be within 20', 'required':'last name is required'}, 
        widget = forms.TextInput(attrs={'placeholder':'last name', 'class':'form-control'}), label='last_name')
    address = forms.CharField(max_length=50, error_messages={'max_length':'Length must be within 50'}, 
        widget = forms.TextInput(attrs={'placeholder':'address', 'class':'form-control', }), label='address', required=False)

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name', 'address']
        
class DriverRegistrationForm(forms.Form):
    
    phone = forms.IntegerField(error_messages={'required':'Phone is required'}, 
        widget = forms.NumberInput(attrs={'placeholder':'Phone', 'class':'form-control'}), label='Phone', required=True)
    car_type = forms.ChoiceField(label='Car Type',
            widget= forms.Select(attrs={'placeholder':'Car Type', 'class':'form-control'}), 
            choices=(("Sedan", "Sedan"),
                    ("SUV", "SUV"),
                    ("Coupe", "Coupe"),
                    ("Van", "Van")),
            error_messages={'required':'Car Type is required'},  required=True
            )
    licenseNum = forms.CharField(error_messages={'required':'License Number is required'}, 
        widget = forms.TextInput(attrs={'placeholder':'License Number', 'class':'form-control'}), label='License Number',  required=True)
    plateNum = forms.CharField(error_messages={'required':'Plate Number is required'}, 
        widget = forms.TextInput(attrs={'placeholder':'Plate Number', 'class':'form-control'}), label='Plate Number',  required=True)
    max_pgers = forms.IntegerField(error_messages={'required':'Max Passenger is required'}, 
        widget = forms.NumberInput(attrs={'placeholder':'Max Passenger', 'class':'form-control'}), label='Max Passenger', required=True)
    special_info = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Special Information', 'class':'form-control'}), 
                                   label='Special Information', required=False)

    # class Meta:
    #     model = DriverInfo
    #     fields = ['phone', 'car_type', 'licenseNum', 'plateNum', 'max_pgers', 'special_info']
    #     widgets = {
    #         'phone': forms.NumberInput(attrs={'placeholder':'Phone', 'class':'form-control'}),
    #         'car_type': forms.TextInput(attrs={'placeholder':'Car Type', 'class':'form-control'}),
    #         'licenseNum': forms.TextInput(attrs={'placeholder':'License Number', 'class':'form-control'}),
    #         'max_pgers': forms.TextInput(attrs={'placeholder':'Max Passengers', 'class':'form-control'}),
    #         'special_info': forms.TextInput(attrs={'placeholder':'Special Information', 'class':'form-control'})
    #     }
        
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
            
        #     for name, field in self.fields.:
        #         field.widget.attrs = {'placeholder':field.label, 'class':'form-control'}
        #         # if name == "special_info":
        #         #     continue
        #         # field.error_messages = {'required': field.label+' is required'}

    