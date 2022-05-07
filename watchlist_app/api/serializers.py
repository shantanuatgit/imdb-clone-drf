from rest_framework import serializers
from watchlist_app.models import *

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.platform')
    class Meta:
        model = WatchList
        fields = '__all__'


class WatchListForStreamPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ['title']


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListForStreamPlatformSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'
