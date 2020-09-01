from django.template.loader import render_to_string
import apps.Util_apps.Util as Utilities
from apps.baliza.models import Baliza, RolUsuario, UsuarioRol, Bracelet, BraceletUmbrals, HistorialRSSI, \
    InstalacionBaliza
from apps.baliza.views.server.Libraries.LibraryRSSItoMts import CalcularDistancia
from apps.baliza.views.server.Libraries.CalculoUbicacion.Library_BLE_location import CalcularPosicion, BalizaInstalada, \
    Ubicacion
from apps.Util_apps.Decoradores import execute_in_thread

from authentication.Config.Constants.Contant import rol_enviar_notificaiones_servidor
from apps.Util_apps.Util import config_files

import os

listadoMacsReportadas = list()

PARAMETROS = dict()


# def render_to_string(nameFile, dictionary):
#     data = str()
#     ruta_archivo_html = ""
#     for i in os.path.abspath(__file__).split("\\")[:-1]:
#         ruta_archivo_html = os.path.join(ruta_archivo_html, i)
#     ruta_archivo_html = os.path.join(ruta_archivo_html, nameFile)
#
#     print(os.path.abspath(__file__), nameFile, ruta_archivo_html)
#
#     with open(ruta_archivo_html, "r") as myfile:
#         data = myfile.read()
#         for key in dictionary:
#             keys = list()
#             keys.append("{{ " + key + " }}")
#             keys.append("{{" + key + " }}")
#             keys.append("{{ " + key + "}}")
#             keys.append("{{" + key + "}}")
#             for llave in keys:
#                 if data.find(llave) >= 0:
#                     data = data.replace(llave, dictionary[key])
#                     break
#     return data


def ModifyHtml(url_path, html):
    cid = url_path.split("/")
    cid_search = cid[-1].split(".")[0]
    html = html.replace(url_path, "cid:" + cid_search)
    return html


def getDestinatariosCorreos():
    rolBuscar = rol_enviar_notificaiones_servidor
    listaCorreosDestinatarios = list()
    for rol in RolUsuario.objects.all():
        # print(rol.rolUsuario, rolBuscar, )
        # print(type(rol.rolUsuario), type(rolBuscar))
        if rol.rolUsuario == rolBuscar:
            for usuarioRevisar in UsuarioRol.objects.all():
                if usuarioRevisar.rolUsuario == rol:
                    listaCorreosDestinatarios.append(usuarioRevisar.usuario.email)
    if len(listaCorreosDestinatarios) == 0:
        print("[System]: No hay destinatarios para reportar los correos")
    return listaCorreosDestinatarios


def PutImagesHtml(imagenes_en_html, html_message):
    for path_url in imagenes_en_html:
        html_message = ModifyHtml(path_url, html_message)
    return html_message


@execute_in_thread(name="hilo ValidarExisteBaliza")
def ValidarExisteBaliza(baliza, request):
    baliza = ExtractMac(baliza[0])

    balizasExistentes = Baliza.objects.all()
    for baliz in balizasExistentes:
        valor_comparar_1 = baliz.macDispositivoBaliza
        valor_comparar_2 = baliza
        if valor_comparar_1 == valor_comparar_2:
            return True

    PARAMETROS = config_files['nueva_baliza']
    diccionarioDatos = dict()
    diccionarioDatos[PARAMETROS['Var'][0]] = str(baliza)
    imagenes_en_html = list()
    imagenes_en_html.append("LOGOFCV.png") #os.path.join("img", "LOGOFCV.png"))
    imagenes_en_html.append("baliza.jpg") #os.path.join("img", "baliza.jpg"))

    html_message = render_to_string(PARAMETROS['File'],
                                    diccionarioDatos)
    html_message = PutImagesHtml(imagenes_en_html, html_message)

    asunto = "Nueva Baliza por registrar (" + baliza + ")"

    listaDestinatarios = getDestinatariosCorreos()
    if len(listaDestinatarios) > 0:
        if not str(baliza) in listadoMacsReportadas:
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaDestinatarios, request)
            print("Nueva Baliza encontrada")
            listadoMacsReportadas.append(str(baliza))
    return False


