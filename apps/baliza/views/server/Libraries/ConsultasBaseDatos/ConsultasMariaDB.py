from apps.baliza.views.server.Libraries.ConsultasBaseDatos.DriverMariaDB import MariaDB
from authentication.Config.DB import MARIADB
from apps.baliza.views.server.Libraries.ConsultasBaseDatos.ComandosMySQL import *

conection = None


def LeerCredenciales():
    CREDENCIALES = MARIADB['default']
    DB = CREDENCIALES['NAME']
    USER = CREDENCIALES['USER']
    PWD = CREDENCIALES['PASSWORD']
    HOST = CREDENCIALES['HOST']
    PORT = CREDENCIALES['PORT']
    return HOST, USER, PWD, DB


def ConsultarMariaDB(comando):
    global conection
    try:
        ALL_RESPONSE = conection.EjecutarConsulta(comando)
        return ALL_RESPONSE
    except:
        print("********************** ABRIENDO CONEXION ************************************")
        HOST, USER, PWD, DB = LeerCredenciales()
        conection = MariaDB(HOST, USER, PWD, DB)
        ALL_RESPONSE = conection.EjecutarConsulta(comando)
        return ALL_RESPONSE

def CerrarConexionDB():
    global conection
    if conection is not None:
        conection.CloseConection()
        print("Cerrando conexion")

def InsertarMariaDB(comando: str):
    global conection
    try:
        ALL_RESPONSE = conection.Insertar(comando)
        return ALL_RESPONSE
    except:
        print("********************** ABRIENDO CONEXION ************************************")
        HOST, USER, PWD, DB = LeerCredenciales()
        conection = MariaDB(HOST, USER, PWD, DB)
        ALL_RESPONSE = conection.Insertar(comando)
        return ALL_RESPONSE


## READ


def ReadIsInArea(idBracelet:int):
    class IsInArea:
        id = int()
        id_bracelet = int()
        id_area = int()
        fechaSalida = str()

    comando = COMANDO_ReadIsInArea
    comando = comando.replace("@idBracelet", str(idBracelet))
    ALL_RESPONSE = ConsultarMariaDB(comando)

    response = list()
    for i in ALL_RESPONSE:
        area = IsInArea()
        area.id = i[0]
        area.id_bracelet = i[1]
        area.id_area = i[2]
        area.fechaSalida = i[3]
        response.append(area.__dict__)

    return response


def ReadAreasPorPiso(idPiso:int):
    class AreaPorPiso:
        id = int()
        area = str()
        xInicial = int()
        xFinal = int()
        yInicial = int()
        yFinal = int()

    comando = COMANDO_ReadAreasPorPiso
    comando = comando.replace("@idPiso", str(idPiso))
    ALL_RESPONSE = ConsultarMariaDB(comando)

    response = list()
    for i in ALL_RESPONSE:
        area = AreaPorPiso()
        area.id = i[0]
        area.area = i[1]
        area.xInicial = i[2]
        area.xFinal = i[3]
        area.yInicial = i[4]
        area.yFinal = i[5]
        response.append(area.__dict__)

    return response



def ReadLastRegisterByCalculateUbication(idBracelet: int):
    import datetime

    class Filter_DB_1:
        id_bracelet = int()
        id_baliza = int()
        rssi = int()
        fecha_registro = datetime.datetime.now()
        txPower = int()
        macBaliza = str()
        id_sede = int()
        id_piso = int()
        x_install = int()
        y_install = int()

    comando = COMANDO_ReadLastRegisterByCalculateUbication
    comando = comando.replace("@idbracelet", str(idBracelet))
    ALL_RESPONSE = ConsultarMariaDB(comando)

    response = list()
    for i in ALL_RESPONSE:
        try:
            data_db = Filter_DB_1()
            data_db.id_bracelet = i[0]
            data_db.id_baliza = i[1]
            data_db.rssi = i[2]
            data_db.fecha_registro = i[3]
            data_db.txPower = i[4]
            data_db.macBaliza = i[5]
            data_db.id_sede = i[6]
            data_db.id_piso = i[7]
            data_db.x_install = i[8]
            data_db.y_install = i[9]
            response.append(data_db.__dict__)
        except:
            print("[ReadLastRegisterByCalculateUbication] ERROR:", i)

    return response


def ReadEmailsAlertas():
    ALL_RESPONSE = ConsultarMariaDB(COMANDO_EmailsDestinatariosAlertas)
    response = list()
    for i in ALL_RESPONSE:
        response.append(i[0])
    return response


