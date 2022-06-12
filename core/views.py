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

# Create your views here.

################################ this is the device api  ##############################


@api_view(["GET", "POST"])
def device(request):
    totp = TOTP.objects.all()
    serializers = TotpSerializer(totp, many=True)

    return Response(serializers.data, status=200)


@api_view(["GET", "POST"])
def device_tm(request):
    device = TM_INTERVAL.objects.all()
    serializers = TotpSerializer(device, many=True)

    return Response(serializers.data, status=200)
################################## authenticaton api ############################


@api_view(["POST"])
def authenticate(request):
    if request.method == 'POST':
        image = request.FILES
        d1 = json.dumps(image)
        # print(json.loads(image))
        # image = cv2.imread(image)
        
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
        

    q = qrcode.make(device.otp)

    image = io.BytesIO()
    q.save(stream=image)
    base64_image = base64.b64encode(image.getvalue()).decode()

    main_code = 'data:image/png;utf8;base64,' + base64_image

    context = {
        'qr_name': main_code,
        'otp': totp.now()
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
        # device.seed = pyotp.random_base32()
        totp = pyotp.TOTP(device.seed)
        device.otp = totp.now()
        device.save()

        #save the seed and otp for 10 minutes period
        TM_INTERVAL.objects.create(totp=device.otp,seed=device.seed)
        

    q = qrcode.make(device.otp)

    image = io.BytesIO()
    q.save(stream=image)
    base64_image = base64.b64encode(image.getvalue()).decode()

    main_code = 'data:image/png;utf8;base64,' + base64_image

    context = {
        'qr_name': main_code,
        'otp': totp.now()
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
            detector = cv2.QRCodeDetector()
            data, vertices_array, binary_qrcode = detector.detectAndDecode(pic)

            if vertices_array is not None:
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



## action part here
def actions(locationid):

    if locationid == 7:

        # do the actions part here for the location id seven
       
        print('this is location id seven')

    print(locationid)