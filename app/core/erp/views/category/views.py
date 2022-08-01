from django.shortcuts import render
from django.views.generic import ListView

from core.erp.models import Category


def category_list(request):
    data = {
        'title': 'Listado de Categorías',
        'categories': Category.objects.all()
    }
    return render(request, 'category/list.html', data)


class CategoryList(ListView):
    model = Category
    template_name = 'category/list.html'

    #Se puede listar solo con modelo y template_name. Hace automaticamente un objects.all
    #Puedes enviar la consulta desde aquí o usar el get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de categorías'
        return context
