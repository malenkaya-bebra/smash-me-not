from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    telegram = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    photo_1 = models.ImageField(upload_to='photos/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/', blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
