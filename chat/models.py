from enum import Enum

from django.db import models

# Create your models here.
from polyclinic.models import MedicalStaff


class RoomType(Enum):
    Group = "GROUP"
    Disc  = "DISC"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)



class OnlineUser(models.Model):
    user = models.OneToOneField(MedicalStaff, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)
    last_view = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username





class Room(models.Model) :
    roomId = models.UUIDField(blank=False, null=False)
    type = models.CharField(choices=RoomType.choices(), null=False, blank=False, max_length=20)
    members = models.ManyToManyField(OnlineUser)
    name = models.CharField(max_length=30, null=True, blank=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(OnlineUser, related_name="sender", null=True, on_delete=models.CASCADE)

    text_message = models.TextField(blank=True, null=True)
    image_message = models.ImageField(upload_to='media/images', blank=True, null=True)
    audio_message = models.FileField(upload_to='social/audios', blank=True, null=True)
    videos_message = models.FileField(upload_to='social/videos', blank=True, null=True)










