# from django.core.mail import send_mail
# EXAMPLE 1:
# send_mail(
#     "asunto prueba",
#     "Hola mundo",
#     "WISROVI",
#     ["wisrovi.rodriguez@gmail.com"],
#     fail_silently=False,
# )


# ESAMPLE 2:
# listaCorreosDestinatarios = list()
# listaCorreosDestinatarios.append("wisrovi.rodriguez@gmail.com")
# diccionarioDatos = dict()
# diccionarioDatos['ADMIN'] = "ejemplo de datos del diccionario"
# html_message = render_to_string('template_email.html', diccionarioDatos)
# asunto = "asunto del correo"
# firmaResumenRemitente = "firma del remitente"
# send_mail(
#     asunto,
#     strip_tags(html_message),
#     firmaResumenRemitente,
#     listaCorreosDestinatarios,
#     fail_silently=False,
#     html_message=html_message
# )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = str()
EMAIL_PORT = int()
EMAIL_HOST_USER = str()
EMAIL_HOST_PASSWORD = str()
EMAIL_USE_TLS = bool()
EMAIL_USE_SSL = bool()

usar = 'FCV'

if usar == 'FCV':
    EMAIL_HOST = 'webmail.fcv.org'
    EMAIL_HOST_USER = 'hospitalsmartbracelet@fcv.org'
    EMAIL_HOST_PASSWORD = 'fBy3clj9fOoKDoj9OtSk'
else:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'hospitalsmartbracelet@gmail.com'
    EMAIL_HOST_PASSWORD = 'Agosto.2020'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False