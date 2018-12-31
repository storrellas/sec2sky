# Django imports
from django.conf.urls import url, include

# Restframework imports
from rest_framework import routers
from rest_framework.authtoken import views

# Project imports
from .views import SensorUserAPIView, DetectionListAPIView
from .views import SensorGroupViewSet, SensorViewSet
#from .views import DetectionViewSet



router = routers.DefaultRouter()
router.register(r'sensorgroup', SensorGroupViewSet)
router.register(r'sensor', SensorViewSet)
#router.register(r'detection', DetectionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^user/', SensorUserAPIView.as_view()),
    url('^sensor/(?P<sensor>.+)/detection/$', DetectionListAPIView.as_view()),
    url(r'^auth/', views.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
