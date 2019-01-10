# Django
from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

# Project includes
from .models import *

app_models = apps.get_app_config('api').get_models()
for model in app_models:
    try:
        if( model == get_user_model() ):
            # Custom Forms are required
            pass
        else:
            admin.site.register(model)
    except AlreadyRegistered:
        pass


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name' , 'last_name', )

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(UserAdmin):
    #add_form = UserCreationForm
    form = UserChangeForm
    model = User

    fieldsets = UserAdmin.fieldsets + (
            ('Extended', {'fields': ('company', 'role',)}),
    )

# Re-register UserAdmin
admin.site.register(User, UserAdmin)
