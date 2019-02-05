# Django imports
from django.conf.urls import url, include

# Restframework imports
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Project imports
from .views import *

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'swarm', SwarmViewSet, basename='swarm')
router.register(r'sensor', SensorViewSet, basename='sensor')
router.register(r'user', UserViewSet, basename='user')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^test/mqtt/$', MQTTTestAPIView.as_view()),
    url(r'^roles/$', RolesView.as_view()),
    url(r'^token/$', Sec2SkyTokenObtainPairView.as_view(), name='api-token'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='api-token-refresh'),
    url(r'^token/verify/$', TokenVerifyView.as_view(), name='api-token-refresh'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
