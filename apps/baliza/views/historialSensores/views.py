from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.baliza.models import HistorialBraceletSensors


@method_decorator(login_required(login_url='signin'), name='dispatch')
class HistorialSensoresListView(ListView):
    model = HistorialBraceletSensors
    template_name = 'Historial/HistorialSensoresListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Historial Sensores Bracelet'
        context['botonesAdicionales'] = 'OK'
        return context
