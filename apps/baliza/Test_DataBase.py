
import time

from models import Baliza

for i in range(100):
    balizaLeida = Baliza.objects.first()
    time.sleep(0.05)
    print(balizaLeida)