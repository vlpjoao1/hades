"""En Pycharm, para ejecutar este archivo. Usaremos el Run/Debug
En la configuración crearemos una nueva configuración.
Seleccionamos un archivo python, le asigmanos nombre y seleccionamos el archivo tests.py y el entorno a ejecutar"""

from django.test import TestCase
#para poder usar el orm de django
from config.wsgi import *
from core.erp.models import Type, Employees

#Type(name='Crasentreno').save()

#querys

#__contains = Contiene
#__icontains =  Contiene (ignorecase)
obj = Type.objects.filter(name__contains='Pre')

#__startswith = Empieza con
#__istarswith = Empieza con (ignorecase)
obj = Type.objects.filter(name__startswith="p")

#__in=[<list_values>] = Busca con esos valores
obj = Type.objects.filter(name__in=['Preentreno','Joao'])

#muestra el código
obj = Type.objects.filter(name__contains='Pre').query

#excluye valores
obj = Type.objects.filter(name__contains='o').exclude(name__istartswith='J')

#Puedes hacer que traiga un rango de valores
obj = Type.objects.filter(name__contains='o')[:3]

#---------------------------------------------------------------------
#podemos hacer subconsultas. Usando como referencia los atributos de la clave foránea.
#Con __<attr> podemos hacer referencia a cualquier atributo de la clave foranea
obj = Employees.objects.filter(type__name='Joao')

#Podemos buscar por rangos de fechas. Cada tipo de valor puede tener criterios de busqueda diferentes
    #obj = Employees.objects.filter(date_created__range=['rango de fechas'])
print(obj)