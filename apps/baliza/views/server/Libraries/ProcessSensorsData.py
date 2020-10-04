from django.template.loader import render_to_string

import apps.Util_apps.Util as Utilities
from apps.Util_apps.Decoradores import execute_in_thread
from apps.Util_apps.Util import config_files
from apps.baliza.models import Baliza, RolUsuario, UsuarioRol, Bracelet, BraceletUmbrals, HistorialRSSI, \
    InstalacionBaliza, Area, HistorialUbicacion
from apps.baliza.views.server.Libraries.CalculoUbicacion.Library_BLE_location import CalcularPosicion, BalizaInstalada, \
    Ubicacion
from apps.baliza.views.server.Libraries.ConsultasBaseDatos.ConsultasMariaDB import *
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
    # rolBuscar = rol_enviar_notificaiones_servidor
    listaCorreosDestinatarios = ReadEmailsAlertas()
    # listaCorreosDestinatarios = list()
    # for rol in RolUsuario.objects.all():
    #     # print(rol.rolUsuario, rolBuscar, )
    #     # print(type(rol.rolUsuario), type(rolBuscar))
    #     if rol.rolUsuario == rolBuscar:
    #         for usuarioRevisar in UsuarioRol.objects.all():
    #             if usuarioRevisar.rolUsuario == rol:
    #                 listaCorreosDestinatarios.append(usuarioRevisar.usuario.email)
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
    if len(listaDestinatarios) > 0 and (not str(baliza) in listadoMacsReportadas):
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

        respond = Utilities.sendMail(asunto, html_message, imagenes_en_html, listaDestinatarios, request)
        if respond:
            print("Nueva Baliza encontrada: ", baliza)
            listadoMacsReportadas.append(baliza)


# correo completo
@execute_in_thread(name="hilo ValidarExisteBracelet")
def NotifyBraceletNotExist(bracelet, request, listaDestinatarios):
    if len(listaDestinatarios) > 0 and (not str(bracelet) in listadoMacsReportadas):
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

        respond = Utilities.sendMail(asunto, html_message, imagenes_en_html, listaDestinatarios, request)
        if respond:
            print("Nuevo Bracelet encontrado: ", bracelet)
        listadoMacsReportadas.append(str(bracelet))


# correo completo
@execute_in_thread(name="hilo ValidarCaida")
def NotifyPersonFallen(macPulsera, request, listaCorreosDestinatarios, paciente):
    if len(listaCorreosDestinatarios) > 0 and se_debe_reportar(NAME_SENSOR_CAI, macPulsera):
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

        Utilities.sendMail(asunto, html_message, imagenes_en_html,
                           listaCorreosDestinatarios, request)


# correo completo
@execute_in_thread(name="hilo ValidadProximidad")
def NotifyPersonRemovedBracelet(macPulsera, request, listaCorreosDestinatarios, paciente):
    if len(listaCorreosDestinatarios) > 0 and se_debe_reportar(NAME_SENSOR_PRO, str(macPulsera)):
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

        Utilities.sendMail(asunto, html_message, imagenes_en_html,
                           listaCorreosDestinatarios, request)


# correo completo
@execute_in_thread(name="hilo ValidarTemperatura")
def NotifyTemperatureAlert(macPulsera, temperaturaActual, request, umbrales, listaCorreosDestinatarios):
    if len(listaCorreosDestinatarios) > 0 and se_debe_reportar(NAME_SENSOR_TEMP, str(macPulsera)):
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

        Utilities.sendMail(asunto, html_message, imagenes_en_html,
                           listaCorreosDestinatarios, request)


@execute_in_thread(name="hilo ValidarNivelBateria")
def NotifyBateryLevelLow(baliza, macPulsera, request, listaCorreosDestinatarios):
    if len(listaCorreosDestinatarios) > 0 and se_debe_reportar(NAME_SENSOR_BAT, str(macPulsera)):
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

        Utilities.sendMail(asunto, html_message, firmaResumenRemitente,
                           listaCorreosDestinatarios, request)
        print("Bracelet alerta bateria baja")


@execute_in_thread(name="hilo ValidarPPM")
def NotifyPpmAlert(macPulsera, ppmActual, request, umbrales, listaCorreosDestinatarios):
    if len(listaCorreosDestinatarios) > 0 and se_debe_reportar(NAME_SENSOR_PPM, str(macPulsera)):
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


