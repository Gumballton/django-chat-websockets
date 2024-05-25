from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class RoomModel(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_closed = models.BooleanField(default=False)
    members = models.ManyToManyField(get_user_model(), related_name='joined_users')

    def __str__(self):
        return self.room_name
    

class MessagesModel(models.Model):
    room_name = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    date_message = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.room_name)