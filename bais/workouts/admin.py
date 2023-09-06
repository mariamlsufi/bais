from django.contrib import admin

from .models import Workouts, WorkoutDates, Exercises, Sets, Bests

# Register your models here.
admin.site.register(Workouts)
admin.site.register(Exercises)
admin.site.register(Sets)
admin.site.register(Bests)
admin.site.register(WorkoutDates)