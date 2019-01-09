# Dependencies
from rest_framework import serializers

# Project imports
from .models import *

class SensorSwarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorSwarm
        fields = ('id', 'name', 'description')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description')

class SensorUserExtendedSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(required=False, source='company')
    sensor_swarms = SensorSwarmSerializer(required=False, source='sensor_swarms_set', many=True)

    class Meta:
        model = SensorUser
        #fields = '__all__'
        fields = ('id', 'username', 'role', 'company_detail', 'sensor_swarms')

class SensorUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = SensorUser
        fields = ('id', 'username', 'password', 'role', 'company')

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class SensorSwarmExtendedSerializer(serializers.ModelSerializer):
    sensor_list_detail = SensorSerializer(required=False, source='sensor_set', many=True)
    sensor_user_set = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=True)
    class Meta:
        model = SensorSwarm
        fields = ('id', 'name', 'description', 'sensor_list_detail', 'sensor_user_set')

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class SensorExtendedSerializer(serializers.ModelSerializer):
    n_detection = serializers.SerializerMethodField()
    n_status = serializers.SerializerMethodField()

    def get_n_detection(self, obj):
        return Detection.objects.filter(sensor=obj).count()

    def get_n_status(self, obj):
        #return "Foo id: %i" % obj.pk
        return Status.objects.filter(sensor=obj).count()

    class Meta:
        model = Sensor
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)
