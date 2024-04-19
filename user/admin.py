from django.contrib import admin
from .models import Profile, FriendRequest, Photo

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Photo)
