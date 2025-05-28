"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import InstruccionEmbarqueForm, ReservaCargaForm
from .models import ReservaCarga

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
            # Despu�s de guardar, redirige a la p�gina de confirmaci�n
            return redirect('confirmacion_instruccion')
    else:
        form = InstruccionEmbarqueForm()

    return render(request, 'app/InstruccionEmbarque.html', {'form': form})

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
    """Vista para mostrar las reservas del usuario."""
    reservas = ReservaCarga.objects.all().order_by('-fecha_creacion_reserva')
    return render(
        request,
        'app/mis_reservas.html',
        {
            'title': 'Mis Reservas',
            'reservas': reservas,
            'year': datetime.now().year,
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
    """Vista para eliminar una reserva."""
    reserva = get_object_or_404(ReservaCarga, id=reserva_id)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada correctamente.')
        return redirect('mis_reservas')
    
    return redirect('mis_reservas')