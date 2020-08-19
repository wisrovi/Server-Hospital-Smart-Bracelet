from time import time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, TemplateView

from apps.baliza.models import Bracelet, HistorialBraceletSensors, Baliza, HistorialRSSI, \
    InstalacionBaliza, Piso

# Create your views here.
from apps.baliza.views.server.Libraries.ProcessSensorsData import ValidarExisteBaliza, ValidarExisteBracelet, \
    ExtractMac, \
    ValidarCaida, ValidadProximidad, ValidarTemperatura, ValidarPPM, DeterminarIgualdad_o_cercano, ValidarNivelBateria, \
    ProcesarUbicacion, DeterminarPocisionPulsera
from apps.baliza.views.server.forms import PackBraceletForm, FiltrarGrafica


class DatoGraficaBubble:
    name = None
    x = None
    y = None
    tipo = None

    def __init__(self, name, x, y, tipo):
        self.name = name
        self.x = x
        self.y = y
        self.tipo = tipo


@method_decorator(login_required(login_url='signin'), name='dispatch')
class VerPiso(TemplateView):
    template_name = 'Server/Graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos = self.request.GET
        id = int(datos['id'])
        piso = Piso.objects.filter(pk=id)

        ubicacionesBalizasPlano = list()
        ubicacionesPulserasPlano = list()
        if len(piso) > 0:
            tipoBaliza = "Baliza"
            todasLasBalizas = Baliza.objects.all()
            for baliza in todasLasBalizas:
                instalacion = InstalacionBaliza.objects.filter(baliza=baliza)
                for instal in instalacion:
                    pis = instal.piso
                    if pis == piso[0]:
                        datosBaliza = DatoGraficaBubble(name=baliza.macDispositivoBaliza,
                                                        x=instalacion[0].instalacionX,
                                                        y=instalacion[0].instalacionY,
                                                        tipo=tipoBaliza)
                        ubicacionesBalizasPlano.append(datosBaliza)

            tipoPulsera = "Manilla"
            todasLasPulseras = Bracelet.objects.all()
            for pulsera in todasLasPulseras:
                CartesianoFinal, idsBalizasUsadas, pisoDeseado = DeterminarPocisionPulsera(pulsera,
                                                                                           pisoDeseado=piso)
                if CartesianoFinal is not None:
                    datosPulsera = DatoGraficaBubble(name=pulsera.macDispositivo,
                                                     x=int(CartesianoFinal[0]),
                                                     y=int(CartesianoFinal[1]),
                                                     tipo=tipoPulsera)
                    ubicacionesPulserasPlano.append(datosPulsera)

            context['title'] = 'Grafica ' + piso[0].__str__()
            context['todasPulseras'] = ubicacionesPulserasPlano
            context['todasBalizas'] = ubicacionesBalizasPlano
            return context