def ActualizarAreaPosicion(pulsera):
    CartesianoFinal, idsBalizasUsadas, pisoDeseado = DeterminarPocisionPulsera(pulsera['id'])
    if CartesianoFinal is not None:
        # print("ubicacion: ", CartesianoFinal, pisoDeseado, idsBalizasUsadas)

        todas_areas_este_piso = ReadAreasPorPiso(pisoDeseado)
        # print("areas: ", todas_areas_este_piso)

        for reg in todas_areas_este_piso:
            xi = float(reg['xInicial'])
            xf = float(reg['xFinal'])
            yi = float(reg['yInicial'])
            yf = float(reg['yFinal'])

            xc = CartesianoFinal[0]
            yc = CartesianoFinal[1]

            if xi < xc < xf and yi < yc < yf:
                actual_area = ReadIsInArea(pulsera['id'])
                if len(actual_area) > 0:
                    actual_area = actual_area[0]
                    # print(actual_area)
                    if actual_area['fechaSalida'] == None:
                        if reg['id'] == actual_area['id_area']:
                            # print("Sigo en la misma area: ", actual_area['id_area'])
                            pass
                        else:
                            # print("He salido del area {} y entrado al area {}".format(str(actual_area['id_area']),                                                                                      str(reg['id'])))
                            UpdateDateOutArea(actual_area['id'])
                            InsertarNuevoRegistroHistorialUbicacion(reg['id'], pulsera['id'])
                else:
                    InsertarNuevoRegistroHistorialUbicacion(reg['id'], pulsera['id'])
                break

    # if pisoDeseado is not None and False:
    #     todas_areas_este_piso = Area.objects.filter(piso=pisoDeseado)
    #     historial_esta_pulsera = HistorialUbicacion.objects.filter(bracelet=pulsera).order_by(
    #         '-fechaIngresoArea')
    #
    #     # print(CartesianoFinal, todas_areas_este_piso)
    #     for are in todas_areas_este_piso:
    #         xi = float(are.xInicial)
    #         xf = float(are.xFinal)
    #         yi = float(are.yInicial)
    #         yf = float(are.yFinal)
    #
    #         xc = CartesianoFinal[0]
    #         yc = CartesianoFinal[1]
    #         if xi < xc < xf and yi < yc < yf:
    #             if len(historial_esta_pulsera) == 0:
    #                 histo = HistorialUbicacion()
    #                 histo.area = are
    #                 histo.bracelet = pulsera
    #                 histo.save()
    #             else:
    #                 for register in historial_esta_pulsera:
    #                     if register.fechaSalidaArea is None:
    #                         if register.area != are:
    #                             register.fechaSalidaArea = Utilities.getFechaHora()
    #                             register.save()
    #                             # print("la persona cambio de area")
    #                             histo = HistorialUbicacion()
    #                             histo.area = are
    #                             histo.bracelet = pulsera
    #                             histo.save()
    #                             # print("Creando nuevo registro")
    #                         else:
    #                             pass
    #                             # print("la persona sigue en el area", are.area)


# @execute_in_thread(name="hilo ProcesarUbicacion")
def ProcesarUbicacion(balizaNow, pulsera, rssi):
    ultimoRegistro = ReadLastRegisterByCalculateUbication(pulsera['id'])   # HistorialRSSI.objects.order_by('-fechaRegistro').filter(bracelet=pulsera, baliza=balizaNow).first()
    # print("rssi", ultimoRegistro)
    if len(ultimoRegistro) > 0:
        ultimoRegistro = ultimoRegistro[0]
        if ultimoRegistro['id_bracelet'] == pulsera['id'] and ultimoRegistro['id_baliza'] == balizaNow['id'] and ultimoRegistro['rssi'] == rssi:
            debe_insertar_nuevo_registro = False
        else:
            debe_insertar_nuevo_registro = True
    else:
        debe_insertar_nuevo_registro = True

    if debe_insertar_nuevo_registro:
        InsertarNuevoRegistroSRRI(rssi=rssi, idBaliza=balizaNow['id'], idBracelet=pulsera['id'])
        # histoRssi = HistorialRSSI()
        # histoRssi.baliza = balizaNow
        # histoRssi.bracelet = pulsera
        # histoRssi.rssi_signal = rssi
        # histoRssi.save()

    ActualizarAreaPosicion(pulsera)
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++")


