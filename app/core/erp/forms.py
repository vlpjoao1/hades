from django.forms import ModelForm, TextInput, Textarea, forms

from core.erp.models import Category, Product


class CategoryForm(ModelForm):
    """
        Usamos el constructor para agregar valores a todo.
        Iteremos los items del formulario para agregarle atributos de forma automatica y no manual.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Iteremos el formulario para agregarle atributos a todos y no repetirlos en los widgets
        for form in self.visible_fields():
            # Se puede hacer de las dos formas.
            # form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                    'autocomplete': 'off'
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripción',
                    'rows':3
                }
            )
        }

    def save(self, commit=True):
        data = {}
        # con esto, recuperamos el formulario
        # podríamos hacerlo con self tambien
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    def clean(self):
        #obtenemos el objeto
        cleaned = super().clean()
        if len(cleaned['name']) <= 4:
            #Agregar errores a los campos.
            self.add_error('name','Te faltan caracteres')
            """Retornar errores que no son propios de los formularios, es decir, errores generales
            Este error se representa con form.non_field_errors (no tienen nada que ver con los fields)
            https://docs.djangoproject.com/en/3.0/ref/forms/api/"""
            raise forms.ValidationError('Validación XX')
        return cleaned

class ProductForm(ModelForm):
    """
        Usamos el constructor para agregar valores a todo.
        Iteremos los items del formulario para agregarle atributos de forma automatica y no manual.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Iteremos el formulario para agregarle atributos a todos y no repetirlos en los widgets
        for form in self.visible_fields():
            # Se puede hacer de las dos formas.
            # form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                    'autocomplete': 'off'
                }
            ),
        }
    def save(self, commit=True):
        data = {}
        # con esto, recuperamos el formulario
        # podríamos hacerlo con self tambien
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data