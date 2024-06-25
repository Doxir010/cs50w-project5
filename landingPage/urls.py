from django.urls import path
from GimnasioWebSite.views import *

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('informacion', views.informacion, name="info"),
    path("register", register, name="register"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
]