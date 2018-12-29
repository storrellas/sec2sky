from django.contrib import admin
from .models import Detection, SensorUser
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

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


class SensorUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = SensorUser
        fields = ('username', 'first_name' , 'last_name', )

class SensorUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = SensorUser

class SensorUserAdmin(UserAdmin):
    #add_form = SensorUserCreationForm
    form = SensorUserChangeForm
    model = SensorUser

    fieldsets = UserAdmin.fieldsets + (
            ('Extended', {'fields': ('company', 'role',)}),
    )

# Re-register UserAdmin
admin.site.register(SensorUser, SensorUserAdmin)
