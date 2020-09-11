from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, DeleteView, UpdateView

from apps.baliza.models import BraceletUmbrals, Bracelet, Baliza
from apps.baliza.views.Bracelet.forms import CreateBraceletForm, BraceletForm, BraceletUmbralesForm


@method_decorator(login_required(login_url='signin'), name='dispatch')
class BraceletListView(ListView):
    model = BraceletUmbrals
    template_name = 'Bracelet/BraceletListView.html'

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
        context['title'] = 'Listado Bracelets'
        context['list_url'] = reverse_lazy('project:form_create_bracelet')
        context['create_url'] = reverse_lazy('project:form_create_bracelet')
        context['entity'] = 'Bracelets'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class BraceletCreateView(FormView):
    form_class = CreateBraceletForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_baliza')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            action = request.POST['action']
            if action == 'add':
                forms = CreateBraceletForm(request.POST)
                if forms.is_valid():
                    mac_bracelet = forms.cleaned_data['mac_bracelet']
                    bracelet_major = forms.cleaned_data['bracelet_major']
                    bracelet_minor = forms.cleaned_data['bracelet_minor']
                    bracelet_tx_power = forms.cleaned_data['bracelet_tx_power']
                    description_bracelet = forms.cleaned_data['description_bracelet']
                    bracelet_temp_min = forms.cleaned_data['bracelet_temp_min']
                    bracelet_temp_max = forms.cleaned_data['bracelet_temp_max']
                    bracelet_ppm_min = forms.cleaned_data['bracelet_ppm_min']
                    bracelet_ppm_max = forms.cleaned_data['bracelet_ppm_max']

                    if len(mac_bracelet) == 17:
                        bracelet_major = int(bracelet_major)
                        bracelet_minor = int(bracelet_minor)
                        bracelet_tx_power = abs(int(bracelet_tx_power))
                        bracelet_temp_min = int(bracelet_temp_min)
                        bracelet_temp_max = int(bracelet_temp_max)
                        bracelet_ppm_min = int(bracelet_ppm_min)
                        bracelet_ppm_max = int(bracelet_ppm_max)
                        if bracelet_major > 0 \
                                and bracelet_minor > 0:
                            if bracelet_tx_power > 0:
                                if 20 < bracelet_temp_min < 35:
                                    if 37 < bracelet_temp_max < 45:
                                        if 40 < bracelet_ppm_min < 60:
                                            if 120 < bracelet_ppm_max < 180:
                                                hayError = False
                                                todasBalizas = Baliza.objects.all()
                                                for thisBaliza in todasBalizas:
                                                    if mac_bracelet == thisBaliza.macDispositivoBaliza:
                                                        data[
                                                            'error'] = 'La MAC ingresada ya esta registrada como Baliza'
                                                        hayError = True
                                                if hayError == False:
                                                    try:
                                                        bracelet = Bracelet()
                                                        bracelet.usuarioRegistra = request.user
                                                        bracelet.txPower = bracelet_tx_power
                                                        bracelet.macDispositivo = mac_bracelet
                                                        bracelet.major = bracelet_major
                                                        bracelet.minor = bracelet_minor
                                                        bracelet.descripcion = description_bracelet
                                                        bracelet.save()
                                                    except:
                                                        hayError = True
                                                        data[
                                                            'error'] = 'La MAC ingresada ya existe para un bracelet, no se pudo registrar'

                                                    if hayError == False:
                                                        bracelet = Bracelet.objects.get(macDispositivo=mac_bracelet)

                                                        umbrales = BraceletUmbrals()
                                                        umbrales.usuarioRegistra = request.user
                                                        umbrales.bracelet = bracelet
                                                        umbrales.minimaTemperatura = bracelet_temp_min
                                                        umbrales.maximaTemperatura = bracelet_temp_max
                                                        umbrales.minimoPulsoCardiaco = bracelet_ppm_min
                                                        umbrales.maximaPulsoCardiaco = bracelet_ppm_max
                                                        umbrales.save()

                                                        data['redirec'] = reverse_lazy('project:form_readlist_bracelet')
                                            else:
                                                data[
                                                    'error'] = 'El valor de PPM máximo es importante para poder determinar la taquicardia (PPM>125)'
                                        else:
                                            data[
                                                'error'] = 'El valor de PPM minimo es importante para poder determinar un posible infarto (PPM<55)'
                                    else:
                                        data[
                                            'error'] = 'El valor de temperatura máximo es importante para poder determinar la fiebre (Temp>37°C)'
                                else:
                                    data[
                                        'error'] = 'El valor de temperatura minimo es importante para poder determinar la hipotermia (20°C<Temp<35°C)'
                            else:
                                data[
                                    'error'] = 'La potencia de transmisión a un metro de distancia debe ser un valor entero, es de suma importancia para poder determinar la Localización dentro del edificio'
                        else:
                            data[
                                'error'] = 'Los datos de fabricación deben estar como números positivos (no se admite el valor 0).'
                    else:
                        data['error'] = 'La MAC ingresada no es valida'
                else:
                    data['error'] = 'Error en datos, favor intentelo de nuevo'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Bracelet'
        context['action'] = 'add'
        context['entity'] = 'Crear Bracelet'
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class BraceletDeleteView(DeleteView):
    model = Bracelet
    form_class = BraceletForm
    template_name = 'DELETE.html'
    success_url = reverse_lazy('project:form_readlist_bracelet')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            self.object.delete()
            data['redirec'] = reverse_lazy('project:form_readlist_bracelet')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación un Bracelet'
        context['entity'] = 'Bracelets'
        context['textoMostrar'] = self.object.macDispositivo + "-" + self.object.descripcion
        context['list_url'] = reverse_lazy('project:form_readlist_bracelet')
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class BraceletUpdateView(UpdateView):
    model = Bracelet
    form_class = BraceletForm
    template_name = 'Bracelet/BraceletUpdateView.html'
    success_url = reverse_lazy('project:form_readlist_bracelet')

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
                data['redirec'] = reverse_lazy('project:form_readlist_bracelet')
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Bracelet'
        context['action'] = 'edit'
        context['entity'] = 'Editar Bracelet'
        context['idUmbralsBracelet'] = BraceletUmbrals.objects.get(bracelet=self.object).id
        return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
class BraceletUmbralsUpdateView(UpdateView):
    model = BraceletUmbrals
    form_class = BraceletUmbralesForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_readlist_bracelet')

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
                data['redirec'] = reverse_lazy('project:form_readlist_bracelet')
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Bracelet (' + str(self.object.bracelet.macDispositivo) + ' - ' + str(
            self.object.bracelet.descripcion) + ')'
        context['action'] = 'edit'
        context['entity'] = 'Editar Bracelet'
        return context
