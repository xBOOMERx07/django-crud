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
from .forms import (
    DatosPersonalesForm, ExperienciaLaboralForm, CursoRealizadoForm,
    HabilidadForm, ReconocimientoForm, ProductoAcademicoForm, ProductoLaboralForm
)

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
            'total_reconocimientos': Reconocimiento.objects.filter(user=request.user).count(),
            'total_productos_academicos': ProductoAcademico.objects.filter(user=request.user).count(),
            'total_productos_laborales': ProductoLaboral.objects.filter(user=request.user).count(),
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
            'total_reconocimientos': 0,
            'total_productos_academicos': 0,
            'total_productos_laborales': 0,
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
    """Editar datos personales del usuario."""
    datos, created = DatosPersonales.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Datos guardados correctamente')
            return redirect('home')
        else:
            return render(request, 'datos_personales/form.html', {
                'form': form,
                'datos': datos,
                'error': 'Por favor corrige los errores marcados.'
            })
    else:
        form = DatosPersonalesForm(instance=datos)
    
    return render(request, 'datos_personales/form.html', {
        'form': form,
        'datos': datos
    })


# ==========================================
# GESTIÓN: EXPERIENCIAS LABORALES
# ==========================================
@login_required
def lista_experiencias(request):
    experiencias = ExperienciaLaboral.objects.filter(user=request.user).order_by('fecha_inicio_gestion')
    return render(request, 'experiencias/lista.html', {'experiencias': experiencias})

