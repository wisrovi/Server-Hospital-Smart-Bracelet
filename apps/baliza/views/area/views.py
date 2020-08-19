from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from apps.baliza.models import Area, Piso
from apps.baliza.views.area.forms import AreaForm


@method_decorator(login_required(login_url='signin'), name='dispatch')
class AreaListView(ListView):
    model = Area
    template_name = 'Ubicacion/AreaListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Areas por Piso en Sede'
        context['list_url'] = reverse_lazy('project:form_create_area')
        context['create_url'] = reverse_lazy('project:form_create_area')
        context['entity'] = 'Sedes'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class AreaCreateView(CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_area')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            action = request.POST['action']
            if action == 'add':
                forms = AreaForm(request.POST)
                if forms.is_valid():
                    area_sel = forms.cleaned_data['area']
                    xInicial = forms.cleaned_data['xInicial']
                    xFinal = forms.cleaned_data['xFinal']
                    yInicial = forms.cleaned_data['yInicial']
                    yFinal = forms.cleaned_data['yFinal']
                    descripcion = forms.cleaned_data['descripcion']
                    piso = forms.cleaned_data['piso']

                    area = Area()
                    area.area = area_sel
                    area.xInicial = xInicial
                    area.xFinal = xFinal
                    area.yInicial = yInicial
                    area.yFinal = yFinal
                    area.descripcion = descripcion
                    area.piso = piso
                    area.usuarioRegistra = request.user
                    area.save()
                    data['redirec'] = reverse_lazy('project:form_readlist_area')
                else:
                    data['error'] = 'Error en datos, favor intentelo de nuevo'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Area'
        context['action'] = 'add'
        context['entity'] = 'Crear Area'
        if Piso.objects.all().count() == 0:
            context['error'] = 'No hay una Piso creado para ninguna sede, por favor cree uno.'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_area')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                print(data)
                data['redirec'] = reverse_lazy('project:form_readlist_area')
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Area'
        context['action'] = 'edit'
        context['entity'] = 'Editar Area'
        return context

@method_decorator(login_required(login_url='signin'), name='dispatch')
class AreaDeleteView(DeleteView):
    model = Area
    form_class = AreaForm
    template_name = 'DELETE.html'
    success_url = reverse_lazy('project:form_readlist_area')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['redirec'] = reverse_lazy('project:form_readlist_area')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Area'
        context['entity'] = 'Sedes'
        context['textoMostrar'] = self.object.area
        context['list_url'] = reverse_lazy('project:form_readlist_area')
        return context