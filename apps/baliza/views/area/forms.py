from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, forms

from apps.baliza.models import Piso, Sede, Area


class AreaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['area'].widget.attrs['autofocus'] = True
        self.fields['piso'] = ModelChoiceField(queryset=Piso.objects.filter(indHabilitado=True))

    class Meta:
        model = Area
        fields = ['piso',
                  'area',
                  'xInicial',
                  'xFinal',
                  'yInicial',
                  'yFinal',
                  'descripcion']  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['fechaRegistro', 'usuarioRegistra', 'indHabilitado']
        widgets = {
            'area': TextInput(
                attrs={'placeholder': 'Escribe un nombre para el Area'}
            ),
            'xInicial': TextInput(
                attrs={'placeholder': 'Escribe un punto inicial de ubicación en X (metros)'}
            ),
            'xFinal': TextInput(
                attrs={'placeholder': 'Escribe un punto final de ubicación en X (metros)'}
            ),
            'yInicial': TextInput(
                attrs={'placeholder': 'Escribe un punto inicial de ubicación en Y (metros)'}
            ),
            'yFinal': TextInput(
                attrs={'placeholder': 'Escribe un punto final de ubicación en Y (metros)'}
            ),
            'descripcion': Textarea(
                attrs={'placeholder': 'Escribe un descripción para el Area'}
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
