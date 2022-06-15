from rest_framework import serializers
from .models import TOTP,TM_INTERVAL


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOTP
        fields = ('totp','seed','created')


class TotpSerializer(serializers.ModelSerializer):
    
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = TM_INTERVAL
        fields = ('totp','image_url')

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.barcode.url)