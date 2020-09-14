from apps.Util_apps.Decoradores import execute_in_thread


@execute_in_thread(name="hilo emulador baliza")
def EnviarDatosURL(paqueteEnviar, SERVER_USE = "PAUL"):
    servidores = dict()
    servidores['OFFICE'] = ("172.16.66.84", 8000)
    servidores['PAUL'] = ("172.30.19.88", 5000)




    ip = servidores[SERVER_USE][0]
    port = servidores[SERVER_USE][1]
    URL = "http://{}:{}/hospitalsmartbracelet/received/".format(ip, port)

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

datos_balizas = list()
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNTIiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDQ1Il19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNTQiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDQ2Il19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNTAiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDQ3Il19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNjMiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDQ4Il19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNTgiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDQ5Il19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNTAiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDUwIl19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNjAiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDUxIl19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNTciLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDUyIl19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNDgiLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDUzIl19")
datos_balizas.append("eyJiZWFjb25zIjpbeyJTRUQiOiIwMDAwIiwiTUFDIjoiQjA3RTExRkU5MUY0IiwiQkFUIjoiMzkiLCJQUE0iOiI3MiIsIkNBSSI6IjAiLCJURU0iOiIzMC4wIiwiUlNJIjoiNDciLCJQUk8iOiIxIn1dLCJiYWxpemEiOlsiNEMxMUFFNzU0MDU0Il19")



import time
for _ in range(1000):
    for dato in datos_balizas:
        EnviarDatosURL(dato)
        time.sleep(0.05)
    print("**************************************")