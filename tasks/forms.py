from django import forms
from .models import (
    DatosPersonales, Direccion, ExperienciaLaboral,
    Reconocimiento, CursoRealizado, ProductoAcademico,
    ProductoLaboral, VentaGarage, Habilidad
)

# ==========================================
# FORM: DATOS PERSONALES
# ==========================================
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        exclude = ['user', 'fecha_creacion', 'fecha_actualizacion']
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Juan Carlos'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pérez González'
            }),
            'numero_cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234567890',
                'maxlength': '10'
            }),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ecuatoriana'
            }),
            'lugar_nacimiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quito, Ecuador'
            }),
            'telefono_convencional': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '02-1234567'
            }),
            'telefono_fijo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0987654321'
            }),
            'email_personal': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@email.com'
            }),
            'direccion_domiciliaria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Av. Principal N12-34 y Secundaria'
            }),
            'direccion_trabajo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle Empresarial 456'
            }),
            'licencia_conducir': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo B'
            }),
            'sitio_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://miportfolio.com'
            }),
            'descripcion_perfil': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ingeniero en Sistemas'
            }),
            'perfil_activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


# ==========================================
# FORM: EXPERIENCIA LABORAL
# ==========================================
class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        exclude = ['user', 'fecha_creacion', 'fecha_actualizacion', 'orden']
        widgets = {
            'cargo_desempenado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Desarrollador Full Stack'
            }),
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tech Solutions S.A.'
            }),
            'lugar_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quito, Ecuador'
            }),
            'email_empresa': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@empresa.com'
            }),
            'sitio_web_empresa': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://empresa.com'
            }),
            'nombre_contacto_empresarial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'María López - RRHH'
            }),
            'telefono_contacto_empresarial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0987654321'
            }),
            'fecha_inicio_gestion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin_gestion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'actualmente_trabajando': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'descripcion_funciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tus funciones y logros principales...'
            }),
            'activar_para_que_se_vea_en_front': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ruta_certificado': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            })
        }


# ==========================================
# FORM: CURSOS REALIZADOS
# ==========================================
class CursoRealizadoForm(forms.ModelForm):
    class Meta:
        model = CursoRealizado
        exclude = ['user', 'fecha_creacion']
        widgets = {
            'nombre_curso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python Avanzado para Data Science'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'total_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '40',
                'min': '1'
            }),
            'descripcion_curso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el contenido del curso...'
            }),
            'entidad_patrocinadora': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Udemy / Coursera / Universidad'
            }),
            'nombre_contacto_auspicia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instructor: John Doe'
            }),
            'telefono_contacto_auspicia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0987654321'
            }),
            'email_empresa_patrocinadora': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'info@plataforma.com'
            }),
            'activar_para_que_se_vea_en_front': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ruta_certificado': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            })
        }


# ==========================================
# FORM: HABILIDADES
# ==========================================
class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        exclude = ['user']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, React, etc.'
            }),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lenguajes de Programación'
            }),
            'activar_para_que_se_vea_en_front': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


# ==========================================
# FORM: RECONOCIMIENTOS
# ==========================================
class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        exclude = ['user', 'fecha_creacion']
        widgets = {
            'tipo_reconocimiento': forms.Select(attrs={'class': 'form-control'}),
            'fecha_reconocimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion_reconocimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'entidad_patrocinadora': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nombre_contacto_auspicia': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'telefono_contacto_auspicia': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'activar_para_que_se_vea_en_front': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'ruta_certificado': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


# ==========================================
# FORM: DIRECCIONES
# ==========================================
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = ['user', 'fecha_creacion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'direccion_completa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Av. Principal N12-34'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quito'
            }),
            'provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pichincha'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '170150'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Frente al parque'
            }),
            'es_principal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
