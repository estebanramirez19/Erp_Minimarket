from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import inicio

urlpatterns = [
    
    path('', inicio, name='inicio'), 
    path('admin/', admin.site.urls),

    # Rutas de las aplicaciones
    path('usuarios/', include('usuarios.urls')),       # Todo lo de usuarios, comienza en "usuarios/"
    path('inventario/', include('inventario.urls')),             # Todo lo de inventario, comienza en "inventario/"
    path('proveedores/', include('proveedores.urls')), # Todo lo de proveedores, comienza en "/proveedores/"
    path('clientes/', include('clientes.urls')),    # Todo lo de clientes, comienza en "/clientes/"
    path('ventas/', include('ventas.urls')),         # Todo lo de ventas, comienza en "/ventas/"
    path('compras/', include('compras.urls')),       # Todo lo de compras, comienza en "/compras/"
    path('integraciones/', include('integraciones.urls')), # Todo lo de integraciones,            # Todo lo de api,
    path('contabilidad/', include('contabilidad.urls')),# Todo lo de contabilidad,
    path('empresa/', include('empresa.urls')),# Todo lo de empresa,

]
# Archivos de usuario (fotos, docs) para modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
