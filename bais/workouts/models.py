
from django.db import models
'''
# Create your models here.
# Create your models here.
from django.db import models
from django.conf import settings

class Workouts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    label = models.CharField

'''