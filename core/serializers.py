from rest_framework import serializers
from .models import TOTP


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOTP
        fields = ('totp','seed','created')

class TotpSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOTP
        fields = ('totp','seed','created')