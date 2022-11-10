from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
import json

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sale, Product, DetSale


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            # Consultamos los productos de esa venta
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_createview')
        context['list_url'] = reverse_lazy('erp:sale_listview')
        context['entity'] = 'Ventas'
        return context


class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'erp.add_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    # Reverse_lazy devuelve la cadena de texto de esa url
    success_url = reverse_lazy('erp:sale_listview')
    url_redirect = success_url

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        #Ya que en el updateview creamos esa variable, aqui la mandamos vacia
        context['det'] = []
        return context

    def post(self, request, *kargs, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                # Recibimos TERM de la funcion del autocomplete en la variable DATA del AJAX
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()  # retornamos el item
                    # Debemos devolver un dict por cada valor porque asi lo maneja el autocomplete en el SELECT
                    item['value'] = i.name  # retornamos el nombre del item
                    data.append(item)
            elif action == 'add':
                """
                    Al recibir los datos, estamos enviando un dict, pero ese dict se convierte en un str, por eso debemos convertirlo en un dict de vuelta
                """
                with transaction.atomic():  # Revertimos las creaciones si hay algun error en el lote de creacion
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    # Cuando hacemos referncia a una FK ponemos _id para la relacion (por convencion)
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    # Registramos los productos, asociamos la venta
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        # precio de venta
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        # Para que se serialize cuando sea una serie de elementos.
        return JsonResponse(data, safe=False)

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


class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'erp.change_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    # Reverse_lazy devuelve la cadena de texto de esa url
    success_url = reverse_lazy('erp:sale_listview')
    url_redirect = success_url

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *kargs, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                # Recibimos TERM de la funcion del autocomplete en la variable DATA del AJAX
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()  # retornamos el item
                    # Debemos devolver un dict por cada valor porque asi lo maneja el autocomplete en el SELECT
                    item['value'] = i.name  # retornamos el nombre del item
                    data.append(item)
            elif action == 'edit':
                """
                    Al recibir los datos, estamos enviando un dict, pero ese dict se convierte en un str, por eso debemos convertirlo en un dict de vuelta
                """
                with transaction.atomic():  # Revertimos las creaciones si hay algun error en el lote de creacion
                    vents = json.loads(request.POST['vents'])
                    #Aqui solo debemos consultar el objeto y lo modificamos
                    #sale = Sale.objects.get(pk=self.get_object().pk)
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    # Cuando hacemos referncia a una FK ponemos _id para la relacion (por convencion)
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    #Por facilidad eliminamos todos los productos y los volvemos a crear.
                    sale.detsale_set.all().delete()
                    # Registramos los productos, asociamos la venta
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        # precio de venta
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        # Para que se serialize cuando sea una serie de elementos.
        return JsonResponse(data, safe=False)

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

    # lo enviamos dentro del contexto
    def get_details_products(self):
        """
        Debemos enviar el formato necesario para meterlo en la variable products, con su respectiva cantidad, precio etc
        """
        data = []
        try:
            # self.kwargs['pk']
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                """Ya que producto es una clave foranea, accedemos a el de esta forma"""
                item = i.prod.toJSON()
                item['cant'] = i.cant
                # No enviamos mas datos ya que el calculo del total y todo eso se hace desde js
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        """ Ya que obtuvimos una lista de diccionarios, esto va a convertir cada diccionario en un valor de diccionario
        pasara de ser una lista a un diccionario de diccionarios 
        """
        context['det'] = json.dumps(self.get_details_products()) #Lo convertimos a json pq eso necesitamos en JS
        return context


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_listview')
    permission_required = 'erp.delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context
