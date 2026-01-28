from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app import models
from watchlist_app.api import serializers


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 Platform", website="https://netflix.com")
        
        
    def test_streamplatform_create(self):
        data = {
            "name": "Amazon Prime",
            "about": "Prime Video",
            "website": "https://primevideo.com"
        }
        
        response = self.client.post(reverse("streamplatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_stremplatform_list(self):
        response = self.client.get(reverse("streamplatform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_steramplatform_detail(self):
        response = self.client.get(reverse("streamplatform-detail", args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_steramplatform_update(self):
        data = {
            "name": "Amazon Prime",
            "about": "Prime Video -- Updated",
            "website": "https://primevideo.com"
        }
        
        response = self.client.put(reverse("streamplatform-detail", args=(self.stream.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_steramplafrom_delete(self):
        response = self.client.delete(reverse("streamplatform-detail", args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class WatchListTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase1", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",about="#1 Platform", website="https://netflix.com"
        )
        
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="Movie #1",
            description="This is my description",
            active=True
        )
        
    def test_watchlist_create(self):
        data = {
            "platform": self.stream.id,
            "title" : "Movie #2",
            "description" : "This is my description for movie 2",
            "active": "true"
        }
        
        response = self.client.post(reverse("movie-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist(self):
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        response = self.client.get(reverse("movie-detail",args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="reviewuser", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(
            name="Netflix",about="#1 Platform", website="https://netflix.com"
        )
        
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="Movie #1",
            description="This is my description",
            active=True
        )
        
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,
            title="Movie #2",
            description="This is my description for movie 2",
            active=True
        )
        
        self.review = models.Review.objects.create(
            review_user=self.user,
            rating=5,
            description="Awesome Movie",
            watchlist=self.watchlist2,
            active=True
        )
        
    def test_review_create(self):
        data = {
            "review_user": self.user.id,
            "rating": 5,
            "description": "Awesome Movie",
            "watchlist": self.watchlist.id,
            "active": True
        }
        
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            "review_user": self.user.id,
            "rating": 5,
            "description": "Awesome Movie",
            "watchlist": self.watchlist.id,
            "active": True
        }
        
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data = {
            "review_user": self.user.id,
            "rating": 4,
            "description": "Good Movie",
            "watchlist": self.watchlist2.id,
            "active": True
        }
        
        response = self.client.put(
            reverse("review-detail", args=(self.review.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse("review-list",args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_detail(self):
        response = self.client.get(reverse("review-detail", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_delete(self):
        response = self.client.delete(reverse("review-detail", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_review_user(self):
        response = self.client.get(
            reverse("user-review") + f"?username={self.user.username}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        