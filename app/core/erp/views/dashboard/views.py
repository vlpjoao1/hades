from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from core.erp.models import Sale


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    #Con esta variable obtenemos el calculo de cada mes del ano
    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            #Iteramos cada mes del ano para calcular las ventas de cada mes
            for m in range(1,13):
                #Obtenemos la sumatoria total de todas las ventas de cada mes
                total = Sale.objects.filter(date_joined__year=year,date_joined__month=m)\
                    .aggregate(result=Coalesce(Sum('total'), 0)).get('result')
                data.append(float(total))
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context