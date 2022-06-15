import json
from tokenize import Token
from django.db import reset_queries
from django.shortcuts import redirect, render, resolve_url
from .serializers import DeviceSerializer,TotpSerializer
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import TM_INTERVAL, TOTP, Device, Authenticate, IntervalTwenty
from django.conf import settings

# for the qr code
from django.core.files import File
import urllib
from django.core.files.base import ContentFile
import os
import io
import base64
import qrcode
from PIL import Image
import cv2
import pyotp
import numpy as np

# for writing barocdes
import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
import cv2
import numpy as np
from pyzbar.pyzbar import decode
# Create your views here.

################################ this is the device api  ##############################

@api_view(["GET", "POST"])
def device(request):
    totp = TOTP.objects.all()
    serializers = TotpSerializer(totp, many=True,context={"request":request})

    return Response(serializers.data, status=200)


@api_view(["GET", "POST"])
def device_tm(request):

    device = TM_INTERVAL.objects.all()
    serializers = TotpSerializer(device, many=True,context={"request":request})

    return Response(serializers.data, status=200)
################################## authenticaton api ############################


@api_view(["POST"])
def authenticate(request):
    if request.method == 'POST':
        image = request.FILES
        d1 = json.dumps(image)
        
        return Response({'status': 'working'})

    return Response({'status': 'something'})


import datetime
################################## home view and logic ##############################
def home(request, locationID):

    # deleting codes in 10 minutes here
    for item in TM_INTERVAL.objects.all():
        created = item.created
        gap = datetime.timedelta(minutes=10)
        expiration = created + gap
        current_time = datetime.datetime.utcnow().time()
        
        if expiration.time() < current_time:
            print('deleted for 10 minutes interval')
            item.delete()



    # deleting the items for the previous day.
    for item in TOTP.objects.all():
        created_day = item.created.date()
        today = datetime.datetime.today().date()

        if created_day < today:
            print('deleted for 24 hours')
            item.delete()


    device = Device.objects.get(location_ID=locationID)

    totp = pyotp.TOTP(device.seed)


    if device.otp != totp.now():
        # device.seed = pyotp.random_base32()
        totp = pyotp.TOTP(device.seed)
        device.otp = totp.now()
        device.save()

        #save the seed and otp for 24 hours period
        TOTP.objects.create(totp=device.otp,seed=device.seed)
        
    barcode_image = TOTP.objects.latest('created')

    context = {
        'barcode_image': barcode_image,
        'otp': totp.now
    }

    return render(request, 'device.html', context)



def tminterval(request, locationID):

    # deleting codes in 10 minutes here
    for item in TM_INTERVAL.objects.all():
        created = item.created
        gap = datetime.timedelta(minutes=10)
        expiration = created + gap
        current_time = datetime.datetime.utcnow().time()
        
        if expiration.time() < current_time:
            item.delete()

    # deleting the items for the previous day.
    for item in TOTP.objects.all():
        created_day = item.created.date().day
        today = datetime.datetime.today().day
        
        if created_day < today:
            item.delete()


    device = Device.objects.get(location_ID=locationID)

    totp = pyotp.TOTP(device.seed)


    if device.otp != totp.now():
        
        totp = pyotp.TOTP(device.seed)
        device.otp = totp.now()
        device.save()

        #save the seed and otp for 10 minutes period
        tm_instance = TM_INTERVAL(totp=device.otp,seed=device.seed)
        tm_instance.save()

    barcode_image = TM_INTERVAL.objects.latest('created')

    context = {
        'barcode_image': barcode_image,
        'otp': totp.now
    }

    return render(request, 'device.html', context)



# import RPi.GPIO as GPIO
# from time import sleep


######################## authentication logic ####################################
def auth(request):

    if request.method == 'POST':

        device = None
        
        try:

            image = request.FILES.get('image')
            
            pic = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            
            data = decoder(pic)
        
    
            if data is not None:
                try:
                    device = TOTP.objects.get(totp=data)
                except:
                    device = TM_INTERVAL.objects.get(totp=data)
        except:
            pass
    

        try:
            code = request.POST.get("totp")
            try:
                device = TOTP.objects.get(totp=code)
            except:
                device = TM_INTERVAL.objects.get(totp=code)
        except:
            pass

        

        if device is not None:
            auth, created = Authenticate.objects.get_or_create(totp=device.totp)
            auth.save()

            ######## assigning to a specific actions #########
            location = Device.objects.get(seed = device.seed)
            actions(location.location_ID)

            ########## SOLENOI.PY HERE #######################




            ################ SOLENOI.PY HERE ###################

            messages.success(request, f'Authentication Successfully done | code - {device.totp}')

            device.delete()

            return render(request, 'auth.html')

        if not device:
            messages.error(request, 'Authentication is not accepted')
            return render(request, 'auth.html')

    return render(request, 'auth.html')



def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        print(barcodeData)
        return barcodeData



## action part here
def actions(locationid):

    if locationid == 7:

        # do the actions part here for the location id seven
       
        print('this is location id seven')

    print(locationid)



