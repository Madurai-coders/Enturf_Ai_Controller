from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AIStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    previousState = models.CharField(max_length=120)
    currentState = models.CharField(max_length=120)
    mobileNumber = models.CharField(max_length=12, unique=True)
    duration = models.CharField(max_length=12, unique=True)
    status_change_time = models.DateTimeField(auto_now=True)  # Automatically updated on create or update


    def __str__(self):
        return str(self.user)
    

class Gallery(models.Model):
    videoPath = models.CharField(max_length=120)
    my_array = models.CharField(max_length=50000)

    def __str__(self):
        return str(self.videoPath)