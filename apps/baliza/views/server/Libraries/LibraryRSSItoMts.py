def CalcularDistancia(measuredPower, rssi):
    # https://iotandelectronics.wordpress.com/2016/10/07/how-to-calculate-distance-from-the-rssi-value-of-the-ble-beacon/#:~:text=At%20maximum%20Broadcasting%20Power%20(%2B,Measured%20Power%20(see%20below).

    N = 2  # Depende del factor ambiental, es una constante que va de 2 a 4
    numerador = (measuredPower) * -1 - (rssi) * -1
    denominador = 10 * N
    fraccion = numerador / denominador
    distancia = pow(10, fraccion)
    distancia = "{0:.2f}".format(distancia)
    distancia = float(distancia)
    # Obviamente, la distancia calculada es la distancia aproximada y no la distancia exacta,
    # ya que para calcular la distancia exacta
    # tenemos que hacer que el factor de pérdida (de factores ambientales) sea cero.
    return distancia
