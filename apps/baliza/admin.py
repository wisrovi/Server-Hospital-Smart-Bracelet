from django.contrib import admin

# Register your models here.
from apps.baliza.models import HistorialUbicacion, InstalacionBaliza, BraceletPatienHospital, HistorialBraceletSensors, \
    BraceletUmbrals, UsuarioRol, Bracelet, Area, Baliza, Piso, Sede, RolUsuario, HistorialRSSI

admin.site.register(RolUsuario)
admin.site.register(UsuarioRol)
admin.site.register(HistorialUbicacion)
admin.site.register(InstalacionBaliza)
admin.site.register(BraceletPatienHospital)
admin.site.register(HistorialBraceletSensors)
admin.site.register(BraceletUmbrals)
admin.site.register(Bracelet)
admin.site.register(Area)
admin.site.register(Baliza)
admin.site.register(Piso)
admin.site.register(Sede)
admin.site.register(HistorialRSSI)
