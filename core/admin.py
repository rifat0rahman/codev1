from django.contrib import admin
from .models import TM_INTERVAL, TOTP, Device,Authenticate,IntervalTwenty

# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['location_ID','seed','otp']

class TOTPAdmin(admin.ModelAdmin):
    list_display = ["totp",'seed','created']

class TMAdmin(admin.ModelAdmin):
    list_display = ["totp",'seed','created']

admin.site.register(Device,DeviceAdmin)
admin.site.register(Authenticate)

admin.site.register(TOTP,TOTPAdmin)

# intervals
admin.site.register(TM_INTERVAL,TMAdmin)
admin.site.register([IntervalTwenty])