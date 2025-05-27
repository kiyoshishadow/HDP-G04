"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest

from .forms import InstruccionEmbarqueForm, ReservaCargaForm

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