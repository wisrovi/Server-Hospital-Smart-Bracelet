from django.template.loader import render_to_string

import apps.Util_apps.Util as Utilities
from apps.Util_apps.Decoradores import execute_in_thread
from apps.Util_apps.Util import config_files
from apps.baliza.models import Baliza, RolUsuario, UsuarioRol, Bracelet, BraceletUmbrals, HistorialRSSI, \
    InstalacionBaliza, Area
from apps.baliza.views.server.Libraries.CalculoUbicacion.Library_BLE_location import CalcularPosicion, BalizaInstalada, \
    Ubicacion
from apps.baliza.views.server.Libraries.LibraryRSSItoMts import CalcularDistancia
from authentication.Config.Constants.Contant import rol_enviar_notificaiones_servidor, time_resend_mail, minimo_nivel_bateria





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
        print("***************************************************** email send *****************************************************")
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


def getUmbrales(macPulsera):
    pulsera = Bracelet.objects.get(macDispositivo=macPulsera)
    # print("pulsera: ", pulsera)
    umbrales = BraceletUmbrals.objects.get(bracelet=pulsera)
    return umbrales

# correo completo
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
    imagenes_en_html.append("LOGOFCV.png")
    imagenes_en_html.append("baliza.jpg")
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

# correo completo
@execute_in_thread(name="hilo ValidarExisteBracelet")
def ValidarExisteBracelet(bracelet, baliza, request):
    bracelet = ExtractMac(bracelet)

    braceletsExistentes = Bracelet.objects.all()
    for brac in braceletsExistentes:
        if bracelet == brac.macDispositivo:
            return True

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
    firmaResumenRemitente = "Hospital Smart Bracelet"

    listaDestinatarios = getDestinatariosCorreos()
    if len(listaDestinatarios) > 0:
        if not str(bracelet) in listadoMacsReportadas:
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaDestinatarios, request)
            print("Nuevo Bracelet encontrado")
            listadoMacsReportadas.append(str(bracelet))
    return False

# correo completo
@execute_in_thread(name="hilo ValidarCaida")
def ValidarCaida(baliza, macPulsera, caida, request):
    if caida:
        diccionarioDatos = dict()
        imagenes_en_html = list()

        PARAMETROS = config_files['alerta_caida']
        diccionarioDatos[PARAMETROS['Var'][0]] = str(ExtractMac(macPulsera))
        diccionarioDatos[PARAMETROS['Var'][1]] = str('<< Paciente >>')
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("caida.jpg")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        asunto = "Alerta, persona caida (" + ExtractMac(macPulsera) + ")"
        firmaResumenRemitente = "Hospital Smart Bracelet"

        listaCorreosDestinatarios = getDestinatariosCorreos()
        if len(listaCorreosDestinatarios) > 0:
            if se_debe_reportar(NAME_SENSOR_CAI, str(macPulsera)):
                Utilities.sendMail(asunto, html_message, imagenes_en_html,
                                   listaCorreosDestinatarios, request)

# correo completo
@execute_in_thread(name="hilo ValidadProximidad")
def ValidadProximidad(baliza, macPulsera, proximidad, request):
    if proximidad == False:
        diccionarioDatos = dict()
        imagenes_en_html = list()
        PARAMETROS = config_files['alerta_proximidad']
        diccionarioDatos[PARAMETROS['Var'][0]] = str(macPulsera)
        diccionarioDatos[PARAMETROS['Var'][1]] = str('<< Paciente >>')
        imagenes_en_html.append("LOGOFCV.png")
        imagenes_en_html.append("no_signal.png")

        html_message = render_to_string(PARAMETROS['File'],
                                        diccionarioDatos)
        html_message = PutImagesHtml(imagenes_en_html, html_message)

        asunto = "Alerta, persona se quitó el bracelet (" + macPulsera + ")"
        firmaResumenRemitente = "Hospital Smart Bracelet"

        listaCorreosDestinatarios = getDestinatariosCorreos()
        if len(listaCorreosDestinatarios) > 0:
            if se_debe_reportar(NAME_SENSOR_PRO, str(macPulsera)):
                Utilities.sendMail(asunto, html_message, imagenes_en_html,
                                   listaCorreosDestinatarios, request)

# correo completo
@execute_in_thread(name="hilo ValidarTemperatura")
def ValidarTemperatura(macPulsera, temperaturaActual, request):
    macPulsera = ExtractMac(macPulsera)
    umbrales = getUmbrales(macPulsera)

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
        if se_debe_reportar(NAME_SENSOR_TEMP, str(macPulsera)):
            Utilities.sendMail(asunto, html_message, imagenes_en_html,
                               listaCorreosDestinatarios, request)



@execute_in_thread(name="hilo ValidarNivelBateria")
def ValidarNivelBateria(nivelBateria, baliza, macPulsera, request):
    if nivelBateria < minimo_nivel_bateria:


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
            if se_debe_reportar(NAME_SENSOR_BAT, str(macPulsera)):
                Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                                   listaCorreosDestinatarios, request)
                print("Bracelet alerta bateria baja")


@execute_in_thread(name="hilo ValidarPPM")
def ValidarPPM(macPulsera, ppmActual, request):
    macPulsera = ExtractMac(macPulsera)
    umbrales = getUmbrales(macPulsera)

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
        print("alarma PPM ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if se_debe_reportar(NAME_SENSOR_PPM, str(macPulsera)):
            Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
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

    # Buscando coordenada actual
    CartesianoFinal, idsBalizasUsadas, pisoDeseado = DeterminarPocisionPulsera(pulsera)
    print(pulsera.macDispositivo, CartesianoFinal)
    if CartesianoFinal is not None:
        print(CartesianoFinal, idsBalizasUsadas, pisoDeseado)

        # print("Baliza:", baliza, ", Pulsera:", macPulsera, ", metros:", distancia)
        #aca se debe calcular la coordenada de la pulsera actual y buscar el area en la que está
        #si el area anterior es diferente al area actual se debe hacer un registro, de lo contrario no se registra y termina el proceso
        print("Falta poner esta pulsera en el historial de ubicacion para mostrar que esta dentro de un area especifico")
        areas = Area.objects.all()
        for area in areas:
            pis = area.piso
            print(pis, pisoDeseado)
            if pis == pisoDeseado:
                print("Esta en el mismo piso")
                xi = area.xInicial
                xf = area.xFinal
                yi = area.yInicial
                yf = area.yFinal


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

                        puntoInstalacion = (datosInstalacionBaliza.instalacionX, datosInstalacionBaliza.instalacionY)
                        print(pulsera.descripcion, "--->", puntoInstalacion, "--->",
                               CalcularDistancia(pulsera.txPower, dato.rssi_signal), "mt", pisoInstalacion)

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
        else:
            print(len(listadoBalizas))
    return None, None, None
