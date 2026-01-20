from django.contrib import admin
from .models import PersonalInfo, ExperienciaLaboral, Educacion, Habilidad, Proyecto, Certificacion

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'titulo_profesional']
    search_fields = ['nombre_completo', 'email']

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ['puesto', 'empresa', 'fecha_inicio', 'fecha_fin', 'actualmente_trabajando']
    list_filter = ['actualmente_trabajando', 'fecha_inicio']
    search_fields = ['puesto', 'empresa']
    ordering = ['-fecha_inicio']

@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'institucion', 'fecha_inicio', 'fecha_fin']
    list_filter = ['actualmente_estudiando']
    search_fields = ['titulo', 'institucion']
    ordering = ['-fecha_inicio']

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nivel', 'categoria', 'user']
    list_filter = ['nivel', 'categoria']
    search_fields = ['nombre']

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'destacado']
    list_filter = ['destacado', 'fecha']
    search_fields = ['nombre', 'tecnologias']
    ordering = ['-fecha']

@admin.register(Certificacion)
class CertificacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'organizacion', 'fecha_obtencion']
    ordering = ['-fecha_obtencion']
    search_fields = ['nombre', 'organizacion']