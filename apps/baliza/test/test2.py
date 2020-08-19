import math


class Ubicacion:
    x = int()
    y = int()

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Baliza:
    nombre = None
    ubicacion = None
    distancia = None

    def __init__(self, ubi, nombre):
        self.ubicacion = ubi
        self.nombre = nombre






listadoBalizas = list()
listadoBalizas.append(Baliza(ubi=Ubicacion(x=5, y=5), nombre="Baliza 1"))
listadoBalizas.append(Baliza(ubi=Ubicacion(x=20, y=7), nombre="Baliza 2"))
listadoBalizas.append(Baliza(ubi=Ubicacion(x=18, y=13), nombre="Baliza 3"))

class DistanciasBalizas:
    baliza1 = None
    baliza2 = None
    distancia = float()

    def __init__(self, baliza1, baliza2, distancia):
        self.baliza1 = baliza1
        self.baliza2 = baliza2
        self.distancia = distancia





def CalcularDistancia(x1, x2, y1, y2):
    return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), 2)


respuestasDistancias = list()
for i in range(len(listadoBalizas)):
    for j in range(i + 1, len(listadoBalizas)):
        baliza1 = listadoBalizas.__getitem__(i)
        baliza2 = listadoBalizas.__getitem__(j)
        distanciaBalizas = CalcularDistancia(x1=baliza1.ubicacion.x, x2=baliza2.ubicacion.x, y1=baliza1.ubicacion.y,
                                             y2=baliza2.ubicacion.y)
        respuestasDistancias.append(DistanciasBalizas(baliza1=baliza1, baliza2=baliza2, distancia=distanciaBalizas))

print(listadoBalizas)


print("Imprimiendo resultados:")
for item in respuestasDistancias:
    print(item.baliza1.nombre, "(", item.baliza1.ubicacion.x, ",", item.baliza1.ubicacion.y, ")", end=" - ")
    print(item.baliza2.nombre, "(", item.baliza2.ubicacion.x, ",", item.baliza2.ubicacion.y, ")", end=" - ")
    print("Distancia:", item.distancia)
