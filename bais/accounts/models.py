# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class DeviceInfo(models.Model):
    device_type = models.CharField(max_length=4)

    def __str__(self):
        return self.device_type

class CustomUser(AbstractUser):
    # misc
    linked_device = models.ForeignKey(DeviceInfo, on_delete=models.SET_NULL, null=True)
    app_greeting = models.CharField(max_length=50, default='prioritize you <3')

    # color scheme
    lightest = models.CharField(max_length = 7, default='#8C8C8C')
    lighter = models.CharField(max_length = 7, default='#626661')
    darker = models.CharField(max_length = 7, default='#4E524D')
    darkest = models.CharField(max_length = 7 default='#313630')

    def __str__(self):
        return self.username