# Generated by Django 5.0.6 on 2024-06-15 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GimnasioWebSite', '0003_alter_plan_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='duracion',
            field=models.IntegerField(),
        ),
    ]
