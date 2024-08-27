from django.contrib import admin
from .models import Profile, ChatMessage, FriendRequest

admin.site.register([Profile, ChatMessage, FriendRequest])
