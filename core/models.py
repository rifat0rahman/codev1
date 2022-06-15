from django.db import models
import pyotp
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import os

# Create your models here.

class Device(models.Model):
    location_ID = models.AutoField(primary_key=True)
    seed = models.CharField(max_length=50,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=50,default=00,null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.seed:
            self.seed = pyotp.random_base32()
        
        return super(Device,self).save(*args, **kwargs)

    
    def __str__(self) -> str:
        display = f'{self.seed}'
        return display


class Authenticate(models.Model):
    location_ID = models.AutoField(primary_key=True)
    totp = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
        display = f'{self.location_ID} + {self.totp} + {self.created}'
        return display


class TOTP(models.Model):
    totp = models.CharField(max_length=50)
    seed = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    barcode = models.ImageField(upload_to='barcodeImages',blank=True,null=True)
    # created.editable = True

    def __str__(self) -> str:
        display = f'{self.totp} + {self.seed}'
        return display

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('code128')
        ean = EAN(f'{self.totp}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'{self.seed}{self.totp}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)



class TM_INTERVAL(models.Model):
    totp = models.CharField(max_length=50)
    seed = models.CharField(max_length=50)
    barcode = models.ImageField(upload_to='barcodeImages',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    # created.editable = True

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('code128')
        ean = EAN(f'{self.totp}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'{self.seed}{self.totp}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)
    

    def __str__(self) -> str:
        display = f'{self.totp} + {self.seed}'
        return display


class IntervalTwenty(models.Model):
    name = models.CharField(max_length=50,default='50')
    start_time = models.TimeField(auto_now_add=True)
    session = models.CharField(max_length=50)

    reached = models.BooleanField(default=False)

    # start_time.editable = True


class IntervalTwenty2(models.Model):
    name = models.CharField(max_length=50,default='60')
    start_time = models.TimeField(auto_now_add=True)
    session = models.CharField(max_length=50)

    reached = models.BooleanField(default=False)

    # start_time.editable = True