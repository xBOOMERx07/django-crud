from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ['nombre_completo', 'numero_cedula', 'edad_display', 'perfil_activo', 'fecha_nacimiento']
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
            'fields': ('telefono_convencional', 'email_personal'),
        }),
        ('🚗 Otros Datos', {
            'fields': ('licencia_conducir', 'sitio_web', 'foto_perfil'),
        }),
        ('📅 Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )
    
    def edad_display(self, obj):
        if obj.fecha_nacimiento:
            import datetime
            hoy = datetime.date.today()
            edad = hoy.year - obj.fecha_nacimiento.year - ((hoy.month, hoy.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day))
            return f"{edad} años"
        return "N/A"
    edad_display.short_description = "Edad"
    
    # ✅ AGREGAR ESTA FUNCIÓN PARA QUE EL ADMIN PUEDA GUARDAR
    def save_model(self, request, obj, form, change):
        # Si no tiene usuario asignado, asignar el usuario actual
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


# ==========================================
# ADMIN: EXPERIENCIA LABORAL
# ==========================================
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ['cargo_desempenado', 'nombre_empresa', 'fecha_inicio_gestion', 'actualmente_trabajando', 'activar_para_que_se_vea_en_front']
    list_filter = ['actualmente_trabajando', 'activar_para_que_se_vea_en_front']
    search_fields = ['cargo_desempenado', 'nombre_empresa']
    ordering = ['-fecha_inicio_gestion']
    
    fieldsets = (
        ('💼 Información', {'fields': ('user', 'cargo_desempenado', 'nombre_empresa')}),
        ('📅 Periodo', {'fields': ('fecha_inicio_gestion', 'fecha_fin_gestion', 'actualmente_trabajando')}),
        ('⚙️ Control', {'fields': ('activar_para_que_se_vea_en_front', 'ruta_certificado')}),
    )

# ==========================================
# ADMIN: VENTA GARAGE
# ==========================================
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'estado_producto', 'valor_formateado', 'vendido', 'activar_para_que_se_vea_en_front']
    list_filter = ['estado_producto', 'vendido', 'activar_para_que_se_vea_en_front']
    search_fields = ['nombre_producto']
    actions = ['marcar_como_vendido']

    def marcar_como_vendido(self, request, queryset):
        queryset.update(vendido=True)
    marcar_como_vendido.short_description = "💰 Marcar seleccionados como VENDIDOS"

    def valor_formateado(self, obj):
        return format_html('<b style="color: #2e7d32;">${:,.2f}</b>', obj.valor_del_bien)
    valor_formateado.short_description = "Precio"

# ==========================================
# REGISTROS SIMPLES
# ==========================================
admin.site.register(Direccion)
admin.site.register(Reconocimiento)
admin.site.register(CursoRealizado)
admin.site.register(ProductoAcademico)
admin.site.register(ProductoLaboral)
admin.site.register(Habilidad)

# ==========================================
# PERSONALIZACIÓN VISUAL FINAL
# ==========================================
admin.site.site_header = format_html(
    '<span style="color: #2563eb; font-weight: bold; font-family: sans-serif;">'
    '🚀 Jean Pierre - Gestión CV Profesional</span>'
)
admin.site.site_title = "Admin Jean Pierre"
admin.site.index_title = "Panel de Control del Sistema"