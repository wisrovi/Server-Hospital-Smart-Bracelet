import math

from sympy import Symbol, sqrt, expand, simplify, Abs, solve

print("iniciando a resolver")

Baliza1 = {
    'x': 5,
    'y': 5
}
Baliza2 = {
    'x': 20,
    'y': 7
}

distancia_a = 15.26
distancia_b = 6.32

print("************************************************")
Xp = Symbol('Xp')
Yp = Symbol('Yp')

distancia_c = sqrt((Baliza1['x'] - Baliza2['x']) ** 2 + (Baliza1['y'] - Baliza2['y']) ** 2)
s = (distancia_a + distancia_b + distancia_c) / 2
area = sqrt(Abs(s * (s - distancia_a) * (s - distancia_b) * (s - distancia_c)))

ecua1 = (-((Baliza1['x'] * Baliza2['y'] - Baliza2['x'] * Baliza1['y']) + Yp * (Baliza2['x'] - Baliza1['x']) + Xp * (
        Baliza1['y'] - Baliza2['y'])) / 2) - area

ecua2 = Xp * (2 * Baliza1['x'] - 2 * Baliza2['x']) + Yp * (2 * Baliza1['y'] - 2 * Baliza2['y']) + (
        Baliza2['x'] ** 2 - Baliza1['x'] ** 2 - distancia_a ** 2 + distancia_b ** 2 + Baliza2['y'] ** 2 - Baliza1[
    'y'] ** 2)

print(ecua1)
print(ecua2)
rta = solve((ecua1, ecua2), dict=True)[0]
Xp = int(round(rta[Xp], 1))
Yp = int(round(rta[Yp], 1))
print(Xp)
print(Yp)
