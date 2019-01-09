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

    def test_sensorswarm_crud(self):
        """
        Company Creation
        """
        self.assertEqual(SensorSwarm.objects.count(), 1)

        # Get token header
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create User
        url = reverse('sensorswarm-list')
        data = {
            'name' : "sensor_swarm_new",
            'description': "sensor swarm description new"
        }
        response = self.client.post(url, data, format='json')

        # Store company ID
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

        # Delete User
        url = reverse('sensorswarm-detail', args=[id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorSwarm.objects.count(), 1)

        """
        # Token for created user
        url = reverse('api-token')
        data = {
            'username' : "user_test",
            'password': "user_test"
        }
        response = self.client.post(url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], Token.objects.get(user__username='user_test').key)

        # Update User
        url = reverse('user-detail', args=[id])
        data = {
            'username' : "user_updated",
            'password': "user_updated",
            'role': "administrator",
            'company': self.company.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SensorUser.objects.count(), 3)
        self.assertEqual(SensorUser.objects.get(pk=id).username, 'user_updated')

        # Token for created user
        url = reverse('api-token')
        data = {
            'username' : "user_updated",
            'password': "user_updated"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], Token.objects.get(user__username='user_updated').key)

        # Delete User
        url = reverse('user-detail', args=[id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SensorUser.objects.count(), 2)
        """

    # def test_user_crud_not_authorized(self):
    #     """
    #     Company Creation
    #     """
    #
    #     # Get token header
    #     token = Token.objects.get(user__username='user')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    #
    #     # Get list of companies
    #     url = reverse('user-list')
    #     response = self.client.get(url, {}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
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
