import profile

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    pic = models.ImageField(upload_to='img', blank=True, null=True)
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True)

        
    def __str__(self):
        return self.name

class FriendRequest(models.Model):
    objects = None
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_request')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_request')
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} sent {self.receiver.username} a friend request"


class ChatMessage(models.Model):
    objects = None
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body

