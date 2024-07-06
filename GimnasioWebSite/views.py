from .models import *
from . import helpers
import sweetify
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

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

@login_required
def verSuscripciones(request):
    return render(request, "GimnasioWebSite/verSuscripciones.html", {
        "Suscripciones": Plan.objects.all()
    })
    
    
@login_required
def pagarSuscripcion(request, id):
    instanciaPlan = get_object_or_404(Plan, pk=id)
    usuario = request.user
    suscripcion_activa = Suscripcion.objects.filter(cliente=usuario, fechaFinal__gte=date.today()).first()

    if request.method == 'POST':
        titular = request.POST["name"]
        numeroTarjeta = request.POST["cardNumber"]
        fechaVencimiento_str = request.POST["expDate"]
        CVV = request.POST["CVV"]

        # Convertir fecha de vencimiento a formato de datetime
        try:
            fechaVencimiento = datetime.strptime(fechaVencimiento_str, '%m/%y').date()
        except ValueError:
            sweetify.error(request, 'Formato de fecha incorrecto. Use MM/YY.', timer=4000)
            return redirect(pagarSuscripcion, id=id)

        # Obtener el último día del mes de la fecha de vencimiento
        fechaVencimiento = fechaVencimiento.replace(day=1) + relativedelta(months=1, days=-1)

        # Validar que la fecha de vencimiento sea posterior a la fecha actual
        if fechaVencimiento < date.today():
            sweetify.error(request, 'La fecha de vencimiento de la tarjeta es anterior a la fecha actual.', timer=4000)
            return redirect(pagarSuscripcion, id=id)

        # Determinar la duración del plan (mensual o semanal)
        duracion_plan = instanciaPlan.duracion

        # Calcular las fechas de inicio y finalización de la suscripción
        if suscripcion_activa:
            fecha_inicio_nueva = suscripcion_activa.fechaFinal + relativedelta(days=1)
        else:
            fecha_inicio_nueva = date.today()

        if duracion_plan == 'M':
            fecha_final_nueva = fecha_inicio_nueva + relativedelta(months=1, days=-1)
        elif duracion_plan == 'S':
            fecha_final_nueva = fecha_inicio_nueva + relativedelta(weeks=1, days=-1)
        else:
            sweetify.error(request, 'Duración de plan no válida.', timer=4000)
            return redirect(pagarSuscripcion, id=id)

        # Crear la nueva suscripción
        nueva_suscripcion = Suscripcion.objects.create(
            cliente=usuario,
            plan=instanciaPlan,
            fechaInicio=fecha_inicio_nueva,
            fechaFinal=fecha_final_nueva
        )

        # Crear el pago
        nuevo_pago = PagoPlan.objects.create(
            cliente=usuario,
            plan=instanciaPlan
        )


        sweetify.success(request, 'Pago realizado exitosamente')
        return redirect('pagarSuscripcion', id=id)
    else:
        return render(request, "GimnasioWebSite/pagoSuscripcion.html", {
            "plan": instanciaPlan
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


@csrf_exempt
def add_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            role_option = data.get('roleOption')
            user_input = data.get('userInput')
            entry_date = parse_datetime(data.get('entryDate'))
            compliance = data.get('compliance')
            entry_time = parse_datetime(data.get('entryTime'))
            exit_time = parse_datetime(data.get('exitTime'))

            if not all([role_option, user_input, (entry_date or entry_time), compliance]):
                return JsonResponse({'success': False, 'error': 'Faltan campos requeridos.'}, status=400)

            usuario = Usuario.objects.get(id=user_input)

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


def get_users_by_role(request):
    role = request.GET.get('role')
    if role == 'Cliente':
        users = Usuario.objects.filter(rol='Cliente')
    else:
        users = Usuario.objects.filter(rol__in=['Entrenador', 'Asistente'])
    user_data = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name} for user in users]
    return JsonResponse(user_data, safe=False)


@login_required
def historialSuscripciones(request):
    user = request.user
    orden = request.GET.get('orden', 'recientes')
    search_query = request.GET.get('search', '')

    if user.rol == 'Cliente':
        pagos = PagoPlan.objects.filter(cliente=user).order_by('-fechaPago' if orden == 'recientes' else 'fechaPago')
    elif user.rol == 'Asistente' or user.is_staff:
        if search_query:
            pagos = PagoPlan.objects.filter(
                Q(cliente__first_name__icontains=search_query) |
                Q(cliente__last_name__icontains=search_query)
            ).order_by('-fechaPago' if orden == 'recientes' else 'fechaPago')
        else:
            pagos = PagoPlan.objects.all().order_by('-fechaPago' if orden == 'recientes' else 'fechaPago')
    else:
        pagos = []

    context = {
        'user': user,
        'pagos': pagos,
        'orden': orden,
        'search_query': search_query,
    }
    return render(request, 'GimnasioWebSite/historialSuscripciones.html', context)

def perfil(request, id):
    pass