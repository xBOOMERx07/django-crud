from django.contrib import admin
from .models import (
    DatosPersonales, Direccion, ExperienciaLaboral, Reconocimiento,
    CursoRealizado, ProductoAcademico, ProductoLaboral,
    VentaGarage, Habilidad
)

# ==========================================
# ADMIN: DATOS PERSONALES
# ==========================================
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'numero_cedula', 'edad', 'perfil_activo', 'fecha_nacimiento']
    list_filter = ['perfil_activo', 'sexo', 'estado_civil', 'nacionalidad']
    search_fields = ['nombres', 'apellidos', 'numero_cedula', 'email_personal']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('⚙️ Control del Perfil', {
            'fields': ('user', 'descripcion_perfil', 'perfil_activo'),
        }),
        ('👤 Información Personal', {
            'fields': ('nombres', 'apellidos', 'numero_cedula', 'sexo', 'fecha_nacimiento'),
        }),
        ('🌍 Origen y Estado', {
            'fields': ('nacionalidad', 'lugar_nacimiento', 'estado_civil'),
        }),
        ('📞 Contacto', {
            'fields': ('telefono_convencional', 'telefono_fijo', 'email_personal'),
        }),
        ('📍 Direcciones', {
            'fields': ('direccion_domiciliaria', 'direccion_trabajo'),
        }),
        ('🚗 Otros Datos', {
            'fields': ('licencia_conducir', 'sitio_web', 'foto_perfil'),
        }),
        ('📅 Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )
    
    def edad(self, obj):
        """Muestra la edad calculada"""
        if obj.edad:
            return f"{obj.edad} años"
        return "N/A"
    edad.short_description = "Edad"


# ==========================================
# ADMIN: DIRECCIONES
# ==========================================
@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'tipo', 'ciudad', 'provincia', 'es_principal']
    list_filter = ['tipo', 'es_principal', 'provincia', 'ciudad']
    search_fields = ['direccion_completa', 'ciudad', 'provincia', 'referencia']
    ordering = ['user', '-es_principal', 'tipo']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Tipo de Dirección', {
            'fields': ('tipo', 'es_principal')
        }),
        ('Dirección', {
            'fields': ('direccion_completa', 'ciudad', 'provincia', 'codigo_postal', 'referencia')
        }),
    )


# ==========================================
# ADMIN: EXPERIENCIA LABORAL
# ==========================================
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ['cargo_desempenado', 'nombre_empresa', 'fecha_inicio_gestion', 'fecha_fin_gestion', 'actualmente_trabajando', 'activar_para_que_se_vea_en_front']
    list_filter = ['actualmente_trabajando', 'activar_para_que_se_vea_en_front', 'fecha_inicio_gestion']
    search_fields = ['cargo_desempenado', 'nombre_empresa', 'lugar_empresa', 'descripcion_funciones']
    ordering = ['-fecha_inicio_gestion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('💼 Información del Cargo', {
            'fields': ('user', 'cargo_desempenado', 'nombre_empresa', 'lugar_empresa')
        }),
        ('📅 Periodo Laboral', {
            'fields': ('fecha_inicio_gestion', 'fecha_fin_gestion', 'actualmente_trabajando'),
        }),
        ('📝 Descripción', {
            'fields': ('descripcion_funciones',)
        }),
        ('📞 Contacto Empresarial', {
            'fields': ('email_empresa', 'sitio_web_empresa', 'nombre_contacto_empresarial', 'telefono_contacto_empresarial'),
            'classes': ('collapse',),
        }),
        ('⚙️ Control', {
            'fields': ('activar_para_que_se_vea_en_front', 'ruta_certificado', 'orden')
        }),
        ('📅 Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )


# ==========================================
# ADMIN: RECONOCIMIENTOS
# ==========================================
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ['tipo_reconocimiento', 'descripcion_corta', 'entidad_patrocinadora', 'fecha_reconocimiento', 'activar_para_que_se_vea_en_front']
    list_filter = ['tipo_reconocimiento', 'activar_para_que_se_vea_en_front']
    search_fields = ['descripcion_reconocimiento', 'entidad_patrocinadora']
    ordering = ['-fecha_reconocimiento']
    
    def descripcion_corta(self, obj):
        return obj.descripcion_reconocimiento[:50] + "..." if len(obj.descripcion_reconocimiento) > 50 else obj.descripcion_reconocimiento
    descripcion_corta.short_description = "Descripción"


# ==========================================
# ADMIN: CURSOS REALIZADOS
# ==========================================
@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    list_display = ['nombre_curso', 'entidad_patrocinadora', 'total_horas', 'fecha_inicio', 'fecha_fin', 'activar_para_que_se_vea_en_front']
    list_filter = ['activar_para_que_se_vea_en_front', 'fecha_inicio']
    search_fields = ['nombre_curso', 'entidad_patrocinadora']
    ordering = ['-fecha_inicio']


# ==========================================
# ADMIN: PRODUCTOS ACADÉMICOS
# ==========================================
@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = ['nombre_recurso', 'clasificador', 'fecha_publicacion', 'activar_para_que_se_vea_en_front']
    list_filter = ['clasificador', 'activar_para_que_se_vea_en_front']
    search_fields = ['nombre_recurso', 'clasificador']
    ordering = ['-fecha_publicacion']


# ==========================================
# ADMIN: PRODUCTOS LABORALES
# ==========================================
@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'fecha_producto', 'empresa_relacionada', 'activar_para_que_se_vea_en_front']
    list_filter = ['activar_para_que_se_vea_en_front']
    search_fields = ['nombre_producto', 'empresa_relacionada']
    ordering = ['-fecha_producto']


# ==========================================
# ADMIN: VENTA GARAGE
# ==========================================
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'estado_producto', 'valor_formateado', 'vendido', 'activar_para_que_se_vea_en_front']
    list_filter = ['estado_producto', 'vendido', 'activar_para_que_se_vea_en_front']
    search_fields = ['nombre_producto']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def valor_formateado(self, obj):
        return f"${obj.valor_del_bien:,.2f}"
    valor_formateado.short_description = "Precio"


# ==========================================
# ADMIN: HABILIDADES
# ==========================================
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nivel', 'categoria', 'activar_para_que_se_vea_en_front']
    list_filter = ['nivel', 'categoria', 'activar_para_que_se_vea_en_front']
    search_fields = ['nombre', 'categoria']


# ==========================================
# PERSONALIZACIÓN
# ==========================================
admin.site.site_header = "🎓 Administración de CV Profesional"
admin.site.site_title = "CV Admin"
admin.site.index_title = "Panel de Control"