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

from .forms import InstruccionEmbarqueForm, ReservaCargaForm, RegistroUsuarioForm, PerfilUsuarioForm, InstruccionEmbarqueForm, DocumentoForm
from .models import ReservaCarga, InstruccionEmbarque, PerfilUsuario, Documento, Puerto
from django.contrib import messages
from django.template.loader import render_to_string # type: ignore

from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from zipfile import ZipFile

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    es_encargado_puerto = request.user.groups.filter(name='encargado_puerto').exists() if request.user.is_authenticated else False
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'es_encargado_puerto': es_encargado_puerto,
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


def crear_reserva(request):
    print("Método de solicitud:", request.method)
    if request.method == 'POST':
        print("Datos POST recibidos:", request.POST)
        form = ReservaCargaForm(request.POST)
        print("Formulario instanciado:", form)
        if form.is_valid():
            print("Formulario válido. Guardando...")
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            if not reserva.estado_reserva:
                reserva.estado_reserva = 'solicitada'  # Valor predeterminado
            reserva.save()
            print("Datos guardados.")
            return render(request, 'app/crear_reserva.html', {'form': form, 'success': True})
        else:
            print("Formulario no válido. Errores:", form.errors)
            return render(request, 'app/crear_reserva.html', {'form': form, 'errors': form.errors})
    else:
        print("Solicitud GET. Mostrando formulario vacío.")
        form = ReservaCargaForm()
    return render(request, 'app/crear_reserva.html', {'form': form})

def mis_reservas(request):
    """Vista para mostrar las reservas del usuario (excepto canceladas)."""
    if request.user.username == "admin":
        reservas = ReservaCarga.objects.exclude(estado_reserva='cancelada').order_by('-fecha_creacion_reserva')
    else:
        reservas = ReservaCarga.objects.filter(usuario=request.user).exclude(estado_reserva='cancelada').order_by('-fecha_creacion_reserva')
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
        form = ReservaCargaForm(request.POST, request.FILES, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            # Si el campo no viene en el POST, mantenemos el valor anterior
            if 'estado_reserva' not in form.cleaned_data or not form.cleaned_data['estado_reserva']:
                reserva.estado_reserva = ReservaCarga.objects.get(pk=reserva.pk).estado_reserva
            reserva.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('mis_reservas')
        else:
            print("Errores del formulario:", form.errors)
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
            return redirect('mis_embarques')
    else:
        form = InstruccionEmbarqueForm(instance=instruccion)
    return render(request, 'app/instrucciones_embarque.html', {'form': form, 'editar': True})

def aprobar_instruccion(request, pk):
    instruccion = get_object_or_404(InstruccionEmbarque, pk=pk)
    instruccion.estado = 'Aprobado'
    instruccion.save()
    messages.success(request, 'La instrucción ha sido aprobada.')
    return redirect('aprobar_bl')


def instruccion_embarque_create(request):
    instrucciones = InstruccionEmbarque.objects.all().order_by('-fecha_creacion')
    return render(request, 'app/lista_instrucciones.html', {'instrucciones': instrucciones})


def descargar_bl(request, pk):
    instruccion = get_object_or_404(InstruccionEmbarque, pk=pk)

    # Validar número de booking
    if not instruccion.numero_booking or instruccion.numero_booking == 'sin booking':
        return HttpResponse("No se puede generar el BL porque el número de booking no es válido.", status=400)

    # Preparar contexto seguro para el PDF
    contexto = {
        "instruccion": instruccion,
        "fecha_actual": datetime.now(),
    }

    # Generar HTML y convertir a PDF
    template = get_template("app/bl_template.html")
    html = template.render(contexto)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)

    # Convertir bytes a archivo compatible con FileField
    filename = f"BL_{instruccion.numero_booking}.pdf"
    instruccion.bl_pdf.save(filename, ContentFile(result.getvalue()), save=True)

    return HttpResponse(result.getvalue(), content_type="application/pdf")

