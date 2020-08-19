from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

import apps.Util_apps.Util as Utilities
from apps.authapp.forms import LoginForm, RegistrationForm
import authentication.Config.PREFERENCES as Preferences


def signin(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        data = dict()
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                diccionarioDatos = dict()
                diccionarioDatos['NAME'] = username
                diccionarioDatos['NAME'] = request.user.email

                listaCorreosDestinatarios = list()
                listaCorreosDestinatarios.append(request.user.email)
                html_message = render_to_string('email_user_create.html', diccionarioDatos)
                asunto = "Bienvenido, has iniciado sesion en tu cuenta"
                firmaResumenRemitente = Preferences.NAME_APP

                Utilities.sendMail(asunto, html_message, firmaResumenRemitente, request.user.email, request)

                data['redirec'] = 'ok'
            else:
                data['error'] = "Usuario o contraseña no son correctos."
        else:
            data['error'] = "Ha ocurrido un error, por favor revise los datos ingresados e intente nuevamente."
        return JsonResponse(data, safe=False)

    context = dict()
    context['form'] = forms
    context['TITLE'] = Preferences.NAME_APP
    return render(request, 'signin.html', context)


def signup_confirm_email(request):
    forms = RegistrationForm()
    code_verification = ""
    if request.method == 'POST':
        parametros = request.POST
        if len(parametros) == 7:
            data = dict()
            if len(parametros['code_verification']) > 0 \
                    and len(parametros['code']) > 0:
                if parametros['code_verification'] == parametros['code']:
                    print('OK')

                    paquete = dict()
                    paquete['firstname'] = parametros['firstname']
                    paquete['lastname'] = parametros['lastname']
                    paquete['email'] = parametros['email']

                    import base64
                    import json
                    # paquete = gzip.compress(bytes(json.dumps(paquete), 'utf-8'))
                    paquete = base64.urlsafe_b64encode(bytes(json.dumps(paquete), 'utf-8')).decode('utf-8')

                    data = dict()
                    data['redirec'] = paquete
                    return JsonResponse(data, safe=False)
                else:
                    data['Value_button'] = 'VALIDAR CODIGO'
                    print('hola mundo')
            else:
                if len(parametros['code_verification']) < 1 \
                        or len(parametros['code_verification']) > 0:
                    if str(parametros['email']).find(Preferences.CORREO_PERMITIDO) >= 0:
                        from random import randint
                        code_verification = str(randint(10000000, 99999999))
                        data['code_verification'] = code_verification

                        diccionarioDatos = dict()
                        diccionarioDatos['NAME'] = parametros['firstname']
                        diccionarioDatos['LASTNAME'] = parametros['lastname']
                        diccionarioDatos['EMAIL'] = parametros['email']
                        diccionarioDatos['TOKEN'] = code_verification

                        listaCorreosDestinatarios = list()
                        listaCorreosDestinatarios.append(parametros['email'])
                        html_message = render_to_string('email_user_create.html', diccionarioDatos)
                        asunto = "Bienvenido, falta confirmar correo"
                        firmaResumenRemitente = Preferences.NAME_APP

                        Utilities.sendMail(asunto, html_message, firmaResumenRemitente, parametros['email'], request)

                    else:
                        data[
                            'error'] = 'Por favor digite un correo institucional con extensión: ' + Preferences.CORREO_PERMITIDO + "."
                else:
                    data['code_verification'] = parametros['code_verification']
                if len(parametros['code_verification']) > 0:
                    data['Value_button'] = 'VALIDAR NUEVO CODIGO'
                else:
                    data['Value_button'] = 'VALIDAR CODIGO'
            return JsonResponse(data, safe=False)
        else:
            data = dict()
            data['error'] = 'Datos invalidos'
            return JsonResponse(data, safe=False)
    context = dict()
    context['form'] = forms
    context['Value_button'] = 'VALIDAR EMAIL'
    context['code_verification'] = code_verification
    context['TITLE'] = Preferences.NAME_APP
    return render(request, 'signup_confim_email.html', context)


def signup(request):
    forms = RegistrationForm()
    value_button = 'Guardar'
    context = dict()
    if request.method == 'GET':
        parametros = request.GET
        datosRecibidos = parametros['D']
        import base64
        import json
        datosRecibidos = base64.urlsafe_b64decode(datosRecibidos)
        # datosRecibidos = gzip.decompress(datosRecibidos).decode('utf-8')
        datosRecibidos = json.loads(datosRecibidos)
        context['firstname'] = datosRecibidos['firstname']
        context['lastname'] = datosRecibidos['lastname']
        context['email'] = datosRecibidos['email']

    if request.method == 'POST':
        parametros = request.POST
        forms = RegistrationForm(parametros)
        if forms.is_valid():
            firstname = forms.cleaned_data['firstname']
            lastname = forms.cleaned_data['lastname']
            email = forms.cleaned_data['email']
            username = email
            password = forms.cleaned_data['password']
            confirm_password = forms.cleaned_data['confirm_password']
            if password == confirm_password:
                try:
                    diccionarioDatos = dict()
                    diccionarioDatos['USERNAME'] = username
                    diccionarioDatos['NAME'] = firstname
                    diccionarioDatos['LASTNAME'] = lastname
                    diccionarioDatos['EMAIL'] = email

                    listaCorreosDestinatarios = list()
                    listaCorreosDestinatarios.append(email)
                    html_message = render_to_string('email_user_create.html', diccionarioDatos)
                    asunto = "Bienvenido, su cuenta ha sido creada correctamente"
                    firmaResumenRemitente = Preferences.NAME_APP

                    Utilities.sendMail(asunto, html_message, firmaResumenRemitente, email, request)

                    User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                             last_name=lastname)

                    data = dict()
                    data['redirec'] = 'ok'
                    return JsonResponse(data, safe=False)
                except:
                    context = {
                        'form': forms,
                        'error': 'This Username Already exists!'
                    }
                    return render(request, 'signup.html', context)

    context['form'] = forms
    context['Value_button'] = value_button
    context['TITLE'] = Preferences.NAME_APP

    return render(request, 'signup.html', context)


def signout(request):
    logout(request)
    return redirect('signin')


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
