from time import time


def count_elapsed_time(f):
    """
    Decorator.
    Execute the function and calculate the elapsed time.
    Print the result to the standard output.
    """

    def wrapper(*args, **kwargs):
        # Start counting.
        start_time = time()
        # Take the original function's return value.
        ret = f(*args, **kwargs)
        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        print("Elapsed time: %0.10f seconds." % elapsed_time)
        return ret

    return wrapper


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
        return (self.puntoCercano_1, self.distanciaPunto_1)

    def getPunto2(self):
        return (self.puntoCercano_2, self.distanciaPunto_2)


class Ubicacion:
    x = int()
    y = int()

    def __init__(self, x, y):
        self.x = x
        self.y = y


class BalizaInstalada:
    nombre = None
    ubicacion = None
    distancia = None

    def __init__(self, ubi, nombre, dist):
        self.ubicacion = ubi
        self.nombre = nombre
        self.distancia = dist


def hallarCoordenada(punto_clave1, punto_clave2):
    puntoA = punto_clave1[0]
    puntoB = punto_clave2[0]
    b = punto_clave1[1]
    a = punto_clave2[1]
    from sympy import Symbol
    from sympy import solve, sqrt
    variable1 = "x"
    variable2 = "y"
    x = Symbol(variable1)
    y = Symbol(variable2)

    x1, y1 = puntoA[0], puntoA[1]
    x2, y2 = puntoB[0], puntoB[1]

    # hallo la distancia entre los dos puntos conocidos
    c = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    # c = round(c, 2)

    # hallo el area del triangulo que forman los tres vectores
    s = (a + b + c) / 2
    contenidoRaiz = s * (s - a) * (s - b) * (s - c)
    contenidoRaiz = abs(contenidoRaiz)
    area = sqrt(contenidoRaiz)
    # area = round(area, 2)

    # defino la ecuacion de la formula del area con el metodo de determinantes
    ecua1 = (-((x1 * y2 - x2 * y1) + y * (x2 - x1) + x * (y1 - y2)) / 2) - area
    # print("Ecuacion 1")
    # print( ecua1 )

    # con las ecuaciones de distancia hallo una segunda ecuación
    ecua2 = x * (2 * x1 - 2 * x2) + y * (2 * y1 - 2 * y2) + (x2 ** 2 - x1 ** 2 - a ** 2 + b ** 2 + y2 ** 2 - y1 ** 2)

    # print(ecua2)

    # hallo los puntos del vertice donde apuntan los dos vectores de los vertices fijos
    rta = solve((ecua1, ecua2), dict=True)[0]
    valorx = round(rta[x], 1)
    valory = round(rta[y], 1)

    if valorx >= 0 and valory >= 0:
        # print(variable1 + "=", valorx)
        # print(variable2 + "=", valory)
        return valorx, valory
    else:
        if valorx >= -0.5 and valory >= -0.5:
            return abs(valorx), abs(valory)
        return None, None


from math import sqrt
def CalcularPuntos(punto_clave1, punto_clave2):
  x_p1 = punto_clave1[0][0]
  y_p1 = punto_clave1[0][1]
  l_p1 = punto_clave1[1]

  x_p2 = punto_clave2[0][0]
  y_p2 = punto_clave2[0][1]
  l_p2 = punto_clave2[1]

  constanteX_ecuacion1 = -(y_p1/2 - y_p2/2)
  constanteY_ecuacion1 = x_p1/2 - x_p2/2

  raizDenominador = sqrt(  pow((x_p1-x_p2),2)  +  pow((y_p1-y_p2),2) )

  denominador1 = -l_p1 + l_p2 + raizDenominador
  denominador2 = l_p1 - l_p2 + raizDenominador
  denominador3 = l_p1 + l_p2 - raizDenominador
  denominador4 = l_p1 + l_p2 + raizDenominador

  denominador = denominador1 * denominador2 * denominador3 * denominador4
  denominador = abs(denominador)
  denominador = sqrt(denominador)

  constanteNumerica_ecuacion1 = (1/4) * denominador  + ((x_p1*y_p2)/2) - ((x_p2*y_p1)/2)
  # print("Ecuacion 1 (Manual)")
  # La ecuacion 1 esta definida de la siguiente manera
  # ecuacion1 = x*(constanteX_ecuacion1) + (y)*(constanteY_ecuacion1) - constanteNumerica_ecuacion1

  print("Ecuacion 2 (Manual)")
  constanteX_ecuacion2 =  2*x_p1 -2*x_p2
  constanteY_ecuacion2 = 2*y_p1 -2*y_p2
  constanteNumerica_ecuacion2 = pow(l_p1, 2) - pow(l_p2, 2) - pow(x_p1, 2) + pow(x_p2, 2) - pow(y_p1, 2) + pow(y_p2, 2)

  # La ecuacion 2 esta definida de la siguiente manera
  # ecuacion2 = x*(constanteX_ecuacion2) + y*(constanteY_ecuacion2)  + constanteNumerica_ecuacion2

  rtaY = -(constanteX_ecuacion1*constanteNumerica_ecuacion2 + constanteX_ecuacion2*constanteNumerica_ecuacion1) / (constanteX_ecuacion1*constanteY_ecuacion2 - constanteX_ecuacion2*constanteY_ecuacion1)
  if constanteX_ecuacion2 == 0:
      return None,None
  rtaX = ( -constanteNumerica_ecuacion2 - constanteY_ecuacion2*rtaY ) / constanteX_ecuacion2

  rtaY = round(rtaY, 1)
  rtaX = round(rtaX, 1)

  if rtaX >= 0 and rtaY >= 0:
      # print(variable1 + "=", valorx)
      # print(variable2 + "=", valory)
      return rtaX, rtaY
  else:
      if rtaX >= -0.5 and rtaY >= -0.5:
          return abs(rtaX), abs(rtaY)
      return None, None



