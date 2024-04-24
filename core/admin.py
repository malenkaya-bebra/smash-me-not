from django.contrib import admin
from .models import Notification, Feed, Post, Comment, Like, SmashRequest

admin.site.register(Notification)
admin.site.register(Feed)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(SmashRequest)
