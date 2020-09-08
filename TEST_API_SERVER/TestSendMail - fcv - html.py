from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib




FOLDER_HTML = "PLANTILLAFCV/"

config_files = dict()
config_files['alerta_caida'] = { 'File' : FOLDER_HTML + 'AlertaCaida.html', 'Var' : [ 'user', 'paciente' ] }
config_files['alerta_ppm'] = { 'File' : FOLDER_HTML + 'AlertaPPM.html', 'Var' : [ 'user', 'paciente' ] }
config_files['alerta_proximidad'] = { 'File' : FOLDER_HTML + 'AlertaProximidad.html', 'Var' : [ 'user', 'paciente' ] }
config_files['alerta_temperatura'] = { 'File' : FOLDER_HTML + 'AlertaTemperatura.html', 'Var' : [ 'user', 'paciente' ] }
config_files['change_password'] = { 'File' : FOLDER_HTML + 'CambioContrasena.html', 'Var' : [ 'user' ] }
config_files['datos_incorrectos'] = { 'File' : FOLDER_HTML + 'DatosIncorretos.html', 'Var' : [ 'user' ] }
config_files['inicio_sesion'] = { 'File' : FOLDER_HTML + 'InicioSeccion.html', 'Var' : [ 'user' ] }
config_files['nueva_baliza'] = { 'File' : FOLDER_HTML + 'NewBaliz.html', 'Var' : [ 'mac_baliza' ] } 
config_files['nuevo_bracelet'] = { 'File' : FOLDER_HTML + 'NewBrazalet.html', 'Var' : [ 'mac_bracelet' ] }
config_files['bienvenido'] = { 'File' : FOLDER_HTML + 'welcome.html', 'Var' : [ 'user' ] }

def render_to_string(nameFile, dictionary):
    data = str()
    with open (nameFile, "r") as myfile:
        data = myfile.read()
        for key in dictionary:
            keys = list()
            keys.append("{{ " + key + " }}")
            keys.append("{{" + key + " }}")
            keys.append("{{ " + key + "}}")
            keys.append("{{" + key + "}}")
            for llave in keys:
                if data.find(llave) >= 0:
                    data = data.replace(llave, dictionary[key])
                    break         
    return data

def ModifyHtml(url_path, html):
    cid = url_path.split("/")
    cid_search = cid[-1].split(".")[0]
    html = html.replace(url_path, "cid:" + cid_search)
    return html

def ChargeImage(url_path ):
    url_path = FOLDER_HTML + url_path
    cid = url_path.split("/")
    cid_search = cid[-1].split(".")[0]
    MIMEImage_search = "<" + cid_search + ">"

    fp = open(url_path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', MIMEImage_search)

    return msgImage

imagenes_en_html = list()
diccionarioDatos = dict()
PARAMETROS = dict()

##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################

def PrepararDatosCorreo_alertaCaida():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['alerta_caida']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')
    diccionarioDatos[PARAMETROS['Var'][1]] = str('Paciente 1')

    imagenes_en_html.append( ( "img/LOGOFCV.png", ChargeImage(FOLDER_HTML + "img/LOGOFCV.png") ) )
    imagenes_en_html.append( ( "img/caida.jpg", ChargeImage(FOLDER_HTML + "img/caida.jpg") ) )

def PrepararDatosCorreo_alertaPPM():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['alerta_ppm']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')
    diccionarioDatos[PARAMETROS['Var'][1]] = str('Paciente 1')

    imagenes_en_html.append( ( "img/LOGOFCV.png", ChargeImage(FOLDER_HTML + "img/LOGOFCV.png") ) )
    imagenes_en_html.append( ( "img/ppm.jpg", ChargeImage(FOLDER_HTML + "img/ppm.jpg") ) )

def PrepararDatosCorreo_alertaProximidad():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['alerta_proximidad']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')
    diccionarioDatos[PARAMETROS['Var'][1]] = str('Paciente 1')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/no_signal.png" )

def PrepararDatosCorreo_alertaTemperatura():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['alerta_temperatura']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')
    diccionarioDatos[PARAMETROS['Var'][1]] = str('Paciente 1')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/iconoCaution.jpg" )

def PrepararDatosCorreo_cambio_password():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['change_password']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/password.png" )

def PrepararDatosCorreo_datos_incorrectos():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['datos_incorrectos']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/error.jpg" )

def PrepararDatosCorreo_inicioSesion():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['inicio_sesion']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/notificacion.jpg" )

def PrepararDatosCorreo_nuevaBaliza():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['nueva_baliza']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('mac baliza')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/baliza.jpg" )

def PrepararDatosCorreo_nuevoBracelet():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['nuevo_bracelet']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('mac bracelet')

    imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/manilla.jpg" )

def PrepararDatosCorreo_bienvenido():
    global imagenes_en_html
    global imagenes_en_html
    global PARAMETROS

    PARAMETROS = config_files['bienvenido']
    diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')

    #imagenes_en_html.append( "img/LOGOFCV.png" )
    imagenes_en_html.append( "img/iconoCaution.jpg" )

PrepararDatosCorreo_nuevoBracelet()

correo_destinatario = 'williamrodriguez@fcv.org' #"cesarfigueroa@fcv.org"

##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################


html_message = render_to_string(PARAMETROS['File'], diccionarioDatos)

for path_url in imagenes_en_html:
    html_message = ModifyHtml(path_url, html_message)


from authentication.Config.ConfigMail import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
user = EMAIL_HOST_USER
port = 587
host = 'webmail.fcv.org'
password = EMAIL_HOST_PASSWORD
token = ""  #token aplication

# create message object instance
msgRoot  = MIMEMultipart('related')

# setup the parameters of the message
msgRoot['Subject'] = "Asunto"
msgRoot['From'] = user
msgRoot['To'] = correo_destinatario

# add in the message body
message = "Thank you"
part1 = MIMEText(html_message, 'html')
part2 = MIMEText(message, 'plain')
msgRoot.attach(part1)
msgRoot.attach(part2)

# Define the image's ID as referenced above
for path_url in imagenes_en_html:
    mime_image = ChargeImage(path_url)
    msgRoot.attach(mime_image)

# create server
server = smtplib.SMTP('{}: {}'.format(host, port))
server.starttls()

# Login Credentials for sending the mail
server.login(msgRoot['From'], password)

# send the message via the server.
server.sendmail(msgRoot ['From'], msgRoot ['To'], msgRoot.as_string())
server.quit()

print("successfully sent email to %s:" % (msgRoot ['To']))





##https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images