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
    """CV público accesible para todos"""
    usuario = get_object_or_404(User, username=username)
    
    try:
        datos_personales = DatosPersonales.objects.get(user=usuario, perfil_activo=True)
    except DatosPersonales.DoesNotExist:
        datos_personales = None
    
    # Obtener solo elementos activos (activar_para_que_se_vea_en_front=True)
    experiencias = ExperienciaLaboral.objects.filter(
        user=usuario, 
        activar_para_que_se_vea_en_front=True
    ).order_by('-fecha_inicio_gestion')
    
    reconocimientos = Reconocimiento.objects.filter(
        user=usuario,
        activar_para_que_se_vea_en_front=True
    ).order_by('-fecha_reconocimiento')
    
    cursos = CursoRealizado.objects.filter(
        user=usuario,
        activar_para_que_se_vea_en_front=True
    ).order_by('-fecha_inicio')
    
    productos_academicos = ProductoAcademico.objects.filter(
        user=usuario,
        activar_para_que_se_vea_en_front=True
    ).order_by('-fecha_publicacion')
    
    productos_laborales = ProductoLaboral.objects.filter(
        user=usuario,
        activar_para_que_se_vea_en_front=True
    ).order_by('-fecha_producto')
    
    habilidades = Habilidad.objects.filter(
        user=usuario,
        activar_para_que_se_vea_en_front=True
    )
    
    direcciones = Direccion.objects.filter(user=usuario).order_by('-es_principal', 'tipo')
    
    context = {
        'datos_personales': datos_personales,
        'experiencias': experiencias,
        'reconocimientos': reconocimientos,
        'cursos': cursos,
        'productos_academicos': productos_academicos,
        'productos_laborales': productos_laborales,
        'habilidades': habilidades,
        'direcciones': direcciones,
        'username': username,
    }
    
    return render(request, 'cv_publico.html', context)


# ==========================================
# DASHBOARD PRINCIPAL
# ==========================================
@login_required
def home(request):
    """Dashboard del usuario"""
    try:
        datos_personales = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        datos_personales = None
    
    # Contadores
    total_experiencias = ExperienciaLaboral.objects.filter(user=request.user).count()
    total_cursos = CursoRealizado.objects.filter(user=request.user).count()
    total_habilidades = Habilidad.objects.filter(user=request.user).count()
    
    context = {
        'datos_personales': datos_personales,
        'total_experiencias': total_experiencias,
        'total_cursos': total_cursos,
        'total_habilidades': total_habilidades,
    }
    return render(request, 'home.html', context)


# ==========================================
# AUTENTICACIÓN
# ==========================================
def signup(request):
    """Registro de nuevos usuarios"""
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('editar_datos_personales')  # Llevar a completar perfil
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe. Intenta con otro nombre.'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden.'
        })


def signin(request):
    """Inicio de sesión"""
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos.'
            })
        login(request, user)
        return redirect('home')


