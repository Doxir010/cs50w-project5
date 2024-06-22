from django.contrib import admin
from .models import Usuario, Plan, Suscripcion, PagoPlan, Asistencia
from django.contrib.auth.admin import UserAdmin

#
class usuarioConfig(UserAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("username", "first_name", "last_name")
    ordering = ("username",)

class planConfig(UserAdmin):
    list_display = ["nombre", "descripcion", "precio"]
    # ordering = ("nombre",)
    # search_fields = ("nombre", "precio")

class suscripcionConfig(UserAdmin):
    list_display = ("id", "cliente__username", "plan", "fechaInicio", "fechaFinal")
    ordering = ("fechaInicio",)
    search_fields = ("cliente__username", "plan__nombre")
    list_filter = ("plan__nombre", "fechaInicio", "fechaFinal")
    
    
class pagoplanConfig(UserAdmin):
    list_display = ("id", "cliente", "plan", "fechaPago")
    
class asistenciaConfig(UserAdmin):
    list_display = ("id", "Usuario", "horaEntrada", "horaSalida")
    ordering = ("horaEntrada",)
    search_fields = ("Usuario__username", "horaEntrada", "horaSalida")

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Plan)
admin.site.register(Suscripcion)
admin.site.register(PagoPlan)
admin.site.register(Asistencia)