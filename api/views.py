# Django importts
from django.shortcuts import render

# Dependencies
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

# Project
from .serializers import DetectionSerializer
from .models import Detection

# Create your views here.
class DetectionViewSet(viewsets.ModelViewSet):
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
    #renderer_classes = (JSONRenderer, )
