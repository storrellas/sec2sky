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
        self.user = User.objects.create_user('user', password='user', company= self.company)

        # Create Sensor Swarm
        self.swarm = Swarm.objects.create(name='swarm', description='swarm_description')
        self.swarm.user_set.set([self.user])

    def set_jwt(self, username, password):
        # Get JWT
        url = reverse('api-token')
        data = { 'username' : username, 'password': password }
        response = self.client.post(url, data, format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_swarm_crud(self):
        """
        Company Creation
        """
        self.assertEqual(Swarm.objects.count(), 1)

        # Set token header
        self.set_jwt(username='admin', password='admin')

        # Create Swarm
        url = reverse('swarm-list')
        data = {
            'name' : "swarm_new",
            'description': "swarm description new"
        }
        response = self.client.post(url, data, format='json')

        # Store ID
        id = response.data['id']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Swarm.objects.count(), 2)
        self.assertEqual(Swarm.objects.get(pk=id).name, 'swarm_new')

        # Update Swarm
        url = reverse('swarm-detail', args=[id])
        data = {
            'name' : "swarm_updated",
            'description': "swarm_updated"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Swarm.objects.count(), 2)
        self.assertEqual(Swarm.objects.get(pk=id).name, 'swarm_updated')

        # Swarm List - admin
        url = reverse('swarm-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Set token header
        self.set_jwt(username='user', password='user')

        # Swarm List - user
        url = reverse('swarm-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Set token header
        self.set_jwt(username='admin', password='admin')

        # Delete Swarm
        url = reverse('swarm-detail', args=[id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Swarm.objects.count(), 1)



    def test_swarm_user(self):
        """
        Company Creation
        """

        # Get token header
        self.set_jwt(username='user', password='user')

        self.swarm.user_set.set([])

        # Swarm List - user
        url = reverse('swarm-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Get token header
        self.set_jwt(username='admin', password='admin')

        # Add user to swarm
        data = {
            "user_set": [self.user.id]
        }
        url = reverse('swarm-user', args=[self.swarm.id])
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Swarm List - user
        url = reverse('swarm-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
