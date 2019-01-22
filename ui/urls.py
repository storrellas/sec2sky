from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

# Set URL patterns
urlpatterns = []
urlpatterns += url('^console/', TemplateView.as_view(template_name="dronetrap/console.html"), name='console'),
urlpatterns += url('^test/', TemplateView.as_view(template_name="dronetrap/console_old.html"), name='console'),
urlpatterns += url('', TemplateView.as_view(template_name="registration/login.html"), name='index'),
