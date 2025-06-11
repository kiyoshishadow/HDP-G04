from app.models import ReservaCarga, Puerto
from django.db import transaction

def poblar_puertos():
    nombres_puertos = set()
    for reserva in ReservaCarga.objects.all():
        if reserva.puerto_origen:
            nombres_puertos.add(reserva.puerto_origen.strip())
        if reserva.puerto_destino:
            nombres_puertos.add(reserva.puerto_destino.strip())
        if hasattr(reserva, 'puerto_transbordo') and reserva.puerto_transbordo:
            nombres_puertos.add(reserva.puerto_transbordo.strip())
    
    creados = 0
    with transaction.atomic():
        for nombre in nombres_puertos:
            if nombre and not Puerto.objects.filter(nombre__iexact=nombre).exists():
                Puerto.objects.create(nombre=nombre, pais="Desconocido")
                print(f"Puerto creado: {nombre}")
                creados += 1
    print(f"Total de puertos creados: {creados}")

if __name__ == "__main__":
    poblar_puertos() 