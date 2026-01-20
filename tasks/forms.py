from django import forms
from .models import PersonalInfo, ExperienciaLaboral, Educacion, Habilidad, Proyecto, Certificacion

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['nombre_completo', 'titulo_profesional', 'email', 'telefono', 
                 'direccion', 'linkedin', 'github', 'sitio_web', 'sobre_mi', 'foto_perfil']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_profesional': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'sobre_mi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ['puesto', 'empresa', 'ubicacion', 'fecha_inicio', 'fecha_fin', 
                 'actualmente_trabajando', 'descripcion', 'orden']
        widgets = {
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actualmente_trabajando': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EducacionForm(forms.ModelForm):
    class Meta:
        model = Educacion
        fields = ['titulo', 'institucion', 'ubicacion', 'fecha_inicio', 'fecha_fin', 
                 'actualmente_estudiando', 'descripcion', 'orden']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actualmente_estudiando': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        fields = ['nombre', 'nivel', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'tecnologias', 'url_proyecto', 
                 'url_github', 'fecha', 'destacado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tecnologias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, JavaScript'}),
            'url_proyecto': forms.URLInput(attrs={'class': 'form-control'}),
            'url_github': forms.URLInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CertificacionForm(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = ['nombre', 'organizacion', 'fecha_obtencion', 'url_credencial']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'organizacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_obtencion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'url_credencial': forms.URLInput(attrs={'class': 'form-control'}),
        }