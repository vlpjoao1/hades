from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale


class SaleCreateView(ValidatePermissionRequiredMixin,CreateView):
    permission_required = 'erp.add_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    # Reverse_lazy devuelve la cadena de texto de esa url
    success_url = reverse_lazy('index')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

    def post(self, request, *kargs, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.form_class(request.POST)
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
