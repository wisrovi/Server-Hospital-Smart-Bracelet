from apps.Util_apps.Decoradores import execute_in_thread


class Bracelet:
    SED = str()
    MAC = str()
    BAT = str()
    PPM = str()
    CAI = str()
    TEM = str()
    RSI = str()
    PRO = str()


class UnZipPackBracelets:
    listBracelets = list()
    listConvert = list()

    def setString(self, contenidoJson):
        if contenidoJson is not None:

            for beacon in contenidoJson['beacons']:
                bracelec = Bracelet()
                bracelec.BAT = beacon['BAT']
                bracelec.MAC = beacon['MAC']
                bracelec.SED = beacon['SED']
                bracelec.PPM = beacon['PPM']
                bracelec.CAI = beacon['CAI']
                bracelec.TEM = beacon['TEM']
                bracelec.RSI = beacon['RSI']
                bracelec.PRO = beacon['PRO']
                self.listBracelets.append(bracelec)
            return self.listBracelets
        else:
            return None

    def LimpiarListas(self):
        self.listBracelets = list()
        self.listConvert = list()

    def convertList(self):
        import json
        self.listConvert = list()
        for bracelet in self.listBracelets:
            self.listConvert.append(json.dumps(bracelet.__dict__))
        return self.listConvert



