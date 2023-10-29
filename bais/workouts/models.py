
from django.db import models

# Create your models here.
# Create your models here.
from django.db import models
from django.conf import settings

class Workouts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    svg = models.TextField()
    date_used = models.DateField(auto_now = True, null=False)

    rel_exercises = models.ManyToManyField('Exercises')

class WorkoutDates(models.Model):
    date = models.DateField(auto_now=True)
    workout = models.ForeignKey(Workouts,  on_delete=models.CASCADE)

class Exercises(models.Model):
    label = models.CharField(max_length=20)
     
    UNITS = (
        ('lbs', 'lbs'),
        ('bw', 'bodyweight'),
        ('bw+', 'bodyweight + '),
        ('kg', 'kilograms'),
    )

    units = models.CharField(
        max_length=3,
        choices=UNITS,
        blank=True,
        default='lbs',
    )

class Sets(models.Model):
    workout = models.ForeignKey(Workouts,  on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises,  on_delete=models.CASCADE)
    reps = models.IntegerField()
    intensity = models.DecimalField(decimal_places=2, max_digits=5)

class Bests(models.Model):
    workout = models.ForeignKey(Workouts,  on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises,  on_delete=models.CASCADE)
    reps = models.IntegerField()
    intensity = models.DecimalField(decimal_places=2, max_digits=5)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)
