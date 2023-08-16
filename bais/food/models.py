# Create your models here.
from django.db import models
from accounts.models import CustomUser
from django.conf import settings

class Meals(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length = 50)
    kcal = models.DecimalField(decimal_places=2)
    g_protein = models.DecimalField(decimal_places=2)

    protein = models.BooleanField()
    fruit = models.BooleanField()
    veg = models.BooleanField()
    grains = models.BooleanField()
    dairy = models.BooleanField()
    fats = models.BooleanField()

    photo =models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.label
    
class CustomFood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length = 50)
    kcal = models.DecimalField(decimal_places=2)
    g_protein = models.DecimalField(decimal_places=2)


class Foods(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length = 50)
    kcal = models.DecimalField(decimal_places=2)
    g_protein = models.DecimalField(decimal_places=2)