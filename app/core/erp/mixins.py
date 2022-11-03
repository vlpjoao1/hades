import datetime

from django.contrib import messages
from django.shortcuts import redirect


# Hereda de object que es la clase base de toda clase Python
from django.urls import reverse_lazy

from config import settings


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    # Si tenemos el metodo get_context_data tambien tendra estos datos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    #Con esto convertimos los permisos en una lista en todos los casos
    def get_perms(self):
        #Si es un str, convierte perms en una lista
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        #Caso contrario, devuelve perms
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('accounts:login')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        #Validamos si el usuario tiene esa lista de permisos
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request,'No tienes los permisos para acceder a este modulo.')
        return redirect(self.get_url_redirect())
