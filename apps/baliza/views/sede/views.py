from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.baliza.models import Sede
from apps.baliza.views.sede.forms import SedeForm


@method_decorator(login_required(login_url='signin'), name='dispatch')
# @method_decorator(csrf_exempt, name='dispatch')
class SedeListView(ListView):
    model = Sede
    template_name = 'Ubicacion/SedeListView.html'

    def dispatch(self, request, *args, **kwargs):
        # todo lo que sucede antes que se cargue la web por primera vez
        # por ejemplo, comprobar que el rol del user le permite ver la lista
        print(request.user)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            data['name'] = 'William'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Sedes'
        context['list_url'] = reverse_lazy('project:form_create_sede')
        context['create_url'] = reverse_lazy('project:form_create_sede')
        context['entity'] = 'Sedes'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class SedeCreateView(CreateView):
    model = Sede
    form_class = SedeForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_sede')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            action = request.POST['action']
            if action == 'add':
                forms = SedeForm(request.POST)
                if forms.is_valid():
                    nombreSede = forms.cleaned_data['nombreSede']
                    descripcion = forms.cleaned_data['descripcion']

                    sede = Sede()
                    sede.nombreSede = nombreSede
                    sede.descripcion = descripcion
                    sede.usuarioRegistra = request.user
                    sede.save()
                    data['redirec'] = reverse_lazy('project:form_readlist_sede')
                else:
                    data['error'] = 'Error en datos, favor intentelo de nuevo'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Sede'
        context['action'] = 'add'
        context['entity'] = 'Crear Sede'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class SedeUpdateView(UpdateView):
    model = Sede
    form_class = SedeForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_sede')

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
                data['redirec'] = reverse_lazy('project:form_readlist_sede')
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Sede'
        context['action'] = 'edit'
        context['entity'] = 'Editar Sede'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class SedeDeleteView(DeleteView):
    model = Sede
    form_class = SedeForm
    template_name = 'DELETE.html'
    success_url = reverse_lazy('project:form_readlist_sede')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            self.object.delete()
            data['redirec'] = reverse_lazy('project:form_readlist_sede')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Sede'
        context['textoMostrar'] = self.object.nombreSede
        context['entity'] = 'Sedes'
        context['list_url'] = reverse_lazy('project:form_readlist_sede')
        return context
