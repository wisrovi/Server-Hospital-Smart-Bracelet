from apps.Util_apps.Decoradores import execute_in_thread
import requests
from django.contrib import messages  # import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

@execute_in_thread(name="hilo request")
def generate_request_get(url, success_callback, error_callback):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        success_callback(response.json())
    else:
        error_callback(url)


from authentication.Config.ConfigMail import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
def send_mail(asunto, html, firma, correo):
    try:
        msg = MIMEMultipart()

        msg['From'] = EMAIL_HOST_USER
        msg['To'] = correo
        msg['Subject'] = asunto

        part1 = MIMEText(html, 'html')
        part2 = MIMEText(firma, 'plain')

        msg.attach(part1)
        msg.attach(part2)

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
