# Dependencies
from rest_framework import serializers

# Project imports
from .models import Detection, SensorUser

class SensorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorUser
        fields = '__all__'

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'
