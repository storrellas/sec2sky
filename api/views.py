# Django importts
from django.shortcuts import render

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Project
from .serializers import DetectionSerializer, SensorUserSerializer
from .serializers import SensorGroupExtendedSerializer, SensorExtendedSerializer
from .models import Detection, SensorUser, SensorGroup, Sensor
from sec2sky import utils

logger = utils.get_logger()

class SensorUserViewSet(viewsets.ModelViewSet):
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    #authentication_classes = (BasicAuthentication,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """
    retrieve:
        Return a single item of Detection

    list:
        Return a list of Detection

    create:
        Creates a Detection model

    destroy:
        Delete a Detection model

    update:
        Update a Detection model

    partial_update:
        Update a Detection model
    """

    model = SensorUser
    queryset = SensorUser.objects.all()
    serializer_class = SensorUserSerializer
    renderer_classes = (JSONRenderer, )


# Create your views here.
class SensorGroupViewSet(viewsets.ModelViewSet):
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    #authentication_classes = (BasicAuthentication,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """
    retrieve:
        Return a single item of Detection

    list:
        Return a list of Detection

    create:
        Creates a Detection model

    destroy:
        Delete a Detection model

    update:
        Update a Detection model

    partial_update:
        Update a Detection model
    """

    model = SensorGroup
    queryset = SensorGroup.objects.all()
    serializer_class = SensorGroupExtendedSerializer
    renderer_classes = (JSONRenderer, )


class SensorViewSet(viewsets.ModelViewSet):
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    #authentication_classes = (BasicAuthentication,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """
    retrieve:
        Return a single item of Detection

    list:
        Return a list of Detection

    create:
        Creates a Detection model

    destroy:
        Delete a Detection model

    update:
        Update a Detection model

    partial_update:
        Update a Detection model
    """

    model = Sensor
    queryset = Sensor.objects.all()
    serializer_class = SensorExtendedSerializer
    renderer_classes = (JSONRenderer, )


class DetectionViewSet(viewsets.ModelViewSet):
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    #authentication_classes = (BasicAuthentication,)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """
    retrieve:
        Return a single item of Detection

    list:
        Return a list of Detection

    create:
        Creates a Detection model

    destroy:
        Delete a Detection model

    update:
        Update a Detection model

    partial_update:
        Update a Detection model
    """

    model = Detection
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        logger.info("Get Queryset for user '" + str(self.request.user) +  "'")
        return self.model.objects.filter(owner=self.request.user)
