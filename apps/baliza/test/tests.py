from apps.baliza.test.LibraryTriangulacionTriliteracion import *





listadoBalizas = list()
listadoBalizas.append(BalizaInstalada(ubi=Ubicacion(x=13, y=0), nombre="Baliza 1", dist=13.4))
listadoBalizas.append(BalizaInstalada(ubi=Ubicacion(x=20, y=7), nombre="Baliza 2", dist=19))
listadoBalizas.append(BalizaInstalada(ubi=Ubicacion(x=18, y=13), nombre="Baliza 3", dist=17.4))
listadoBalizas.append(BalizaInstalada(ubi=Ubicacion(x=5, y=14), nombre="Baliza 4", dist=9))
listadoBalizas.append(BalizaInstalada(ubi=Ubicacion(x=0, y=0), nombre="Baliza 5", dist=22))

CartesianoFinal, idsBalizasUsadas = CalcularPosicion(listadoBalizas)
constantePresicion = 6
print("El valor estimado de ubicación (x,y) es", CartesianoFinal, "+-", constantePresicion)
print("Para este bracelet se usaron las siguientes balizas: ", end="")
for i in idsBalizasUsadas:
    print(listadoBalizas[i].nombre, end=",")