def mis_embarques(request):
    if request.user.username == "admin":
        embarques = InstruccionEmbarque.objects.all().order_by('-fecha_creacion')
    else:
        embarques = InstruccionEmbarque.objects.filter(reserva__usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'app/mis_embarques.html', {
        'embarques': embarques,
        'title': 'Mis Embarques',
        'year': datetime.now().year,
    })

def documentos_embarque(request):
    if request.user.username == "admin":
        documentos = InstruccionEmbarque.objects.filter(estado='Aprobado').order_by('-fecha_creacion')
    else:
        documentos = InstruccionEmbarque.objects.filter(reserva__usuario=request.user, estado='Aprobado').order_by('-fecha_creacion')
    return render(request, 'app/documentos_embarque.html', {
        'documentos': documentos,
        'title': 'Documentos de Embarque',
        'year': datetime.now().year,
    })

def instrucciones_embarque(request):
    if request.method == 'POST':
        form = InstruccionEmbarqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instrucción de embarque creada correctamente.')
            return redirect('mis_embarques')
    else:
        form = InstruccionEmbarqueForm()
    return render(request, 'app/instrucciones_embarque.html', {'form': form})

def aprobar_bl(request):
    instrucciones = InstruccionEmbarque.objects.exclude(estado='Aprobado').order_by('-fecha_creacion')
    return render(request, 'app/aprobar_bl.html', {'instrucciones': instrucciones})

@login_required
def subir_documento(request, embarque_id):
    embarque = get_object_or_404(InstruccionEmbarque, pk=embarque_id)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.embarque = embarque
            documento.save()
            return redirect('detalle_embarque', embarque_id=embarque.id)
    else:
        form = DocumentoForm(initial={'embarque': embarque})
    return render(request, 'app/subir_documento.html', {'form': form, 'embarque': embarque})

@login_required
def detalle_embarque(request, embarque_id):
    embarque = get_object_or_404(InstruccionEmbarque, pk=embarque_id)
    documentos = embarque.documentos.all()
    # Obtener puertos de la ruta
    puertos_ruta = []
    if embarque.puerto_embarque:
        puertos_ruta.append(embarque.puerto_embarque)
    if embarque.reserva and hasattr(embarque.reserva, 'puerto_transbordo') and embarque.reserva.puerto_transbordo:
        puertos_ruta.append(embarque.reserva.puerto_transbordo)
    if embarque.puerto_destino:
        puertos_ruta.append(embarque.puerto_destino)
    # Número de referencia sugerido
    numero_referencia_sugerido = embarque.numero_booking or (str(embarque.reserva.id) if embarque.reserva else '')
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, puertos_ruta=puertos_ruta)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.embarque = embarque
            # Asignar puerto_objeto automáticamente si no se seleccionó
            if not documento.puerto_objeto:
                puerto_nombre = embarque.puerto_embarque or (puertos_ruta[0] if puertos_ruta else None)
                if puerto_nombre:
                    documento.puerto_objeto = Puerto.objects.filter(nombre__iexact=puerto_nombre.strip()).first()
            documento.save()
            return redirect('detalle_embarque', embarque_id=embarque.id)
    else:
        form = DocumentoForm(initial={'embarque': embarque, 'numero_referencia': numero_referencia_sugerido}, puertos_ruta=puertos_ruta)
    return render(request, 'app/detalle_embarque.html', {
        'embarque': embarque,
        'documentos': documentos,
        'form': form,
        'puertos_ruta': puertos_ruta,
        'numero_referencia_sugerido': numero_referencia_sugerido,
    })

