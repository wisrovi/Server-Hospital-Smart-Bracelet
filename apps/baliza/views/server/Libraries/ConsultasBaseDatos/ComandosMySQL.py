

## READ

COMANDO_ReadLastRegisterByCalculateUbication = """
    SELECT A.bracelet_id, A.baliza_id, A.rssi_signal, A.fechaRegistro, 
E.txPower, F.macDispositivoBaliza AS macBaliza,
D.sede_id, C.piso_id, C.instalacionX, C.instalacionY
    
    /* , ROUND(NOW() - A.fechaRegistro) AS seconds*/
    
    FROM baliza_historialrssi A
    
    INNER JOIN (
      SELECT bracelet_id,baliza_id, max(fechaRegistro) AS fechaRegistro
      FROM baliza_historialrssi
      GROUP BY bracelet_id, baliza_id
    ) B
    ON A.bracelet_id=B.bracelet_id AND A.baliza_id=B.baliza_id AND A.fechaRegistro=B.fechaRegistro
    
    INNER JOIN (
      SELECT  baliza_id, instalacionX, instalacionY, piso_id
      FROM baliza_instalacionbaliza
    ) C
    ON C.baliza_id = A.baliza_id
    
    INNER JOIN(
      SELECT id AS piso_id, sede_id FROM baliza_piso
    ) D
    ON D.piso_id = C.piso_id
    
    INNER JOIN baliza_bracelet E
    ON E.id = A.bracelet_id
    
    INNER JOIN baliza_baliza F
    ON F.id = A.baliza_id
    
    WHERE DATEDIFF(NOW(),A.fechaRegistro)<=3
    AND YEAR(A.fechaRegistro)=YEAR(NOW())
    AND MONTH(A.fechaRegistro)=MONTH(NOW())
    AND DAY(A.fechaRegistro)=DAY(NOW())     
    AND ROUND(NOW() - A.fechaRegistro) <= 30
    AND A.bracelet_id = @idbracelet         

    ORDER BY A.bracelet_id,A.baliza_id, A.fechaRegistro DESC;
    """


COMANDO_ReadAreasPorPiso = """
SELECT id, area, xInicial, xFinal, yInicial, yFinal FROM baliza_area
WHERE piso_id = @idPiso;
"""


COMANDO_ReadIsInArea = """
SELECT A.id, A.bracelet_id, A.area_id, A.fechaSalidaArea
FROM baliza_historialubicacion A 

INNER JOIN baliza_area B
ON A.area_id = B.id

WHERE A.bracelet_id = @idBracelet
ORDER BY id DESC LIMIT 1;
"""


COMANDO_EmailsDestinatariosAlertas = """
SELECT atu.email FROM baliza_rolusuario bru

INNER JOIN baliza_usuariorol bur
ON bru.id = bur.rolUsuario_id

INNER JOIN auth_user atu
ON atu.id = bur.usuario_id

WHERE	bru.rolUsuario = 'Server'
"""

COMANDO_ReadDataBalizaByMac = """
SELECT id, macDispositivoBaliza, descripcion, indHabilitado FROM baliza_baliza
WHERE	macDispositivoBaliza = '@mac';
"""

COMANDO_ReadDataBraceletByMac = """
SELECT bbra.id, bbra.macDispositivo, bbra.major, bbra.minor, bbra.txPower, bbra.descripcion, 
bbra.indHabilitado, bbraum.minimaTemperatura, bbraum.maximaTemperatura, 
bbraum.minimoPulsoCardiaco, bbraum.maximaPulsoCardiaco, bbrapath.idDatosPaciente 
FROM  baliza_bracelet bbra

INNER JOIN baliza_braceletumbrals bbraum
ON bbra.id = bbraum.bracelet_id

INNER JOIN baliza_braceletpatienhospital bbrapath
ON bbra.id = bbrapath.bracelet_id

WHERE	macDispositivo = '@mac';
"""

COMANDO_ReadLastRegisterSensors = """
SELECT hsb.ppm_sensor, hsb.caida_sensor, hsb.proximidad_sensor, hsb.temperatura_sensor, hsb.nivel_bateria
FROM baliza_historialbraceletsensors hsb
WHERE hsb.bracelet_id = @idBracelet
ORDER BY id DESC 
LIMIT 1;
"""


## INSERT


COMANDO_InsertarNuevoDatoHistorialSensores = """
INSERT INTO baliza_historialbraceletsensors (ppm_sensor, caida_sensor, proximidad_sensor, temperatura_sensor, 
nivel_bateria,fechaRegistro, baliza_id, bracelet_id)
VALUES (
@ppm, 
@caida, 
@proximidad, 
@temperatura, 
@bateria, 
NOW(), 
@idBaliza, 
@idBracelet);

"""

COMANDO_InsertarNuevoRegistroSRRI = """
INSERT INTO baliza_historialrssi (rssi_signal, fechaRegistro, baliza_id, bracelet_id) VALUES (@rssi, NOW(), @idBaliza, @idBracelet);
"""


COMANDO_InsertarNuevoRegistroHistorialUbicacion = """
INSERT INTO baliza_historialubicacion 
(fechaIngresoArea, fechaSalidaArea, area_id, bracelet_id) 
VALUES (NOW(), NULL, @idArea, @idBracelet);
"""


## UPDATE

COMANDO_UpdateDateOutArea = """
UPDATE baliza_historialubicacion 
SET fechaSalidaArea = NOW()
WHERE id = @idRegistro;
"""