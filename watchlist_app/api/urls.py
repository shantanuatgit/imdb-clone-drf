"""imdb_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from watchlist_app.api import views
from rest_framework.routers  import DefaultRouter

router = DefaultRouter()
router.register('movies', views.WatchListViewSet, basename='movie-list')
urlpatterns = [
    # watchlist
    path('list/', include(router.urls)),
    # Stream Platform
    path('stream/', views.StreamPlatformList.as_view(), name='stream-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetail.as_view(), name='stream-detail'),
    # Reviews
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail')
]
