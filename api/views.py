# Django importts
from django.shortcuts import render

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Project
from .serializers import DetectionSerializer
from .models import Detection

# Create your views here.
class DetectionViewSet(viewsets.ModelViewSet):
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    authentication_classes = (BasicAuthentication,)
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

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    renderer_classes = (JSONRenderer, )
