from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "test@example.com",
            "password": "Test@123",
            "password2": "Test@123"
        }
        res = self.client.post(reverse('register'), data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="Test@123"
        )
    def test_login(self):
        data = {
            "username": "test",
            "password": "Test@123"
        }
        res = self.client.post(reverse('login'), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_logout(self):
    #
    #     data = {
    #         "username": "test",
    #         "password": "Test@123"
    #     }
    #     res = self.client.post(reverse('logout'))
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
