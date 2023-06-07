from django.db import models
from datetime import datetime
from aplications.authentication.models import User, Professional

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(default=datetime.now, blank=True)
    state = models.BooleanField(default=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user_name = models.CharField(max_length=1000000)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)