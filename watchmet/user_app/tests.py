from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTests(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase1",
            "email": "testcase1@gmail.com",
            "password": "Password@123",
            "password_confirm": "Password@123"
        }

        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCases(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase2", password="Password@123")
        
    def test_login(self):
        data = {
            "username": "testcase2",
            "password" : "Password@123"
        }
        
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)