def ReadDataBalizaByMac(macBaliza):
    class DataBaliza:
        id = int()
        descripcion = str()
        mac = str()
        indHabilitado = bool()

    comando = COMANDO_ReadDataBalizaByMac.replace('@mac', macBaliza)
    ALL_RESPONSE = ConsultarMariaDB(comando)

    response = list()
    for i in ALL_RESPONSE:
        data_db = DataBaliza()
        data_db.id = i[0]
        data_db.descripcion = i[1]
        data_db.mac = i[2]
        data_db.indHabilitado = i[3]
        response.append(data_db.__dict__)

    return response


def ReadDataBraceletByMac(macBracelet):
    class DataBracelet:
        id = int()
        mac = str()
        major = int()
        minor = int()
        txPower = int()
        descripcion = str()
        indHabilitado = bool()
        tempMin = int()
        tempMax = int()
        PpmMin = int()
        PpmMax = int()
        idDatosPaciente = str()

    comando = COMANDO_ReadDataBraceletByMac.replace('@mac', macBracelet)
    ALL_RESPONSE = ConsultarMariaDB(comando)

    response = list()
    for i in ALL_RESPONSE:
        data_db = DataBracelet()
        data_db.id = i[0]
        data_db.mac = i[1]
        data_db.major = i[2]
        data_db.minor = i[3]
        data_db.txPower = i[4]
        data_db.descripcion = i[5]
        data_db.indHabilitado = i[6]
        data_db.tempMin = i[7]
        data_db.tempMax = i[8]
        data_db.PpmMin = i[9]
        data_db.PpmMax = i[10]
        data_db.idDatosPaciente = i[11]
        response.append(data_db.__dict__)

    return response


def ReadLastRegisterSensors(idBracelet: int):
    class LastRegisterSensors:
        ppm_sensor = str()
        caida_sensor = bool()
        proximidad_sensor = bool()
        tempertura_sensor = int()
        nivel_bateria = int()

    comando = COMANDO_ReadLastRegisterSensors.replace('@idBracelet', str(idBracelet))
    ALL_RESPONSE = ConsultarMariaDB(comando)

    response = list()
    for i in ALL_RESPONSE:
        data_db = LastRegisterSensors()
        data_db.ppm_sensor = i[0]
        data_db.caida_sensor = i[1]
        data_db.proximidad_sensor = i[2]
        data_db.tempertura_sensor = i[3]
        data_db.nivel_bateria = i[4]
        response.append(data_db.__dict__)

    return response


## INSERT

def InsertarNuevoDatoHistorialSensores(idBracelet: int, idBaliza: int, caida: bool, bateria: int, proximidad: bool,
                                       temperatura: int, ppm: int):
    comando = COMANDO_InsertarNuevoDatoHistorialSensores
    comando = comando.replace("@idBracelet", str(idBracelet))
    comando = comando.replace("@idBaliza", str(idBaliza))
    comando = comando.replace("@caida", str(caida))
    comando = comando.replace("@bateria", str(bateria))
    comando = comando.replace("@proximidad", str(proximidad))
    comando = comando.replace("@temperatura", str(temperatura))
    comando = comando.replace("@ppm", str(ppm))

    ALL_RESPONSE = InsertarMariaDB(comando)
    return ALL_RESPONSE


def InsertarNuevoRegistroSRRI(rssi:int, idBaliza:int, idBracelet:int):
    comando = COMANDO_InsertarNuevoRegistroSRRI
    comando = comando.replace("@idBracelet", str(idBracelet))
    comando = comando.replace("@idBaliza", str(idBaliza))
    comando = comando.replace("@rssi", str(rssi))

    ALL_RESPONSE = InsertarMariaDB(comando)
    return ALL_RESPONSE

def InsertarNuevoRegistroHistorialUbicacion(idArea:int, idBracelet:int):
    comando = COMANDO_InsertarNuevoRegistroHistorialUbicacion
    comando = comando.replace("@idArea", str(idArea))
    comando = comando.replace("@idBracelet", str(idBracelet))

    print(comando)
    ALL_RESPONSE = InsertarMariaDB(comando)
    return ALL_RESPONSE


## UPDATE


def UpdateDateOutArea(idRegistro:int):
    comando = COMANDO_UpdateDateOutArea
    comando = comando.replace("@idRegistro", str(idRegistro))

    ALL_RESPONSE = InsertarMariaDB(comando)
    return ALL_RESPONSE