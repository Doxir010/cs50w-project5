from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    telefonoEmergencia = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        # return f"Nombre: {self.first_name} {self.last_name} // Telefono: {self.telefono} // Dirección: {self.direccion} // Telefono de emergencia: {self.telefonoEmergencia}"
        return f"Nombre: {self.first_name} {self.last_name}"
    
    
class Plan(models.Model):
    nombre = models.CharField(max_length=12)
    descripcion = models.TextField(max_length=60)
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Nombre: {self.nombre} // Duracion: {self.duracion} // Precio: {self.precio}"
    
    
class Suscripcion(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    fechaFinal = models.DateField()
    
    def __str__(self):
        return f"Nombre del cliente: {self.cliente} // Plan pagado: {self.plan} // Fecha de inicio del plan: {self.fechaInicio} // Fecha final del plan: {self.fechaFinal}"


class PagoPlan(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fechaPago = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Nombre del cliente: {self.cliente} // Plan pagado: {self.plan} // Fecha de pago: {self.fechaPago}"

class Asistencia(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    horaEntrada = models.DateTimeField(auto_now_add=True)
    horaSalida = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Nombre: {self.Usuario.first_name} {self.Usuario.last_name} // Fecha y hora de entrada: {self.horaEntrada} // Fecha y hora de salida: {self.horaSalida}"