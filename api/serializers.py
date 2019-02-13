# Dependencies
from rest_framework import serializers

# Project imports
from .models import *

class SwarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swarm
        fields = ('id', 'name', 'description')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description')

class UserExtendedSerializer(serializers.ModelSerializer):
    company_detail = CompanySerializer(required=False, source='company')
    swarms = SwarmSerializer(required=False, source='swarms_set', many=True)

    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id', 'username', 'role', 'company_detail', 'swarms')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'company')

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user

class CompanyExtendedSerializer(serializers.ModelSerializer):
    user_list_detail = UserSerializer(required=False, source='user_set', many=True)
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'user_list_detail')

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class SwarmExtendedSerializer(serializers.ModelSerializer):
    sensor_list_detail = SensorSerializer(required=False, source='sensor_set', many=True)
    user_set = serializers.PrimaryKeyRelatedField(required=False, many=True, read_only=True)
    class Meta:
        model = Swarm
        fields = ('id', 'name', 'description', 'sensor_list_detail', 'user_set')

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class SensorExtendedSerializer(serializers.ModelSerializer):
    n_detection = serializers.SerializerMethodField()
    n_status = serializers.SerializerMethodField()
    swarm = SwarmSerializer()
    last_status = serializers.SerializerMethodField()

    def get_n_detection(self, obj):
        return Detection.objects.filter(sensor=obj).count()

    def get_n_status(self, obj):
        return Status.objects.filter(sensor=obj).count()

    def get_last_status(self, obj):
        status = Status.objects.filter(sensor=obj).first()
        if status is None:
            return {}
        else:
            serializer = StatusSerializer(status)
            return serializer.data

    class Meta:
        model = Sensor
        fields = '__all__'
