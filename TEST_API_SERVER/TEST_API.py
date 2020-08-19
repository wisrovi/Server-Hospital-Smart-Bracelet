from TEST_API_SERVER.LibraryEmulate import SetPulseras, setURL, PrepararPaqueteEnviar, EnviarDatosURL

listaMacs = ["90E202048AE8", "90E202048AE9", "90E202048AE7", ]
semilla = ["0000"]

pulsera1 = {
    "SED": semilla[0],
    "MAC": listaMacs[0],
    "BAT": str(35),
    "PPM": str(85),
    "CAI": str(int(False)),
    "TEM": str(366),
    "PRO": str(int(True))
}

pulsera2 = {
    "SED": semilla[0],
    "MAC": listaMacs[1],
    "BAT": str(33),
    "PPM": str(78),
    "CAI": str(int(False)),
    "TEM": str(327),
    "PRO": str(int(True))
}

pulsera3 = {
    "SED": semilla[0],
    "MAC": listaMacs[2],
    "BAT": str(33),
    "PPM": str(95),
    "CAI": str(int(False)),
    "TEM": str(357),
    "PRO": str(int(True))
}

SetPulseras(pulsera1, pulsera2, pulsera3)
setURL("http://localhost:5000/hospitalsmartbracelet/received/")

balizas = ["80:E2:02:04:8A:E7"]

Datos = dict()
Datos["80:E2:02:04:8A:E7"] = (80, 69, 60)
Datos["80:E2:02:04:8A:E8"] = (70, 60, 80)
Datos["80:E2:02:04:8A:E9"] = (61, 68, 80)
Datos["80:E2:02:04:8A:EA"] = (61, 67, 80)



for macBaliza in Datos:
    paqueteEnviar = PrepararPaqueteEnviar(Datos[macBaliza][0], Datos[macBaliza][1], Datos[macBaliza][2], macBaliza)
    print(macBaliza, end="->")
    EnviarDatosURL(paqueteEnviar)



