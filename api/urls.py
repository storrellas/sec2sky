# Django imports
from django.conf.urls import url, include

# Restframework imports
from rest_framework import routers
from rest_framework.authtoken import views

# Project imports
from .views import *

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'swarm', SwarmViewSet, basename='swarm')
router.register(r'sensor', SensorViewSet, basename='sensor')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    url(r'^', include(router.urls)),
    url('^test/mqtt/$', MQTTTestAPIView.as_view()),
    url(r'^auth/', views.obtain_auth_token, name='api-token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
