from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.lista_perfiles, name='perfiles'),  # /usuarios/perfiles/
    path('crear/', views.crear_perfil, name='crear_perfil'), # /usuarios/perfiles/crear/
    path('editar/<int:perfil_id>/', views.editar_perfil, name='editar_perfil'),  # /usuarios/perfiles/editar/3/
    path('eliminar/<int:perfil_id>/', views.eliminar_perfil, name='eliminar_perfil'), # /usuarios/perfiles/eliminar/3/
]
