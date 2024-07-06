# Generated by Django 5.0.6 on 2024-07-05 23:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GimnasioWebSite', '0009_remove_asistencia_usuario_asistencia_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistencia',
            name='nombre',
        ),
        migrations.AddField(
            model_name='asistencia',
            name='Usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]