@method_decorator(login_required(login_url='signin'), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class FiltrarGraficaUbicacion(TemplateView):
    template_name = 'Server/GraphFilter.html'

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            action = request.POST['action']
            if action == 'graph_ubicacion':
                id = request.POST['id']
                piso = Piso.objects.filter(pk=id)

                ubicacionesBalizasPlano = list()
                tipoBaliza = "Baliza"
                todasLasBalizas = Baliza.objects.all()
                for baliza in todasLasBalizas:
                    instalacion = InstalacionBaliza.objects.filter(baliza=baliza)
                    for instal in instalacion:
                        pis = instal.piso
                        if pis == piso[0]:
                            elemento = list()
                            elemento.append(baliza.macDispositivoBaliza)
                            elemento.append(instalacion[0].instalacionX)
                            elemento.append(instalacion[0].instalacionY)
                            elemento.append(tipoBaliza)
                            ubicacionesBalizasPlano.append(elemento)

                ubicacionesPulserasPlano = list()
                tipoPulsera = "Manilla"
                todasLasPulseras = Bracelet.objects.all()
                for pulsera in todasLasPulseras:
                    CartesianoFinal, idsBalizasUsadas, pisoDeseado = DeterminarPocisionPulsera(pulsera,
                                                                                               pisoDeseado=piso)
                    if CartesianoFinal is not None:
                        constantePresicion = 6
                        print("El valor estimado de ubicación (x,y) es", CartesianoFinal[0], CartesianoFinal[1], "+-",
                              constantePresicion)
                        elemento = list()
                        elemento.append(pulsera.macDispositivo)
                        elemento.append(CartesianoFinal[0])
                        elemento.append(CartesianoFinal[1])
                        elemento.append(tipoPulsera)
                        ubicacionesPulserasPlano.append(elemento)

                data['todasBalizas'] = ubicacionesBalizasPlano
                data['todasPulseras'] = ubicacionesPulserasPlano
                data['idPiso'] = piso[0].id
            elif action == 'search_ubicacion':
                data = list()
                elemento = dict()
                elemento['id'] = 0
                elemento['text'] = "-----------------"
                data.append(elemento)

                for i in Piso.objects.filter(sede_id=request.POST['id']):
                    elemento = dict()
                    elemento['id'] = i.id
                    elemento['text'] = i.__str__()
                    data.append(elemento)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grafica Ubicaciones'
        context['form'] = FiltrarGrafica()
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ServerReceivedCreateView(FormView):
    form_class = PackBraceletForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_received_baliza_ok')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            key = request.POST['key']
            if key == 'ESP32':
                forms = PackBraceletForm(request.POST)
                if forms.is_valid():
                    string_pack = forms.cleaned_data['string_pack']

                    # Despues de obtener el dato se decodifica y se convierte en JSON
                    import base64
                    string_pack = base64.b64decode(string_pack).decode("utf-8")
                    import json
                    string_pack = json.loads(string_pack)

                    # Se extrae del JSON los beacons y la baliza que entrega el reporte
                    listBracelets = string_pack['beacons']
                    baliza = string_pack['baliza']

                    # Se valida que la baliza exista, de lo contrario se envía un correo notificando newBaliza
                    if ValidarExisteBaliza(baliza, request):
                        # evaluo cada Bracelet (Beacon) por separado
                        for bracelet in listBracelets:
                            # Valido que el Bracelet exista, de lo contrario envio correo notificando newBracelet
                            if ValidarExisteBracelet(bracelet['MAC'], baliza, request):
                                ####################################################################
                                ####################################################################
                                ###################                       ##########################
                                ###################  Procesando Sensores  ##########################
                                ###################                       ##########################
                                ####################################################################
                                ####################################################################

                                # print("Procesando datos de los sensores")

                                # leo en la DB el objeto de Bracelet y traigo todos los campos
                                pulsera = Bracelet.objects.get(macDispositivo=ExtractMac(bracelet['MAC']))
                                balizaNow = Baliza.objects.get(macDispositivoBaliza=baliza)

                                # Creo un nuevo registro de historial, pero aún no lo guardo
                                histNew = HistorialBraceletSensors()
                                histNew.bracelet = pulsera
                                histNew.baliza = balizaNow
                                histNew.caida_sensor = bool(int(bracelet['CAI']))
                                histNew.nivel_bateria = int(bracelet['BAT'])
                                histNew.proximidad_sensor = bool(int(bracelet['PRO']))
                                histNew.temperatura_sensor = int(bracelet['TEM'])
                                histNew.rssi_signal = int(bracelet['RSI'])
                                histNew.ppm_sensor = int(bracelet['PPM'])

                                # Leo el ultimo registro para este Bracelet que se está procesando
                                hist = HistorialBraceletSensors.objects.filter(bracelet=pulsera).order_by(
                                    '-fechaRegistro')
                                registroYaExiste = False
                                if len(hist) > 0:
                                    if hist[0].bracelet.macDispositivo == ExtractMac(bracelet['MAC']):
                                        # Valido que no hayan registros seguidos repetidos
                                        factorVariacion = 0.05
                                        if hist[0].caida_sensor == bool(int(bracelet['CAI'])) \
                                                and hist[0].proximidad_sensor == bool(int(bracelet['PRO'])) \
                                                and DeterminarIgualdad_o_cercano(hist[0].nivel_bateria,
                                                                                 int(bracelet['BAT']), factorVariacion) \
                                                and DeterminarIgualdad_o_cercano(hist[0].temperatura_sensor,
                                                                                 int(bracelet['TEM']), factorVariacion) \
                                                and DeterminarIgualdad_o_cercano(hist[0].ppm_sensor,
                                                                                 int(bracelet['PPM']), factorVariacion):
                                            registroYaExiste = True

                                if registroYaExiste == False:
                                    # Si no existe ningún registro para este bracelet, guardo el registro que se preparó anteriormente
                                    # Si el registro actual no es un registro repetido al anterior, entonces guardo el registro que se preparó anteriormente
                                    histNew.save()

                                ValidarCaida(baliza, bracelet['MAC'], bool(int(bracelet['CAI'])), request)
                                ValidadProximidad(baliza, bracelet['MAC'], bool(int(bracelet['PRO'])), request)
                                ValidarTemperatura(bracelet['MAC'], int(bracelet['TEM']), request)
                                ValidarPPM(bracelet['MAC'], int(bracelet['PPM']), request)
                                ValidarNivelBateria(int(bracelet['BAT']), baliza, bracelet['MAC'], request)

                                print("Procesando datos de ubicación")
                                ProcesarUbicacion(baliza, bracelet['MAC'], bracelet['RSI'])
                else:
                    data['error'] = 'Error en datos, favor intentelo de nuevo'
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recibir un dato de Baliza'
        context['entity'] = 'Crear Dato'
        return context


def setReceivedOK(request):
    return render(request, 'Server/receivedOK.html', {})


@method_decorator(login_required(login_url='signin'), name='dispatch')
# @method_decorator(csrf_exempt, name='dispatch')
class HistorialRssi_ListView(ListView):
    model = HistorialRSSI
    template_name = 'Server/HistorialRssiListView.html'

    def dispatch(self, request, *args, **kwargs):
        # todo lo que sucede antes que se cargue la web por primera vez
        print(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial RSSI'
        return context
