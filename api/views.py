# Python imports
import json

# Django imports
from django.shortcuts import render
from django.conf import settings

# REST framework
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework import mixins

# MQTT
from paho.mqtt import publish

# Project
from . import serializers
from .models import Detection, SensorUser, SensorGroup, Sensor, Company
from sec2sky import utils

logger = utils.get_logger()

class CompanyViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    model = Company
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    renderer_classes = (JSONRenderer, )

class SensorUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    model = SensorUser
    queryset = SensorUser.objects.all()
    serializer_class = serializers.SensorUserExtendedSerializer
    renderer_classes = (JSONRenderer, )

    def create(self, request, format=None):
        serializer = serializers.SensorUserSerializer(data=request.data)
        user = SensorUser.objects.create_user(**serializer.validated_data)

        # Return complete response
        serializer = serializers.SensorUserExtendedSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def whoami(self, request, pk=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

class SensorGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    model = SensorGroup
    queryset = SensorGroup.objects.all()
    serializer_class = serializers.SensorGroupExtendedSerializer
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        logger.info("Get Queryset for user '" + str(self.request.user) +  "'")
        return self.model.objects.filter(managers=self.request.user)

class SensorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Sensor
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorExtendedSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=True, methods=['get'])
    def detection(self, request, pk=None):
        queryset = Detection.objects.filter(sensor__pk=pk)
        serializer = serializers.DetectionSerializer(queryset, many=True)
        return Response(serializer.data)

class DetectionListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DetectionSerializer
    renderer_classes = (JSONRenderer, )


    def get_queryset(self):
        sensor = self.kwargs['sensor']
        return Detection.objects.filter(sensor__pk=sensor)


class MQTTTestAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        # MQTT publish message
        publish.single(request.data['topic'], json.dumps(request.data['payload']), hostname=settings.MQTT['hostname'])

        # Return generic response
        return Response({'response': 'ok'})
