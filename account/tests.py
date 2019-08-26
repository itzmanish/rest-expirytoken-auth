import json

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse


class LoginViewTest(APITestCase):
    url = reverse('login')

    def test_login_failed(self):
        data = {
            'username': 'rudra',
            'password': 'pass123'
        }
        res = self.client.post(self.url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        data = {
            'username': 'rudra',
            'password': 'rudra@108',
        }
        res = self.client.post(self.url, data=data, format='json')
        print(dir(res))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
