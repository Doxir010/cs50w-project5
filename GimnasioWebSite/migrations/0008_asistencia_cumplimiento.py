# Generated by Django 5.0.6 on 2024-07-04 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GimnasioWebSite', '0007_alter_maquina_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='cumplimiento',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]