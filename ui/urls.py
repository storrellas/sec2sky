from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

# Set URL patterns
urlpatterns = []
urlpatterns += url('', TemplateView.as_view(template_name="registration/login.html"), name='index'),
