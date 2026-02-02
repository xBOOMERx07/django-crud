from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # Autenticación y Home
    # ==========================================
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    
    # ==========================================
    # CV Público y PDF
    # ==========================================
    path('cv/<str:username>/', views.cv_publico, name='cv_publico'),
    path('cv/<str:username>/pdf/', views.descargar_pdf, name='descargar_pdf'),  
    
    # ==========================================
    # Gestión de Datos Personales
    # ==========================================
    path('datos-personales/editar/', views.editar_datos_personales, name='editar_datos_personales'),
    
    # ==========================================
    # Gestión de Experiencia Laboral
    # ==========================================
    path('experiencias/', views.lista_experiencias, name='lista_experiencias'),
    path('experiencias/crear/', views.crear_experiencia, name='crear_experiencia'),
    path('experiencias/<int:pk>/editar/', views.editar_experiencia, name='editar_experiencia'),
    path('experiencias/<int:pk>/eliminar/', views.eliminar_experiencia, name='eliminar_experiencia'),
    
    # ==========================================
    # Gestión de Cursos
    # ==========================================
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/crear/', views.crear_curso, name='crear_curso'),
    path('cursos/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:pk>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    
    # ==========================================
    # Gestión de Habilidades
    # ==========================================
    path('habilidades/', views.lista_habilidades, name='lista_habilidades'),
    path('habilidades/crear/', views.crear_habilidad, name='crear_habilidad'),
    path('habilidades/<int:pk>/editar/', views.editar_habilidad, name='editar_habilidad'),
    path('habilidades/<int:pk>/eliminar/', views.eliminar_habilidad, name='eliminar_habilidad'),

    # ==========================================
    # Gestión de Reconocimientos
    # ==========================================
    path('reconocimientos/', views.lista_reconocimientos, name='lista_reconocimientos'),
    path('reconocimientos/crear/', views.crear_reconocimiento, name='crear_reconocimiento'),
    path('reconocimientos/<int:pk>/editar/', views.editar_reconocimiento, name='editar_reconocimiento'),
    path('reconocimientos/<int:pk>/eliminar/', views.eliminar_reconocimiento, name='eliminar_reconocimiento'),

    # ==========================================
    # Gestión de Productos Académicos
    # ==========================================
    path('productos-academicos/', views.lista_productos_academicos, name='lista_productos_academicos'),
    path('productos-academicos/crear/', views.crear_producto_academico, name='crear_producto_academico'),
    path('productos-academicos/<int:pk>/editar/', views.editar_producto_academico, name='editar_producto_academico'),
    path('productos-academicos/<int:pk>/eliminar/', views.eliminar_producto_academico, name='eliminar_producto_academico'),

    # ==========================================
    # Gestión de Productos Laborales
    # ==========================================
    path('productos-laborales/', views.lista_productos_laborales, name='lista_productos_laborales'),
    path('productos-laborales/crear/', views.crear_producto_laboral, name='crear_producto_laboral'),
    path('productos-laborales/<int:pk>/editar/', views.editar_producto_laboral, name='editar_producto_laboral'),
    path('productos-laborales/<int:pk>/eliminar/', views.eliminar_producto_laboral, name='eliminar_producto_laboral'),

    # ==========================================
    # Gestión de Venta Garage
    # ==========================================
    path('venta-garage/', views.lista_ventas_garage, name='lista_ventas_garage'),
    path('venta-garage/crear/', views.crear_venta_garage, name='crear_venta_garage'),
    path('venta-garage/<int:pk>/editar/', views.editar_venta_garage, name='editar_venta_garage'),
    path('venta-garage/<int:pk>/eliminar/', views.eliminar_venta_garage, name='eliminar_venta_garage'),
]


















