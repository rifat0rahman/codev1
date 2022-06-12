from django.urls import path
from . import views

urlpatterns = [
    path('api/device',views.device),

    # update devices
    path('api/device-tm',views.device_tm),
    # update ends here
    
    path("api/authenticate",views.authenticate, name="auth"),

    #templates
    path('',views.auth, name="authen"),
    path("<int:locationID>",views.home, name="home"),
    path("tm/<int:locationID>",views.tminterval, name="tm"),

]
