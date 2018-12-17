# Dependencies
from rest_framework import serializers

# Project imports
from .models import Detection

class DetectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'