@execute_in_thread(name="hilo ValidarExisteBracelet")
def ValidarExisteBracelet(bracelet, baliza, request):
    bracelet = ExtractMac(bracelet)

    braceletsExistentes = Bracelet.objects.all()
    for brac in braceletsExistentes:
        if bracelet == brac.macDispositivo:
            return True

    diccionarioDatos = dict()
    diccionarioDatos['ADMIN'] = str('Admin Server')
    diccionarioDatos['BALIZA'] = str(baliza)
    diccionarioDatos['MAC'] = str(bracelet)
    diccionarioDatos['PROJECT'] = str('Hospital Smart Bracelet')
    diccionarioDatos['FIRMA'] = str('WISROVI')
    html_message = render_to_string('email/bracelet_report_bad_sensors.html',
                                    diccionarioDatos)

    asunto = "Nuevo Bracelet por registrar (" + bracelet + ")"
    firmaResumenRemitente = "Hospital Smart Bracelet"

    listaDestinatarios = getDestinatariosCorreos()
    if len(listaDestinatarios) > 0:
        if not diccionarioDatos['MAC'] in listadoMacsReportadas:
            Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                               listaDestinatarios, request)
            print("Nuevo Bracelet encontrado")
            listadoMacsReportadas.append(diccionarioDatos['MAC'])
    return False


def ExtractMac(string):
    macPulsera_complete = string[0:2] \
                          + ":" + string[2:4] \
                          + ":" + string[4:6] \
                          + ":" + string[6:8] \
                          + ":" + string[8:10] \
                          + ":" + string[10:12]
    return macPulsera_complete


def getUmbrales(macPulsera):
    pulsera = Bracelet.objects.get(macDispositivo=ExtractMac(macPulsera))
    umbrales = BraceletUmbrals.objects.get(bracelet=pulsera)
    return umbrales


@execute_in_thread(name="hilo ValidarCaida")
def ValidarCaida(baliza, macPulsera, caida, request):
    if caida:
        diccionarioDatos = dict()
        diccionarioDatos['ADMIN'] = str('Admin Server')
        diccionarioDatos['BALIZA'] = str(baliza)
        diccionarioDatos['MAC'] = str(ExtractMac(macPulsera))
        diccionarioDatos['PROJECT'] = str('Hospital Smart Bracelet')
        diccionarioDatos['FIRMA'] = str('WISROVI')
        html_message = render_to_string(
            'email/bracelet_alerta_persona_caida.html',
            diccionarioDatos)
        asunto = "Alerta, persona caida (" + ExtractMac(macPulsera) + ")"
        firmaResumenRemitente = "Hospital Smart Bracelet"

        listaCorreosDestinatarios = getDestinatariosCorreos()
        if len(listaCorreosDestinatarios) > 0:
            Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                               listaCorreosDestinatarios, request)
            print("Bracelet alerta caida")


@execute_in_thread(name="hilo ValidadProximidad")
def ValidadProximidad(baliza, macPulsera, proximidad, request):
    if proximidad == False:
        diccionarioDatos = dict()
        diccionarioDatos['ADMIN'] = str('Admin Server')
        diccionarioDatos['BALIZA'] = str(baliza)
        diccionarioDatos['MAC'] = str(macPulsera)
        diccionarioDatos['PROJECT'] = str('Hospital Smart Bracelet')
        diccionarioDatos['FIRMA'] = str('WISROVI')
        html_message = render_to_string(
            'email/bracelet_alerta_persona_seQuitoPulsera.html',
            diccionarioDatos)
        asunto = "Alerta, persona se quitó el bracelet (" + macPulsera + ")"
        firmaResumenRemitente = "Hospital Smart Bracelet"

        listaCorreosDestinatarios = getDestinatariosCorreos()
        if len(listaCorreosDestinatarios) > 0:
            Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                               listaCorreosDestinatarios, request)
            print("Bracelet alerta proximidad")


