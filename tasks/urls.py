from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # CV Público
    path('cv/<str:username>/', views.cv_publico, name='cv_publico'),
    path('cv/<str:username>/pdf/', views.descargar_pdf, name='descargar_pdf'),  
    
    # Datos Personales
    path('datos-personales/editar/', views.editar_datos_personales, name='editar_datos_personales'),
    
    # Experiencia Laboral
    path('experiencias/', views.lista_experiencias, name='lista_experiencias'),
    path('experiencias/crear/', views.crear_experiencia, name='crear_experiencia'),
    path('experiencias/<int:pk>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),
    
    # Cursos
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    
    # Habilidades
    path('habilidades/', views.lista_habilidades, name='lista_habilidades'),
    path('habilidades/crear/', views.crear_habilidad, name='crear_habilidad'),
    path('habilidades/<int:pk>/eliminar/', views.eliminar_habilidad, name='eliminar_habilidad'),
]
# Venta Garage
path('venta-garage/', views.lista_ventas_garage, name='lista_ventas_garage'),
path('venta-garage/crear/', views.crear_venta_garage, name='crear_venta_garage'),
path('venta-garage/<int:pk>/editar/', views.editar_venta_garage, name='editar_venta_garage'),
path('venta-garage/<int:pk>/eliminar/', views.eliminar_venta_garage, name='eliminar_venta_garage'),