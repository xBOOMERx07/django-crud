from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # 1. Ruta del Administrador
    path('admin/', admin.site.urls),
    
    # 2. Rutas de tu aplicación (Tasks, CV, Venta Garage)
    path('', include('tasks.urls')),
    
    # 3. Regla de Oro para Render: Sirve archivos MEDIA (fotos) incluso si DEBUG es False
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Configuración extra para desarrollo local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)