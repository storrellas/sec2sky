from django.contrib import admin
from .models import Detection
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

app_models = apps.get_app_config('api').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass


# admin.site.register(Detection)
# admin.site.register(Detection)
