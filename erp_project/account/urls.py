
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.dashboard, name='inicio'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/owner/', views.register_owner, name='register_owner'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/nuevo/', views.crear_subcuenta, name='crear_subcuenta'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]