@execute_in_thread(name="hilo ValidarTemperatura")
def ValidarTemperatura(macPulsera, temperaturaActual, request):
    umbrales = getUmbrales(macPulsera)

    diccionarioDatos = dict()
    diccionarioDatos['ADMIN'] = str('Admin Server')
    diccionarioDatos['MAC'] = str(macPulsera)
    diccionarioDatos['PROJECT'] = str('Hospital Smart Bracelet')
    diccionarioDatos['FIRMA'] = str('WISROVI')
    html_message = render_to_string(
        'email/bracelet_alerta_persona_seQuitoPulsera.html',
        diccionarioDatos)
    asunto = None
    hayAlarma = False

    temperaturaActual = temperaturaActual / 10

    if temperaturaActual > umbrales.maximaTemperatura:
        asunto = "Alerta, persona (" + macPulsera + ")" + " tiene temperatura alta (" + str(temperaturaActual) + ")"
        hayAlarma = True

    if temperaturaActual < umbrales.minimaTemperatura:
        asunto = "Alerta, persona (" + macPulsera + ")" + " tiene temperatura baja (" + str(temperaturaActual) + ")"
        hayAlarma = True

    firmaResumenRemitente = "Hospital Smart Bracelet"

    listaCorreosDestinatarios = getDestinatariosCorreos()
    if len(listaCorreosDestinatarios) > 0 and hayAlarma:
        Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                           listaCorreosDestinatarios, request)
        print("Bracelet alerta temperatura")


@execute_in_thread(name="hilo ValidarNivelBateria")
def ValidarNivelBateria(nivelBateria, baliza, macPulsera, request):
    if nivelBateria < 30:
        diccionarioDatos = dict()
        diccionarioDatos['ADMIN'] = str('Admin Server')
        diccionarioDatos['BALIZA'] = str(baliza)
        diccionarioDatos['MAC'] = str(macPulsera)
        diccionarioDatos['PROJECT'] = str('Hospital Smart Bracelet')
        diccionarioDatos['FIRMA'] = str('WISROVI')
        html_message = render_to_string(
            'email/bracelet_alerta_persona_seQuitoPulsera.html',
            diccionarioDatos)
        asunto = "Alerta, bracelet (" + macPulsera + ") con bateria baja."
        firmaResumenRemitente = "Hospital Smart Bracelet"

        listaCorreosDestinatarios = getDestinatariosCorreos()
        if len(listaCorreosDestinatarios) > 0:
            Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                               listaCorreosDestinatarios, request)
            print("Bracelet alerta bateria baja")


@execute_in_thread(name="hilo ValidarPPM")
def ValidarPPM(macPulsera, ppmActual, request):
    umbrales = getUmbrales(macPulsera)

    diccionarioDatos = dict()
    diccionarioDatos['ADMIN'] = str('Admin Server')
    diccionarioDatos['MAC'] = str(macPulsera)
    diccionarioDatos['PROJECT'] = str('Hospital Smart Bracelet')
    diccionarioDatos['FIRMA'] = str('WISROVI')
    html_message = render_to_string(
        'email/bracelet_alerta_persona_seQuitoPulsera.html',
        diccionarioDatos)
    asunto = None

    hayAlarma = False

    if ppmActual > umbrales.maximaPulsoCardiaco:
        asunto = "Alerta, persona (" + macPulsera + ")" + " tiene PPM alta (" + str(ppmActual) + ")"
        hayAlarma = True

    if ppmActual < umbrales.minimoPulsoCardiaco:
        asunto = "Alerta, persona (" + macPulsera + ")" + " tiene PPM baja (" + str(ppmActual) + ")"
        hayAlarma = True

    firmaResumenRemitente = "Hospital Smart Bracelet"

    listaCorreosDestinatarios = getDestinatariosCorreos()
    if len(listaCorreosDestinatarios) > 0 and hayAlarma:
        Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                           listaCorreosDestinatarios, request)
        print("Bracelet alerta temperatura")


def DeterminarIgualdad_o_cercano(valorAnterior, valorActual, variacion):
    if valorAnterior == valorActual:
        return True

    indiceVariacion = valorAnterior * variacion
    variacionSuperior = valorAnterior + indiceVariacion
    variacionInferior = valorAnterior - indiceVariacion

    if valorActual > variacionSuperior:
        return False

    if valorActual < variacionInferior:
        return False

    return True


