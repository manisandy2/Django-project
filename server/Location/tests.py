from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from Account.models import CustomUser
from Profile.models import Account
from .models import Destination, Log
import uuid

class DestinationLogTests(APITestCase):

    def setUp(self):
        # Create user and token
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create account and destination
        self.account = Account.objects.create(name="Test Account")
        self.destination = Destination.objects.create(
            account=self.account,
            url='https://webhook.site/test',
            method='POST',
            headers={'Content-Type': 'application/json'},
            created_by=self.user,
            updated_by=self.user,
        )

    def test_create_destination(self):
        url = reverse('destination-list')
        data = {
            'account': self.account.id,
            'url': 'https://example.com/hook',
            'method': 'POST',
            'headers': {'Authorization': 'Token 123'},
            'created_by': self.user.id,
            'updated_by': self.user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['url'], 'https://example.com/hook')

    def test_get_destinations(self):
        url = reverse('destination-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_log_read_only(self):
        Log.objects.create(
            event_id=uuid.uuid4(),
            account=self.account,
            destination=self.destination,
            received_timestamp=now(),
            processed_timestamp=now(),
            received_data={"foo": "bar"},
            status="success"
        )
        url = reverse('log-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # POST should be disallowed
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)