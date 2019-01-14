# Django includes
from django.urls import reverse

# Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Project includes
from .models import *

class TestCase(APITestCase):

    def setUp(self):

        # Create superuser
        self.admin = User.objects.create_user('admin', password='admin')
        self.admin.is_superuser=True
        self.admin.is_staff=True
        self.admin.save()

        # Create Company
        self.company = Company.objects.create(name="MyCompany",description="MyDescription")

        # Create user
        self.user = User.objects.create_user('user', password='user', company=self.company)

        # Create Sensor Swarm
        self.swarm = Swarm.objects.create(name='swarm', description='swarm_description')
        self.swarm.user_set.set([self.user])

        # Create Sensor
        self.sensor = Sensor.objects.create(name='CMF001',
                                            description='CMF001_description',
                                            latitude = 2.3,
                                            longitude = 2.3)

        # Detection/Status
        self.detection = Detection.objects.create(sensor=self.sensor,
                                                  description='MyDescription',
                                                  latitude = 2.3,
                                                  altitude = 2.3,
                                                  longitude = 2.3,
                                                  home_latitude = 2.3,
                                                  home_longitude = 2.3,
                                                  rssi=2.3)
        self.detection = Detection.objects.create(sensor=self.sensor,
                                                  description='MyDescription2',
                                                  latitude = 2.3,
                                                  altitude = 2.3,
                                                  longitude = 2.3,
                                                  home_latitude = 2.3,
                                                  home_longitude = 2.3,
                                                  rssi=2.3)
        self.status = Status.objects.create(sensor=self.sensor,
                                            code='MyDescription',
                                            description='MyDescription')

    def set_jwt(self, username, password):
        # Get JWT
        url = reverse('api-token')
        data = { 'username' : username, 'password': password }
        response = self.client.post(url, data, format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_sensor(self):
        """
        Company Creation
        """
        self.assertEqual(Sensor.objects.count(), 1)

        # Get token header
        self.set_jwt(username='user', password='user')

        # Get Sensor
        url = reverse('sensor-list')
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'CMF001')
        self.assertEqual(response.data[0]['n_detection'], 2)
        self.assertEqual(response.data[0]['n_status'], 1)

        # Store ID
        id = response.data[0]['id']

        # Get Detection
        url = reverse('sensor-detection', args=[id])
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Get Detection
        url = reverse('sensor-status', args=[id])
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Check no sensors in swarm
        url = reverse('swarm-detail', args=[id])
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sensor_list_detail']), 0)


        # Assign to Swarm
        url = reverse('sensor-detail', args=[id])
        data = {
            "n_detection": 0,
            "name": "CMF001",
            "description": "Development Dept. Sensor1",
            "latitude": "43.20",
            "longitude": "2.10",
            "swarm": self.swarm.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sensor.objects.get(pk=id).swarm, self.swarm)

        # Get Swarm
        url = reverse('swarm-detail', args=[id])
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sensor_list_detail']), 1)
