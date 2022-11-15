from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.erp.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from core.user.forms import UserForm
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
        context['create_url'] = reverse_lazy('user:user_createview')
        context['entity'] = 'Usuarios'
        context['list_url'] = reverse_lazy('user:user_listview')
        return context


"""
    Estas vistas se pueden usar solamente poniendo el modelo, el formulario y el template.
    Sobreescribir los métodos, ya es más para personalización.
"""
class UserCreateView(ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'user.user'
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    # Reverse_lazy devuelve la cadena de texto de esa url
    success_url = reverse_lazy('user:user_listview')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

    def post(self, request, *kargs, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.form_class(request.POST, request.FILES)
                data = form.save()
                # if form.is_valid():
                #     form.save()
                # else:
                #     data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
        """Este codigo sería para retornar los errores sin ajax"""
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponseRedirect(self.success_url)
        # #self.object es el objeto que se está creando. Si el objeto no se ha creado
        # #el valor deberá ser None, es decir, si ha ocurrido un error.
        # self.object = None
        # context = self.get_context_data(**kwargs)
        # context['form'] = form
        # # si queremos devolver los datos del formulario a la vista, podemos hacerlo así
        # # Enviando el formulario con su instancia de request.POST
        # return render(request, self.template_name, context)

class UserUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'user.change_user'
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_listview')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #Como object no tiene un valor, tenemos que asignarselo
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UserDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'user.delete_user'
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:user_listview')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # lo creamos en el dispatch porque al sobreescribir el metodo POST no existe de una el self.object
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # si sobreescribimos el método post, la variable self.object aun no tiene un valor,por lo qe
    # debemos asignarle el valor a self.object en el dispatch
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context