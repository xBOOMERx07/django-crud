from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import PersonalInfo, ExperienciaLaboral, Educacion, Habilidad, Proyecto, Certificacion
from .forms import (PersonalInfoForm, ExperienciaLaboralForm, EducacionForm, 
                   HabilidadForm, ProyectoForm, CertificacionForm)

# Vista pública del CV
def cv_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    
    try:
        info_personal = PersonalInfo.objects.get(user=usuario)
    except PersonalInfo.DoesNotExist:
        info_personal = None
    
    experiencias = ExperienciaLaboral.objects.filter(user=usuario).order_by('-fecha_inicio')
    educacion = Educacion.objects.filter(user=usuario).order_by('-fecha_inicio')
    habilidades = Habilidad.objects.filter(user=usuario)
    proyectos = Proyecto.objects.filter(user=usuario).order_by('-fecha')
    certificaciones = Certificacion.objects.filter(user=usuario).order_by('-fecha_obtencion')
    
    context = {
        'info_personal': info_personal,
        'experiencias': experiencias,
        'educacion': educacion,
        'habilidades': habilidades,
        'proyectos': proyectos,
        'certificaciones': certificaciones,
        'username': username,
    }
    
    return render(request, 'cv_publico.html', context)

# Dashboard principal
@login_required
def home(request):
    try:
        info_personal = PersonalInfo.objects.get(user=request.user)
    except PersonalInfo.DoesNotExist:
        info_personal = None
    
    experiencias = ExperienciaLaboral.objects.filter(user=request.user)[:3]
    educacion = Educacion.objects.filter(user=request.user)[:3]
    proyectos = Proyecto.objects.filter(user=request.user, destacado=True)[:3]
    
    context = {
        'info_personal': info_personal,
        'experiencias': experiencias,
        'educacion': educacion,
        'proyectos': proyectos,
    }
    return render(request, 'home.html', context)

# Registro de usuarios
def signup(request):
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
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

# Login
def signin(request):
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
                'error': 'Usuario o contraseña incorrectos'
            })
        login(request, user)
        return redirect('home')

# Logout
@login_required
def signout(request):
    logout(request)
    return redirect('signin')

# CRUD - Información Personal
@login_required
def editar_info_personal(request):
    try:
        info_personal = PersonalInfo.objects.get(user=request.user)
    except PersonalInfo.DoesNotExist:
        info_personal = None
    
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=info_personal)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            return redirect('home')
    else:
        form = PersonalInfoForm(instance=info_personal)
    
    return render(request, 'editar_info_personal.html', {'form': form})

# CRUD - Experiencia Laboral
@login_required
def lista_experiencias(request):
    experiencias = ExperienciaLaboral.objects.filter(user=request.user)
    return render(request, 'lista_experiencias.html', {'experiencias': experiencias})

