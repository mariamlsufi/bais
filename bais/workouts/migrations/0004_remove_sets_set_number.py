# Generated by Django 4.2.3 on 2023-10-12 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0003_alter_workouts_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sets',
            name='set_number',
        ),
    ]
