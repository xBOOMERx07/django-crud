import os
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse  
from xhtml2pdf import pisa    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import (
    DatosPersonales, Direccion, ExperienciaLaboral, 
    Reconocimiento, CursoRealizado, ProductoAcademico,
    ProductoLaboral, VentaGarage, Habilidad
)

# ==========================================
# VISTA PÚBLICA DEL CV
# ==========================================
def cv_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    
    # Protegido contra Error 500
    datos_personales = DatosPersonales.objects.filter(user=usuario, perfil_activo=True).first()
    
    experiencias = ExperienciaLaboral.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_inicio_gestion')
    reconocimientos = Reconocimiento.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_reconocimiento')
    cursos = CursoRealizado.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_inicio')
    productos_academicos = ProductoAcademico.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_publicacion')
    productos_laborales = ProductoLaboral.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_producto')
    habilidades = Habilidad.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True)
    direcciones = Direccion.objects.filter(user=usuario).order_by('-es_principal', 'tipo')
    
    # Módulo Venta Garage
    productos_garage = VentaGarage.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True, vendido=False).order_by('-fecha_creacion')
    
    context = {
        'datos_personales': datos_personales,
        'experiencias': experiencias,
        'reconocimientos': reconocimientos,
        'cursos': cursos,
        'productos_academicos': productos_academicos,
        'productos_laborales': productos_laborales,
        'habilidades': habilidades,
        'direcciones': direcciones,
        'productos_garage': productos_garage,
        'username': username,
    }
    return render(request, 'cv_publico.html', context)

# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
@login_required
def home(request):
    datos_personales = DatosPersonales.objects.filter(user=request.user).first()
    context = {
        'datos_personales': datos_personales,
        'total_experiencias': ExperienciaLaboral.objects.filter(user=request.user).count(),
        'total_cursos': CursoRealizado.objects.filter(user=request.user).count(),
        'total_habilidades': Habilidad.objects.filter(user=request.user).count(),
        'total_ventas': VentaGarage.objects.filter(user=request.user, vendido=False).count(),
    }
    return render(request, 'home.html', context)

# ==========================================
# AUTENTICACIÓN
# ==========================================
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    if request.POST['password1'] == request.POST['password2']:
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('editar_datos_personales')
        except IntegrityError:
            return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'El usuario ya existe.'})
    return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Contraseñas no coinciden.'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user:
        login(request, user)
        return redirect('home')
    return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Credenciales incorrectas.'})

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

# ==========================================
# GESTIÓN: DATOS PERSONALES
# ==========================================
@login_required
def editar_datos_personales(request):
    datos = DatosPersonales.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if not datos:
            datos = DatosPersonales(user=request.user)
        datos.nombres = request.POST.get('nombres')
        datos.apellidos = request.POST.get('apellidos')
        datos.numero_cedula = request.POST.get('numero_cedula')
        datos.sexo = request.POST.get('sexo', 'H')
        datos.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        datos.telefono_convencional = request.POST.get('telefono_convencional')
        datos.email_personal = request.POST.get('email_personal')
        datos.estado_civil = request.POST.get('estado_civil', 'Soltero/a')
        datos.descripcion_perfil = request.POST.get('descripcion_perfil')
        datos.perfil_activo = request.POST.get('perfil_activo') == 'on'
        if request.FILES.get('foto_perfil'):
            datos.foto_perfil = request.FILES['foto_perfil']
        datos.save()
        return redirect('home')
    return render(request, 'datos_personales/form.html', {'datos': datos})

# ==========================================
# GESTIÓN: EXPERIENCIAS
# ==========================================
@login_required
def lista_experiencias(request):
    experiencias = ExperienciaLaboral.objects.filter(user=request.user).order_by('-fecha_inicio_gestion')
    return render(request, 'experiencias/lista.html', {'experiencias': experiencias})

@login_required
def crear_experiencia(request):
    if request.method == 'POST':
        ExperienciaLaboral.objects.create(
            user=request.user,
            cargo_desempenado=request.POST.get('cargo_desempenado'),
            nombre_empresa=request.POST.get('nombre_empresa'),
            fecha_inicio_gestion=request.POST.get('fecha_inicio_gestion'),
            fecha_fin_gestion=request.POST.get('fecha_fin_gestion') or None,
            actualmente_trabajando=request.POST.get('actualmente_trabajando') == 'on',
            descripcion_funciones=request.POST.get('descripcion_funciones', ''),
            activar_para_que_se_vea_en_front=request.POST.get('activar_para_que_se_vea_en_front') == 'on',
        )
        return redirect('lista_experiencias')
    return render(request, 'experiencias/form.html', {'action': 'Crear'})

