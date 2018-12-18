from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Detection(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
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
