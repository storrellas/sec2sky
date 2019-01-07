# Dependencies
from rest_framework import serializers

# Project imports
from .models import Detection, SensorUser, Company, Sensor

class SensorGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description')

class SensorUserSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    sensor_groups = SensorGroupSerializer(source='sensor_groups_set', many=True)
    class Meta:
        model = SensorUser
        #fields = '__all__'
        fields = ('id', 'username', 'role', 'company', 'sensor_groups')

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class SensorGroupExtendedSerializer(serializers.ModelSerializer):
    sensor_list = SensorSerializer(source='sensor_set', many=True)
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'sensor_list')


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model(**validated_data)

class SensorExtendedSerializer(serializers.ModelSerializer):
    n_detection = serializers.SerializerMethodField()

    def get_n_detection(self, obj):
        #return "Foo id: %i" % obj.pk
        return Detection.objects.filter(sensor=obj).count()

    class Meta:
        model = Sensor
        fields = '__all__'
