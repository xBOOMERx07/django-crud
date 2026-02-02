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
from django.contrib import messages
from django.db import IntegrityError
from .models import (
    DatosPersonales, Direccion, ExperienciaLaboral, 
    Reconocimiento, CursoRealizado, ProductoAcademico,
    ProductoLaboral, VentaGarage, Habilidad
)
from .forms import DatosPersonalesForm

# ==========================================
# VISTA PÚBLICA DEL CV
# ==========================================
def cv_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    
    # Protegido contra Error 500
    datos_personales = DatosPersonales.objects.filter(user=usuario, perfil_activo=True).first()
    
    # 🔄 Orden cronológico ASCENDENTE (más antiguo primero)
    experiencias = ExperienciaLaboral.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('fecha_inicio_gestion')
    reconocimientos = Reconocimiento.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('fecha_reconocimiento')
    cursos = CursoRealizado.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('fecha_inicio')
    
    productos_academicos = ProductoAcademico.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('fecha_publicacion')
    productos_laborales = ProductoLaboral.objects.filter(user=usuario, activar_para_que_se_vea_en_front=True).order_by('fecha_producto')
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
    try:
        datos_personales = DatosPersonales.objects.filter(user=request.user).first()
        context = {
            'datos_personales': datos_personales,
            'total_experiencias': ExperienciaLaboral.objects.filter(user=request.user).count(),
            'total_cursos': CursoRealizado.objects.filter(user=request.user).count(),
            'total_habilidades': Habilidad.objects.filter(user=request.user).count(),
            'total_ventas': VentaGarage.objects.filter(user=request.user, vendido=False).count(),
        }
        return render(request, 'home.html', context)
    except Exception as e:
        print(f"Error en home: {e}")
        return render(request, 'home.html', {
            'datos_personales': None,
            'total_experiencias': 0,
            'total_cursos': 0,
            'total_habilidades': 0,
            'total_ventas': 0,
        })

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
    """
    Editar datos personales del usuario.
    
    ARREGLO: Se asegura que el formulario siempre tenga instance=datos
    para que los campos se pre-llenen correctamente, incluyendo fecha_nacimiento.
    """
    # Obtener o crear datos personales
    datos, created = DatosPersonales.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Usar el formulario Django con los datos POST y archivos
        form = DatosPersonalesForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            # Guardar (el usuario ya está asignado por get_or_create)
            form.save()
            messages.success(request, '✅ Datos guardados correctamente')
            return redirect('home')
        else:
            # Si hay errores, mostrar el formulario con errores
            return render(request, 'datos_personales/form.html', {
                'form': form,
                'datos': datos,
                'error': 'Por favor corrige los errores marcados.'
            })
    else:
        # GET: Mostrar formulario con datos existentes
        form = DatosPersonalesForm(instance=datos)
    
    return render(request, 'datos_personales/form.html', {
        'form': form,
        'datos': datos
    })


# ==========================================
# GESTIÓN: EXPERIENCIAS
# ==========================================
@login_required
def lista_experiencias(request):
    # 🔄 Orden cronológico ASCENDENTE
    experiencias = ExperienciaLaboral.objects.filter(user=request.user).order_by('fecha_inicio_gestion')
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
    # 🔄 Orden cronológico ASCENDENTE
    cursos = CursoRealizado.objects.filter(user=request.user).order_by('fecha_inicio')
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
# 📄 GENERAR PDF DINÁMICO CON SECCIONES SELECCIONADAS
# ==========================================
def descargar_pdf(request, username):
    """
    Genera un PDF personalizado con las secciones seleccionadas por el usuario.
    
    Parámetros GET esperados:
    - incluir_experiencias: 'on' si se debe incluir
    - incluir_cursos: 'on' si se debe incluir
    - incluir_reconocimientos: 'on' si se debe incluir
    - incluir_productos_academicos: 'on' si se debe incluir
    - incluir_productos_laborales: 'on' si se debe incluir
    - incluir_habilidades: 'on' si se debe incluir
    """
    usuario = get_object_or_404(User, username=username)
    datos_personales = DatosPersonales.objects.filter(user=usuario, perfil_activo=True).first()
    
    # 📋 Obtener parámetros de secciones a incluir
    incluir_experiencias = request.GET.get('incluir_experiencias') == 'on'
    incluir_cursos = request.GET.get('incluir_cursos') == 'on'
    incluir_reconocimientos = request.GET.get('incluir_reconocimientos') == 'on'
    incluir_productos_academicos = request.GET.get('incluir_productos_academicos') == 'on'
    incluir_productos_laborales = request.GET.get('incluir_productos_laborales') == 'on'
    incluir_habilidades = request.GET.get('incluir_habilidades') == 'on'
    
    # 🔄 Cargar datos en orden cronológico ASCENDENTE (más antiguo primero)
    context = {
        'datos_personales': datos_personales,
        'direcciones': Direccion.objects.filter(user=usuario).order_by('-es_principal'),
        
        # Flags para controlar qué secciones mostrar
        'incluir_experiencias': incluir_experiencias,
        'incluir_cursos': incluir_cursos,
        'incluir_reconocimientos': incluir_reconocimientos,
        'incluir_productos_academicos': incluir_productos_academicos,
        'incluir_productos_laborales': incluir_productos_laborales,
        'incluir_habilidades': incluir_habilidades,
    }
    
    # Solo cargar los datos si la sección está incluida (optimización)
    if incluir_experiencias:
        context['experiencias'] = ExperienciaLaboral.objects.filter(
            user=usuario, 
            activar_para_que_se_vea_en_front=True
        ).order_by('fecha_inicio_gestion')
    
    if incluir_cursos:
        context['cursos'] = CursoRealizado.objects.filter(
            user=usuario, 
            activar_para_que_se_vea_en_front=True
        ).order_by('fecha_inicio')
    
    if incluir_reconocimientos:
        context['reconocimientos'] = Reconocimiento.objects.filter(
            user=usuario, 
            activar_para_que_se_vea_en_front=True
        ).order_by('fecha_reconocimiento')
    
    if incluir_productos_academicos:
        context['productos_academicos'] = ProductoAcademico.objects.filter(
            user=usuario, 
            activar_para_que_se_vea_en_front=True
        ).order_by('fecha_publicacion')
    
    if incluir_productos_laborales:
        context['productos_laborales'] = ProductoLaboral.objects.filter(
            user=usuario, 
            activar_para_que_se_vea_en_front=True
        ).order_by('fecha_producto')
    
    if incluir_habilidades:
        context['habilidades'] = Habilidad.objects.filter(
            user=usuario, 
            activar_para_que_se_vea_en_front=True
        )
    
    # Renderizar template y generar PDF
    html_string = render_to_string('cv_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{username}.pdf"'
    pisa.CreatePDF(html_string, dest=response)
    return response