# @count_elapsed_time
def DeterminarPocisionPulsera(idPulsera:int, pisoDeseado=None):
    ultimosRegistrosParaUbicacion = ReadLastRegisterByCalculateUbication(idPulsera)

    RegistrosValidosParaProcesarUbicacion = list()
    if len(ultimosRegistrosParaUbicacion) > 0:
        for reg in ultimosRegistrosParaUbicacion:
            if pisoDeseado is not None:
                if pisoDeseado == reg['id_piso']:
                    RegistrosValidosParaProcesarUbicacion.append(reg)
            else:
                pisoDeseado = reg['id_piso']
                RegistrosValidosParaProcesarUbicacion.append(reg)

    # print("calcularUbicacion: ", len(RegistrosValidosParaProcesarUbicacion), RegistrosValidosParaProcesarUbicacion)
    listadoBalizas = list()
    if len(RegistrosValidosParaProcesarUbicacion) == 3:
        for reg in RegistrosValidosParaProcesarUbicacion:
            listadoBalizas.append(
                BalizaInstalada(
                    ubi=Ubicacion(
                        x=reg['x_install'],
                        y=reg['y_install']),
                    nombre=reg['macBaliza'],
                    dist=CalcularDistancia(reg['txPower'], reg['rssi']))
            )

        CartesianoFinal, idsBalizasUsadas = CalcularPosicion(listadoBalizas)
        idsBalizasUsadas[0] = RegistrosValidosParaProcesarUbicacion[idsBalizasUsadas[0]]
        idsBalizasUsadas[1] = RegistrosValidosParaProcesarUbicacion[idsBalizasUsadas[1]]
        idsBalizasUsadas[2] = RegistrosValidosParaProcesarUbicacion[idsBalizasUsadas[2]]
        return CartesianoFinal, idsBalizasUsadas, pisoDeseado

    if False:
        print("Hallando ubicación Baliza")
        ConstanteSegundosMaximosSeparacionRegistros = 15



        lastDate = None
        datosEstaPulsera = HistorialRSSI.objects.order_by('-fechaRegistro').filter(bracelet=pulsera)

        UltimosDatosRegistradosPorCadaBaliza = list()
        macBalizasProcesadas = list()
        for dato in datosEstaPulsera:
            thisBaliza = dato.baliza
            macBaliza = thisBaliza.macDispositivoBaliza
            if not macBaliza in macBalizasProcesadas:
                macBalizasProcesadas.append(macBaliza)
                datosInstalacionBaliza = InstalacionBaliza.objects.get(baliza=thisBaliza)

                datosProcesar = dict()
                datosProcesar['BALIZA'] = thisBaliza
                datosProcesar['INSTALATION'] = datosInstalacionBaliza
                datosProcesar['DATE'] = dato.fechaRegistro
                datosProcesar['RSSI'] = dato.rssi_signal

                UltimosDatosRegistradosPorCadaBaliza.append(datosProcesar)

        if len(UltimosDatosRegistradosPorCadaBaliza) > 0:
            if len(UltimosDatosRegistradosPorCadaBaliza) >= 3:
                # print("Balizas a usar, pero primero validar que tengan la separación en tiempo minima requerida")
                # la primera fecha determina el ultimo registro, los demas no deben estar
                primera_fecha = None
                RegistrosValidosParaProcesarUbicacion = list()
                for registro in UltimosDatosRegistradosPorCadaBaliza:
                    baliza_registrada = registro['BALIZA']
                    fecha = registro['DATE']
                    instalacion = registro['INSTALATION']
                    rssi = registro['RSSI']

                    datosProcesar = dict()
                    datosProcesar['BALIZA'] = baliza_registrada
                    datosProcesar['INSTALATION'] = instalacion
                    datosProcesar['DATE'] = fecha
                    datosProcesar['RSSI'] = rssi

                    if primera_fecha is None:
                        primera_fecha = fecha
                        RegistrosValidosParaProcesarUbicacion.append(datosProcesar)
                    else:
                        diferencia = primera_fecha - fecha
                        if diferencia.seconds <= ConstanteSegundosMaximosSeparacionRegistros:
                            RegistrosValidosParaProcesarUbicacion.append(datosProcesar)
                if len(RegistrosValidosParaProcesarUbicacion) >= 3:
                    for registro in RegistrosValidosParaProcesarUbicacion:
                        baliza_registrada = registro['BALIZA']
                        instalacion = registro['INSTALATION']
                        rssi = registro['RSSI']

                        if pisoDeseado is None:
                            guardar = True
                            pisoDeseado = instalacion.piso
                        else:
                            if pisoDeseado == instalacion.piso:
                                guardar = True
                            else:
                                guardar = False

                        if guardar:
                            listadoBalizas.append(
                                BalizaInstalada(
                                    ubi=Ubicacion(
                                        x=instalacion.instalacionX,
                                        y=instalacion.instalacionY),
                                    nombre=baliza_registrada.macDispositivoBaliza,
                                    dist=CalcularDistancia(pulsera.txPower, rssi))
                            )
                    if len(listadoBalizas) >= 3:
                        print("hallando posición")
                        # print(listadoBalizas)

                        CartesianoFinal, idsBalizasUsadas = CalcularPosicion(listadoBalizas)
                        return CartesianoFinal, idsBalizasUsadas, pisoDeseado
                    else:
                        print("Hay datos de balizas que registran ver la pulsera, pero estas no corresponden al mismo piso, esto es un caso exepcional")
                else:
                    print("No hay suficientes registros validos para procesar ubicacion")
            else:
                print("No hay suficientes ubicaciones para hallar la posición de la pulsera")
            print()
        # print(UltimosDatosRegistradosPorCadaBaliza)


        #
        # piso_detectado = None
        # if len(datosEstaPulsera) > 0:
        #     for dato in datosEstaPulsera:
        #         if lastDate is None:
        #             lastDate = dato.fechaRegistro
        #         else:
        #             diferencia = lastDate - dato.fechaRegistro
        #             diferencia = diferencia.seconds
        #             if diferencia < ConstanteSegundosMaximosSeparacionRegistros:
        #                 baliza = dato.baliza
        #                 if not baliza.macDispositivoBaliza in macBalizasProcesadas:
        #                     macBalizasProcesadas.append(baliza.macDispositivoBaliza)
        #
        #                     try:
        #                         datosInstalacionBaliza = InstalacionBaliza.objects.get(baliza=baliza)
        #                     except ValueError:
        #                         print(ValueError)
        #                         return None, None, None
        #
        #                     pisoInstalacion = datosInstalacionBaliza.piso
        #
        #                     puntoInstalacion = (datosInstalacionBaliza.instalacionX, datosInstalacionBaliza.instalacionY)
        #                     # print(pulsera.descripcion, "--->", puntoInstalacion, "--->",
        #                     #        CalcularDistancia(pulsera.txPower, dato.rssi_signal), "mt", pisoInstalacion)
        #
        #                     if pisoDeseado is not None:
        #                         puntoInstalacionBaliza = InstalacionBaliza.objects.filter(baliza=baliza)
        #                         for puntito in puntoInstalacionBaliza:
        #                             pisitoPuntito = puntito.piso
        #                             puntitoDeseado = pisoDeseado[0]
        #                             if pisitoPuntito == puntitoDeseado:
        #                                 listadoBalizas.append(
        #                                     BalizaInstalada(
        #                                         ubi=Ubicacion(
        #                                             x=datosInstalacionBaliza.instalacionX,
        #                                             y=datosInstalacionBaliza.instalacionY),
        #                                         nombre=baliza.macDispositivoBaliza,
        #                                         dist=CalcularDistancia(pulsera.txPower, dato.rssi_signal))
        #                                 )
        #                     else:
        #                         if piso_detectado is None or piso_detectado == pisoInstalacion:
        #                             piso_detectado = pisoInstalacion
        #                             listadoBalizas.append(
        #                                 BalizaInstalada(
        #                                     ubi=Ubicacion(
        #                                         x=datosInstalacionBaliza.instalacionX,
        #                                         y=datosInstalacionBaliza.instalacionY),
        #                                     nombre=baliza.macDispositivoBaliza,
        #                                     dist=CalcularDistancia(pulsera.txPower, dato.rssi_signal))
        #                             )
        #
        #     if len(listadoBalizas) >= 3:
        #         CartesianoFinal, idsBalizasUsadas = CalcularPosicion(listadoBalizas)
        #         if pisoDeseado is None:
        #             pisoDeseado = piso_detectado
        #         return CartesianoFinal, idsBalizasUsadas, pisoDeseado
        #     else:
        #         # print(len(listadoBalizas))
        #         pass
    return None, None, None
