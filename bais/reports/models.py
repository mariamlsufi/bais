from django.db import models

from django.conf import settings
# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   
    TYPES = (
        ('y', 'year'),
        ('m', 'month'),
        ('w', 'week'),
        ('d', 'day'),
    )

    type = models.CharField(
        max_length=1,
        choices=TYPES,
        blank=True,
        default='w',
    )


    start = models.DateField()

    avg_improvement = models.DecimalField(decimal_places=2, max_digits=10)
    workouts_completed = models.IntegerField()
    
    avg_protein = models.DecimalField(decimal_places=2, max_digits=10)
    fruit = models.IntegerField()
    veg = models.IntegerField()
    dariy = models.IntegerField()
    fats = models.IntegerField()
    protein = models.IntegerField()
    grains = models.IntegerField()

    cal_in = models.IntegerField()