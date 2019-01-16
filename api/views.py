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
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

# MQTT
from paho.mqtt import publish

# Project
from . import serializers
from .models import *
from sec2sky import utils

logger = utils.get_logger()

class CompanyViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    model = Company
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    renderer_classes = (JSONRenderer, )

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

    model = User
    queryset = User.objects.all()
    serializer_class = serializers.UserExtendedSerializer
    renderer_classes = (JSONRenderer, )

    def create(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)

            # Generate response
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, format=None):

        user = User.objects.get(pk=pk)
        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid() and user is not None:
            serializer.save()

            # Update password
            user.set_password(serializer.data['password'])
            user.save()

            # Generate response
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def whoami(self, request, pk=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SwarmViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Swarm
    queryset = Swarm.objects.all()
    serializer_class = serializers.SwarmExtendedSerializer
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        logger.info("Get Queryset for user '" + str(self.request.user) +  "'")
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user_set=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def user(self, request, pk=None):

        # TODO: Check whether all users belong to same company
        #raise APIException("My first exception")
        #User.objects.filter(pk__in=[3, 4]).values_list('company', flat=True)
        #request.user.company_id

        # Assign new user_set
        swarm = self.model.objects.get(pk=pk)
        swarm.user_set.set(request.data['user_set'])
        serializer = self.serializer_class(swarm)
        return Response(serializer.data)

class SensorViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    model = Sensor
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorExtendedSerializer
    renderer_classes = (JSONRenderer, )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, *kwargs)

        # Notify sensor if unassigned
        sensor = self.get_object()
        if sensor.swarm is None:
            logger.info("Swarm is None. Notifying sensor for unset")
            topic = settings.MQTT['topic_manager_unset'].replace('+', str(settings.MQTT['id']))
        else:
            logger.info("Swarm is None. Notifying sensor for set")
            topic = settings.MQTT['topic_manager_set'].replace('+', str(settings.MQTT['id']))

        # MQTT  message
        serializer = serializers.SensorSerializer(sensor)
        publish.single(topic, json.dumps(serializer.data), hostname=settings.MQTT['hostname'])

        return response




    @action(detail=True, methods=['get'])
    def detection(self, request, pk=None):
        queryset = Detection.objects.filter(sensor__pk=pk)
        serializer = serializers.DetectionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        queryset = Status.objects.filter(sensor__pk=pk)
        serializer = serializers.StatusSerializer(queryset, many=True)
        return Response(serializer.data)


# class DetectionListAPIView(ListAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = serializers.DetectionSerializer
#     renderer_classes = (JSONRenderer, )
#
#     def get_queryset(self):
#         sensor = self.kwargs['sensor']
#         return Detection.objects.filter(sensor__pk=sensor)


class MQTTTestAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        # MQTT publish message
        publish.single(request.data['topic'], json.dumps(request.data['payload']), hostname=settings.MQTT['hostname'])

        # Return generic response
        return Response({'response': 'ok'})
