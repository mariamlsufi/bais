# Generated by Django 4.2.3 on 2023-10-26 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0009_alter_workouts_svg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workouts',
            name='svg',
            field=models.TextField(),
        ),
    ]
