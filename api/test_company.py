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

        # Create user
        self.user = User.objects.create_user('user', password='user')

    def set_jwt(self, username, password):
        # Get JWT
        url = reverse('api-token')
        data = { 'username' : username, 'password': password }
        response = self.client.post(url, data, format='json')
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_company_crud(self):
        """
        Company Creation
        """

        self.assertEqual(Company.objects.count(), 0)

        # Get JWT
        self.set_jwt(username='admin', password='admin')

        # Create Company
        url = reverse('company-list')
        data = {
            'name' : "MyCompany",
            'description': "MyCompanyDescription"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'MyCompany')

        # Store company ID
        id = response.data['id']

        # Update Company
        url = reverse('company-detail', args=[id])
        data = {
            'name' : "MyCompanyUpdated",
            'description': "MyCompanyDescription"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'MyCompanyUpdated')

        # Company List
        url = reverse('company-list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Delete Company
        url = reverse('company-detail', args=[id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

    def test_company_crud_not_authorized(self):
        """
        Company Creation
        """

        # Get JWT
        self.set_jwt(username='user', password='user')

        # Get list of companies
        url = reverse('company-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
