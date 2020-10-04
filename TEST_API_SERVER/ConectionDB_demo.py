import datetime
from apps.baliza.views.server.Libraries.ConsultasBaseDatos.ConsultasMariaDB import *

import warnings
warnings.filterwarnings("ignore")

import time

# for i in range(1):
#     response = ReadLastRegisterByCalculateUbication()
#     print(i, " -> ", response)
#     time.sleep(0.005)

print("correos: ", ReadEmailsAlertas())

print("baliza: ", ReadDataBalizaByMac('4C:11:AE:75:40:44')[0])

print("Bracelet: ", ReadDataBraceletByMac('B0:7E:11:FE:91:F4')[0])

print("sensors:", ReadLastRegisterSensors(3))

print("history RSSI", ReadLastRegisterByCalculateUbication(3))

# print("insertar:", InsertarNuevoDatoHistorialSensores(
#     idBracelet=3,
#     idBaliza=14,
#     temperatura=35,
#     bateria=33,
#     caida=False,
#     proximidad=True,
#     ppm=75
# ))
