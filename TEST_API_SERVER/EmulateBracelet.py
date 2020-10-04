import json
import random
import base64

###############################


from apps.Util_apps.Decoradores import execute_in_thread


def getLocalIp():
    import socket
    nombre_equipo = socket.gethostname()
    direccion_equipo = socket.gethostbyname(nombre_equipo)
    return direccion_equipo


# @execute_in_thread(name="hilo emulador baliza")
def EnviarDatosURL(paqueteEnviar, SERVER_USE="ME", port=8000):
    servidores = dict()
    servidores['OFFICE'] = ("172.16.66.84", 8000)
    servidores['PAUL'] = ("172.30.19.88", 5000)
    servidores['ME'] = (getLocalIp(), port)

    ip = servidores[SERVER_USE][0]
    port = servidores[SERVER_USE][1]
    URL = "http://{}:{}/hospitalsmartbracelet/received/".format(ip, port)

    PARAMS = {
        "key": "ESP32",
        "string_pack": paqueteEnviar
    }

    import requests
    try:
        r = requests.post(url=URL, data={"{}".format(PARAMS): 0})
        if r.status_code == 200:
            print("[TEST_API]: Paquete enviado correctamente")
            # print(r.text)
        else:
            print("Failed")
    except Exception as e:
        print(str(e))


###############################


def GenerateNumber(min=0, max=100, isFloat=True):
    if isFloat:
        number = float("{0:.1f}".format(random.uniform(min, max)))
    else:
        number = random.randint(min, max)
    return number


def GenerateBool(minimaTendenciaTrue=3):
    number = GenerateNumber()
    if number > minimaTendenciaTrue:
        return True
    else:
        return False


###############################


def GenerateTemperature():
    alerta = GenerateBool(85)
    if alerta:
        superior = GenerateBool(50)
        if superior:
            return GenerateNumber(min=38, max=42)
        else:
            return GenerateNumber(min=20, max=25)
    else:
        return GenerateNumber(min=26, max=37)


def GeneratePPM():
    alerta = GenerateBool(85)
    if alerta:
        superior = GenerateBool(50)
        if superior:
            return GenerateNumber(min=130, max=155, isFloat=False)
        else:
            return GenerateNumber(min=40, max=54, isFloat=False)
    else:
        return GenerateNumber(min=55, max=129, isFloat=False)


def GenerateBatery():
    alerta = GenerateBool(90)
    if alerta:
        superior = GenerateBool(50)
        if superior:
            return GenerateNumber(min=41, max=42, isFloat=False)
        else:
            return GenerateNumber(min=25, max=29, isFloat=False)
    else:
        return GenerateNumber(min=30, max=40, isFloat=False)


###############################


def CreateBeacon(sed=None, mac=None, bat=None, ppm=None, cai=False, tem=None, rsi=None, pro=True):
    beacon = dict()
    beacon['SED'] = sed
    beacon['MAC'] = mac
    beacon['BAT'] = str(bat)
    beacon['PPM'] = str(ppm)
    beacon['CAI'] = str(int(cai))
    beacon['TEM'] = str(tem)
    beacon['RSI'] = str(rsi)
    beacon['PRO'] = str(int(pro))
    return beacon


def CreateScan(beacons: list, balizas: list, codificar: bool = False):
    escaneo = dict()
    escaneo['beacons'] = beacons
    escaneo['baliza'] = balizas

    escaneo_json = json.dumps(escaneo)

    if codificar:
        escaneo_json = str(base64.urlsafe_b64encode(escaneo_json.encode("utf-8")), "utf-8")
    return escaneo_json


def CreateRandomBeacon(mac: str, rssi: int):
    beacon = CreateBeacon(sed="0000",
                          mac=mac,
                          bat=GenerateBatery(),  # 90% de probabilidad de que haya ppm sin alerta y 10% de alerta
                          ppm=GeneratePPM(),  # 85% de probabilidad de que haya ppm sin alerta y 15% de alerta
                          cai=GenerateBool(90),  # 10% se haber una alerta de caida y 90% de que no haya caida
                          tem=GenerateTemperature(),
                          # 85% de probabilidad de que haya temperatura sin alerta y 15% de alerta
                          rsi=rssi,
                          pro=GenerateBool(30))  # 70% de que haya proximidad y 30% de que no haya proximidad
    return beacon


###############################


beacons = list()
beacons.append(CreateRandomBeacon(mac="B07E11FE91F4", rssi=70))

balizas = list()
balizas.append("4C11AE754045")

escaneo_json = CreateScan(beacons, balizas, codificar=True)

###############################


print(escaneo_json)

datos_balizas = list()
datos_balizas.append(escaneo_json)

numero_envios = 1  # 1000

import time

for _ in range(numero_envios):
    for dato in datos_balizas:
        EnviarDatosURL(dato, port=5000, SERVER_USE='PAUL')
        time.sleep(0.05)
    print("**************************************")
