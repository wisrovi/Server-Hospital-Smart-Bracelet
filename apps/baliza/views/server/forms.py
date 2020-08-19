from django import forms

from apps.baliza.models import Sede, Piso


class PackBraceletForm(forms.Form):
    key = forms.CharField(
        label='Key',
        max_length=5000,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'y_position_baliza',
                   'placeholder': 'Escribe una key', 'autocomplete': 'off'}))
    string_pack = forms.CharField(
        label='StringPack',
        max_length=5000,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text', 'name': 'y_position_baliza',
                   'placeholder': 'Escribe un value', 'autocomplete': 'off'}))


class FiltrarGrafica(forms.Form):
    # select2 es una clase que se pone en una lista desplegable para que este haga update a otras listas, select anidados
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'name': 'Sede'
            }
        )
    )

    ubicacion = forms.ModelChoiceField(
        queryset=Piso.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2',
                'name': 'Piso',
                'disable': 'true'
            }
        )
    )
