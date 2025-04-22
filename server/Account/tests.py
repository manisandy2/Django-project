from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import CustomUser

User = get_user_model()

class CustomUserViewSetTest(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.admin_user = User.objects.create_user(email='admin', password='adminpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # Create a sample user for testing
        self.test_user = CustomUser.objects.create(
            email='test@gmail.com',
            password='testuser',
            created_by=self.admin_user,
            updated_by=self.admin_user,
        )

    def test_list_users(self):
        response = self.client.get(reverse('customuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        response = self.client.get(reverse('customuser-detail', args=[self.test_user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@gmail.com')

    def test_create_user(self):
        data = {
            
            'email': 'new@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('customuser-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'new@example.com')

    def test_update_user(self):
        data = {'email': 'updated@example.com'}
        response = self.client.patch(reverse('customuser-detail', args=[self.test_user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'updated@example.com')

    def test_delete_user(self):
        response = self.client.delete(reverse('customuser-detail', args=[self.test_user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)