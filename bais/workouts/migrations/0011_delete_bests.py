# Generated by Django 4.2.3 on 2023-10-27 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0010_alter_workouts_svg'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bests',
        ),
    ]