@login_required
def signout(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('signin')


# ==========================================
# GESTIÓN: DATOS PERSONALES
# ==========================================
@login_required
def editar_datos_personales(request):
    """Crear o editar datos personales"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        datos = None
    
    if request.method == 'POST':
        # Procesar formulario manualmente (simplificado)
        if datos:
            # Actualizar
            datos.nombres = request.POST.get('nombres', '')
            datos.apellidos = request.POST.get('apellidos', '')
            datos.numero_cedula = request.POST.get('numero_cedula', '')
            datos.sexo = request.POST.get('sexo', 'H')
            datos.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            datos.telefono_convencional = request.POST.get('telefono_convencional', '')
            datos.email_personal = request.POST.get('email_personal', '')
            datos.estado_civil = request.POST.get('estado_civil', 'Soltero/a')
            datos.descripcion_perfil = request.POST.get('descripcion_perfil', '')
            datos.perfil_activo = request.POST.get('perfil_activo') == 'on'
            
            # Manejar foto de perfil
            if request.FILES.get('foto_perfil'):
                datos.foto_perfil = request.FILES['foto_perfil']
            
            datos.save()
        else:
            # Crear
            datos = DatosPersonales.objects.create(
                user=request.user,
                nombres=request.POST.get('nombres', ''),
                apellidos=request.POST.get('apellidos', ''),
                numero_cedula=request.POST.get('numero_cedula', ''),
                sexo=request.POST.get('sexo', 'H'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                telefono_convencional=request.POST.get('telefono_convencional', ''),
                email_personal=request.POST.get('email_personal', ''),
                estado_civil=request.POST.get('estado_civil', 'Soltero/a'),
                descripcion_perfil=request.POST.get('descripcion_perfil', ''),
                perfil_activo=request.POST.get('perfil_activo') == 'on'
            )
            
            # Manejar foto de perfil en creación
            if request.FILES.get('foto_perfil'):
                datos.foto_perfil = request.FILES['foto_perfil']
                datos.save()
        
        return redirect('home')
    
    return render(request, 'datos_personales/form.html', {'datos': datos})


# ==========================================
# GESTIÓN: EXPERIENCIA LABORAL
# ==========================================
@login_required
def lista_experiencias(request):
    """Lista de experiencias laborales"""
    experiencias = ExperienciaLaboral.objects.filter(user=request.user)
    return render(request, 'experiencias/lista.html', {'experiencias': experiencias})


@login_required
def crear_experiencia(request):
    """Crear nueva experiencia"""
    if request.method == 'POST':
        ExperienciaLaboral.objects.create(
            user=request.user,
            cargo_desempenado=request.POST.get('cargo_desempenado'),
            nombre_empresa=request.POST.get('nombre_empresa'),
            fecha_inicio_gestion=request.POST.get('fecha_inicio_gestion'),
            fecha_fin_gestion=request.POST.get('fecha_fin_gestion') or None,
            actualmente_trabajando=request.POST.get('actualmente_trabajando') == 'on',
            descripcion_funciones=request.POST.get('descripcion_funciones', ''),
        )
        return redirect('lista_experiencias')
    
    return render(request, 'experiencias/form.html', {'action': 'Crear'})


@login_required
def eliminar_experiencia(request, pk):
    """Eliminar experiencia"""
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
    """Lista de cursos"""
    cursos = CursoRealizado.objects.filter(user=request.user)
    return render(request, 'cursos/lista.html', {'cursos': cursos})


@login_required
def crear_curso(request):
    """Crear nuevo curso"""
    if request.method == 'POST':
        CursoRealizado.objects.create(
            user=request.user,
            nombre_curso=request.POST.get('nombre_curso'),
            entidad_patrocinadora=request.POST.get('entidad_patrocinadora'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin') or None,
            total_horas=int(request.POST.get('total_horas', 1)),
            descripcion_curso=request.POST.get('descripcion_curso', ''),
        )
        return redirect('lista_cursos')
    
    return render(request, 'cursos/form.html', {'action': 'Crear'})


# ==========================================
# GESTIÓN: HABILIDADES
# ==========================================
@login_required
def lista_habilidades(request):
    """Lista de habilidades"""
    habilidades = Habilidad.objects.filter(user=request.user)
    return render(request, 'habilidades/lista.html', {'habilidades': habilidades})


@login_required
def crear_habilidad(request):
    """Crear nueva habilidad"""
    if request.method == 'POST':
        Habilidad.objects.create(
            user=request.user,
            nombre=request.POST.get('nombre'),
            nivel=request.POST.get('nivel', 'basico'),
            categoria=request.POST.get('categoria', ''),
        )
        return redirect('lista_habilidades')
    
    return render(request, 'habilidades/form.html', {'action': 'Crear'})


@login_required
def eliminar_habilidad(request, pk):
    """Eliminar habilidad"""
    hab = get_object_or_404(Habilidad, pk=pk, user=request.user)
    if request.method == 'POST':
        hab.delete()
        return redirect('lista_habilidades')
    return render(request, 'confirmar_eliminar.html', {'objeto': hab, 'tipo': 'Habilidad'})