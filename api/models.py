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
    device_id = models.CharField(max_length=100, null=True)
    serial_num = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    version = models.CharField(max_length=100, null=True)
    available = models.BooleanField(default=True)
    energy = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.serial_num

class Detection(models.Model):

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500, null=True)
    thread_id = models.IntegerField(null=True)
    home_latitude = models.DecimalField(max_digits=20, null=True, decimal_places=10)
    home_longitude = models.DecimalField(max_digits=20, null=True, decimal_places=10)
    latitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    altitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    rssi = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    signal_type = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.description

class Status(models.Model):

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    latitude = models.DecimalField(max_digits=20, null=True, decimal_places=10)
    longitude = models.DecimalField(max_digits=20, null=True, decimal_places=10)
    orientation = models.DecimalField(max_digits=20, null=True, decimal_places=10)
    wifi_status = models.CharField(max_length=20, null=True)
    rf0_status = models.CharField(max_length=20, null=True)
    rf1_status = models.CharField(max_length=20, null=True)
    gps_status = models.CharField(max_length=20, null=True)
    gps_sats = models.CharField(max_length=20, null=True)
    cpu = models.CharField(max_length=20, null=True)
    temp = models.CharField(max_length=20, null=True)
    ram_total = models.IntegerField(default=0)
    ram_used = models.IntegerField(default=0)
    ram_free = models.IntegerField(default=0)
    disk_total = models.CharField(max_length=20, null=True)
    disk_used = models.CharField(max_length=20, null=True)
    disk_free = models.CharField(max_length=20, null=True)
    disk_percent = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.sensor
