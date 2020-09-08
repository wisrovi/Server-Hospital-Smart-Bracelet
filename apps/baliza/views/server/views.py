from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, TemplateView

from apps.baliza.models import Bracelet, HistorialBraceletSensors, Baliza, HistorialRSSI, \
    InstalacionBaliza, Piso, Area
# Create your views here.
from apps.baliza.views.server.Libraries.ConsultasBaseDatos.ConsultasBaseDatos import \
    BuscarHistorialSensoresParaBracelet, BuscarUmbralesBraceletDB
from apps.baliza.views.server.Libraries.ProcessSensorsData import ValidarExisteBaliza, ValidarExisteBracelet, \
    ExtractMac, \
    ValidarCaida, ValidadProximidad, ValidarTemperatura, ValidarPPM, DeterminarIgualdad_o_cercano, ValidarNivelBateria, \
    ProcesarUbicacion, DeterminarPocisionPulsera
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
                historialSensores = HistorialBraceletSensors.objects.filter(bracelet=this_bracelet).order_by(
                    '-fechaRegistro')
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


@method_decorator(csrf_exempt, name='dispatch')
class ServerReceivedCreateView(FormView):
    form_class = PackBraceletForm
    template_name = 'FORM.html'
    success_url = reverse_lazy('project:form_received_baliza_ok')

    def post(self, request, *args, **kwargs):
        data = dict()
        try:
            import json
            d = request.POST
            data_received = ""
            keys = d.keys()
            for key in keys:
                # print(key)
                data_received = json.loads(str(key))

            # print(data_received['key'], data_received['string_pack'])
            if data_received['key'] == 'ESP32':
                forms = PackBraceletForm(data_received)
                if forms.is_valid():
                    string_pack = forms.cleaned_data['string_pack']

                    # Despues de obtener el dato se decodifica y se convierte en JSON
                    import base64
                    string_pack = string_pack.replace("*", "=")
                    string_pack = base64.b64decode(string_pack).decode("utf-8")
                    import json
                    string_pack = json.loads(string_pack)

                    # Se extrae del JSON los beacons y la baliza que entrega el reporte
                    listBracelets = string_pack['beacons']
                    baliza = string_pack['baliza']

                    # Se valida que la baliza exista, de lo contrario se envía un correo notificando newBaliza
                    findBaliza, balizaObjectModel = ValidarExisteBaliza(baliza, request)
                    if findBaliza:
                        # evaluo cada Bracelet (Beacon) por separado
                        for bracelet in listBracelets:
                            # Valido que el Bracelet exista, de lo contrario envio correo notificando newBracelet
                            findBracelet, braceletObject = ValidarExisteBracelet(bracelet['MAC'], baliza, request)
                            if findBracelet:
                                ####################################################################
                                ####################################################################
                                ###################                       ##########################
                                ###################  Procesando Sensores  ##########################
                                ###################                       ##########################
                                ####################################################################
                                ####################################################################

                                # print("Procesando datos de los sensores")

                                # leo en la DB el objeto de Bracelet y traigo todos los campos
                                pulsera = braceletObject
                                balizaNow = balizaObjectModel

                                # nuevos datos de sensores recibidos
                                nivelBateriaRecibido_nuevo = int(bracelet['BAT'])
                                nivelTemperaturaRecibido_nuevo = int(bracelet['TEM'])
                                nivelPPMRecibido_nuevo = int(bracelet['PPM'])

                                # Leo el ultimo registro para este Bracelet que se está procesando
                                hist = BuscarHistorialSensoresParaBracelet(pulsera)

                                registroYaExiste = False
                                if len(hist) > 0:
                                    nivelBateriaGuardadoDB = hist[0].nivel_bateria
                                    nivelTemperaturaGuardadoDB = hist[0].temperatura_sensor
                                    nivelPPMGuardadoDB = hist[0].ppm_sensor

                                    if hist[0].bracelet.macDispositivo == ExtractMac(bracelet['MAC']):
                                        # Valido que no hayan registros seguidos repetidos o cercanos
                                        if nivelBateriaRecibido_nuevo < minimo_nivel_bateria:
                                            factorVariacionBateria = 0.2
                                        else:
                                            factorVariacionBateria = 0.05

                                        if nivelTemperaturaRecibido_nuevo > 37 or nivelTemperaturaRecibido_nuevo < 25:
                                            factorVariacionTemperatura = 0.05
                                        else:
                                            factorVariacionTemperatura = 0.2

                                        if nivelPPMRecibido_nuevo > 120 or nivelPPMRecibido_nuevo < 55:
                                            factorVariacionPPM = 0.05
                                        else:
                                            factorVariacionPPM = 0.2

                                        if hist[0].caida_sensor == bool(int(bracelet['CAI'])) \
                                                and hist[0].proximidad_sensor == bool(int(bracelet['PRO'])) \
                                                and DeterminarIgualdad_o_cercano(nivelBateriaGuardadoDB,
                                                                                 nivelBateriaRecibido_nuevo,
                                                                                 factorVariacionBateria) \
                                                and DeterminarIgualdad_o_cercano(nivelTemperaturaGuardadoDB,
                                                                                 nivelTemperaturaRecibido_nuevo,
                                                                                 factorVariacionTemperatura) \
                                                and DeterminarIgualdad_o_cercano(nivelPPMGuardadoDB,
                                                                                 nivelPPMRecibido_nuevo,
                                                                                 factorVariacionPPM):
                                            registroYaExiste = True

                                if not registroYaExiste:
                                    # Si no existe ningún registro para este bracelet, guardo el registro que se preparó anteriormente
                                    # Si el registro actual no es un registro repetido al anterior, entonces guardo el registro que se preparó anteriormente
                                    # Creo un nuevo registro de historial y lo guardo
                                    histNew = HistorialBraceletSensors()
                                    histNew.bracelet = pulsera
                                    histNew.baliza = balizaNow
                                    histNew.caida_sensor = bool(int(bracelet['CAI']))
                                    histNew.nivel_bateria = int(bracelet['BAT'])
                                    histNew.proximidad_sensor = bool(int(bracelet['PRO']))
                                    histNew.temperatura_sensor = int(bracelet['TEM'])
                                    histNew.rssi_signal = int(bracelet['RSI'])
                                    histNew.ppm_sensor = int(bracelet['PPM'])
                                    histNew.save()

                                macBracelet = str(ExtractMac(bracelet['MAC']))
                                ValidarCaida(macBracelet, bool(int(bracelet['CAI'])), request)
                                ValidadProximidad(macBracelet, bool(int(bracelet['PRO'])), request)

                                findUmbrals, braceletUmbralsObject = BuscarUmbralesBraceletDB(pulsera)
                                if findUmbrals:
                                    ValidarTemperatura(macBracelet, nivelTemperaturaRecibido_nuevo, braceletUmbralsObject, request)
                                    ValidarPPM(macBracelet, nivelPPMRecibido_nuevo, braceletUmbralsObject, request)
                                    ValidarNivelBateria(nivelBateriaRecibido_nuevo, baliza, macBracelet, request)

                                # print("Procesando datos de ubicación")
                                nivelRssiRecibido_nuevo = int(bracelet['RSI'])
                                ProcesarUbicacion(balizaNow, pulsera, nivelRssiRecibido_nuevo)
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
