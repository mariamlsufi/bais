from django.contrib import admin

from .models import Meals, CustomFood, Foods

# Register your models here.
admin.site.register(Meals)
admin.site.register(CustomFood)
admin.site.register(Foods)