# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )

def crear_reserva(request):
    """Renders the crear reserva page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/crear_reserva.html',
        {
            'title': 'Crear Reserva',
            'message': 'Pagina para crear una nueva reserva.',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )

def mis_reservas(request):
    """Renders the mis reservas page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/mis_reservas.html',
        {
            'title': 'Mis Reservas',
            'message': 'Página para ver tus reservas.',
            'year': datetime.now().year,
        }
    )
