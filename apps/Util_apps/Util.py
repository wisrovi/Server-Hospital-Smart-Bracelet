from apps.Util_apps.Decoradores import execute_in_thread
import requests
from django.contrib import messages

from authentication.Config.ConfigMail import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
import datetime



FOLDER_HTML = "PLANTILLAFCV"
config_files = dict()
config_files['alerta_caida'] = {'File': os.path.join(FOLDER_HTML, 'AlertaCaida.html'), 'Var': ['user', 'paciente']}
config_files['alerta_ppm'] = {'File': os.path.join(FOLDER_HTML, 'AlertaPPM.html'), 'Var': ['user', 'paciente']}
config_files['alerta_proximidad'] = {'File': os.path.join(FOLDER_HTML, 'AlertaProximidad.html'),
                                     'Var': ['user', 'paciente']}
config_files['alerta_temperatura'] = {'File': os.path.join(FOLDER_HTML, 'AlertaTemperatura.html'),
                                      'Var': ['user', 'paciente']}
config_files['change_password'] = {'File': os.path.join(FOLDER_HTML, 'CambioContrasena.html'), 'Var': ['user']}
config_files['datos_incorrectos'] = {'File': os.path.join(FOLDER_HTML, 'DatosIncorretos.html'), 'Var': ['user']}
config_files['inicio_sesion'] = {'File': os.path.join(FOLDER_HTML, 'InicioSeccion.html'), 'Var': ['user']}
config_files['nueva_baliza'] = {'File': os.path.join(FOLDER_HTML, 'NewBaliz.html') , 'Var': ['mac_baliza']}
config_files['nuevo_bracelet'] = {'File': os.path.join(FOLDER_HTML, 'NewBrazalet.html'), 'Var': ['mac_bracelet']}
config_files['bienvenido'] = {'File': os.path.join(FOLDER_HTML, 'welcome.html'), 'Var': ['user']}



def getFechaHora():
    fecha_hora = datetime.datetime.now()
    # fecha_hora = (fecha_hora.year, fecha_hora.month, fecha_hora.day, fecha_hora.hour, fecha_hora.minute, fecha_hora.second)
    return fecha_hora


@execute_in_thread(name="hilo request")
def generate_request_get(url, success_callback, error_callback):
    response = requests.get(url)
    #print(url)
    if response.status_code == 200:
        success_callback(response.json())
    else:
        error_callback(url)


from authentication.settings import MEDIA_ROOT
from django.contrib.staticfiles import finders


def ChargeImage(url_path):
    url_path_folder =  os.path.join("emails",  url_path )
    MIMEImage_search = "<" + url_path.split(".")[0] + ">"

    with open(finders.find(url_path_folder), 'rb') as fp:
        imagen_cargar = fp.read()
    msgImage = MIMEImage(imagen_cargar)
    msgImage.add_header('Content-ID', MIMEImage_search)
    # print(url_path_folder, MIMEImage_search)
    return msgImage


def send_mail(asunto, html, firma, correo):
    try:
        msg = MIMEMultipart('related')

        msg['Subject'] = asunto
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = correo

        part1 = MIMEText(html, 'html')
        msg.attach(part1)


        if isinstance(firma, list):
            # print("imagen", firma)
            for path_url in firma:
                mime_image = ChargeImage(path_url)
                msg.attach(mime_image)
        else:
            # print("plano")
            part2 = MIMEText(firma, 'plain')
            msg.attach(part2)

        #print("***************************************************** chao mundo *****************************************************")

        server = smtplib.SMTP('{}: {}'.format(EMAIL_HOST, EMAIL_PORT))
        #print("***************************************************** conect mundo *****************************************************")

        server.starttls()

        server.login(msg['From'], EMAIL_HOST_PASSWORD)
        #print("***************************************************** login mundo *****************************************************")

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        # print("***************************************************** {} *****************************************************".format(getFechaHora()))
    except NameError:
        print("failed send email to {} - error {}".format(correo, NameError))


@execute_in_thread(name="Send Mail")
def sendMail(asunto, html, firma, correo, request):
    if type(correo) != list:
        correo = [correo]

    for email in correo:
        send_mail(asunto, html, firma, email)

    # send_mail(
    #     asunto,
    #     strip_tags(html),
    #     firma,
    #     correo,
    #     fail_silently=False,
    #     html_message=html
    # )
    messages.success(request, "Mensaje enviado")
