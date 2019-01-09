# Django includes
from django.urls import reverse

# Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Project includes
from .models import *

class CompanyTestCase(APITestCase):

    def setUp(self):

        # Create superuser
        self.admin = SensorUser.objects.create_user('admin', password='admin')
        self.admin.is_superuser=True
        self.admin.is_staff=True
        self.admin.save()

        # Create user
        self.user = SensorUser.objects.create_user('user', password='user')

    def test_company_crud(self):
        """
        Company Creation
        """

        # Get token header
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

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
        company_id = response.data['id']

        # Update Company
        url = reverse('company-detail', args=[company_id])
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
        url = reverse('company-detail', args=[company_id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

    def test_company_crud_not_authorized(self):
        """
        Company Creation
        """

        # Get token header
        token = Token.objects.get(user__username='user')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Get list of companies
        url = reverse('company-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
