from django.template.loader import render_to_string

import apps.Util_apps.Util as Utilities
from apps.Util_apps.Decoradores import execute_in_thread
from apps.Util_apps.Util import config_files
from apps.baliza.models import Baliza, RolUsuario, UsuarioRol, Bracelet, BraceletUmbrals, HistorialRSSI, \
    InstalacionBaliza, Area, HistorialUbicacion
from apps.baliza.views.server.Libraries.CalculoUbicacion.Library_BLE_location import CalcularPosicion, BalizaInstalada, \
    Ubicacion
from apps.baliza.views.server.Libraries.LibraryRSSItoMts import CalcularDistancia
from authentication.Config.Constants.Contant import rol_enviar_notificaiones_servidor, time_resend_mail, \
    minimo_nivel_bateria

listadoMacsReportadas = list()

NAME_SENSOR_TEMP = 'TEMP'
NAME_SENSOR_PRO = 'PRO'
NAME_SENSOR_PPM = 'PPM'
NAME_SENSOR_CAI = 'CAI'
NAME_SENSOR_BAT = 'BAT'
AlertasSensoresDic = dict()


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


def se_debe_reportar(nameSensor, macBracelet):
    respuesta = False
    existe_mac = False
    existe_sensor = False
    for mac_in_history in AlertasSensoresDic:
        if mac_in_history == macBracelet:
            existe_mac = True
            datos_sensores = AlertasSensoresDic[mac_in_history]
            for sensor in datos_sensores:
                if nameSensor == sensor:
                    existe_sensor = True
                    horaUltimoRegistro = AlertasSensoresDic[mac_in_history][nameSensor]
                    diferencia = (Utilities.getFechaHora() - horaUltimoRegistro).seconds
                    if diferencia >= time_resend_mail:
                        respuesta = True
                        AlertasSensoresDic[mac_in_history][nameSensor] = Utilities.getFechaHora()
            if not existe_sensor:
                AlertasSensoresDic[mac_in_history][nameSensor] = Utilities.getFechaHora()
    if not existe_mac:
        newSensor = dict()
        newSensor[nameSensor] = Utilities.getFechaHora()
        AlertasSensoresDic[macBracelet] = newSensor
        respuesta = True

    if respuesta:
        # print("***************************************************** email send *****************************************************")
        print("Bracelet alerta ", nameSensor)
    return respuesta


def ModifyHtml(url_path, html):
    cid_search = url_path.split(".")[0]
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


def ExtractMac(string):
    macPulsera_complete = string[0:2] \
                          + ":" + string[2:4] \
                          + ":" + string[4:6] \
                          + ":" + string[6:8] \
                          + ":" + string[8:10] \
                          + ":" + string[10:12]
    return macPulsera_complete


# correo completo
@execute_in_thread(name="hilo ValidarExisteBaliza")
def NotifyBalizaNotExist(baliza, request, listaDestinatarios):
    if len(listaDestinatarios) > 0:
        PARAMETROS = config_files['nueva_baliza']
        diccionarioDatos = dict()
        diccionarioDatos[PARAMETROS['Var'][0]] = baliza
        imagenes_en_html = list()
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("baliza.jpg")
        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        asunto = "Nueva Baliza por registrar (" + baliza + ")"

        if not str(baliza) in listadoMacsReportadas:
            respond = Utilities.sendMail(asunto, html_message, imagenes_en_html, listaDestinatarios, request)
            if respond:
                print("Nueva Baliza encontrada: ", baliza)
                listadoMacsReportadas.append(baliza)


# correo completo
@execute_in_thread(name="hilo ValidarExisteBracelet")
def NotifyBraceletNotExist(bracelet, request, listaDestinatarios):
    if len(listaDestinatarios) > 0:
        PARAMETROS = config_files['nuevo_bracelet']

        diccionarioDatos = dict()
        diccionarioDatos[PARAMETROS['Var'][0]] = str(bracelet)

        imagenes_en_html = list()
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("manilla.jpg")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        asunto = "Nuevo Bracelet por registrar (" + bracelet + ")"

        if not str(bracelet) in listadoMacsReportadas:
            respond = Utilities.sendMail(asunto, html_message, imagenes_en_html, listaDestinatarios, request)
            if respond:
                print("Nuevo Bracelet encontrado: ", bracelet)
            listadoMacsReportadas.append(str(bracelet))


# correo completo
@execute_in_thread(name="hilo ValidarCaida")
def NotifyPersonFallen(macPulsera, request, listaCorreosDestinatarios, paciente):
    if len(listaCorreosDestinatarios) > 0:
        diccionarioDatos = dict()
        imagenes_en_html = list()

        PARAMETROS = config_files['alerta_caida']
        diccionarioDatos[PARAMETROS['Var'][0]] = macPulsera
        diccionarioDatos[PARAMETROS['Var'][1]] = paciente
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("caida.jpg")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        asunto = "Alerta, persona caida (" + macPulsera + ")"

        if se_debe_reportar(NAME_SENSOR_CAI, macPulsera):
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaCorreosDestinatarios, request)


# correo completo
@execute_in_thread(name="hilo ValidadProximidad")
def NotifyPersonRemovedBracelet(macPulsera, request, listaCorreosDestinatarios, paciente):
    if len(listaCorreosDestinatarios) > 0:
        diccionarioDatos = dict()
        imagenes_en_html = list()
        PARAMETROS = config_files['alerta_proximidad']
        diccionarioDatos[PARAMETROS['Var'][0]] = str(macPulsera)
        diccionarioDatos[PARAMETROS['Var'][1]] = paciente
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("no_signal.png")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        asunto = "Alerta, persona se quitó el bracelet (" + macPulsera + ")"

        if se_debe_reportar(NAME_SENSOR_PRO, str(macPulsera)):
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaCorreosDestinatarios, request)


