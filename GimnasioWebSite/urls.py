from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.CerrarSesion, name="logout"),
    path("suscripciones/pago/<str:nombre>", views.pagarSuscripcion, name="pagoSuscripcion"),
    path("suscripciones/ver", views.verSuscripciones, name="verSuscripciones"),
    path("info/staff", views.verStaff, name="infoStaff"),
    path("info/maquinas", views.verMaquinas, name="infoMaquinas"),
    path('asistencias', views.asistencias, name='asistencias'),
    
    #URLs de API
    path('asistencias/data', views.get_attendance_data, name='get_attendance_data'),
    path('asistencias/add', views.add_attendance, name='add_attendance'),
]
