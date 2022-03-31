from django.db import models


class StreamPlatform(models.Model):
    platform = models.CharField(max_length=225)
    about = models.CharField(max_length=225)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.platform


class WatchList(models.Model):
    title = models.CharField(max_length=225)
    storyline = models.CharField(max_length=225)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
