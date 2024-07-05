from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import Role_options as roles
from .helpers import Machines_Types as MaquinasTipo

# Create your models here.

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    telefonoEmergencia = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=25, blank=True, null=True, choices=roles)
    
    def __str__(self):
        return f"ID: {self.id} - Nombre: {self.first_name} {self.last_name}"


class Staff(Usuario):
    imagen = models.URLField(max_length = 200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rol}"
    
    
class Maquina(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.URLField(max_length = 200)
    descripcion = models.TextField(blank=True, null=True)
    masInfo = models.URLField(max_length = 200, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=MaquinasTipo)
    
    def __str__(self):
        return f"{self.nombre}"
    
    
class Plan(models.Model):
    nombre = models.CharField(max_length=12)
    descripcion = models.TextField(max_length=60)
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.nombre} - Duracion: {self.duracion} - Precio: {self.precio}"
    
    
class Suscripcion(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    fechaFinal = models.DateField()
    
    def __str__(self):
        return f"Cliente: {self.cliente} - Plan pagado: {self.plan} - Fecha de inicio: {self.fechaInicio}"


class PagoPlan(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fechaPago = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cliente: {self.cliente} // Plan pagado: {self.plan} // Fecha de pago: {self.fechaPago}"
    

class Factura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pago = models.OneToOneField(PagoPlan, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.id} - {self.usuario.username}"

class Asistencia(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    horaEntrada = models.DateTimeField(auto_now_add=True)
    horaSalida = models.DateTimeField(null=True, blank=True)
    cumplimiento = models.CharField(max_length=8,null=True,blank=True)
    
    def __str__(self):
        return f"Nombre: {self.Usuario.first_name} {self.Usuario.last_name} - Fecha y hora de entrada: {self.horaEntrada}"