@execute_in_thread(name="hilo ProcesarUbicacion")
def ProcesarUbicacion(baliza, macPulsera, rssi):
    macPulsera = ExtractMac(macPulsera)
    pulsera = Bracelet.objects.get(macDispositivo=macPulsera)

    measuredPower = pulsera.txPower
    rssi = int(rssi)

    distancia = CalcularDistancia(measuredPower, rssi)

    macBaliza = ExtractMac(baliza[0])

    balizaNow = Baliza.objects.get(macDispositivoBaliza=macBaliza)
    histoRssi = HistorialRSSI()
    histoRssi.baliza = balizaNow
    histoRssi.bracelet = pulsera
    histoRssi.rssi_signal = rssi

    ultimoRegistro = HistorialRSSI.objects.filter(bracelet=pulsera,
                                                  baliza=balizaNow).order_by('-fechaRegistro')
    if len(ultimoRegistro) > 0:
        if ultimoRegistro[0].rssi_signal != rssi:
            histoRssi.save()
    else:
        histoRssi.save()

    print("Baliza:", baliza, ", Pulsera:", macPulsera, ", metros:", distancia)


# @count_elapsed_time
def DeterminarPocisionPulsera(pulsera, pisoDeseado=None):
    ConstanteSegundosMaximosSeparacionRegistros = 15

    listadoBalizas = list()

    lastDate = None
    datosEstaPulsera = HistorialRSSI.objects.filter(bracelet=pulsera).order_by('-fechaRegistro')
    macBalizasProcesadas = list()
    if len(datosEstaPulsera) > 0:
        for dato in datosEstaPulsera:
            if lastDate is None:
                lastDate = dato.fechaRegistro
            else:
                diferencia = lastDate - dato.fechaRegistro
                diferencia = diferencia.seconds
                if diferencia < ConstanteSegundosMaximosSeparacionRegistros:
                    baliza = dato.baliza
                    if not baliza.macDispositivoBaliza in macBalizasProcesadas:
                        macBalizasProcesadas.append(baliza.macDispositivoBaliza)

                        datosInstalacionBaliza = InstalacionBaliza.objects.get(baliza=baliza)
                        pisoInstalacion = datosInstalacionBaliza.piso

                        # puntoInstalacion = (datosInstalacionBaliza.instalacionX, datosInstalacionBaliza.instalacionY)
                        # print(pulsera.descripcion, "--->", puntoInstalacion, "--->",
                        #       CalcularDistancia(pulsera.txPower, dato.rssi_signal), "mt", pisoInstalacion)

                        if pisoDeseado is not None:
                            puntoInstalacionBaliza = InstalacionBaliza.objects.filter(baliza=baliza)
                            for puntito in puntoInstalacionBaliza:
                                pisitoPuntito = puntito.piso
                                puntitoDeseado = pisoDeseado[0]
                                if pisitoPuntito == puntitoDeseado:
                                    listadoBalizas.append(
                                        BalizaInstalada(
                                            ubi=Ubicacion(
                                                x=datosInstalacionBaliza.instalacionX,
                                                y=datosInstalacionBaliza.instalacionY),
                                            nombre=baliza.macDispositivoBaliza,
                                            dist=CalcularDistancia(pulsera.txPower, dato.rssi_signal))
                                    )
                        else:
                            listadoBalizas.append(
                                BalizaInstalada(
                                    ubi=Ubicacion(
                                        x=datosInstalacionBaliza.instalacionX,
                                        y=datosInstalacionBaliza.instalacionY),
                                    nombre=baliza.macDispositivoBaliza,
                                    dist=CalcularDistancia(pulsera.txPower, dato.rssi_signal))
                            )

        if len(listadoBalizas) >= 3:
            CartesianoFinal, idsBalizasUsadas = CalcularPosicion(listadoBalizas)
            return CartesianoFinal, idsBalizasUsadas, pisoDeseado
    return None, None, None
