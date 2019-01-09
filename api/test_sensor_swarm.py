# Django includes
from django.urls import reverse

# Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Project includes
from .models import *

class UserTestCase(APITestCase):

    def setUp(self):

        # Create superuser
        self.admin = SensorUser.objects.create_user('admin', password='admin')
        self.admin.is_superuser=True
        self.admin.is_staff=True
        self.admin.save()

        # Create Company
        self.company = Company.objects.create(name="MyCompany",description="MyDescription")

        # Create user
        self.user = SensorUser.objects.create_user('user', password='user', company= self.company)

        # Create Sensor Swarm
        self.sensor_swarm = SensorSwarm.objects.create(name='sensor_swarm', description='sensor_swarm_description')
        self.sensor_swarm.sensor_user_set.set([self.user])

    def test_sensorswarm_crud(self):
        """
        Company Creation
        """
        self.assertEqual(SensorSwarm.objects.count(), 1)

        # Set token header
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create Swarm
        url = reverse('sensorswarm-list')
        data = {
            'name' : "sensor_swarm_new",
            'description': "sensor swarm description new"
        }
        response = self.client.post(url, data, format='json')

        # Store ID
        id = response.data['id']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SensorSwarm.objects.count(), 2)
        self.assertEqual(SensorSwarm.objects.get(pk=id).name, 'sensor_swarm_new')

        # Update Swarm
        url = reverse('sensorswarm-detail', args=[id])
        data = {
            'name' : "sensor_swarm_updated",
            'description': "sensor_swarm_updated"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SensorSwarm.objects.count(), 2)
        self.assertEqual(SensorSwarm.objects.get(pk=id).name, 'sensor_swarm_updated')

        # Swarm List - admin
        url = reverse('sensorswarm-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Set token header
        token = Token.objects.get(user__username='user')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Swarm List - user
        url = reverse('sensorswarm-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Set token header
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Delete Swarm
        url = reverse('sensorswarm-detail', args=[id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorSwarm.objects.count(), 1)



    def test_sensorswarm_sensoruser(self):
        """
        Company Creation
        """

        # Get token header
        token = Token.objects.get(user__username='user')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.sensor_swarm.sensor_user_set.set([])

        # Swarm List - user
        url = reverse('sensorswarm-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Add user to swarm
        data = {
            "sensor_user_set": [self.user.id]
        }
        url = reverse('sensorswarm-sensoruser', args=[self.sensor_swarm.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Swarm List - user
        url = reverse('sensorswarm-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    #
    #
    # def test_user_whoami(self):
    #     """
    #     Company Creation
    #     """
    #
    #     # Get token header
    #     token = Token.objects.get(user__username='user')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    #
    #     # Get list of companies
    #     url = reverse('user-whoami')
    #     response = self.client.get(url, {}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['username'], 'user')
