from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Temporalmente vacío - se actualizará después
    path('', auth_views.LoginView.as_view(), name='home'),
]