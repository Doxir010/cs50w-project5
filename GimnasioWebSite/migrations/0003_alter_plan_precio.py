# Generated by Django 5.0.6 on 2024-06-15 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GimnasioWebSite', '0002_plan_alter_usuario_direccion_asistencia_pagoplan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]