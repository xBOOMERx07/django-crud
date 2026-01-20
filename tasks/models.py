from django.db import models
from django.contrib.auth.models import User

# Información Personal
class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    titulo_profesional = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=300, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    sitio_web = models.URLField(blank=True)
    sobre_mi = models.TextField()
    foto_perfil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre_completo

# Experiencia Laboral
class ExperienciaLaboral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actualmente_trabajando = models.BooleanField(default=False)
    descripcion = models.TextField()
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.puesto} en {self.empresa}"

# Educación
class Educacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    actualmente_estudiando = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.titulo} - {self.institucion}"

# Habilidades
class Habilidad(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    categoria = models.CharField(max_length=100, blank=True)  # Ej: "Lenguajes", "Frameworks", etc.
    
    def __str__(self):
        return f"{self.nombre} ({self.nivel})"

# Proyectos
class Proyecto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tecnologias = models.CharField(max_length=300)  # Separadas por comas
    url_proyecto = models.URLField(blank=True)
    url_github = models.URLField(blank=True)
    fecha = models.DateField()
    destacado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return self.nombre

# Certificaciones
class Certificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    organizacion = models.CharField(max_length=200)
    fecha_obtencion = models.DateField()
    url_credencial = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-fecha_obtencion']
    
    def __str__(self):
        return f"{self.nombre} - {self.organizacion}"