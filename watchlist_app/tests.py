from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(
            platform="test",
            about="testdetail",
            website="https://test.com"
            )


    def test_stream_platform_create(self):
        data = {
            "platform": "test",
            "about": "test platform",
            "website": "https://test.com"
        }
        res = self.client.post(reverse('stream-list'), data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_streamplatform_list(self):
        res = self.client.get(reverse('stream-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        res = self.client.get(reverse('stream-detail', args=(self.stream.id,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(
            platform="test",
            about="testdetail",
            website="https://test.com"
            )

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="test",
            storyline="test detail",
            active=True

        )

    def test_watchlist_create(self):
        data = {
            "platform": "test",
            "title": "Test123",
            "storyline": "testexample",
            "active": True
        }
        res = self.client.post(reverse('watchlist-list'), data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_watchlist_list(self):
        res = self.client.get(reverse('watchlist-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        res = self.client.get(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, "test")


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(
            platform="test",
            about="testdetail",
            website="https://test.com"
            )

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="test",
            storyline="test detail",
            active=True

        )

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "test detail",
            "watchlist": self.watchlist,
            "active": True
        }

        res = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
