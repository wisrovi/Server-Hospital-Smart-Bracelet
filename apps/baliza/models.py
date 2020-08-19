from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User


# Create your models here.


## Tablas referentes al usuario
class RolUsuario(models.Model):
    rolUsuario = models.CharField(max_length=50, blank=False, null=False, verbose_name='Rol Usuario', unique=True)
    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return self.rolUsuario

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Rol Usuario'
        verbose_name_plural = 'Roles Usuario'
        ordering = ['id']


class UsuarioRol(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    rolUsuario = models.ForeignKey(RolUsuario, on_delete=models.CASCADE, verbose_name='Rol Usuario')

    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return str(self.usuario)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']


## Las balizas son los dispositivos receptor de la señal de las pulseras
class Baliza(models.Model):
    macDispositivoBaliza = models.CharField(max_length=17, blank=False, null=False,
                                            verbose_name='MAC Dispositivo Baliza', unique=True)
    descripcion = models.CharField(max_length=100, blank=False, null=False, verbose_name='Descripción Baliza')

    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{} - {}".format(self.macDispositivoBaliza, self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Baliza'
        verbose_name_plural = 'Balizas'
        ordering = ['id']


class Bracelet(models.Model):
    macDispositivo = models.CharField(max_length=17, blank=False, null=False, verbose_name='MAC Dispositivo Bracelet',
                                      unique=True)
    major = models.PositiveIntegerField(verbose_name="Major")
    minor = models.PositiveIntegerField(verbose_name="Minor")
    txPower = models.IntegerField(verbose_name="Potencia a un metro de distancia")
    descripcion = models.CharField(max_length=100, blank=False, null=False, verbose_name='Descripción Bracelet')

    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "[mac={}] - [name={}] [Serial=({}/{})] [Tx={}]".format(self.macDispositivo, self.descripcion, self.minor,
                                                                      self.major,
                                                                      self.txPower)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Bracelet'
        verbose_name_plural = 'Bracelets'
        ordering = ['id']


## Ubicación
class Sede(models.Model):
    nombreSede = models.CharField(max_length=50, blank=False, null=False, verbose_name='Nombre Sede',
                                  unique=True)
    descripcion = models.CharField(max_length=100, blank=False, null=False, verbose_name='Descripción Sede')

    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return self.nombreSede

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'
        ordering = ['id']


class Piso(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, verbose_name='Sede')
    piso = models.PositiveIntegerField(blank=False, null=False, verbose_name='piso')
    descripcion = models.CharField(max_length=100, blank=False, null=False, verbose_name='Descripción piso')

    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{} - piso {}".format(self.sede, self.piso)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'piso'
        verbose_name_plural = 'Pisos'
        ordering = ['id']


class Area(models.Model):
    area = models.CharField(max_length=50, blank=False, null=False, verbose_name='Area',
                            unique=True)
    xInicial = models.PositiveIntegerField(verbose_name="Posición X cartesiana (punto inicial)")
    xFinal = models.PositiveIntegerField(verbose_name="Posición X cartesiana (punto final)")
    yInicial = models.PositiveIntegerField(verbose_name="Posición Y cartesiana (punto inicial)")
    yFinal = models.PositiveIntegerField(verbose_name="Posición Y cartesiana (punto final)")
    descripcion = models.CharField(max_length=100, blank=False, null=False, verbose_name='Descripción Area')
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE, verbose_name='piso')

    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{} ({} [({},{}),({},{})])".format(self.area, self.piso, self.xInicial, self.yInicial, self.xFinal,
                                                  self.yFinal)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['id']


## Relación instalación balizas
class InstalacionBaliza(models.Model):
    baliza = models.ForeignKey(Baliza, on_delete=models.CASCADE, verbose_name='Baliza')
    instalacionX = models.PositiveIntegerField(verbose_name="Posición X cartesiana (punto instalación)")
    instalacionY = models.PositiveIntegerField(verbose_name="Posición Y cartesiana (punto instalación)")
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE, verbose_name='piso')

    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    indHabilitado = models.BooleanField(default=True, verbose_name="Indicador Habilitado")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "[{}] - ({},{}) - [{}]".format(self.baliza, self.instalacionX, self.instalacionY, self.piso)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Instalación Baliza'
        verbose_name_plural = 'Instalación Balizas'
        ordering = ['id']


