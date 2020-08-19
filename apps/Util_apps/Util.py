from apps.Util_apps.Decoradores import execute_in_thread
import requests
from django.contrib import messages  # import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags


@execute_in_thread(name="hilo request")
def generate_request_get(url, success_callback, error_callback):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        success_callback(response.json())
    else:
        error_callback(url)


@execute_in_thread(name="Send Mail")
def sendMail(asunto, html, firma, correo, request):
    if type(correo) != list:
        correo = [correo]

    send_mail(
        asunto,
        strip_tags(html),
        firma,
        correo,
        fail_silently=False,
        html_message=html
    )
    messages.success(request, "Mensaje enviado")
