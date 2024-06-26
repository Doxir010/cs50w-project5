# Generated by Django 5.0.6 on 2024-06-25 21:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GimnasioWebSite', '0004_alter_plan_duracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='rol',
            field=models.CharField(blank=True, choices=[('Cliente', 'Cliente'), ('Asistente', 'Asistente'), ('Entrenador', 'Entrenador')], max_length=25, null=True),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fecha_vencimiento', models.DateField()),
                ('pagado', models.BooleanField(default=False)),
                ('pago', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='GimnasioWebSite.pagoplan')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