@login_required
def crear_experiencia(request):
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.user = request.user
            experiencia.save()
            return redirect('lista_experiencias')
    else:
        form = ExperienciaLaboralForm()
    
    return render(request, 'form_experiencia.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            return redirect('lista_experiencias')
    else:
        form = ExperienciaLaboralForm(instance=experiencia)
    
    return render(request, 'form_experiencia.html', {'form': form, 'action': 'Editar'})

@login_required
def eliminar_experiencia(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk, user=request.user)
    if request.method == 'POST':
        experiencia.delete()
        return redirect('lista_experiencias')
    return render(request, 'confirmar_eliminar.html', {'objeto': experiencia, 'tipo': 'Experiencia'})

# CRUD - Educación
@login_required
def lista_educacion(request):
    educacion = Educacion.objects.filter(user=request.user)
    return render(request, 'lista_educacion.html', {'educacion': educacion})

@login_required
def crear_educacion(request):
    if request.method == 'POST':
        form = EducacionForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()
            return redirect('lista_educacion')
    else:
        form = EducacionForm()
    
    return render(request, 'form_educacion.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_educacion(request, pk):
    educacion = get_object_or_404(Educacion, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EducacionForm(request.POST, instance=educacion)
        if form.is_valid():
            form.save()
            return redirect('lista_educacion')
    else:
        form = EducacionForm(instance=educacion)
    
    return render(request, 'form_educacion.html', {'form': form, 'action': 'Editar'})

@login_required
def eliminar_educacion(request, pk):
    educacion = get_object_or_404(Educacion, pk=pk, user=request.user)
    if request.method == 'POST':
        educacion.delete()
        return redirect('lista_educacion')
    return render(request, 'confirmar_eliminar.html', {'objeto': educacion, 'tipo': 'Educación'})

# CRUD - Habilidades
@login_required
def lista_habilidades(request):
    habilidades = Habilidad.objects.filter(user=request.user)
    return render(request, 'lista_habilidades.html', {'habilidades': habilidades})

@login_required
def crear_habilidad(request):
    if request.method == 'POST':
        form = HabilidadForm(request.POST)
        if form.is_valid():
            habilidad = form.save(commit=False)
            habilidad.user = request.user
            habilidad.save()
            return redirect('lista_habilidades')
    else:
        form = HabilidadForm()
    
    return render(request, 'form_habilidad.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_habilidad(request, pk):
    habilidad = get_object_or_404(Habilidad, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabilidadForm(request.POST, instance=habilidad)
        if form.is_valid():
            form.save()
            return redirect('lista_habilidades')
    else:
        form = HabilidadForm(instance=habilidad)
    
    return render(request, 'form_habilidad.html', {'form': form, 'action': 'Editar'})

@login_required
def eliminar_habilidad(request, pk):
    habilidad = get_object_or_404(Habilidad, pk=pk, user=request.user)
    if request.method == 'POST':
        habilidad.delete()
        return redirect('lista_habilidades')
    return render(request, 'confirmar_eliminar.html', {'objeto': habilidad, 'tipo': 'Habilidad'})

# CRUD - Proyectos
@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.filter(user=request.user)
    return render(request, 'lista_proyectos.html', {'proyectos': proyectos})

@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.user = request.user
            proyecto.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm()
    
    return render(request, 'form_proyecto.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    
    return render(request, 'form_proyecto.html', {'form': form, 'action': 'Editar'})

@login_required
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk, user=request.user)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('lista_proyectos')
    return render(request, 'confirmar_eliminar.html', {'objeto': proyecto, 'tipo': 'Proyecto'})

# CRUD - Certificaciones
@login_required
def lista_certificaciones(request):
    certificaciones = Certificacion.objects.filter(user=request.user)
    return render(request, 'lista_certificaciones.html', {'certificaciones': certificaciones})

@login_required
def crear_certificacion(request):
    if request.method == 'POST':
        form = CertificacionForm(request.POST)
        if form.is_valid():
            certificacion = form.save(commit=False)
            certificacion.user = request.user
            certificacion.save()
            return redirect('lista_certificaciones')
    else:
        form = CertificacionForm()
    
    return render(request, 'form_certificacion.html', {'form': form, 'action': 'Crear'})

@login_required
def editar_certificacion(request, pk):
    certificacion = get_object_or_404(Certificacion, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CertificacionForm(request.POST, instance=certificacion)
        if form.is_valid():
            form.save()
            return redirect('lista_certificaciones')
    else:
        form = CertificacionForm(instance=certificacion)
    
    return render(request, 'form_certificacion.html', {'form': form, 'action': 'Editar'})

@login_required
def eliminar_certificacion(request, pk):
    certificacion = get_object_or_404(Certificacion, pk=pk, user=request.user)
    if request.method == 'POST':
        certificacion.delete()
        return redirect('lista_certificaciones')
    return render(request, 'confirmar_eliminar.html', {'objeto': certificacion, 'tipo': 'Certificación'})