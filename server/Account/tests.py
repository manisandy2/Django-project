from django.test import TestCase

from .models import Account,User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status


from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser

class CustomUserTests(APITestCase):

    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(email='admin@example.com', password='admin123')
        self.client.force_authenticate(user=self.admin)

    def test_list_users(self):
        url = reverse('customuser-list')  # DRF auto-generated name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        url = reverse('customuser-list')
        data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)