## Historial Bracelet Ubicación
class HistorialUbicacion(models.Model):
    bracelet = models.ForeignKey(Bracelet, on_delete=models.CASCADE, verbose_name='Bracelet')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Area')
    fechaIngresoArea = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Ingreso Area')
    fechaSalidaArea = models.DateTimeField(verbose_name='Fecha Salida Area', null=True, blank=True)

    def __str__(self):
        return "[{}] - [{}]".format(self.bracelet, self.area)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Historial Ubicacion'
        verbose_name_plural = 'Historial Ubicaciones'
        ordering = ['id']


class HistorialRSSI(models.Model):
    bracelet = models.ForeignKey(Bracelet, on_delete=models.CASCADE, verbose_name='Bracelet')
    baliza = models.ForeignKey(Baliza, on_delete=models.CASCADE, verbose_name="Baliza")
    rssi_signal = models.IntegerField(verbose_name="Intensidad señal BLE (RSSI)")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{}  ------->  {}  ====== {} (RSSI)".format(self.bracelet, self.baliza, self.rssi_signal)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Historial RSSI'
        verbose_name_plural = 'Historials RSSI'
        ordering = ['-fechaRegistro']


class HistorialBraceletSensors(models.Model):
    bracelet = models.ForeignKey(Bracelet, on_delete=models.CASCADE, verbose_name='Bracelet')
    ppm_sensor = models.PositiveIntegerField(verbose_name="Pulso cardiaco persona")
    caida_sensor = models.BooleanField(verbose_name="Detección caídas de la persona")
    proximidad_sensor = models.BooleanField(default=True,
                                            verbose_name="Sensor proximidad para detectar ManillaPuesta en la persona")
    temperatura_sensor = models.PositiveIntegerField(verbose_name="Temperatura persona")
    nivel_bateria = models.PositiveIntegerField(verbose_name="Porcentaje nivel Bateria")
    baliza = models.ForeignKey(Baliza, on_delete=models.CASCADE, verbose_name="Baliza")
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{} (sensors)".format(self.bracelet)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Historial Bracelet Sensors'
        verbose_name_plural = 'Historials Bracelet Sensors'
        ordering = ['-id']


## Configuración Bracelet
class BraceletUmbrals(models.Model):
    bracelet = models.ForeignKey(Bracelet, on_delete=models.CASCADE, verbose_name='Bracelet')
    minimaTemperatura = models.PositiveIntegerField(verbose_name="Temperatura minima")
    maximaTemperatura = models.PositiveIntegerField(verbose_name="Temperatura maxima")
    minimoPulsoCardiaco = models.PositiveIntegerField(verbose_name="Pulso Cardiaco minimo")
    maximaPulsoCardiaco = models.PositiveIntegerField(verbose_name="Pulso Cardiaco maximo")
    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{} (umbrales)".format(self.bracelet)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Bracele tUmbral'
        verbose_name_plural = 'Bracelet Umbrales'
        ordering = ['id']


class BraceletPatienHospital(models.Model):
    bracelet = models.ForeignKey(Bracelet, on_delete=models.CASCADE, verbose_name='Bracelet')
    idDatosPaciente = models.CharField(max_length=50, blank=False, null=False,
                                       verbose_name='Id datos almacenados que identifican al paciente', unique=True)
    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario que realiza el registro')
    fechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro', null=False,
                                         blank=False)

    def __str__(self):
        return "{} - {}".format(self.bracelet, self.idDatosPaciente)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Bracelet Patien Hospital'
        verbose_name_plural = 'Bracelet Patiens Hospital'
        ordering = ['id']
