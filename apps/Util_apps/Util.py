from apps.Util_apps.Decoradores import execute_in_thread
import requests
from django.contrib import messages  # import messages
# from django.core.mail import send_mail
# from django.utils.html import strip_tags

from authentication.Config.ConfigMail import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os

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




@execute_in_thread(name="hilo request")
def generate_request_get(url, success_callback, error_callback):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        success_callback(response.json())
    else:
        error_callback(url)


def ChargeImage(url_path):
    #url_path =  os.path.join("images",  url_path )


    cid = url_path.split("/")
    cid_search = cid[-1].split(".")[0]
    MIMEImage_search = "<" + cid_search + ">"

    msgImage = None
    if os.path.isfile(url_path):
        with open(url_path, 'rb') as fp:
            print("poniendo imagenes en email", url_path)
            msgImage = MIMEImage(fp.read())
            msgImage.add_header('Content-ID', MIMEImage_search)
    print("No se encontro la imagen para cargar", url_path)
    return None




def send_mail(asunto, html, firma, correo):
    try:
        msg = MIMEMultipart('related')

        msg['Subject'] = asunto
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = correo


        part1 = MIMEText(html, 'html')

        if isinstance(firma, list):
            for path_url in firma:
                mime_image = ChargeImage(path_url)
                if mime_image is not  None:
                    msg.attach(mime_image)
        else:
            part2 = MIMEText(firma, 'plain')
            msg.attach(part2)

        msg.attach(part1)



        server = smtplib.SMTP('{}: {}'.format(EMAIL_HOST, EMAIL_PORT))
        server.starttls()


        server.login(msg['From'], EMAIL_HOST_PASSWORD)

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
    except:
        print("failed send email to %s:" % (correo))


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
