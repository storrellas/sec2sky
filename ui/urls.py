from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

# Set URL patterns
urlpatterns = []
urlpatterns += url('^console/', TemplateView.as_view(template_name="dronetrap/base.html"), name='console'),
urlpatterns += url('^test/', TemplateView.as_view(template_name="dronetrap/test.html"), name='console'),
urlpatterns += url('', TemplateView.as_view(template_name="registration/login.html"), name='index'),
