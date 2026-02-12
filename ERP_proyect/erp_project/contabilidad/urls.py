from django.urls import path
from .views import (
    GastoList, GastoDetail, GastoCreate, GastoUpdate, GastoDelete,
    SistemaCajaList, SistemaCajaDetail, SistemaCajaCreate, SistemaCajaUpdate, SistemaCajaDelete,
    InversorList, InversorDetail, InversorCreate, InversorUpdate, InversorDelete,
    DetalleInversionList, DetalleInversionDetail, DetalleInversionCreate, DetalleInversionUpdate, DetalleInversionDelete,
    DescuentoPromocionalList, DescuentoPromocionalDetail, DescuentoPromocionalCreate, DescuentoPromocionalUpdate, DescuentoPromocionalDelete,
)

urlpatterns = [

    # URLs gasto
    path('gastos/', GastoList.as_view(), name='gasto_list'),
    path('gastos/<int:pk>/', GastoDetail.as_view(), name='gasto_detail'),
    path('gastos/create/', GastoCreate.as_view(), name='gasto_create'),
    path('gastos/<int:pk>/update/', GastoUpdate.as_view(), name='gasto_update'),
    path('gastos/<int:pk>/delete/', GastoDelete.as_view(), name='gasto_delete'),

    # URLs sistema caja
    path('cajas/', SistemaCajaList.as_view(), name='sistemacaja_list'),
    path('cajas/<int:pk>/', SistemaCajaDetail.as_view(), name='sistemacaja_detail'),
    path('cajas/create/', SistemaCajaCreate.as_view(), name='sistemacaja_create'),
    path('cajas/<int:pk>/update/', SistemaCajaUpdate.as_view(), name='sistemacaja_update'),
    path('cajas/<int:pk>/delete/', SistemaCajaDelete.as_view(), name='sistemacaja_delete'),

    # URLs inversor
    path('inversores/', InversorList.as_view(), name='inversor_list'),
    path('inversores/<int:pk>/', InversorDetail.as_view(), name='inversor_detail'),
    path('inversores/create/', InversorCreate.as_view(), name='inversor_create'),
    path('inversores/<int:pk>/update/', InversorUpdate.as_view(), name='inversor_update'),
    path('inversores/<int:pk>/delete/', InversorDelete.as_view(), name='inversor_delete'),

    # URLs detalle inversion
    path('detalles/', DetalleInversionList.as_view(), name='detalleinversion_list'),
    path('detalles/<int:pk>/', DetalleInversionDetail.as_view(), name='detalleinversion_detail'),
    path('detalles/create/', DetalleInversionCreate.as_view(), name='detalleinversion_create'),
    path('detalles/<int:pk>/update/', DetalleInversionUpdate.as_view(), name='detalleinversion_update'),
    path('detalles/<int:pk>/delete/', DetalleInversionDelete.as_view(), name='detalleinversion_delete'),

    # URLs descuentos promocionales
    path('descuentos/', DescuentoPromocionalList.as_view(), name='descuentopromocional_list'),
    path('descuentos/<int:pk>/', DescuentoPromocionalDetail.as_view(), name='descuentopromocional_detail'),
    path('descuentos/create/', DescuentoPromocionalCreate.as_view(), name='descuentopromocional_create'),
    path('descuentos/<int:pk>/update/', DescuentoPromocionalUpdate.as_view(), name='descuentopromocional_update'),
    path('descuentos/<int:pk>/delete/', DescuentoPromocionalDelete.as_view(), name='descuentopromocional_delete'),
]