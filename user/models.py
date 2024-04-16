from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    photos = models.ManyToManyField('Photo', blank=True)

    def __str__(self):
        return self.user.username


class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
