"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest

from .forms import InstruccionEmbarqueForm

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
    return render(request, 'app/ConfirmacionEmbarque.html')