from django.urls import path

from apps.baliza.views.Bracelet.views import BraceletListView, BraceletCreateView, BraceletDeleteView, \
    BraceletUpdateView, BraceletUmbralsUpdateView
from apps.baliza.views.server.views import setReceivedOK, ServerReceivedCreateView, \
    HistorialRssi_ListView, FiltrarGraficaUbicacion, VerPiso
from apps.baliza.views.baliza.views import BalizaListView, BalizaCreateView, BalizaDeleteView, BalizaUpdateView, \
    BalizaInstalacionUpdateView

from apps.baliza.views.sede.views import SedeListView, SedeCreateView, SedeUpdateView, SedeDeleteView
from apps.baliza.views.piso.views import PisoListView, PisoCreateView, PisoUpdateView, PisoDeleteView
from apps.baliza.views.area.views import AreaListView, AreaCreateView, AreaUpdateView, AreaDeleteView
from apps.baliza.views.historialUbicacion.views import HistorialUbicacionListView
from apps.baliza.views.historialSensores.views import HistorialSensoresListView

app_name = 'project'

urlpatterns = [
    # Server
    path('DeterminarPosicion/', FiltrarGraficaUbicacion.as_view(), name='filtro_graph_posicion'),
    path('GraficarPiso/', VerPiso.as_view(), name='graph_piso'),

    path('received/', ServerReceivedCreateView.as_view(), name='form_received_baliza2'),
    path('rssi/', HistorialRssi_ListView.as_view(), name='form_readlist_rssi'),
    path('receivedOK/', setReceivedOK, name='form_received_baliza_ok'),

    # Bracelet
    path('bracelet/list/', BraceletListView.as_view(), name='form_readlist_bracelet'),
    path('bracelet/create/', BraceletCreateView.as_view(), name='form_create_bracelet'),
    path('bracelet/edit/<int:pk>/', BraceletUpdateView.as_view(), name='form_update_bracelet'),
    path('bracelet/editUmbrals/<int:pk>/', BraceletUmbralsUpdateView.as_view(), name='form_update_bracelet_umbrals'),
    path('bracelet/delete/<int:pk>/', BraceletDeleteView.as_view(), name='form_delete_bracelet'),

    # Baliza
    path('baliza/list/', BalizaListView.as_view(), name='form_readlist_baliza'),
    path('baliza/create/', BalizaCreateView.as_view(), name='form_create_baliza'),
    path('baliza/edit/<int:pk>/', BalizaUpdateView.as_view(), name='form_update_baliza'),
    path('baliza/editInstalacion/<int:pk>/', BalizaInstalacionUpdateView.as_view(),
         name='form_update_baliza_instalacion'),
    path('baliza/delete/<int:pk>/', BalizaDeleteView.as_view(), name='form_delete_baliza'),

    # Sedes
    path('sede/list/', SedeListView.as_view(), name='form_readlist_sede'),
    path('sede/create/', SedeCreateView.as_view(), name='form_create_sede'),
    path('sede/edit/<int:pk>/', SedeUpdateView.as_view(), name='form_update_sede'),
    path('sede/delete/<int:pk>/', SedeDeleteView.as_view(), name='form_delete_sede'),

    # Piso
    path('piso/list/', PisoListView.as_view(), name='form_readlist_piso'),
    path('piso/create/', PisoCreateView.as_view(), name='form_create_piso'),
    path('piso/edit/<int:pk>/', PisoUpdateView.as_view(), name='form_update_piso'),
    path('piso/delete/<int:pk>/', PisoDeleteView.as_view(), name='form_delete_piso'),

    # Area
    path('area/list/', AreaListView.as_view(), name='form_readlist_area'),
    path('area/create/', AreaCreateView.as_view(), name='form_create_area'),
    path('area/edit/<int:pk>/', AreaUpdateView.as_view(), name='form_update_area'),
    path('area/delete/<int:pk>/', AreaDeleteView.as_view(), name='form_delete_area'),

    # Historial
    path('historial/Ubicacion/', HistorialUbicacionListView.as_view(), name='form_read_historial_ubicacion'),
    path('historial/Sensores/', HistorialSensoresListView.as_view(), name='form_read_historial_sensores'),
]