# correo completo
@execute_in_thread(name="hilo ValidarTemperatura")
def NotifyTemperatureAlert(macPulsera, temperaturaActual, request, umbrales, listaCorreosDestinatarios):
    if len(listaCorreosDestinatarios) > 0:
        diccionarioDatos = dict()
        imagenes_en_html = list()
        PARAMETROS = config_files['alerta_temperatura']
        diccionarioDatos[PARAMETROS['Var'][0]] = str(macPulsera)
        diccionarioDatos[PARAMETROS['Var'][1]] = str('<< Paciente >>')
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("iconoCaution.jpg")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        temperaturaActual = temperaturaActual / 10

        if temperaturaActual >= umbrales.maximaTemperatura:
            asunto = "Alerta, persona (" + macPulsera + ")" + " tiene fiebre (" + str(temperaturaActual) + ")"
        else:
            asunto = "Alerta, persona (" + macPulsera + ")" + " tiene hipotermia (" + str(temperaturaActual) + ")"

        if se_debe_reportar(NAME_SENSOR_TEMP, str(macPulsera)):
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaCorreosDestinatarios, request)


@execute_in_thread(name="hilo ValidarNivelBateria")
def NotifyBateryLevelLow(baliza, macPulsera, request, listaCorreosDestinatarios):
    if len(listaCorreosDestinatarios) > 0:
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

        if se_debe_reportar(NAME_SENSOR_BAT, str(macPulsera)):
            Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                               listaCorreosDestinatarios, request)
            print("Bracelet alerta bateria baja")


@execute_in_thread(name="hilo ValidarPPM")
def NotifyPpmAlert(macPulsera, ppmActual, request, umbrales, listaCorreosDestinatarios):
    if len(listaCorreosDestinatarios) > 0:
        diccionarioDatos = dict()
        imagenes_en_html = list()
        PARAMETROS = config_files['alerta_ppm']
        diccionarioDatos[PARAMETROS['Var'][0]] = str(macPulsera)
        diccionarioDatos[PARAMETROS['Var'][1]] = str('<< Paciente >>')
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("ppm.jpg")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        if ppmActual > umbrales.maximaPulsoCardiaco:
            asunto = "Alerta, persona (" + macPulsera + ")" + " tiene PPM alta (" + str(ppmActual) + ")"
        else:
            asunto = "Alerta, persona (" + macPulsera + ")" + " tiene PPM baja (" + str(ppmActual) + ")"

        if se_debe_reportar(NAME_SENSOR_PPM, str(macPulsera)):
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaCorreosDestinatarios, request)


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



def ActualizarAreaPosicion(macPulsera):
    CartesianoFinal, idsBalizasUsadas, pisoDeseado = DeterminarPocisionPulsera(macPulsera)

    if pisoDeseado is not None:
        todas_areas_este_piso = Area.objects.filter(piso=pisoDeseado)
        historial_esta_pulsera = HistorialUbicacion.objects.filter(bracelet=macPulsera).order_by(
            '-fechaIngresoArea')

        # print(CartesianoFinal, todas_areas_este_piso)
        for are in todas_areas_este_piso:
            xi = float(are.xInicial)
            xf = float(are.xFinal)
            yi = float(are.yInicial)
            yf = float(are.yFinal)
            if xi < CartesianoFinal[0] < xf and yi < CartesianoFinal[1] < yf:
                if len(historial_esta_pulsera) == 0:
                    histo = HistorialUbicacion()
                    histo.area = are
                    histo.bracelet = macPulsera
                    histo.save()
                else:
                    for register in historial_esta_pulsera:
                        if register.fechaSalidaArea is None:
                            if register.area != are:
                                register.fechaSalidaArea = Utilities.getFechaHora()
                                register.save()
                                # print("la persona cambio de area")
                                histo = HistorialUbicacion()
                                histo.area = are
                                histo.bracelet = macPulsera
                                histo.save()
                                # print("Creando nuevo registro")
                            else:
                                pass
                                # print("la persona sigue en el area", are.area)


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

    ActualizarAreaPosicion(pulsera)


# @count_elapsed_time
def DeterminarPocisionPulsera(pulsera, pisoDeseado=None):
    ConstanteSegundosMaximosSeparacionRegistros = 15

    listadoBalizas = list()

    lastDate = None
    datosEstaPulsera = HistorialRSSI.objects.filter(bracelet=pulsera).order_by('-fechaRegistro')
    macBalizasProcesadas = list()
    piso_detectado = None
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

                        puntoInstalacion = (datosInstalacionBaliza.instalacionX, datosInstalacionBaliza.instalacionY)
                        # print(pulsera.descripcion, "--->", puntoInstalacion, "--->",
                        #        CalcularDistancia(pulsera.txPower, dato.rssi_signal), "mt", pisoInstalacion)

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
                            if piso_detectado is None or piso_detectado == pisoInstalacion:
                                piso_detectado = pisoInstalacion
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
            if pisoDeseado is None:
                pisoDeseado = piso_detectado
            return CartesianoFinal, idsBalizasUsadas, pisoDeseado
        else:
            # print(len(listadoBalizas))
            pass
    return None, None, None
