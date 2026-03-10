# contabilidad/urls.py
from django.urls import path
from .views import (
    GastoListView, GastoCreateView, GastoUpdateView,
    CajaListView, CajaUpdateView,
    InversorListView, InversorCreateView, InversorUpdateView,
    DetalleInversionListView, DetalleInversionCreateView, DetalleInversionUpdateView,
)

app_name = "contabilidad"

urlpatterns = [
    # GASTOS
    path("gastos/", GastoListView.as_view(), name="gasto_list"),
    path("gastos/nuevo/", GastoCreateView.as_view(), name="gasto_create"),
    path("gastos/<int:pk>/editar/", GastoUpdateView.as_view(), name="gasto_update"),

    # CAJA
    path("cajas/", CajaListView.as_view(), name="caja_list"),
    path("cajas/<int:pk>/editar/", CajaUpdateView.as_view(), name="caja_update"),

    # INVERSORES
    path("inversores/", InversorListView.as_view(), name="inversor_list"),
    path("inversores/nuevo/", InversorCreateView.as_view(), name="inversor_create"),
    path("inversores/<int:pk>/editar/", InversorUpdateView.as_view(), name="inversor_update"),

    # INVERSIONES
    path("inversiones/", DetalleInversionListView.as_view(), name="inversion_list"),
    path("inversiones/nuevo/", DetalleInversionCreateView.as_view(), name="inversion_create"),
    path("inversiones/<int:pk>/editar/", DetalleInversionUpdateView.as_view(), name="inversion_update"),
]
