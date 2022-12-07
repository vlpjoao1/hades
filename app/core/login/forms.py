from django import forms

from core.user.models import User


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class':'form-control',
        'autocomplete':'off'
    }))

    # Esto se ejecuta cuando haces el form.is_valid()
    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            # Mensaje de error customizado por cada validación
            self._errors['error'] = self._errors.get('error',self.error_class())
            self._errors['error'].append(f'El usuario *{cleaned["username"]}* no existe')
            #raise forms.ValidationError(f'El usuario *{cleaned["username"]}* no existe')
        #si no hay erro retornamos la instancia de cleaned
        return cleaned

    def get_user(self):
        username = self.cleaned_data['username']
        return User.objects.get(username=username)