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
from django.contrib import admin
from django.urls import path
from watchlist_app.api import views
urlpatterns = [
    path('list/', views.watch_list, name='movie-list'),
    path('list/<int:pk>', views.watchlist_detail, name='movie-detail'),
    path('stream/', views.StreamPlatformList.as_view(), name='stream-list'),
    path('stream/<int:pk>', views.StreamPlatformDetail.as_view(), name='stream-detail'),
    path('stream/<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail')
]
