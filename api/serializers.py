# Dependencies
from rest_framework import serializers

# Project imports
from .models import Detection

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'
