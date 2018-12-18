from rest_framework import routers
from .views import DetectionViewSet
from django.conf.urls import url, include
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register(r'detection', DetectionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', views.obtain_auth_token)
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
