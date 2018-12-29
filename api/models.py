from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

class Company(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name


# See https://wsvincent.com/django-custom-user-model-tutorial/
class SensorUser(AbstractUser):
    VIEWER = 'VI'
    OPERATOR = 'OP'
    CONFIGURATOR = 'CO'
    ADMINISTRATOR = 'AD'
    EMPOWERED = 'EM'
    S2S_MANAGER = 'SM'
    S2S_TECHNICIAN = 'ST'
    ROLE_CHOICES = (
        (VIEWER, 'viewer'),
        (OPERATOR, 'operator'),
        (CONFIGURATOR, 'configurator'),
        (ADMINISTRATOR, 'administrator'),
        (EMPOWERED, 'empowered'),
        (S2S_MANAGER, 's2s_manager'),
        (S2S_TECHNICIAN, 's2s_technician'),
    )

    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=VIEWER,)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'SensorUser'
        verbose_name_plural = 'SensorUsers'

class SensorGroup(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    managers = models.ManyToManyField(SensorUser, blank=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    sensor_group = models.ForeignKey(SensorGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Detection(models.Model):

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500, null=True)
    thread_id = models.IntegerField(null=True)
    home_latitude = models.DecimalField(max_digits=5, decimal_places=2)
    home_longitude = models.DecimalField(max_digits=5, decimal_places=2)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    altitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    rssi = models.DecimalField(max_digits=5, decimal_places=2)
    signal_type = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
