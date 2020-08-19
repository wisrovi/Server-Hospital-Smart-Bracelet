pulsera1 = dict()
pulsera2 = dict()
pulsera3 = dict()

URL = str()


def SetPulseras(p1, p2, p3):
    global pulsera1, pulsera2, pulsera3
    pulsera1 = p1
    pulsera2 = p2
    pulsera3 = p3


def setURL(url):
    global URL
    URL = url


def PonerRSSI(rssi_p1, rssi_p2, rssi_p3):
    global pulsera1, pulsera2, pulsera3
    # poniendo RSSI
    pulsera1['RSI'] = str(rssi_p1)
    pulsera2['RSI'] = str(rssi_p2)
    pulsera3['RSI'] = str(rssi_p3)


def PrepararPaqueteEnviar(rssi_p1, rssi_p2, rssi_p3, macBaliza):
    PonerRSSI(rssi_p1, rssi_p2, rssi_p3)

    listadoPulseras = list()
    listadoPulseras.append(pulsera1)
    listadoPulseras.append(pulsera2)
    listadoPulseras.append(pulsera3)

    paqueteEnviar = {
        "beacons": listadoPulseras,
        "baliza": macBaliza
    }

    import base64
    import json
    paqueteEnviar = base64.b64encode(bytes(json.dumps(paqueteEnviar), 'utf-8'))

    return paqueteEnviar


def EnviarDatosURL(paqueteEnviar):
    global URL
    PARAMS = {
        'key': "ESP32",
        "string_pack": paqueteEnviar
    }

    import requests
    try:
        r = requests.post(url=URL, data=PARAMS)
        if r.status_code == 200:
            print("[TEST_API]: Paquete enviado correctamente")
            # print(r.text)
        else:
            print("Failed")
    except Exception as e:
        print(str(e))

