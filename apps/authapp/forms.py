from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'text', 'name': 'username', 'placeholder': 'Escribe tu nombre de usuario'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'password', 'name': 'password', 'placeholder': 'Escribe tu contraseña'}))


class RegistrationForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'text', 'name': 'firstname', 'placeholder': 'Escribe tu nombre'}))
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'text', 'name': 'lastname', 'placeholder': 'Escribe tu apellido'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'email', 'name': 'email', 'placeholder': 'Escribe tu email'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'password', 'name': 'password', 'placeholder': 'Escribe tu contraseña'}))
    confirm_password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'password', 'name': 'confirm-password',
               'placeholder': 'Escriba su contraseña nuevamente'}))
