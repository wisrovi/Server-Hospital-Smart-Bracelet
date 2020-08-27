from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.template.loader import render_to_string




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






PARAMETROS = config_files['alerta_caida']

diccionarioDatos = dict()
diccionarioDatos[PARAMETROS['Var'][0]] = str('Usuario 1')
diccionarioDatos[PARAMETROS['Var'][1]] = str('Paciente 1')

html_message = render_to_string(PARAMETROS['File'], diccionarioDatos)











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

user = "hospitalsmartbracelet@fcv.org"
port = 587
host = 'webmail.fcv.org'
password = "fBy3clj9fOoKDoj9OtSk"
token = ""  #token aplication

# create message object instance
msg = MIMEMultipart()

# setup the parameters of the message
msg['From'] = user
msg['To'] = "wisrovi.rodriguez@gmail.com"
msg['Subject'] = "Subscription"

# add in the message body
message = "Thank you"
part1 = MIMEText(html_message, 'html')
part2 = MIMEText(message, 'plain')
msg.attach(part1)
msg.attach(part2)

# create server
server = smtplib.SMTP('{}: {}'.format(host, port))
server.starttls()

# Login Credentials for sending the mail
if len(token) > 0:
    password = token
server.login(msg['From'], password)

# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()

print("successfully sent email to %s:" % (msg['To']))