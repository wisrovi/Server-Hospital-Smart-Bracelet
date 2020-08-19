from django import forms
from django.forms import ModelForm, TextInput, Textarea

from apps.baliza.models import Piso, Bracelet, BraceletUmbrals


class CreateBraceletForm(forms.Form):
    mac_bracelet = forms.CharField(
        label='MAC Bracelet',
        max_length=17,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'mac_bracelet',
                   'placeholder': 'Escribe la MAC del Bracelet', 'autocomplete': 'off'}))
    bracelet_major = forms.CharField(
        label='Total lote',
        max_length=5,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_major',
                   'placeholder': 'Escribe la cantidad total de fabricación de lote de Bracelets',
                   'autocomplete': 'off'}))
    bracelet_minor = forms.CharField(
        label='Serial dentro del lote',
        max_length=5,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_minor',
                   'placeholder': 'Escribe el número de fabricación dentro del lote fabricado', 'autocomplete': 'off'}))
    bracelet_tx_power = forms.CharField(
        label='TxPower (1mt) distancia',
        max_length=4,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_tx_power',
                   'placeholder': 'Escribe la Potencia (DB) a un metro de distancia (médido)', 'autocomplete': 'off'}))
    description_bracelet = forms.CharField(
        label='Descripción Bracelet',
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'description_bracelet',
                   'placeholder': 'Escribe una descripción para el Bracelet', 'autocomplete': 'off'}))

    bracelet_temp_min = forms.CharField(
        label='Temperatura mínima',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_temp_min',
                   'placeholder': 'Hipotermia (20°C<Temp<33°C)', 'autocomplete': 'off', 'value': '30'}))
    bracelet_temp_max = forms.CharField(
        label='Temperatura Máxima',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_temp_max',
                   'placeholder': 'Fiebre (Temp>37°C)', 'autocomplete': 'off', 'value': '38'}))
    bracelet_ppm_min = forms.CharField(
        label='Pulso Cardiaco mínimo',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_ppm_min',
                   'placeholder': 'Infarto (PPM<55)', 'autocomplete': 'off', 'value': '52'}))
    bracelet_ppm_max = forms.CharField(
        label='Pulso Cardiaco máximo',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'bracelet_ppm_max',
                   'placeholder': 'Taquicardia (PPM>125)', 'autocomplete': 'off', 'value': '130'}))

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


class BraceletForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['macDispositivo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Bracelet
        fields = ['macDispositivo',
                  'major',
                  'minor',
                  'txPower',
                  'descripcion']  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['fechaRegistro', 'usuarioRegistra', 'indHabilitado']
        widgets = {
            'macDispositivo': TextInput(
                attrs={'placeholder': 'Escribe la MAC para el Bracelet'}
            ),
            'major': TextInput(
                attrs={'placeholder': 'Escribe la cantidad total de fabricación de lote de Bracelets'}
            ),
            'minor': TextInput(
                attrs={'placeholder': 'Escribe el número de fabricación dentro del lote fabricado'}
            ),
            'txPower': TextInput(
                attrs={'placeholder': 'Escribe la Potencia (DB) a un metro de distancia (médido)'}
            ),
            'descripcion': Textarea(
                attrs={'placeholder': 'Escribe una descripción para el Bracelet'}
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


class BraceletUmbralesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['minimaTemperatura'].widget.attrs['autofocus'] = True

    class Meta:
        model = BraceletUmbrals
        fields = ['minimaTemperatura',
                  'maximaTemperatura',
                  'minimoPulsoCardiaco',
                  'maximaPulsoCardiaco', ]  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['bracelet','fechaRegistro', 'usuarioRegistra']
        widgets = {
            'minimaTemperatura': TextInput(
                attrs={'placeholder': 'Hipotermia (20°C<Temp<33°C)'}
            ),
            'maximaTemperatura': TextInput(
                attrs={'placeholder': 'Fiebre (Temp>37°C)'}
            ),
            'minimoPulsoCardiaco': TextInput(
                attrs={'placeholder': 'Infarto (PPM<55)'}
            ),
            'maximaPulsoCardiaco': TextInput(
                attrs={'placeholder': 'Taquicardia (PPM>125)'}
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
