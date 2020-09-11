


def EnviarDatosURL(paqueteEnviar):
    URL = "http://192.168.0.110:5000/hospitalsmartbracelet/received/"

    PARAMS = {
        "key": "ESP32",
        "string_pack": paqueteEnviar
    }

    import requests
    try:
        r = requests.post(url=URL, data={ "{}".format(PARAMS) : 0})
        if r.status_code == 200:
            print("[TEST_API]: Paquete enviado correctamente")
            print(r.text)
        else:
            print("Failed")
    except Exception as e:
        print(str(e))

data = "eyJiZWFjb25zIjpbXSwiYmFsaXphIjpbIjRDMTFBRTc1NDA0NCJdfQ**"
EnviarDatosURL(data)