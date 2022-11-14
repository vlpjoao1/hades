from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.erp.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from core.user.models import User


class UserListView(ValidatePermissionRequiredMixin, ListView):
    permission_required = 'user.view_user'
    model = User
    template_name = 'user/list.html'

    # decoradores: Son funciones que añaden funcionalidades a otras funciones.
    # ej: si queremos añadir una validación al metodo dispatch, podemos usar un decorador.

    # dispatch: Es un metodo que se ejecuta al principio de la llamada de una vista. Se encarga de
    # redireccionar a la peticion que se haga, sea post o get.
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
            # data = User.objects.get(pk=request.POST['id']).toJson()
        except Exception as e:
            data['error'] = str(e)
        # Para serializar los elementos que no sean diccionaros, debes establecer safe=False
        # Ya que estamos enviando una lista de diccionarios, no un diccionario solo
        return JsonResponse(data, safe=False)

    # Se puede listar solo con modelo y template_name. Hace automaticamente un objects.all
    # Puedes enviar la consulta desde aquí o usar el get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = ''#reverse_lazy('erp:category_createview')
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('user:user_listview')
        return context


"""
    Estas vistas se pueden usar solamente poniendo el modelo, el formulario y el template.
    Sobreescribir los métodos, ya es más para personalización.
"""
