# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # misc
    app_greeting = models.CharField(max_length=50, default='prioritize you <3')

    # color scheme
    lightest = models.CharField(max_length = 7, default='#8C8C8C')
    lighter = models.CharField(max_length = 7, default='#626661')
    darker = models.CharField(max_length = 7, default='#4E524D')
    darkest = models.CharField(max_length = 7, default='#313630')

    # goals (daily)
    protein_goal = models.DecimalField(decimal_places=2, max_digits=10, default=70)
    fruit_goal = models.IntegerField(default=3)
    veg_goal = models.IntegerField(default=3)
    dairy_goal = models.IntegerField(default=3)
    fats_goal = models.IntegerField(default=3)
    protein_goal = models.IntegerField(default=3)
    grains_goal = models.IntegerField(default=3)

    cal_goal = models.IntegerField(default=2000)

    def __str__(self):
        return self.username