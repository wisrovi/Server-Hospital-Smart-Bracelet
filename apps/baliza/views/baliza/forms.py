from django import forms
from django.forms import ModelForm, TextInput, ChoiceField

from apps.baliza.models import Piso, Baliza, InstalacionBaliza


class CreateBalizaForm(forms.Form):
    mac_baliza = forms.CharField(
        label='MAC Baliza',
        max_length=17,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'mac_baliza',
                   'placeholder': 'Escribe la MAC de la Baliza', 'autocomplete': 'off'}))
    description_baliza = forms.CharField(
        label='Descripción Baliza',
        max_length=17,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'description_baliza',
                   'placeholder': 'Escribe una descripción para la Baliza', 'autocomplete': 'off'}))
    x_position_baliza = forms.CharField(
        label='Posición en X para la Baliza',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'x_position_baliza',
                   'placeholder': 'Escribe una posición en X para la Baliza', 'autocomplete': 'off'}))
    y_position_baliza = forms.CharField(
        label='Posición en Y para la Baliza',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'y_position_baliza',
                   'placeholder': 'Escribe una posición en Y para la Baliza', 'autocomplete': 'off'}))
    piso_instalacion_baliza = forms.ModelChoiceField(
        queryset=Piso.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'name': 'piso_instalacion_baliza', }))

    def save(self, commit=True):
        data = dict()
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class BalizaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['macDispositivoBaliza'].widget.attrs['autofocus'] = True

    class Meta:
        model = Baliza
        fields = ['macDispositivoBaliza',
                  'descripcion']  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['fechaRegistro', 'usuarioRegistra', 'indHabilitado']
        widgets = {
            'bracelet': TextInput(
                attrs={'placeholder': 'Escribe la MAC para la Baliza'}
            ),
            'descripcion': TextInput(
                attrs={'placeholder': 'Escribe una descripción para la Baliza'}
            ),
        }

    def save(self, commit=True):
        data = dict()
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class BalizaInstalacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['instalacionX'].widget.attrs['autofocus'] = True

    class Meta:
        model = InstalacionBaliza
        fields = ['instalacionX',
                  'instalacionY',
                  'piso', ]  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['baliza','fechaRegistro', 'usuarioRegistra', 'indHabilitado']
        widgets = {
            'instalacionX': TextInput(
                attrs={'placeholder': 'Hipotermia (20°C<Temp<33°C)'}
            ),
            'instalacionY': TextInput(
                attrs={'placeholder': 'Fiebre (Temp>37°C)'}
            ),
        }

    def save(self, commit=True):
        data = dict()
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
