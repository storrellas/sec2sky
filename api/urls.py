# Django imports
from django.conf.urls import url, include

# Restframework imports
from rest_framework import routers
from rest_framework.authtoken import views

# Project imports
from .views import DetectionViewSet, SensorUserViewSet, SensorGroupViewSet

router = routers.DefaultRouter()
router.register(r'detection', DetectionViewSet)
router.register(r'user', SensorUserViewSet)
router.register(r'sensorgroup', SensorGroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
