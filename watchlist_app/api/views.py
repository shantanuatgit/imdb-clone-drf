from django.shortcuts import render
from watchlist_app.models import *
from watchlist_app.api.serializers import *
from .permissions import *
from watchlist_app.api.pagination import *
from watchlist_app.api.throttling import *
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class WatchListViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListPagination
    permission_classes = [IsAdminOrReadOnly]

class ReviewUser(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)
# @api_view(['GET', 'POST'])
# def watch_list(request):
#     if request.method == 'GET':
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def watchlist_detail(request, pk):
#     try:
#         movie = WatchList.objects.get(pk=pk)
#     except WatchList.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformList(generics.ListCreateAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        print(review_user)
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        if movie.total_rating == 0:
            movie.average_rating = serializer.validated_data['rating']
        else:
            movie.average_rating = (movie.average_rating + serializer.validated_data['rating']) / 2
        movie.total_rating += 1
        movie.save()
        serializer.save(watchlist=movie, review_user=review_user)


class ReviewList(mixins.ListModelMixin, generics.GenericAPIView):
    pagination_class = WatchListPagination
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [filters.OrderingFilter]
    # filterset_fields = ['review_user__username', 'active']
    ordering_filter = ['rating']

    def get(self, request, *args, **kwargs):
        return self.list(request)


class ReviewDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

    def get(self, request, pk):
        return self.retrieve(request,pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request)