@login_required
def crear_experiencia(request):
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, '✅ Experiencia creada correctamente')
            return redirect('lista_experiencias')
    else:
        form = ExperienciaLaboralForm()
    return render(request, 'experiencias/form.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_experiencia(request, pk):
    exp = get_object_or_404(ExperienciaLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES, instance=exp)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Experiencia actualizada correctamente')
            return redirect('lista_experiencias')
    else:
        form = ExperienciaLaboralForm(instance=exp)
    return render(request, 'experiencias/form.html', {'form': form, 'action': 'Editar', 'objeto': exp})

@login_required
def eliminar_experiencia(request, pk):
    exp = get_object_or_404(ExperienciaLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, '✅ Experiencia eliminada correctamente')
        return redirect('lista_experiencias')
    return render(request, 'confirmar_eliminar.html', {'objeto': exp, 'tipo': 'Experiencia'})

# ==========================================
# GESTIÓN: CURSOS
# ==========================================
@login_required
def lista_cursos(request):
    cursos = CursoRealizado.objects.filter(user=request.user).order_by('fecha_inicio')
    return render(request, 'cursos/lista.html', {'cursos': cursos})

@login_required
def crear_curso(request):
    if request.method == 'POST':
        form = CursoRealizadoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.user = request.user
            curso.save()
            messages.success(request, '✅ Curso creado correctamente')
            return redirect('lista_cursos')
    else:
        form = CursoRealizadoForm()
    return render(request, 'cursos/form.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_curso(request, pk):
    curso = get_object_or_404(CursoRealizado, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CursoRealizadoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Curso actualizado correctamente')
            return redirect('lista_cursos')
    else:
        form = CursoRealizadoForm(instance=curso)
    return render(request, 'cursos/form.html', {'form': form, 'action': 'Editar', 'objeto': curso})

@login_required
def eliminar_curso(request, pk):
    curso = get_object_or_404(CursoRealizado, pk=pk, user=request.user)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, '✅ Curso eliminado correctamente')
        return redirect('lista_cursos')
    return render(request, 'confirmar_eliminar.html', {'objeto': curso, 'tipo': 'Curso'})

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
        form = HabilidadForm(request.POST)
        if form.is_valid():
            hab = form.save(commit=False)
            hab.user = request.user
            hab.save()
            messages.success(request, '✅ Habilidad creada correctamente')
            return redirect('lista_habilidades')
    else:
        form = HabilidadForm()
    return render(request, 'habilidades/form.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_habilidad(request, pk):
    hab = get_object_or_404(Habilidad, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabilidadForm(request.POST, instance=hab)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Habilidad actualizada correctamente')
            return redirect('lista_habilidades')
    else:
        form = HabilidadForm(instance=hab)
    return render(request, 'habilidades/form.html', {'form': form, 'action': 'Editar', 'objeto': hab})

@login_required
def eliminar_habilidad(request, pk):
    hab = get_object_or_404(Habilidad, pk=pk, user=request.user)
    if request.method == 'POST':
        hab.delete()
        messages.success(request, '✅ Habilidad eliminada correctamente')
        return redirect('lista_habilidades')
    return render(request, 'confirmar_eliminar.html', {'objeto': hab, 'tipo': 'Habilidad'})

# ==========================================
# GESTIÓN: RECONOCIMIENTOS
# ==========================================
@login_required
def lista_reconocimientos(request):
    reconocimientos = Reconocimiento.objects.filter(user=request.user).order_by('fecha_reconocimiento')
    return render(request, 'reconocimientos/lista.html', {'reconocimientos': reconocimientos})

@login_required
def crear_reconocimiento(request):
    if request.method == 'POST':
        form = ReconocimientoForm(request.POST, request.FILES)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.user = request.user
            rec.save()
            messages.success(request, '✅ Reconocimiento creado correctamente')
            return redirect('lista_reconocimientos')
    else:
        form = ReconocimientoForm()
    return render(request, 'reconocimientos/form.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_reconocimiento(request, pk):
    rec = get_object_or_404(Reconocimiento, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReconocimientoForm(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Reconocimiento actualizado correctamente')
            return redirect('lista_reconocimientos')
    else:
        form = ReconocimientoForm(instance=rec)
    return render(request, 'reconocimientos/form.html', {'form': form, 'action': 'Editar', 'objeto': rec})

@login_required
def eliminar_reconocimiento(request, pk):
    rec = get_object_or_404(Reconocimiento, pk=pk, user=request.user)
    if request.method == 'POST':
        rec.delete()
        messages.success(request, '✅ Reconocimiento eliminado correctamente')
        return redirect('lista_reconocimientos')
    return render(request, 'confirmar_eliminar.html', {'objeto': rec, 'tipo': 'Reconocimiento'})

# ==========================================
# GESTIÓN: PRODUCTOS ACADÉMICOS
# ==========================================
@login_required
def lista_productos_academicos(request):
    productos = ProductoAcademico.objects.filter(user=request.user).order_by('fecha_publicacion')
    return render(request, 'productos_academicos/lista.html', {'productos': productos})

@login_required
def crear_producto_academico(request):
    if request.method == 'POST':
        form = ProductoAcademicoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.user = request.user
            producto.save()
            messages.success(request, '✅ Producto académico creado correctamente')
            return redirect('lista_productos_academicos')
    else:
        form = ProductoAcademicoForm()
    return render(request, 'productos_academicos/form.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_producto_academico(request, pk):
    producto = get_object_or_404(ProductoAcademico, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductoAcademicoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto académico actualizado correctamente')
            return redirect('lista_productos_academicos')
    else:
        form = ProductoAcademicoForm(instance=producto)
    return render(request, 'productos_academicos/form.html', {'form': form, 'action': 'Editar', 'producto': producto})

@login_required
def eliminar_producto_academico(request, pk):
    prod = get_object_or_404(ProductoAcademico, pk=pk, user=request.user)
    if request.method == 'POST':
        prod.delete()
        messages.success(request, '✅ Producto académico eliminado correctamente')
        return redirect('lista_productos_academicos')
    return render(request, 'confirmar_eliminar.html', {'objeto': prod, 'tipo': 'Producto Académico'})

# ==========================================
# GESTIÓN: PRODUCTOS LABORALES
# ==========================================
@login_required
def lista_productos_laborales(request):
    productos = ProductoLaboral.objects.filter(user=request.user).order_by('fecha_producto')
    return render(request, 'productos_laborales/lista.html', {'productos': productos})

@login_required
def crear_producto_laboral(request):
    if request.method == 'POST':
        form = ProductoLaboralForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.user = request.user
            producto.save()
            messages.success(request, '✅ Producto laboral creado correctamente')
            return redirect('lista_productos_laborales')
    else:
        form = ProductoLaboralForm()
    return render(request, 'productos_laborales/form.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_producto_laboral(request, pk):
    producto = get_object_or_404(ProductoLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductoLaboralForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto laboral actualizado correctamente')
            return redirect('lista_productos_laborales')
    else:
        form = ProductoLaboralForm(instance=producto)
    return render(request, 'productos_laborales/form.html', {'form': form, 'action': 'Editar', 'producto': producto})

@login_required
def eliminar_producto_laboral(request, pk):
    prod = get_object_or_404(ProductoLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        prod.delete()
        messages.success(request, '✅ Producto laboral eliminado correctamente')
        return redirect('lista_productos_laborales')
    return render(request, 'confirmar_eliminar.html', {'objeto': prod, 'tipo': 'Producto Laboral'})

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
        messages.success(request, '✅ Producto creado correctamente')
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
        messages.success(request, '✅ Producto actualizado correctamente')
        return redirect('lista_ventas_garage')
    return render(request, 'venta_garage/form.html', {'action': 'Editar', 'producto': producto})

@login_required
def eliminar_venta_garage(request, pk):
    producto = get_object_or_404(VentaGarage, pk=pk, user=request.user)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, '✅ Producto eliminado correctamente')
        return redirect('lista_ventas_garage')
    return render(request, 'confirmar_eliminar.html', {'objeto': producto, 'tipo': 'Producto'})

# ==========================================
# 📄 GENERAR PDF DINÁMICO CON SECCIONES SELECCIONADAS
# ==========================================
def descargar_pdf(request, username):
    """Genera un PDF personalizado con las secciones seleccionadas por el usuario."""
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