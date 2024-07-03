from .models import *
from . import helpers

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
import json

# Create your views here.

def home (request):
    return render(request, 'GimnasioWebSite/landingPage.html')

def register(request):
    if request.method == "POST":
        nombres = request.POST["names"]
        apellidos = request.POST["lastNames"]
        numeroTelefonico = request.POST["number"]
        numeroTelefonicoEmergencia = request.POST["emergencyNumber"]
        direccion = request.POST["address"]
        correo = request.POST["email"]
        password = request.POST["password"]
        passwordConfirmation = request.POST["confirmation"]
        
        if password == passwordConfirmation:
            try:
                username = helpers.generarUsername(nombres, apellidos)
                nuevoUsuario = Usuario.objects.create_user(
                    username=username, email=correo, password=password, first_name=nombres, last_name=apellidos,
                      telefono=numeroTelefonico, telefonoEmergencia=numeroTelefonicoEmergencia, direccion=direccion, rol="Cliente")
                login(request, nuevoUsuario)
                return redirect(home)
            except IntegrityError as e:
                print(e)
                return render(request, "GimnasioWebSite/register.html")
    
    else:
        return render(request, "GimnasioWebSite/register.html")
    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        AutenticacionUsuario = authenticate(request, username=username, password=password)
        
        if AutenticacionUsuario is not None:
            login(request, AutenticacionUsuario)
            return redirect(home)
            
        else:
            mensaje ='Nombre de usuario o contraseña no valida'
            return render(request, "GimnasioWebSite/login.html", {
                "alerta":mensaje
            })
    
    else:
        return render(request, "GimnasioWebSite/login.html")
    
    
def CerrarSesion(request):
    logout(request)
    return redirect(home)


def pagarSuscripcion(request, nombre):
    instanciaPlan = nombre
    if request.method == 'POST':
        titular = request.POST["name"]
        numeroTarjeta = request.POST["cardNumber"]
        fechaVencimiento = request.POST["expDate"]
        CVV = request.POST["CVV"]
        print(titular)
        print(numeroTarjeta)
        print(fechaVencimiento)
        print(CVV)

        return redirect(pagarSuscripcion, nombre=nombre)
    return render(request, "GimnasioWebSite/pagoSuscripcion.html", {
        'Plan': instanciaPlan
    })


def verSuscripciones(request):
    return render(request, "GimnasioWebSite/verSuscripciones.html", {
        "Suscripciones": Plan.objects.all()
    })