from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.CerrarSesion, name="logout"),
    path("suscripciones/pago/<int:id>", views.pagarSuscripcion, name="pagoSuscripcion"),
    path("suscripciones/ver", views.verSuscripciones, name="verSuscripciones"),
    path("info/staff", views.verStaff, name="infoStaff"),
    path("info/maquinas", views.verMaquinas, name="infoMaquinas"),
    path('asistencias', views.asistencias, name='asistencias'),
    path('suscripciones/historial', views.historialSuscripciones, name="historial"),
    path('perfil/<int:id>', views.perfil, name="perfil"),
    
    #URLs de API
    path('asistencias/data', views.get_attendance_data, name='get_attendance_data'),
    path('asistencias/add', views.add_attendance, name='add_attendance'),
    path('usuarios/data', views.get_users_by_role, name='get_users_by_role'),
]
