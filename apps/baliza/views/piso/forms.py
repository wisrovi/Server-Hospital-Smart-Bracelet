from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, forms

from apps.baliza.models import Piso, Sede


class PisoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['piso'].widget.attrs['autofocus'] = True
        self.fields['sede'] = ModelChoiceField(queryset=Sede.objects.filter(indHabilitado=True))

    class Meta:
        model = Piso
        fields = ['sede',
                  'piso',
                  'descripcion']  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['fechaRegistro', 'usuarioRegistra', 'indHabilitado']
        widgets = {
            'piso': TextInput(
                attrs={'placeholder': 'Escribe un número para el Piso'}
            ),
            'descripcion': Textarea(
                attrs={'placeholder': 'Escribe un descripción para la Piso'}
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