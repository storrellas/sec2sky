from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

# Set URL patterns
urlpatterns = []
urlpatterns += url('^console', TemplateView.as_view(template_name="dronetrap/console.html"), name='ui-console'),
urlpatterns += url('^profile', TemplateView.as_view(template_name="dronetrap/profile.html"), name='ui-profile'),
urlpatterns += url('^company', TemplateView.as_view(template_name="dronetrap/company.html"), name='ui-company'),
urlpatterns += url('^user', TemplateView.as_view(template_name="dronetrap/user.html"), name='ui-user'),
urlpatterns += url('^swarm', TemplateView.as_view(template_name="dronetrap/swarm.html"), name='ui-swarm'),
urlpatterns += url('^test', TemplateView.as_view(template_name="dronetrap/console_old.html"), name='console'),
urlpatterns += url('', TemplateView.as_view(template_name="registration/login.html"), name='ui-login'),
