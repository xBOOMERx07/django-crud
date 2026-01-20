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
    
    # Información Personal
    path('perfil/editar/', views.editar_info_personal, name='editar_info_personal'),
    
    # Experiencia Laboral
    path('experiencias/', views.lista_experiencias, name='lista_experiencias'),
    path('experiencias/crear/', views.crear_experiencia, name='crear_experiencia'),
    path('experiencias/<int:pk>/editar/', views.editar_experiencia, name='editar_experiencia'),
    path('experiencias/<int:pk>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),
    
    # Educación
    path('educacion/', views.lista_educacion, name='lista_educacion'),
    path('educacion/crear/', views.crear_educacion, name='crear_educacion'),
    path('educacion/<int:pk>/editar/', views.editar_educacion, name='editar_educacion'),
    path('educacion/<int:pk>/eliminar/', views.eliminar_educacion, name='eliminar_educacion'),
    
    # Habilidades
    path('habilidades/', views.lista_habilidades, name='lista_habilidades'),
    path('habilidades/crear/', views.crear_habilidad, name='crear_habilidad'),
    path('habilidades/<int:pk>/editar/', views.editar_habilidad, name='editar_habilidad'),
    path('habilidades/<int:pk>/eliminar/', views.eliminar_habilidad, name='eliminar_habilidad'),
    
    # Proyectos
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/<int:pk>/editar/', views.editar_proyecto, name='editar_proyecto'),
    path('proyectos/<int:pk>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),
    
    # Certificaciones
    path('certificaciones/', views.lista_certificaciones, name='lista_certificaciones'),
    path('certificaciones/crear/', views.crear_certificacion, name='crear_certificacion'),
    path('certificaciones/<int:pk>/editar/', views.editar_certificacion, name='editar_certificacion'),
    path('certificaciones/<int:pk>/eliminar/', views.eliminar_certificacion, name='eliminar_certificacion'),
]