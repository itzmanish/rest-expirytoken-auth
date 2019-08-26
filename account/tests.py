import json

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class LoginViewTest(APITestCase):
    url = reverse('login')

    def setUp(self):
        UserModel.objects.create_user(
            username='rudra', email='rudra@gmal.com', password='rudra@108')

    def test_created_user(self):
        user = UserModel.objects.filter(username='rudra')
        self.assertEquals(user.count(), 1)

    def test_login_failed(self):
        data = {
            'username': 'rudra',
            'password': 'pass123'
        }
        res = self.client.post(self.url, data=data, format='json')
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        data = {
            'username': 'rudr',
            'password': 'rudra@108',
        }
        res = self.client.post(self.url, data=data)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class RegisterViewTest(APITestCase):

    url = reverse('register')

    def setUp(self):
        UserModel.objects.create_user(
            username='rudr', email='rudra@gmail.com', password='rudra@108')

    def test_created_user(self):
        user = UserModel.objects.filter(username='rudr')
        self.assertEquals(user.count(), 1)

    def test_registration_failed_api(self):
        data = {
            'username': 'rud',
            'email': 'rudfa@gmail.co',
            'password': 'rudra@108',
            'password_confirm': 'rudra@10'
        }

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_api(self):
        data = {
            'username': 'rud',
            'email': 'rudfa@gmail.com',
            'password': 'rudra@108',
            'password_confirm': 'rudra@108'
        }

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
