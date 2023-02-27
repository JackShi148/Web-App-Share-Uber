from django.db import models
from django.contrib.auth.models import User

class RiderInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='phone', max_length=11, null=True, blank=True)
    address = models.CharField(verbose_name='address', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

class DriverInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='phone', max_length=11, null=True, blank=True)
    car_choice = (
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("Coupe", "Coupe"),
        ("Van", "Van")
    )
    car_type = models.CharField(verbose_name='car_type', max_length=10, choices=car_choice)
    licenseNum = models.CharField(verbose_name='licenseNum', max_length=100)
    plateNum = models.CharField(verbose_name='plateNum', max_length=100)
    max_pgers = models.IntegerField(verbose_name='max_pgers')
    special_info = models.CharField(verbose_name='special_information', max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username



