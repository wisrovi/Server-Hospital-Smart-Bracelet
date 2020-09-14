from django.contrib.auth.decorators import login_required
from django.db import close_old_connections, connections
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, TemplateView


# Create your views here.
from apps.baliza.models import Bracelet, HistorialBraceletSensors, Baliza, HistorialRSSI, \
    InstalacionBaliza, Piso, Area, BraceletPatienHospital, BraceletUmbrals
from apps.baliza.views.server.Libraries.ProcessSensorsData import NotifyBalizaNotExist, ExtractMac, NotifyPersonFallen, \
    NotifyPersonRemovedBracelet, NotifyTemperatureAlert, NotifyPpmAlert, DeterminarIgualdad_o_cercano, \
    NotifyBateryLevelLow, \
    DeterminarPocisionPulsera, NotifyBraceletNotExist, getDestinatariosCorreos, ProcesarUbicacion
from apps.baliza.views.server.forms import PackBraceletForm, FiltrarGrafica
from authentication.Config.Constants.Contant import minimo_nivel_bateria


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

def ExtractMac(string):
    macPulsera_complete = string[0:2] \
                          + ":" + string[2:4] \
                          + ":" + string[4:6] \
                          + ":" + string[6:8] \
                          + ":" + string[8:10] \
                          + ":" + string[10:12]
    return macPulsera_complete

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
                area_seleccionada = request.POST['area']
                piso = Piso.objects.filter(pk=id)

                if area_seleccionada != "":
                    area_seleccionada = Area.objects.get(pk=area_seleccionada)
                    area_seleccionada = (
                        area_seleccionada.xInicial,
                        area_seleccionada.yInicial,
                        area_seleccionada.xFinal,
                        area_seleccionada.yFinal
                    )

                ubicacionesBalizasPlano = list()
                tipoBaliza = "Baliza"
                todasLasBalizas = Baliza.objects.all()
                for baliza in todasLasBalizas:
                    instalacion = InstalacionBaliza.objects.filter(baliza=baliza)
                    for instal in instalacion:
                        pis = instal.piso
                        if pis == piso[0]:
                            elemento = list()
                            coordenadas = (instalacion[0].instalacionX, instalacion[0].instalacionY)
                            if area_seleccionada != "":
                                # print("Area en: ({}, {}) -> ({}, {})".format(
                                #     area_seleccionada[0],
                                #     area_seleccionada[1],
                                #     area_seleccionada[2],
                                #     area_seleccionada[3]
                                # ))
                                # print(coordenadas[0], coordenadas[1])
                                if area_seleccionada[0] < coordenadas[0] < area_seleccionada[2] and \
                                    area_seleccionada[1] < coordenadas[1] < area_seleccionada[3]:
                                    elemento.append(baliza.macDispositivoBaliza)
                                    elemento.append(coordenadas[0])
                                    elemento.append(coordenadas[1])
                                    elemento.append(tipoBaliza)
                                    # print("registro OK")
                                    ubicacionesBalizasPlano.append(elemento)
                            else:
                                elemento.append(baliza.macDispositivoBaliza)
                                elemento.append(coordenadas[0])
                                elemento.append(coordenadas[1])
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
                        # print("El valor estimado de ubicación (x,y) es", CartesianoFinal[0], CartesianoFinal[1], "+-",
                        #       constantePresicion)
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
            elif action == 'search_area':
                data = list()

                elemento = dict()
                elemento['id'] = 0
                elemento['text'] = "-----------------"
                data.append(elemento)

                idUbicacion = request.POST['id']
                piso_selecionado = Piso.objects.get(pk=idUbicacion)
                listado_areas = Area.objects.filter(piso=piso_selecionado)
                for are in listado_areas:
                    elemento = dict()
                    elemento['id'] = are.id
                    elemento['text'] = are.area
                    data.append(elemento)
            elif action == 'search_sensors':
                mac_bracelet = request.POST['mac']
                this_bracelet = Bracelet.objects.get(macDispositivo=mac_bracelet)
                historialSensores = HistorialBraceletSensors.objects.filter(bracelet=this_bracelet).order_by('-fechaRegistro')
                for hist in historialSensores:
                    data = dict()
                    data['ppm'] = hist.ppm_sensor
                    data['pro'] = hist.proximidad_sensor
                    data['cai'] = hist.caida_sensor
                    data['temp'] = hist.temperatura_sensor
                    data['bat'] = hist.nivel_bateria
                    data['fec'] = hist.fechaRegistro
                    break
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


def decodeReceived(data):
    import base64
    string_pack = data.replace("*", "=")
    string_pack = base64.b64decode(string_pack).decode("utf-8")
    import json
    data = json.loads(string_pack)
    return data


def ExtractKey(d):
    import json
    data_received = ""
    keys = d.keys()
    for key in keys:
        key = str(key)
        key = key.replace("'", '"')
        # print(key)
        data_received = json.loads(str(key))
        return data_received


def CloseOldConectionDB():
    try:
        connections.close_all()
        close_old_connections()
    except:
        pass

