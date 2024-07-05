from .models import *
from . import helpers

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.dateparse import parse_datetime
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
                return render(request, "GimnasioWebSite/register.html", {
                    "message": "ERROR: usuario ya existente"
                })
        else:
            return render(request, "GimnasioWebSite/register.html", {
            "message": "La contraseña y su validacion deben ser iguales"
            })
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
                "message": mensaje
            })
    
    else:
        return render(request, "GimnasioWebSite/login.html")
    
@login_required 
def CerrarSesion(request):
    logout(request)
    return redirect(home)

def verStaff(request):
    return render(request, "GimnasioWebSite/infoStaff.html")


def verMaquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, "GimnasioWebSite/Maquinas.html", {
        "Maquinas": maquinas,
    })


def verSuscripciones(request):
    return render(request, "GimnasioWebSite/verSuscripciones.html", {
        "Suscripciones": Plan.objects.all()
    })
    
    
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
    
    else:
        return render(request, "GimnasioWebSite/pagoSuscripcion.html", {
            "Plan": instanciaPlan
        })
        

@login_required
def asistencias(request):
    return render(request, 'GimnasioWebSite/asistencias.html')

def get_attendance_data(request):
    role = request.GET.get('role', 'all')
    order = request.GET.get('order', 'asc')
    name = request.GET.get('name', '')

    if role == 'Cliente':
        users = Usuario.objects.filter(rol='Cliente')
    elif role == 'Staff':
        users = Usuario.objects.filter(rol__in=['Asistente', 'Entrenador'])
    else:
        users = Usuario.objects.all()

    if name:
        users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)

    if order == 'asc':
        asistencias = Asistencia.objects.filter(Usuario__in=users).order_by('horaEntrada')
    else:
        asistencias = Asistencia.objects.filter(Usuario__in=users).order_by('-horaEntrada')

    data = []
    for asistencia in asistencias:
        data.append({
            'nombreCompleto': f"{asistencia.Usuario.first_name} {asistencia.Usuario.last_name}",
            'horaEntrada': asistencia.horaEntrada.isoformat(),
            'horaSalida': asistencia.horaSalida.isoformat() if asistencia.horaSalida else None,
            'cumplimiento': asistencia.cumplimiento,
        })

    return JsonResponse(data, safe=False)

def add_attendance(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud como JSON
            data = json.loads(request.body.decode('utf-8'))

            # Extraer datos del JSON
            role_option = data.get('roleOption')
            user_input = data.get('userInput')
            entry_date = parse_datetime(data.get('entryDate'))
            compliance = data.get('compliance')
            entry_time = parse_datetime(data.get('entryTime'))
            exit_time = parse_datetime(data.get('exitTime'))

            # Verificar que todos los campos requeridos están presentes
            if not all([role_option, user_input, entry_date, compliance, entry_time]):
                return JsonResponse({'success': False, 'error': 'Faltan campos requeridos.'}, status=400)

            # Obtener el usuario por ID
            usuario = Usuario.objects.get(id=user_input)

            # Crear una nueva asistencia
            if role_option == 'Cliente':
                Asistencia.objects.create(
                    Usuario=usuario,
                    horaEntrada=entry_date,
                    cumplimiento=compliance
                )
            else:
                Asistencia.objects.create(
                    Usuario=usuario,
                    horaEntrada=entry_time,
                    horaSalida=exit_time
                )
            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Error de decodificación JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'success': False, 'error': f'Falta el campo requerido: {e}'}, status=400)
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return HttpResponseBadRequest('Método no permitido')


