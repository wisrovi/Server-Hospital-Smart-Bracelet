from apps.baliza.models import Baliza, Bracelet, BraceletUmbrals, HistorialBraceletSensors

OPTIMIZED = True

def BuscarBalizaDB(macBaliza):
    if OPTIMIZED:
        try:
            macBaliza = Baliza.objects.get(macDispositivoBaliza=macBaliza)
            return True, macBaliza
        except:
            return False, None
    else:
        balizasExistentes = Baliza.objects.all()
        for baliz in balizasExistentes:
            if baliz.macDispositivoBaliza == macBaliza:
                return True, baliz
        return False, None

def BuscarBraceletDB(macBracelet):
    if OPTIMIZED:
        try:
            macBracelet = Bracelet.objects.get(macDispositivo=macBracelet)
            return True, macBracelet
        except:
            return False, None
    else:
        braceletsExistentes = Bracelet.objects.all()
        for brac in braceletsExistentes:
            if macBracelet == brac.macDispositivo:
                return True, brac
        return False, None

def BuscarUmbralesBraceletDB(macBracelet):
    find = False
    if type(macBracelet) == str():
        find, braceletObject = BuscarBraceletDB(macBracelet)

    if find:
        try:
            umbrales = BraceletUmbrals.objects.get(bracelet=braceletObject)
            return umbrales
        except:
            return None
    else:
        return None

def BuscarHistorialSensoresParaBracelet(braceletObject):
    hist = HistorialBraceletSensors.objects.filter(bracelet=braceletObject).order_by(
        '-fechaRegistro')