from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.baliza.models import Piso, Sede
from apps.baliza.views.piso.forms import PisoForm


@method_decorator(login_required(login_url='signin'), name='dispatch')
class PisoListView(ListView):
    model = Piso
    template_name = 'Ubicacion/PisoListView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Pisos por sede'
        context['list_url'] = reverse_lazy('project:form_create_piso')
        context['create_url'] = reverse_lazy('project:form_create_piso')
        context['entity'] = 'Pisos'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class PisoCreateView(CreateView):
    model = Piso
    form_class = PisoForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_piso')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            action = request.POST['action']
            if action == 'add':
                forms = PisoForm(request.POST)
                if forms.is_valid():
                    sede = forms.cleaned_data['sede']
                    piso_user = forms.cleaned_data['piso']
                    descripcion = forms.cleaned_data['descripcion']

                    piso = Piso()
                    piso.sede = sede
                    piso.piso = piso_user
                    piso.descripcion = descripcion
                    piso.usuarioRegistra = request.user
                    piso.save()
                    data['redirec'] = reverse_lazy('project:form_readlist_piso')
                else:
                    data['error'] = 'Error en datos, favor intentelo de nuevo'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Piso'
        context['action'] = 'add'
        context['entity'] = 'Crear Piso'

        if Sede.objects.all().count() == 0:
            context['error'] = 'No hay una Sede creada, por favor cree una para poder crear un piso en la Sede.'
        return context



@method_decorator(login_required(login_url='signin'), name='dispatch')
class PisoUpdateView(UpdateView):
    model = Piso
    form_class = PisoForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_piso')

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
                data['redirec'] = reverse_lazy('project:form_readlist_piso')
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
class PisoDeleteView(DeleteView):
    model = Piso
    form_class = PisoForm
    template_name = 'DELETE.html'
    success_url = reverse_lazy('project:form_readlist_piso')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['redirec'] = reverse_lazy('project:form_readlist_piso')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Area'
        context['entity'] = 'Sedes'
        context['textoMostrar'] = "Piso " + str(self.object.piso)
        context['list_url'] = reverse_lazy('project:form_readlist_piso')
        return context