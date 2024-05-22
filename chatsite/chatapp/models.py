from django.db import models

# Create your models here.

class RoomModel(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name
    

class MessagesModel(models.Model):
    room_name = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room_name)