@login_required
def eliminar_experiencia(request, pk):
    exp = get_object_or_404(ExperienciaLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        exp.delete()
        return redirect('lista_experiencias')
    return render(request, 'confirmar_eliminar.html', {'objeto': exp, 'tipo': 'Experiencia'})

# ==========================================
# GESTIÓN: CURSOS
# ==========================================
@login_required
def lista_cursos(request):
    cursos = CursoRealizado.objects.filter(user=request.user).order_by('-fecha_inicio')
    return render(request, 'cursos/lista.html', {'cursos': cursos})

@login_required
def crear_curso(request):
    if request.method == 'POST':
        CursoRealizado.objects.create(
            user=request.user,
            nombre_curso=request.POST.get('nombre_curso'),
            entidad_patrocinadora=request.POST.get('entidad_patrocinadora'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin') or None,
            total_horas=int(request.POST.get('total_horas', 1)),
            descripcion_curso=request.POST.get('descripcion_curso', ''),
            activar_para_que_se_vea_en_front=request.POST.get('activar_para_que_se_vea_en_front') == 'on',
        )
        return redirect('lista_cursos')
    return render(request, 'cursos/form.html', {'action': 'Crear'})

# ==========================================
# GESTIÓN: HABILIDADES
# ==========================================
@login_required
def lista_habilidades(request):
    habilidades = Habilidad.objects.filter(user=request.user)
    return render(request, 'habilidades/lista.html', {'habilidades': habilidades})

@login_required
def crear_habilidad(request):
    if request.method == 'POST':
        Habilidad.objects.create(
            user=request.user,
            nombre=request.POST.get('nombre'),
            nivel=request.POST.get('nivel', 'basico'),
            categoria=request.POST.get('categoria', ''),
            activar_para_que_se_vea_en_front=request.POST.get('activar_para_que_se_vea_en_front') == 'on',
        )
        return redirect('lista_habilidades')
    return render(request, 'habilidades/form.html', {'action': 'Crear'})

@login_required
def eliminar_habilidad(request, pk):
    hab = get_object_or_404(Habilidad, pk=pk, user=request.user)
    if request.method == 'POST':
        hab.delete()
        return redirect('lista_habilidades')
    return render(request, 'confirmar_eliminar.html', {'objeto': hab, 'tipo': 'Habilidad'})

# ==========================================
# GESTIÓN: VENTA GARAGE
# ==========================================
@login_required
def lista_ventas_garage(request):
    productos = VentaGarage.objects.filter(user=request.user).order_by('-fecha_creacion')
    return render(request, 'venta_garage/lista.html', {'productos': productos})

@login_required
def crear_venta_garage(request):
    if request.method == 'POST':
        producto = VentaGarage.objects.create(
            user=request.user,
            nombre_producto=request.POST.get('nombre_producto'),
            estado_producto=request.POST.get('estado_producto', 'Bueno'),
            descripcion=request.POST.get('descripcion', ''),
            valor_del_bien=float(request.POST.get('valor_del_bien', 0)),
            activar_para_que_se_vea_en_front=request.POST.get('activar_para_que_se_vea_en_front') == 'on',
        )
        if request.FILES.get('foto_producto'):
            producto.foto_producto = request.FILES['foto_producto']
            producto.save()
        return redirect('lista_ventas_garage')
    return render(request, 'venta_garage/form.html', {'action': 'Crear', 'producto': None})

@login_required
def editar_venta_garage(request, pk):
    producto = get_object_or_404(VentaGarage, pk=pk, user=request.user)
    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.estado_producto = request.POST.get('estado_producto', 'Bueno')
        producto.descripcion = request.POST.get('descripcion', '')
        producto.valor_del_bien = float(request.POST.get('valor_del_bien', 0))
        producto.vendido = request.POST.get('vendido') == 'on'
        producto.activar_para_que_se_vea_en_front = request.POST.get('activar_para_que_se_vea_en_front') == 'on'
        if request.FILES.get('foto_producto'):
            producto.foto_producto = request.FILES['foto_producto']
        producto.save()
        return redirect('lista_ventas_garage')
    return render(request, 'venta_garage/form.html', {'action': 'Editar', 'producto': producto})

@login_required
def eliminar_venta_garage(request, pk):
    producto = get_object_or_404(VentaGarage, pk=pk, user=request.user)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_ventas_garage')
    return render(request, 'confirmar_eliminar.html', {'objeto': producto, 'tipo': 'Producto'})

# ==========================================
# GENERAR PDF
# ==========================================
def descargar_pdf(request, username):
    usuario = get_object_or_404(User, username=username)
    datos_personales = DatosPersonales.objects.filter(user=usuario, perfil_activo=True).first()
    context = {
        'datos_personales': datos_personales,
        'experiencias': ExperienciaLaboral.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_inicio_gestion'),
        'cursos': CursoRealizado.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('-fecha_inicio'),
        'habilidades': Habilidad.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True),
        'reconocimientos': Reconocimiento.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True),
        'productos_academicos': ProductoAcademico.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True),
        'productos_laborales': ProductoLaboral.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True),
        'direcciones': Direccion.objects.filter(user=usuario).order_by('-es_principal'),
    }
    html_string = render_to_string('cv_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{username}.pdf"'
    pisa.CreatePDF(html_string, dest=response)
    return response