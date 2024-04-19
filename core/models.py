from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Notification(models.Model):
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.message


class Feed(models.Model):
    CATEGORY_CHOICES = [
        ('serious_relationship', 'Serious Relationship'),
        ('one_night_stand', 'One Night Stand'),
        ('friends_with_benefits', 'Friends with Benefits'),
        ('online_chatting', 'Online Chatting'),
        ('activities', 'Activities'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Feed"


class Post(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Post by {self.feed.user.username} at {self.created_at}"


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.username} on {self.post.id}"


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)


class SmashRequest(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='smash_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='smash_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Smash request from {self.sender.username} to {self.receiver.username} for post {self.post.id}"