@login_required
@require_POST
def validar_documento(request, documento_id):
    """Vista para validar un documento por parte del encargado del puerto."""
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Verificar que el usuario sea encargado del puerto correspondiente
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        if perfil.puerto and perfil.puerto == documento.puerto:
            documento.estado = 'validado'
            documento.fecha_validacion = now()
            documento.validado_por = request.user
            documento.observaciones = request.POST.get('observaciones', '')
            documento.save()
            messages.success(request, f'El documento {documento.get_tipo_display()} ha sido validado exitosamente.')
        else:
            messages.error(request, 'No tienes permisos para validar documentos en este puerto.')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
    
    return redirect('detalle_embarque', embarque_id=documento.embarque.id)

@login_required
@require_POST
def rechazar_documento(request, documento_id):
    """Vista para rechazar un documento por parte del encargado del puerto."""
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Verificar que el usuario sea encargado del puerto correspondiente
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        if perfil.puerto and perfil.puerto == documento.puerto:
            documento.estado = 'rechazado'
            documento.fecha_validacion = now()
            documento.validado_por = request.user
            documento.observaciones = request.POST.get('observaciones', '')
            documento.save()
            messages.warning(request, f'El documento {documento.get_tipo_display()} ha sido rechazado.')
        else:
            messages.error(request, 'No tienes permisos para rechazar documentos en este puerto.')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
    
    return redirect('detalle_embarque', embarque_id=documento.embarque.id)

@login_required
def solicitar_correccion(request, documento_id):
    """Vista para solicitar corrección de un documento."""
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Verificar que el usuario sea encargado del puerto correspondiente
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        if perfil.puerto and perfil.puerto == documento.puerto:
            if request.method == "POST":
                documento.estado = 'requiere_correccion'
                documento.fecha_validacion = now()
                documento.validado_por = request.user
                documento.observaciones = request.POST.get('observaciones', '')
                documento.save()
                messages.info(request, f'Se ha solicitado corrección para el documento {documento.get_tipo_display()}.')
                return redirect('detalle_embarque', embarque_id=documento.embarque.id)
        else:
            messages.error(request, 'No tienes permisos para solicitar correcciones en documentos de este puerto.')
            return redirect('detalle_embarque', embarque_id=documento.embarque.id)
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil de usuario no encontrado.')
        return redirect('detalle_embarque', embarque_id=documento.embarque.id)
    
    return render(request, 'app/solicitar_correccion.html', {
        'documento': documento,
    })

@login_required
def documentos_pendientes(request):
    """Vista para mostrar documentos pendientes de validación para el puerto asignado al encargado."""
    # Si el usuario es staff (admin), ve todos los documentos pendientes
    if request.user.is_staff:
        documentos = Documento.objects.filter(estado='pendiente').order_by('fecha_subida')
        titulo = "Todos los Documentos Pendientes"
    else:
        # Si es un usuario normal (encargado de puerto), solo ve los de su puerto
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            if perfil.puerto:
                documentos = Documento.objects.filter(puerto=perfil.puerto, estado='pendiente').order_by('fecha_subida')
                titulo = f"Documentos Pendientes - Puerto {perfil.puerto}"
            else:
                documentos = []
                titulo = "No hay puerto asignado"
                messages.warning(request, "No tienes un puerto asignado para validar documentos.")
        except PerfilUsuario.DoesNotExist:
            documentos = []
            titulo = "Perfil no configurado"
            messages.error(request, "Tu perfil de usuario no está configurado correctamente.")
    
    return render(request, 'app/documentos_pendientes.html', {
        'documentos': documentos,
        'title': titulo,
    })