def HallarMejorSolucion2(Distancia, puntos, constantePresicion=1.5):
    valores = []
    for i in Distancia:
        valores.append(Distancia[i])
    valores = sorted(valores)

    itemEvaluar = []
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

        respuestas = []

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
            return (tupla[0], -tupla[1])

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


def HallarMejorSolucion1(Distancia, puntos, constantePresicion=1.5):
    valores = []
    for i in Distancia:
        valores.append(Distancia[i])
    valores = sorted(valores)

    itemEvaluar = []
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

        respuestas = []

        person_option_one = Persona(
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]],
            puntos[str(itemsUsar[1])],
            Distancia[itemsUsar[1]]
        )
        x_one, y_one = hallarCoordenada(person_option_one.getPunto1(), person_option_one.getPunto2())
        respuestas.append((x_one, y_one))

        person_option_two = Persona(
            puntos[str(itemsUsar[1])],
            Distancia[itemsUsar[1]],
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]]
        )
        x_two, y_two = hallarCoordenada(person_option_two.getPunto1(), person_option_two.getPunto2())
        respuestas.append((x_two, y_two))

        person_option_three = Persona(
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]],
            puntos[str(itemsUsar[2])],
            Distancia[itemsUsar[2]]
        )
        x_three, y_three = hallarCoordenada(person_option_three.getPunto1(), person_option_three.getPunto2())
        respuestas.append((x_three, y_three))

        person_option_for = Persona(
            puntos[str(itemsUsar[2])],
            Distancia[itemsUsar[2]],
            puntos[str(itemsUsar[0])],
            Distancia[itemsUsar[0]]
        )
        x_for, y_for = hallarCoordenada(person_option_for.getPunto1(), person_option_for.getPunto2())
        respuestas.append((x_for, y_for))

        filtro = []
        for i in respuestas:
            if i[0] is not None:
                filtro.append(i)
        respuestas = filtro

        def clave_ordenacion(tupla):
            return (tupla[0], -tupla[1])

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




# @count_elapsed_time
def CalcularPosicion(listadoBalizas=list(), precision=10, opcion1=True):
    Balizas = dict()
    Distancias = dict()
    for i in range(len(listadoBalizas)):
        baliza = listadoBalizas[i]
        Balizas[str(i)] = (baliza.ubicacion.x, baliza.ubicacion.y)
        Distancias[i] = baliza.distancia
    if opcion1:
        return HallarMejorSolucion1(Distancias, Balizas, precision)
    else:
        return HallarMejorSolucion2(Distancias, Balizas, precision)



puntoA = (2, 12)
distancia_al_puntoA = 0.4

puntoB = (10, 10)
distancia_al_puntoB = 1.12

puntoC = (2, 2)
distancia_al_puntoC = 3.55


# A y B
punto_clave1 = puntoA, distancia_al_puntoA
punto_clave2 = puntoB, distancia_al_puntoB
print(hallarCoordenada(punto_clave1, punto_clave2))

# A y C
punto_clave1 = puntoA, distancia_al_puntoA
punto_clave2 = puntoC, distancia_al_puntoC
print(hallarCoordenada(punto_clave1, punto_clave2))


# B y C
punto_clave1 = puntoB, distancia_al_puntoB
punto_clave2 = puntoC, distancia_al_puntoC
print(hallarCoordenada(punto_clave1, punto_clave2))
