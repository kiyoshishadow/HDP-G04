"""
Definition of views.
"""

from datetime import datetime
from pickle import TRUE
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import HttpRequest, JsonResponse # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.utils.timezone import now # type: ignore # type: ignore
from django.db.models import Q # type: ignore
import json
import os
from django.conf import settings

from .forms import InstruccionEmbarqueForm, ReservaCargaForm, RegistroUsuarioForm, PerfilUsuarioForm, InstruccionEmbarqueForm
from .models import ReservaCarga, InstruccionEmbarque, PerfilUsuario
from django.contrib import messages

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def crear_instruccion_embarque(request):
    if request.method == 'POST':
        form = InstruccionEmbarqueForm(request.POST)
        if form.is_valid():
            form.save()
            # Después de guardar, redirige a la página de confirmación
            return redirect('confirmacion_instruccion')
    else:
        form = InstruccionEmbarqueForm()

    return render(request, 'app/InstruccionEmbarque.html', {'form': form})

def confirmacion_instruccion(request):
    return render(request, 'app/ConfirmacionEmbarque.html'), ({"form": form, "submitSuccess": submit_success})


def confirmacion_instruccion(request):
    return render(request, 'app/ConfirmacionEmbarque.html')


def crear_reserva(request):
    print("Método de solicitud:", request.method)
    if request.method == 'POST':
        print("Datos POST recibidos:", request.POST)
        form = ReservaCargaForm(request.POST)
        print("Formulario instanciado:", form)
        if form.is_valid():
            print("Formulario válido. Guardando...")
            form.save()
            print("Datos guardados.")
            # Redirigir a una página de éxito o mostrar un mensaje
            # Considera redirigir a una URL específica después de guardar
            # return redirect('nombre_de_tu_pagina_de_exito')
            return render(request, 'app/crear_reserva.html', {'form': form, 'success': True})
        else:
            print("Formulario no válido. Errores:", form.errors)
            # Mostrar errores en el formulario
            return render(request, 'app/crear_reserva.html', {'form': form, 'errors': form.errors})
    else:
        print("Solicitud GET. Mostrando formulario vacío.")
        form = ReservaCargaForm()
    return render(request, 'app/crear_reserva.html', {'form': form})

def mis_reservas(request):
    """Vista para mostrar las reservas del usuario (excepto canceladas)."""
    reservas = ReservaCarga.objects.exclude(estado_reserva='cancelada').order_by('-fecha_creacion_reserva')
    return render(
        request,
        'app/mis_reservas.html',
        {
            'title': 'Mis Reservas',
            'reservas': reservas,
            'year': datetime.now().year,
            'now': now(),
        }
    )

def editar_reserva(request, reserva_id):
    """Vista para editar una reserva existente."""
    reserva = get_object_or_404(ReservaCarga, id=reserva_id)
    
    if request.method == 'POST':
        form = ReservaCargaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('mis_reservas')
    else:
        form = ReservaCargaForm(instance=reserva)
    
    return render(
        request,
        'app/editar_reserva.html',
        {
            'form': form,
            'reserva': reserva,
            'title': 'Editar Reserva',
            'year': datetime.now().year,
        }
    )

def eliminar_reserva(request, reserva_id):
    """Vista para cancelar una reserva (no eliminar físicamente)."""
    reserva = get_object_or_404(ReservaCarga, id=reserva_id)
    
    if request.method == 'POST':
        reserva.estado_reserva = 'cancelada'
        reserva.save()
        messages.success(request, 'Reserva cancelada correctamente.')
        return redirect('mis_reservas')
    
    return redirect('mis_reservas')

def register(request):
    if request.method == 'POST':
        user_form = RegistroUsuarioForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        user_form = RegistroUsuarioForm()
        perfil_form = PerfilUsuarioForm()
    return render(request, 'app/register.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

def servicios_adicionales(request):
    """Vista para mostrar servicios adicionales."""
    return render(request, 'app/servicios_adicionales.html', {
        'title': 'Servicios Adicionales',
        'year': datetime.now().year,
    })

def mapa(request):
    """Vista para mostrar el mapa."""
    return render(request, 'app/mapa.html', {
        'title': 'Mapa',
        'year': datetime.now().year,
    })

# Vista para historial de reservas
def historial_reservas(request):
    """Vista para mostrar el historial de reservas."""
    estado = request.GET.get('estado', 'todos')
    reservas = ReservaCarga.objects.all()

    if estado == 'en_curso':
        reservas = reservas.filter(Q(fecha_limite_llegada__gt=now().date()) & ~Q(estado_reserva='cancelada'))
    elif estado == 'canceladas':
        reservas = reservas.filter(estado_reserva='cancelada')
    elif estado == 'completadas':
        reservas = reservas.filter(Q(fecha_limite_llegada__lte=now().date()) & ~Q(estado_reserva='cancelada'))

    return render(request, 'app/historial_reservas.html', {
        'title': 'Historial de Reservas',
        'reservas': reservas,
        'estado': estado,
        'year': datetime.now().year,
        'now': now(),
    })

def autocomplete_puertos_local(request):
    query = request.GET.get('q', '').lower()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    ports_path = os.path.join(settings.BASE_DIR, 'app', 'data', 'ports.json')
    with open(ports_path, encoding='utf-8') as f:
        ports_data = json.load(f)

    results = []
    for country, ports in ports_data.items():
        for port in ports:
            nombre = port.get('name', '')
            pais = port.get('country', country)
            codigo = port.get('unlocs', [None])[0] if 'unlocs' in port and port['unlocs'] else ''
            if query in nombre.lower() or query in pais.lower():
                results.append({
                    'nombre': nombre,
                    'pais': pais,
                    'codigo': codigo
                })
            if len(results) >= 10:
                return JsonResponse({'results': results})
    return JsonResponse({'results': results})



def lista_instrucciones(request):
    instrucciones = InstruccionEmbarque.objects.all().order_by('-fecha_creacion')
    return render(request, 'app/bill_of_lading.html', {'instrucciones': instrucciones})

def editar_instruccion(request, pk):
    instruccion = get_object_or_404(InstruccionEmbarque, pk=pk)
    if request.method == 'POST':
        form = InstruccionEmbarqueForm(request.POST, instance=instruccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'La instrucción fue actualizada correctamente.')
            return redirect('lista_instrucciones')
    else:
        form = InstruccionEmbarqueForm(instance=instruccion)
    return render(request, 'app/instruccionEmbarque.html', {'form': form, 'editar': True})

def aprobar_instruccion(request, pk):
    instruccion = get_object_or_404(InstruccionEmbarque, pk=pk)
    instruccion.estado = 'Aprobado'
    instruccion.save()
    messages.success(request, 'La instrucción ha sido aprobada.')
    return redirect('lista_instrucciones')

