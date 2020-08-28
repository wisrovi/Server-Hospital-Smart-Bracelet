from math import sqrt

"""
Se tienen unos puntos conocidos (Balizas) con posiciones (X,Y) también conocidas, 
de repente aparece un punto nuevo (Bracelet) con posición (X,Y) desconocida
y se necesita determinar la posición (X,Y) de ese nuevo punto, 
los unicos datos que se otorgan son la dsitancia de este nuevo punto a los puntos conocidos, es decir la longitud de cada vector

Se modelo una ecuación de triangulación para determinar que el punto nuevo esta dentro del area de otros tres puntos conocidos 
(se requieren minimo tres puntos conocidos para establecer una figura geometrica con un area, y por menor canidad de puntos se usa el triangulo para los calculos)

Se modelo una ecuacion de triliteración para relacionar las coordenadas del nuevo punto con el area de un triangulo
Latex: - 0.5 x \left(y_{1} - y_{2}\right) - 0.5 x_{1} y_{2} + 0.5 x_{2} y_{1} + 0.5 y \left(x_{1} - x_{2}\right) - 0.25 \left|{\left(- l_{1} + l_{2} + \sqrt{\left(x_{1} - x_{2}\right)^{2} + \left(y_{1} - y_{2}\right)^{2}}\right) \left(l_{1} - l_{2} + \sqrt{\left(x_{1} - x_{2}\right)^{2} + \left(y_{1} - y_{2}\right)^{2}}\right) \left(l_{1} + l_{2} - \sqrt{\left(x_{1} - x_{2}\right)^{2} + \left(y_{1} - y_{2}\right)^{2}}\right) \left(l_{1} + l_{2} + \sqrt{\left(x_{1} - x_{2}\right)^{2} + \left(y_{1} - y_{2}\right)^{2}}\right)}\right|^{0.5}



Se hace una solución de ecuaciones y la funcion siguiente entrega los valores de (x,Y) del nuevo punto
Latex: l_{1}^{2} - l_{2}^{2} + 2.0 x \left(x_{1} - x_{2}\right) - x_{1}^{2} + x_{2}^{2} + 2.0 y \left(y_{1} - y_{2}\right) - y_{1}^{2} + y_{2}^{2}



Obteniendo así la respuesta del sistema donde las variables son X ^ Y son encontradas a partir de conocer los origenes de los vectores mas cercanos y la longitud de los mismos
 

Nota: ver grafico en esta carpeta: Ecuaciones.png
"""


def CalcularPuntos(punto_clave1, punto_clave2):
    """
    :param punto_clave1: Este es el punto de la baliza1 a comparar
    :param punto_clave2: Este es el punto de la baliza2 a comparar
                                        #viene compuesto de la manera: (x,y), distancia al punto a hallar

    :return: puntos de (x,y) donde se encuentra ubicado el punto a hallar
    """
    x_p1 = punto_clave1[0][0]
    y_p1 = punto_clave1[0][1]
    l_p1 = punto_clave1[1]

    x_p2 = punto_clave2[0][0]
    y_p2 = punto_clave2[0][1]
    l_p2 = punto_clave2[1]

    ##################################################################################################################
    constanteX_ecuacion1 = -(y_p1 / 2 - y_p2 / 2)
    constanteY_ecuacion1 = x_p1 / 2 - x_p2 / 2
    raizDenominador = sqrt(pow((x_p1 - x_p2), 2) + pow((y_p1 - y_p2), 2))
    denominador1 = -l_p1 + l_p2 + raizDenominador
    denominador2 = l_p1 - l_p2 + raizDenominador
    denominador3 = l_p1 + l_p2 - raizDenominador
    denominador4 = l_p1 + l_p2 + raizDenominador
    denominador = denominador1 * denominador2 * denominador3 * denominador4
    denominador = abs(denominador)
    denominador = sqrt(denominador)
    constanteNumerica_ecuacion1 = (1 / 4) * denominador + ((x_p1 * y_p2) / 2) - ((x_p2 * y_p1) / 2)
    # print("Ecuacion 1 (Manual)")
    # La ecuacion 1 esta definida de la siguiente manera
    # ecuacion1 = x*(constanteX_ecuacion1) + (y)*(constanteY_ecuacion1) - constanteNumerica_ecuacion1

    ##################################################################################################################
    # print("Ecuacion 2 (Manual)")
    constanteX_ecuacion2 = 2 * x_p1 - 2 * x_p2
    constanteY_ecuacion2 = 2 * y_p1 - 2 * y_p2
    constanteNumerica_ecuacion2 = pow(l_p1, 2) - pow(l_p2, 2) - pow(x_p1, 2) + pow(x_p2, 2) - pow(y_p1, 2) + pow(y_p2,
                                                                                                                 2)

    # La ecuacion 2 esta definida de la siguiente manera
    # ecuacion2 = x*(constanteX_ecuacion2) + y*(constanteY_ecuacion2)  + constanteNumerica_ecuacion2

    ##################################################################################################################
    rtaY = -(
            constanteX_ecuacion1 * constanteNumerica_ecuacion2 + constanteX_ecuacion2 * constanteNumerica_ecuacion1) / (
                   constanteX_ecuacion1 * constanteY_ecuacion2 - constanteX_ecuacion2 * constanteY_ecuacion1)

    rtaX = -(
            constanteNumerica_ecuacion1 * constanteY_ecuacion2 + constanteNumerica_ecuacion2 * constanteY_ecuacion1) / (
                   constanteX_ecuacion2 * constanteY_ecuacion1 - constanteX_ecuacion1 * constanteY_ecuacion2)

    ## redondear para quitar decimales
    rtaX = abs(round(rtaX, 1))
    rtaY = abs(round(rtaY, 1))

    return rtaX, rtaY


