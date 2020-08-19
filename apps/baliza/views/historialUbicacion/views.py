from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.baliza.models import HistorialUbicacion


@method_decorator(login_required(login_url='signin'), name='dispatch')
class HistorialUbicacionListView(ListView):
    model = HistorialUbicacion
    template_name = 'Historial/HistorialUbicacionListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Historial Ubicaciones Bracelet'
        return context