@method_decorator(csrf_exempt, name='dispatch')
class ServerReceivedCreateView(FormView):
    form_class = PackBraceletForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_received_baliza_ok')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            data_received = ExtractKey(request.POST)
            if data_received['key'] == 'ESP32':
                forms = PackBraceletForm(data_received)
                if forms.is_valid():
                    dataJson = decodeReceived(forms.cleaned_data['string_pack'])
                    baliza = ExtractMac(dataJson['baliza'][0])

                    CloseOldConectionDB()
                    listaDestinatarios = getDestinatariosCorreos()

                    if len(listaDestinatarios) > 0:
                        try:
                            thisBaliza = Baliza.objects.get(macDispositivoBaliza=baliza)
                            print(thisBaliza)
                            findBaliza = True
                        except:
                            findBaliza = False

                        if findBaliza:
                            listBracelets = dataJson['beacons']
                            for braceletJson in listBracelets:
                                macBracelet = ExtractMac(braceletJson['MAC'])
                                try:
                                    thisBracelet = Bracelet.objects.get(macDispositivo=macBracelet)
                                    print(thisBracelet)
                                    findBracelet = True
                                except:
                                    findBracelet = False

                                if findBracelet:
                                    proximity_received_data = bool(int(braceletJson['PRO']))
                                    batery_received_data = int(braceletJson['BAT'])
                                    temperature_received_data = int(float(braceletJson['TEM']))
                                    ppm_received_data = int(braceletJson['PPM'])
                                    caida_received_data = bool(int(braceletJson['CAI']))
                                    rssi_received_data = int(braceletJson['RSI'])

                                    try:
                                        paciente = BraceletPatienHospital.objects.get(bracelet=thisBracelet).idDatosPaciente
                                    except:
                                        paciente = str('<< Paciente >>')

                                    try:
                                        hist = HistorialBraceletSensors.objects.order_by('-fechaRegistro').filter(bracelet=thisBracelet).first()
                                        if hist is not None:
                                            new_register_rssi = False
                                        else:
                                            new_register_rssi = True
                                    except:
                                        new_register_rssi = True  # No hay historial, se crea el primer registro para este bracelet

                                    if not new_register_rssi:
                                        ValidProximityForReport = hist.proximidad_sensor != proximity_received_data
                                        if proximity_received_data:
                                            VariationConstantBatery = 0.05
                                            VariationConstantPPM = 0.15
                                            VariationConstantTemperature = 0.10
                                            ValidBateryForReport = not DeterminarIgualdad_o_cercano(hist.nivel_bateria, batery_received_data, VariationConstantBatery)
                                            ValidTemperatureForReport = not DeterminarIgualdad_o_cercano(hist.temperatura_sensor, temperature_received_data, VariationConstantTemperature)
                                            ValidPpmForReport = not DeterminarIgualdad_o_cercano(hist.ppm_sensor, ppm_received_data, VariationConstantPPM)
                                            ValidDropForReport = hist.caida_sensor != caida_received_data
                                        else:
                                            ValidBateryForReport = False
                                            ValidTemperatureForReport = False
                                            ValidPpmForReport = False
                                            ValidDropForReport = False

                                        if ValidBateryForReport or ValidTemperatureForReport or ValidPpmForReport or ValidDropForReport or ValidProximityForReport:
                                            new_register_rssi = True

                                    if new_register_rssi:
                                        histNew = HistorialBraceletSensors()
                                        histNew.bracelet = thisBracelet
                                        histNew.baliza = thisBaliza
                                        histNew.caida_sensor = caida_received_data
                                        histNew.nivel_bateria = batery_received_data
                                        histNew.proximidad_sensor = proximity_received_data
                                        histNew.temperatura_sensor = temperature_received_data
                                        histNew.rssi_signal = rssi_received_data
                                        histNew.ppm_sensor = ppm_received_data
                                        histNew.save()

                                    if not proximity_received_data:
                                        NotifyPersonRemovedBracelet(macBracelet, request, listaDestinatarios, paciente)
                                    else:
                                        if caida_received_data:
                                            NotifyPersonFallen(macBracelet, request, listaDestinatarios, paciente)

                                        if batery_received_data <= minimo_nivel_bateria:
                                            NotifyBateryLevelLow(baliza, macBracelet, request, listaDestinatarios)

                                        try:
                                            umbrals = BraceletUmbrals.objects.get(bracelet=thisBracelet)
                                            thereUmbrals = True
                                        except:
                                            thereUmbrals = False

                                        if thereUmbrals:
                                            if (temperature_received_data >= umbrals.maximaTemperatura) or (temperature_received_data <= umbrals.minimaTemperatura):
                                                NotifyTemperatureAlert(macBracelet, temperature_received_data, request, umbrals, listaDestinatarios)

                                            if (ppm_received_data >= umbrals.maximaPulsoCardiaco) or (ppm_received_data <= umbrals.minimoPulsoCardiaco):
                                                NotifyPpmAlert(macBracelet, ppm_received_data, request, umbrals, listaDestinatarios)

                                    # print("Procesando datos de ubicación")
                                    ProcesarUbicacion(thisBaliza, thisBracelet, rssi_received_data)
                                else:
                                    NotifyBraceletNotExist(macBracelet, request, listaDestinatarios)  # by send mail async: new Bracelet
                        else:
                            NotifyBalizaNotExist(baliza, request, listaDestinatarios)  # by send mail async: new Baliza
                    else:
                        print()
                        print("No hay usuario para destinar los correos de notificación, por favor registre un usuario.")
                        print()
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