class Persona:
    puntoCercano_1 = None
    distanciaPunto_1 = 0
    puntoCercano_2 = None
    distanciaPunto_2 = 0

    def __init__(self, punto1, dist1, punto2, dist2):
        self.puntoCercano_1 = punto1
        self.distanciaPunto_1 = dist1
        self.puntoCercano_2 = punto2
        self.distanciaPunto_2 = dist2

    def getPunto1(self):
        return self.puntoCercano_1, self.distanciaPunto_1

    def getPunto2(self):
        return self.puntoCercano_2, self.distanciaPunto_2


class BalizaInstalada:
    nombre = None
    ubicacion = None
    distancia = None

    def __init__(self, ubi, nombre, dist):
        self.ubicacion = ubi
        self.nombre = nombre
        self.distancia = dist


class Ubicacion:
    x = int()
    y = int()

    def __init__(self, x, y):
        self.x = x
        self.y = y


def HallarMejorSolucion(Distancia: dict, puntos: dict, constantePresicion=1.5):
    """
    :param Distancia: diccionario de distancias de las balizas, este contiene la longitud de los vectores de cada baliza hasta el punto a hallar
    :param puntos: diccionario de ubicaciones e cada baliza
    :param constantePresicion: valor absoluto de variacion de error, esto es para no descartar todas las respuestas
    :return: Entrega la ubicación lo mas precisa posible de acuerdo a los puntos entregados para analizar
    """
    valores = list()
    for i in Distancia:
        valores.append(Distancia[i])
    valores = sorted(valores)

    itemEvaluar = list()
    for i in valores:
        if len(itemEvaluar) == 3:
            break
        else:
            if i > 0:
                itemEvaluar.append(i)
    valores = itemEvaluar

    itemsUsar = []
    for i in Distancia:
        if len(itemsUsar) == 3:
            break

        if Distancia[i] >= 0:
            if Distancia[i] == valores[0]:
                itemsUsar.append(i)
            elif Distancia[i] == valores[1]:
                itemsUsar.append(i)

            elif Distancia[i] == valores[2]:
                itemsUsar.append(i)
    if len(itemsUsar) == 3:

        # print("Balizas usar:", itemsUsar)

        respuestas = list()

        person_option_one = Persona(
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]],
            puntos[str(itemsUsar[1])],
            Distancia[itemsUsar[1]]
        )
        x_one, y_one = CalcularPuntos(person_option_one.getPunto1(), person_option_one.getPunto2())
        respuestas.append((x_one, y_one))

        person_option_two = Persona(
            puntos[str(itemsUsar[1])],
            Distancia[itemsUsar[1]],
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]]
        )
        x_two, y_two = CalcularPuntos(person_option_two.getPunto1(), person_option_two.getPunto2())
        respuestas.append((x_two, y_two))

        person_option_three = Persona(
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]],
            puntos[str(itemsUsar[2])],
            Distancia[itemsUsar[2]]
        )
        x_three, y_three = CalcularPuntos(person_option_three.getPunto1(), person_option_three.getPunto2())
        respuestas.append((x_three, y_three))

        person_option_for = Persona(
            puntos[str(itemsUsar[2])],
            Distancia[itemsUsar[2]],
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]]
        )
        x_for, y_for = CalcularPuntos(person_option_for.getPunto1(), person_option_for.getPunto2())
        respuestas.append((x_for, y_for))

        filtro = []
        for i in respuestas:
            if i[0] is not None:
                filtro.append(i)
        respuestas = filtro

        def clave_ordenacion(tupla):
            return tupla[0], -tupla[1]

        respuestas = sorted(respuestas, key=clave_ordenacion)

        for i in respuestas:
            # print(i)
            pass

        # print("***************")
        CartesianoFinal = None
        for i in range(len(respuestas) - 1):
            x1, y1 = respuestas[i]
            x2, y2 = respuestas[i + 1]
            evaluarX = x1 + constantePresicion
            evaluarY = y1 + constantePresicion
            if evaluarX >= x2 and evaluarY >= y2:
                promedioX = round(x1 + round((x2 - x1) / 2, 2), 2)
                promedioY = round(y1 + round((y2 - y1) / 2, 2), 2)
                CartesianoFinal = (promedioX, promedioY)
                break
        if CartesianoFinal is None:
            for i in respuestas:
                print(i)
            print("Con ese valor de constante no es posible hallar una ubicación")
        else:
            pass
            # print("El valor estimado de ubicación (x,y) es", CartesianoFinal, "+-", constantePresicion)
        return CartesianoFinal, itemsUsar

    else:
        print("No hay suficientes puntos para hallar la posición")


def CalcularPosicion(listadoBalizas: list, precision=10):
    """
    :param listadoBalizas: listado de las balizas instaladas, estas se reorganizaran para usar las mas cercanas al punto a buscar
    :param precision: Las ecuaciones dan un valor de presición en la busqueda de (x,Y) y este valor puede ser editado para obtener una mejor respuesta
    :return: Entrega la ubicación lo mas precisa posible de acuerdo a los puntos entregados para analizar
    """
    Balizas = dict()
    Distancias = dict()
    for i in range(len(listadoBalizas)):
        baliza = listadoBalizas[i]
        Balizas[str(i)] = (baliza.ubicacion.x, baliza.ubicacion.y)
        Distancias[i] = baliza.distancia
    return HallarMejorSolucion(Distancias, Balizas, precision)
