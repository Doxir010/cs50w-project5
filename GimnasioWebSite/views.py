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
    return render(request, 'GimnasioWebSite/gym.html')

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
                    username, correo, password, nombres, apellidos, numeroTelefonico, numeroTelefonicoEmergencia, direccion)
                nuevoUsuario.save()
            except IntegrityError as e:
                print(e)
                return render(request, "GimnasioWebSite/register.html")
    
    else:
        return render(request, "GimnasioWebSite/register.html")
    

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        AutenticacionUsuario = authenticate(request, username=username, password=password)
        
        if AutenticacionUsuario is not None:
            login(request, AutenticacionUsuario)
            return redirect(home)
    
    else:
        return render(request, "GimnasioWebSite/login.html")
    
    
def CerrarSesion(request):
    logout(request)
    return redirect(home)