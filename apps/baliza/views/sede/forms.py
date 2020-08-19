from django.forms import ModelForm, TextInput, Textarea

from apps.baliza.models import Sede


class SedeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombreSede'].widget.attrs['autofocus'] = True

    class Meta:
        model = Sede
        fields = ['nombreSede',
                  'descripcion']  # se recomienda listar los campos, si no son muchos para mejor lectura del codigo
        # fields = '__all__'
        exclude = ['fechaRegistro', 'usuarioRegistra', 'indHabilitado']
        widgets = {
            'nombreSede': TextInput(
                attrs={'placeholder': 'Escribe un nombre para la sede'}
            ),
            'descripcion': Textarea(
                attrs={'placeholder': 'Escribe un descripción para la sede'}
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
