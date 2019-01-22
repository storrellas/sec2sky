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
class User(AbstractUser):
    VIEWER = 'viewer'
    OPERATOR = 'operator'
    CONFIGURATOR = 'configurator'
    ADMINISTRATOR = 'administrator'
    EMPOWERED = 'empowered'
    S2S_MANAGER = 's2s_manager'
    S2S_TECHNICIAN = 's2s_technician'
    ROLE_CHOICES = (
        (VIEWER, 'viewer'),
        (OPERATOR, 'operator'),
        (CONFIGURATOR, 'configurator'),
        (ADMINISTRATOR, 'administrator'),
        (EMPOWERED, 'empowered'),
        (S2S_MANAGER, 's2s_manager'),
        (S2S_TECHNICIAN, 's2s_technician'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=VIEWER,)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class SessionUser(models.Model):
    remote_addr = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20, null=True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'SessionUser'
        verbose_name_plural = 'SessionUsers'

class Swarm(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    user_set = models.ManyToManyField(User, related_name="swarm_set", blank=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    swarm = models.ForeignKey(Swarm, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    latitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)

    def __str__(self):
        return self.name

class Detection(models.Model):

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500, null=True)
    thread_id = models.IntegerField(null=True)
    home_latitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    home_longitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    latitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    altitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    rssi = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    signal_type = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class Status(models.Model):

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
