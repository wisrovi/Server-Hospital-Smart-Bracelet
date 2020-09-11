


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
            # print(r.text)
        else:
            print("Failed")
    except Exception as e:
        print(str(e))

data = "eyJiZWFjb25zIjpbXSwiYmFsaXphIjpbIjRDMTFBRTc1NDBDNCJdfQ**"
data2 = "eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzYiLCJQUE0iOiIwMDAiLCJDQUkiOiIwIiwiVEVNIjoiMjYwIiwiUlNJIjoiODMiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDQ0Il19"

lapzo_temporal_envio_datos = 2
import time
for _ in range(1000):
    time.sleep(lapzo_temporal_envio_datos)
    EnviarDatosURL(data2)
    time.sleep(0.5)
    EnviarDatosURL(data)