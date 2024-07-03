from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.CerrarSesion, name="logout"),
    path("suscripciones/pago/<str:nombre>", views.pagarSuscripcion, name="pagoSuscripcion"),
    path("suscripciones/ver", views.verSuscripciones, name="verSuscripciones"),
]
