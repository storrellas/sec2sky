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

# MQTT
from paho.mqtt import publish

# Project
from .serializers import DetectionSerializer, SensorUserSerializer
from .serializers import SensorGroupExtendedSerializer, SensorExtendedSerializer
from .models import Detection, SensorUser, SensorGroup, Sensor
from sec2sky import utils

logger = utils.get_logger()

class SensorUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    model = SensorUser
    queryset = SensorUser.objects.all()
    serializer_class = SensorUserSerializer
    renderer_classes = (JSONRenderer, )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def whoami(self, request, pk=None):
        serializer = SensorUserSerializer(request.user)
        return Response(serializer.data)

class SensorGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    model = SensorGroup
    queryset = SensorGroup.objects.all()
    serializer_class = SensorGroupExtendedSerializer
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        logger.info("Get Queryset for user '" + str(self.request.user) +  "'")
        return self.model.objects.filter(managers=self.request.user)


class SensorViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Sensor
    queryset = Sensor.objects.all()
    serializer_class = SensorExtendedSerializer
    renderer_classes = (JSONRenderer, )

    # def list(self, request):
    #     queryset = self.model.objects.all()
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def detection(self, request, pk=None):
        queryset = Detection.objects.filter(sensor__pk=pk)
        serializer = DetectionSerializer(queryset, many=True)
        return Response(serializer.data)

class DetectionListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DetectionSerializer
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