@login_required
def descargar_documento(request, documento_id):
    """Vista para descargar un documento PDF."""
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Verificar permisos: el propietario del embarque o un encargado de puerto
    es_propietario = documento.embarque.usuario == request.user if hasattr(documento.embarque, 'usuario') else False
    es_encargado = False
    
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        es_encargado = perfil.puerto and perfil.puerto == documento.puerto
    except PerfilUsuario.DoesNotExist:
        pass
    
    if request.user.is_staff or es_propietario or es_encargado:
        try:
            with open(documento.archivo.path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{documento.get_tipo_display()}-{documento.puerto}.pdf"'
                return response
        except Exception as e:
            messages.error(request, f"Error al descargar el documento: {str(e)}")
            return redirect('detalle_embarque', embarque_id=documento.embarque.id)
    else:
        messages.error(request, "No tienes permisos para descargar este documento.")
        return redirect('home')

@login_required
def reemplazar_documento(request, documento_id):
    """Vista para reemplazar un documento existente."""
    documento = get_object_or_404(Documento, id=documento_id)
    
    # Solo permitir actualizar si el documento requiere corrección o es el propietario
    es_propietario = documento.embarque.usuario == request.user if hasattr(documento.embarque, 'usuario') else False
    if not (es_propietario or request.user.is_staff):
        messages.error(request, "No tienes permisos para actualizar este documento.")
        return redirect('detalle_embarque', embarque_id=documento.embarque.id)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            # Actualizar solo el archivo y cambiar estado a pendiente
            documento.archivo = request.FILES['archivo']
            documento.estado = 'pendiente'
            documento.fecha_validacion = None
            documento.validado_por = None
            documento.observaciones = f"Documento reemplazado el {now().strftime('%d/%m/%Y %H:%M')}."
            documento.save()
            messages.success(request, f"El documento {documento.get_tipo_display()} ha sido reemplazado y está pendiente de validación.")
            return redirect('detalle_embarque', embarque_id=documento.embarque.id)
    else:
        form = DocumentoForm(instance=documento)
    
    return render(request, 'app/reemplazar_documento.html', {
        'form': form,
        'documento': documento,
    })

@login_required
def documentos_por_puerto(request, puerto_id):
    """Vista para mostrar documentos por puerto específico."""
    puerto = get_object_or_404(Puerto, id=puerto_id)
    
    # Verificar que el usuario sea encargado del puerto o administrador
    if not request.user.is_staff:
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            if not perfil.puerto or perfil.puerto != puerto.nombre:
                messages.error(request, "No tienes permisos para ver documentos de este puerto.")
                return redirect('home')
        except PerfilUsuario.DoesNotExist:
            messages.error(request, "No tienes un perfil configurado correctamente.")
            return redirect('home')
    
    # Filtrar documentos por puerto
    documentos = Documento.objects.filter(
        Q(puerto=puerto.nombre) | Q(puerto_objeto=puerto)
    ).order_by('-fecha_subida')
    
    return render(request, 'app/documentos_por_puerto.html', {
        'puerto': puerto,
        'documentos': documentos,
        'title': f'Documentos del puerto {puerto.nombre}',
    })

@login_required
def lista_puertos(request):
    """Lista todos los puertos disponibles."""
    if request.user.is_staff:
        puertos = Puerto.objects.all().order_by('nombre')
    else:
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            if perfil.puerto:
                puertos = Puerto.objects.filter(nombre=perfil.puerto)
            else:
                messages.warning(request, "No tienes un puerto asignado.")
                puertos = []
        except PerfilUsuario.DoesNotExist:
            messages.error(request, "No tienes un perfil configurado correctamente.")
            puertos = []
    
    return render(request, 'app/lista_puertos.html', {
        'puertos': puertos,
        'title': 'Puertos Disponibles',
    })

@login_required
def verificar_documentos_embarque(request, embarque_id):
    """Vista para que los encargados de puerto verifiquen los documentos de un embarque específico."""
    embarque = get_object_or_404(InstruccionEmbarque, id=embarque_id)
    
    # Verificar si el usuario tiene permisos para ver este embarque
    if not request.user.is_staff:
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            if not perfil.puerto or (perfil.puerto != embarque.puerto_embarque and perfil.puerto != embarque.puerto_destino):
                messages.error(request, "No tienes permisos para verificar los documentos de este embarque.")
                return redirect('home')
        except PerfilUsuario.DoesNotExist:
            messages.error(request, "No tienes un perfil configurado correctamente.")
            return redirect('home')
    
    # Obtener documentos asociados al embarque
    documentos = embarque.documentos.all().order_by('tipo', '-fecha_subida')
    
    return render(request, 'app/verificar_documentos.html', {
        'embarque': embarque,
        'documentos': documentos,
        'title': f'Verificación de Documentos - Embarque {embarque.numero_booking}',
    })

@login_required
def confirmar_desembarco(request, embarque_id):
    """Vista para que los encargados de puerto confirmen el desembarco después de validar los documentos."""
    embarque = get_object_or_404(InstruccionEmbarque, id=embarque_id)
    
    # Verificar si el usuario tiene permisos para confirmar este desembarco
    if not request.user.is_staff:
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            if not perfil.puerto or perfil.puerto != embarque.puerto_destino:
                messages.error(request, "No tienes permisos para confirmar el desembarco en este puerto.")
                return redirect('home')
        except PerfilUsuario.DoesNotExist:
            messages.error(request, "No tienes un perfil configurado correctamente.")
            return redirect('home')
    
    # Verificar que todos los documentos requeridos estén validados
    documentos_pendientes = embarque.documentos.filter(
        es_obligatorio=True, 
        estado__in=['pendiente', 'rechazado', 'requiere_correccion']
    )
    
    if request.method == 'POST':
        if documentos_pendientes.exists():
            messages.error(request, "No se puede confirmar el desembarco. Hay documentos obligatorios pendientes de validación.")
        else:
            embarque.estado = "Desembarcado"
            embarque.save()
            messages.success(request, f"El embarque {embarque.numero_booking} ha sido confirmado para desembarco en {embarque.puerto_destino}.")
            return redirect('mis_embarques')
    
    # Obtener los documentos asociados al embarque
    documentos = embarque.documentos.all().order_by('estado', 'tipo')
    
    return render(request, 'app/confirmar_desembarco.html', {
        'embarque': embarque,
        'documentos': documentos,
        'documentos_pendientes': documentos_pendientes,
        'title': f'Confirmar Desembarco - {embarque.numero_booking}',
    })

@require_GET
@login_required
def datos_reserva(request):
    reserva_id = request.GET.get('reserva_id')
    if not reserva_id:
        return JsonResponse({'error': 'No se proporcionó ID de reserva'}, status=400)
    try:
        reserva = ReservaCarga.objects.get(pk=reserva_id)
        data = {
            'numero_booking': reserva.numero_cotizacion or '',
            'numero_contenedor': str(reserva.id),  # Usar el ID de la reserva como número de contenedor
            'exportador': reserva.shipper_nombre or '',
            'consignatario': reserva.consignee_nombre or '',
            'notificar_a': reserva.notify_nombre or '',
            'puerto_embarque': reserva.puerto_origen or '',
            'puerto_destino': reserva.puerto_destino or '',
            'descripcion_carga': reserva.descripcion_mercancia or '',
            'instrucciones_especiales': reserva.instrucciones_especiales or '',
        }
        return JsonResponse(data)
    except ReservaCarga.DoesNotExist:
        return JsonResponse({'error': 'Reserva no encontrada'}, status=404)

@login_required
@require_POST
def eliminar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    embarque_id = documento.embarque.id
    if documento.archivo:
        documento.archivo.delete(save=False)
    documento.delete()
    messages.success(request, 'Documento eliminado correctamente.')
    return redirect('detalle_embarque', embarque_id=embarque_id)

@login_required
@require_POST
def eliminar_instruccion(request, embarque_id):
    embarque = get_object_or_404(InstruccionEmbarque, id=embarque_id)
    # Eliminar documentos asociados y sus archivos
    for doc in embarque.documentos.all():
        if doc.archivo:
            doc.archivo.delete(save=False)
        doc.delete()
    embarque.delete()
    messages.success(request, 'Embarque eliminado correctamente.')
    return redirect('mis_embarques')

@login_required
def descargar_documentos_zip(request, embarque_id):
    """Descarga todos los documentos subidos de un embarque como un ZIP."""
    embarque = get_object_or_404(InstruccionEmbarque, id=embarque_id)
    documentos = embarque.documentos.filter(archivo__isnull=False).exclude(archivo='')
    if not documentos.exists():
        messages.error(request, "No hay documentos para descargar.")
        return redirect('detalle_embarque', embarque_id=embarque.id)

    buffer = BytesIO()
    with ZipFile(buffer, 'w') as zip_file:
        for doc in documentos:
            if doc.archivo and doc.archivo.name:
                nombre = f"{doc.get_tipo_display()}_{doc.id}.pdf"
                with doc.archivo.open('rb') as f:
                    zip_file.writestr(nombre, f.read())
    buffer.seek(0)
    nombre_zip = f"documentos_embarque_{embarque.numero_booking or embarque.id}.zip"
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{nombre_zip}"'
    return response

@login_required
def mis_documentos_usuario(request):
    documentos = InstruccionEmbarque.objects.filter(reserva__usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'app/mis_documentos_usuario.html', {
        'documentos': documentos,
        'title': 'Mis Documentos',
    })

@login_required
def subir_documentos_usuario(request):
    reservas = ReservaCarga.objects.filter(usuario=request.user).order_by('-fecha_creacion_reserva')
    reserva_id = request.GET.get('reserva_id')
    numero_referencia_sugerido = ''
    reserva_seleccionada = None
    embarque = None
    documentos = None
    if reserva_id:
        try:
            reserva_seleccionada = reservas.get(pk=reserva_id)
            numero_referencia_sugerido = reserva_seleccionada.numero_cotizacion or str(reserva_seleccionada.id)
            # Buscar o crear embarque asociado
            from .models import InstruccionEmbarque
            embarque, _ = InstruccionEmbarque.objects.get_or_create(reserva=reserva_seleccionada, defaults={
                'numero_booking': reserva_seleccionada.numero_cotizacion or '',
                'numero_contenedor': str(reserva_seleccionada.id),
                'exportador': getattr(reserva_seleccionada, 'shipper_nombre', ''),
                'consignatario': getattr(reserva_seleccionada, 'consignee_nombre', ''),
                'notificar_a': getattr(reserva_seleccionada, 'notify_nombre', ''),
                'puerto_embarque': getattr(reserva_seleccionada, 'puerto_origen', ''),
                'puerto_destino': getattr(reserva_seleccionada, 'puerto_destino', ''),
                'descripcion_carga': getattr(reserva_seleccionada, 'descripcion_mercancia', ''),
                'instrucciones_especiales': getattr(reserva_seleccionada, 'instrucciones_especiales', ''),
            })
            documentos = embarque.documentos.all().order_by('-fecha_subida')
        except ReservaCarga.DoesNotExist:
            pass
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if reserva_id and embarque:
            if form.is_valid():
                documento = form.save(commit=False)
                documento.embarque = embarque
                documento.save()
                return redirect(f'{request.path}?reserva_id={reserva_id}')
    else:
        form = DocumentoForm()
    return render(request, 'app/subir_documentos_usuario.html', {
        'form': form,
        'reservas': reservas,
        'numero_referencia_sugerido': numero_referencia_sugerido,
        'reserva_seleccionada': reserva_seleccionada,
        'embarque': embarque,
        'documentos': documentos,
    })

@login_required
def aceptar_documentacion_usuario(request):
    if request.method == 'POST':
        embarque_id = request.POST.get('embarque_id')
        if not embarque_id:
            return JsonResponse({'success': False, 'error': 'No se proporcionó embarque.'})
        embarque = get_object_or_404(InstruccionEmbarque, pk=embarque_id, reserva__usuario=request.user)
        if not embarque.documentos.exists():
            return JsonResponse({'success': False, 'error': 'Debes subir al menos un documento antes de enviar.'})
        embarque.estado = 'Enviada para revisión'
        embarque.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})
