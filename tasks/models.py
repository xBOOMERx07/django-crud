from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

# ==========================================
# TABLA 1: DATOS PERSONALES (Maestra)
# ==========================================
class DatosPersonales(models.Model):
    """
    Información personal completa del usuario
    Equivalente a: DATOSPERSONALES
    """
    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('Soltero/a', 'Soltero/a'),
        ('Casado/a', 'Casado/a'),
        ('Divorciado/a', 'Divorciado/a'),
        ('Viudo/a', 'Viudo/a'),
        ('Unión Libre', 'Unión Libre'),
    ]
    
    # Relación con usuario Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='datos_personales')
    
    # Campos del esquema del profesor
    descripcion_perfil = models.TextField(blank=True, help_text="Descripción amplia sobre ti (varios párrafos permitidos)")
    perfil_activo = models.BooleanField(default=True, help_text="Activar/desactivar perfil completo")
    
    # 🎓 CAMPOS: Educación y Título Profesional
    nivel_educacion = models.CharField(
        max_length=50,
        choices=[
            ('sin_estudios', 'Sin estudios formales'),
            ('primaria_incompleta', 'Primaria incompleta'),
            ('primaria_completa', 'Primaria completa'),
            ('secundaria_incompleta', 'Secundaria incompleta'),
            ('bachiller', 'Bachiller'),
            ('tecnico', 'Técnico/Tecnólogo'),
            ('universitario_incompleto', 'Universitario incompleto'),
            ('tercer_nivel', 'Tercer Nivel (Licenciatura/Ingeniería)'),
            ('cuarto_nivel', 'Cuarto Nivel (Especialización)'),
            ('maestria', 'Maestría'),
            ('doctorado', 'Doctorado/PhD'),
        ],
        blank=True,
        default='',
        verbose_name="Nivel de Educación",
        help_text="Máximo nivel educativo alcanzado"
    )
    
    titulo_profesional = models.CharField(
        max_length=80,
        blank=True,
        default='',
        verbose_name="Título Profesional",
        help_text='Título que aparecerá debajo de tu nombre en el CV (ej: "Ingeniero en Sistemas", "Ama de Casa")'
    )
    
    # Nombre separado (como pide el profesor)
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    
    # Datos de identidad
    nacionalidad = models.CharField(max_length=20, default='Ecuatoriana')
    lugar_nacimiento = models.CharField(max_length=60, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    # Cédula con validación
    cedula_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="La cédula debe tener exactamente 10 dígitos"
    )
    numero_cedula = models.CharField(
        max_length=10, 
        unique=True,
        validators=[cedula_validator],
        help_text="10 dígitos sin guiones"
    )
    
    # Información personal
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado_civil = models.CharField(max_length=50, choices=ESTADO_CIVIL_CHOICES)
    licencia_conducir = models.CharField(max_length=6, blank=True, help_text="Tipo: A, B, C, etc.")
    
    # Contacto
    telefono_convencional = models.CharField(max_length=15, blank=True)
    telefono_fijo = models.CharField(max_length=15, blank=True)
    
    # Direcciones (compatibilidad con esquema profesor)
    direccion_trabajo = models.CharField(max_length=50, blank=True, help_text="Dirección principal de trabajo")
    direccion_domiciliaria = models.CharField(max_length=50, blank=True, help_text="Dirección principal de domicilio")
    
    # Web y Redes Sociales
    sitio_web = models.URLField(max_length=60, blank=True)
    linkedin_url = models.URLField(max_length=200, blank=True, verbose_name="LinkedIn")
    github_url = models.URLField(max_length=200, blank=True, verbose_name="GitHub")  
    twitter_url = models.URLField(max_length=200, blank=True, verbose_name="Twitter/X")
    portfolio_url = models.URLField(max_length=200, blank=True, verbose_name="Portafolio Personal")
    
    # 📱 REDES SOCIALES ADICIONALES
    facebook_url = models.URLField(
        max_length=200,
        blank=True,
        default='',
        verbose_name="Facebook URL"
    )
    
    instagram_url = models.URLField(
        max_length=200,
        blank=True,
        default='',
        verbose_name="Instagram URL"
    )
    
    whatsapp_numero = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name="Número WhatsApp",
        help_text='Número con código de país, ej: +593987654321'
    )
    
    # Campos adicionales (mejoras)
    email_personal = models.EmailField(blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Datos Personales"
        verbose_name_plural = "Datos Personales"
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def edad(self):
        """Calcula la edad actual"""
        if self.fecha_nacimiento:
            return relativedelta(date.today(), self.fecha_nacimiento).years
        return None
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        # Validar que la fecha de nacimiento no sea futura
        if self.fecha_nacimiento and self.fecha_nacimiento > date.today():
            raise ValidationError({
                'fecha_nacimiento': 'La fecha de nacimiento no puede ser futura.'
            })
        
        # Validar edad mínima (18 años) y máxima (70 años)
        if self.fecha_nacimiento:
            edad = relativedelta(date.today(), self.fecha_nacimiento).years
            if edad < 18:
                raise ValidationError({
                    'fecha_nacimiento': f'Debe ser mayor de edad (18 años). Edad actual: {edad} años.'
                })
            if edad > 70:
                raise ValidationError({
                    'fecha_nacimiento': f'La edad máxima permitida es 70 años. Edad actual: {edad} años.'
                })
        
        # Validar que la cédula tenga exactamente 10 dígitos numéricos
        if self.numero_cedula and not self.numero_cedula.isdigit():
            raise ValidationError({
                'numero_cedula': 'La cédula debe contener solo números.'
            })
        
        # Validar que apellidos y nombres no sean vacíos
        if self.apellidos and not self.apellidos.strip():
            raise ValidationError({
                'apellidos': 'Los apellidos no pueden estar vacíos.'
            })
        
        if self.nombres and not self.nombres.strip():
            raise ValidationError({
                'nombres': 'Los nombres no pueden estar vacíos.'
            })
        
        # Validar que apellidos y nombres no contengan números
        if self.apellidos and any(char.isdigit() for char in self.apellidos):
            raise ValidationError({
                'apellidos': 'Los apellidos no deben contener números.'
            })
        
        if self.nombres and any(char.isdigit() for char in self.nombres):
            raise ValidationError({
                'nombres': 'Los nombres no deben contener números.'
            })
        
        # Validar formato de teléfonos
        import re
        telefono_pattern = re.compile(r'^[\d\s\-\+\(\)]+$')
        
        if self.telefono_convencional and not telefono_pattern.match(self.telefono_convencional):
            raise ValidationError({
                'telefono_convencional': 'El teléfono debe contener solo números y caracteres válidos (-, +, paréntesis).'
            })
        
        if self.telefono_fijo and not telefono_pattern.match(self.telefono_fijo):
            raise ValidationError({
                'telefono_fijo': 'El teléfono debe contener solo números y caracteres válidos (-, +, paréntesis).'
            })


# ==========================================
# TABLA NUEVA: DIRECCIONES (Mejora)
# ==========================================
class Direccion(models.Model):
    """
    Permite múltiples direcciones por usuario
    (Domicilio, Trabajo, Otra)
    """
    TIPO_CHOICES = [
        ('Domicilio', 'Domicilio'),
        ('Trabajo', 'Trabajo'),
        ('Otra', 'Otra'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    direccion_completa = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50, blank=True)
    provincia = models.CharField(max_length=50, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    referencia = models.CharField(max_length=200, blank=True, help_text="Referencias para ubicar")
    es_principal = models.BooleanField(default=False, help_text="Dirección principal")
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ['-es_principal', 'tipo']
    
    def __str__(self):
        principal = " (Principal)" if self.es_principal else ""
        return f"{self.tipo}: {self.direccion_completa}{principal}"
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        # Validar que la dirección no esté vacía
        if self.direccion_completa and not self.direccion_completa.strip():
            raise ValidationError({
                'direccion_completa': 'La dirección no puede estar vacía.'
            })


# ==========================================
# TABLA 2: EXPERIENCIA LABORAL (Transaccional)
# ==========================================
class ExperienciaLaboral(models.Model):
    """
    Historial laboral del usuario
    Equivalente a: EXPERIENCIALABORAL
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias_laborales')
    
    # Información del cargo
    cargo_desempenado = models.CharField(max_length=100, verbose_name="Cargo Desempeñado")
    nombre_empresa = models.CharField(max_length=50, verbose_name="Nombre de la Empresa")
    lugar_empresa = models.CharField(max_length=50, blank=True, verbose_name="Ubicación")
    
    # Contacto empresarial
    email_empresa = models.EmailField(max_length=100, blank=True)
    sitio_web_empresa = models.URLField(max_length=100, blank=True)
    nombre_contacto_empresarial = models.CharField(max_length=100, blank=True)
    telefono_contacto_empresarial = models.CharField(max_length=60, blank=True)
    
    # Fechas
    fecha_inicio_gestion = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin_gestion = models.DateField(null=True, blank=True, verbose_name="Fecha de Fin")
    actualmente_trabajando = models.BooleanField(default=False)
    
    # Descripción
    descripcion_funciones = models.TextField(verbose_name="Descripción de Funciones")
    
    # Control de visualización
    activar_para_que_se_vea_en_front = models.BooleanField(default=True, verbose_name="Mostrar en CV Público")
    
    # Certificado
    ruta_certificado = models.FileField(upload_to='certificados/laborales/', blank=True, null=True, verbose_name="Certificado Laboral")
    
    # Ordenamiento
    orden = models.IntegerField(default=0)
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_inicio_gestion']
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"
    
    def __str__(self):
        return f"{self.cargo_desempenado} en {self.nombre_empresa}"
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        # Validar que fecha_fin no sea anterior a fecha_inicio
        if self.fecha_inicio_gestion and self.fecha_fin_gestion:
            if self.fecha_fin_gestion < self.fecha_inicio_gestion:
                raise ValidationError({
                    'fecha_fin_gestion': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
                })
        
        # Si actualmente trabajando, no debe tener fecha_fin
        if self.actualmente_trabajando and self.fecha_fin_gestion:
            raise ValidationError({
                'fecha_fin_gestion': 'No puede tener fecha de fin si actualmente está trabajando aquí.',
                'actualmente_trabajando': 'Desmarque esta opción si ya tiene fecha de fin.'
            })
        
        # Si no trabaja actualmente, debe tener fecha_fin
        if not self.actualmente_trabajando and not self.fecha_fin_gestion:
            raise ValidationError({
                'fecha_fin_gestion': 'Debe especificar una fecha de fin o marcar "Actualmente trabajando".'
            })
        
        # Validar que las fechas no sean futuras
        if self.fecha_inicio_gestion and self.fecha_inicio_gestion > date.today():
            raise ValidationError({
                'fecha_inicio_gestion': 'La fecha de inicio no puede ser futura.'
            })
        
        # Validar antigüedad razonable (máximo 50 años)
        if self.fecha_inicio_gestion:
            antiguedad_dias = (date.today() - self.fecha_inicio_gestion).days
            antiguedad_anios = antiguedad_dias / 365.25
            if antiguedad_anios > 50:
                raise ValidationError({
                    'fecha_inicio_gestion': f'La antigüedad no puede ser mayor a 50 años ({int(antiguedad_anios)} años).'
                })
        
        # Validar campos no vacíos
        if self.cargo_desempenado and not self.cargo_desempenado.strip():
            raise ValidationError({'cargo_desempenado': 'El cargo no puede estar vacío.'})
        
        if self.nombre_empresa and not self.nombre_empresa.strip():
            raise ValidationError({'nombre_empresa': 'El nombre de la empresa no puede estar vacío.'})


# ==========================================
# TABLA 3: RECONOCIMIENTOS (Maestra)
# ==========================================
class Reconocimiento(models.Model):
    """Reconocimientos académicos, públicos o privados"""
    TIPO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reconocimientos')
    tipo_reconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES)
    fecha_reconocimiento = models.DateField()
    descripcion_reconocimiento = models.TextField()
    entidad_patrocinadora = models.CharField(max_length=100)
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True)
    telefono_contacto_auspicia = models.CharField(max_length=60, blank=True)
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    ruta_certificado = models.FileField(upload_to='certificados/reconocimientos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_reconocimiento']
        verbose_name = "Reconocimiento"
        verbose_name_plural = "Reconocimientos"
    
    def __str__(self):
        return f"{self.tipo_reconocimiento} - {self.descripcion_reconocimiento[:50]}"
    
    def clean(self):
        if self.fecha_reconocimiento and self.fecha_reconocimiento > date.today():
            raise ValidationError({'fecha_reconocimiento': 'La fecha no puede ser futura.'})


# ==========================================
# TABLA 4: CURSOS REALIZADOS (Transaccional)
# ==========================================
class CursoRealizado(models.Model):
    """Cursos, talleres y capacitaciones"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos_realizados')
    nombre_curso = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    total_horas = models.IntegerField(validators=[MinValueValidator(1)])
    descripcion_curso = models.TextField()
    entidad_patrocinadora = models.CharField(max_length=100)
    nombre_contacto_auspicia = models.CharField(max_length=100, blank=True)
    telefono_contacto_auspicia = models.CharField(max_length=60, blank=True)
    email_empresa_patrocinadora = models.EmailField(max_length=60, blank=True)
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    ruta_certificado = models.FileField(upload_to='certificados/cursos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = "Curso Realizado"
        verbose_name_plural = "Cursos Realizados"
    
    def __str__(self):
        return f"{self.nombre_curso} ({self.total_horas}h)"
    
    def clean(self):
        # Fecha fin >= fecha inicio
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError({'fecha_fin': 'La fecha de finalización no puede ser anterior a la fecha de inicio.'})
        
        # No fechas futuras
        if self.fecha_inicio and self.fecha_inicio > date.today():
            raise ValidationError({'fecha_inicio': 'La fecha de inicio no puede ser futura.'})
        
        if self.fecha_fin and self.fecha_fin > date.today():
            raise ValidationError({'fecha_fin': 'La fecha de finalización no puede ser futura.'})
        
        # Horas razonables
        if self.total_horas and self.total_horas > 10000:
            raise ValidationError({'total_horas': f'El total de horas parece excesivo ({self.total_horas}h).'})
        
        # Duración razonable
        if self.fecha_inicio and self.fecha_fin:
            duracion_dias = (self.fecha_fin - self.fecha_inicio).days
            if duracion_dias > 1825:  # 5 años
                raise ValidationError({'fecha_fin': f'La duración del curso es muy larga ({duracion_dias//365} años).'})


# ==========================================
# TABLA 5: PRODUCTOS ACADÉMICOS
# ==========================================
class ProductoAcademico(models.Model):
    """Publicaciones, investigaciones, papers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos_academicos')
    nombre_recurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_publicacion = models.DateField(null=True, blank=True)
    url_publicacion = models.URLField(blank=True)
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = "Producto Académico"
        verbose_name_plural = "Productos Académicos"
    
    def __str__(self):
        return f"{self.nombre_recurso} ({self.clasificador})"


# ==========================================
# TABLA 6: PRODUCTOS LABORALES
# ==========================================
class ProductoLaboral(models.Model):
    """Productos desarrollados en el ámbito laboral"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos_laborales')
    nombre_producto = models.CharField(max_length=100)
    fecha_producto = models.DateField()
    descripcion = models.TextField()
    empresa_relacionada = models.CharField(max_length=100, blank=True)
    url_producto = models.URLField(blank=True)
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_producto']
        verbose_name = "Producto Laboral"
        verbose_name_plural = "Productos Laborales"
    
    def __str__(self):
        return self.nombre_producto


# ==========================================
# TABLA 7: VENTA GARAGE
# ==========================================
class VentaGarage(models.Model):
    """Productos personales en venta"""
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_garage')
    nombre_producto = models.CharField(max_length=100)
    estado_producto = models.CharField(max_length=40, choices=ESTADO_CHOICES)
    descripcion = models.TextField()
    valor_del_bien = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    foto_producto = models.ImageField(upload_to='garage/', blank=True, null=True)
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    vendido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Venta Garage"
        verbose_name_plural = "Ventas Garage"
    
    def __str__(self):
        return f"{self.nombre_producto} - ${self.valor_del_bien}"
    
    def clean(self):
        if self.valor_del_bien and self.valor_del_bien > 999999.99:
            raise ValidationError({'valor_del_bien': f'El valor parece excesivo (${self.valor_del_bien}).'})


# ==========================================
# TABLA 8: HABILIDADES
# ==========================================
class Habilidad(models.Model):
    """Habilidades técnicas y blandas"""
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habilidades')
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    categoria = models.CharField(max_length=100, blank=True)
    activar_para_que_se_vea_en_front = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
    
    def __str__(self):
        return f"{self.nombre} ({self.nivel})"