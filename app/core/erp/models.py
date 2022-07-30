from contextlib import nullcontext
from django.db import models
from datetime import datetime


# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

        # Como queremos que se llame la tabla
        db_table = 'tipo_emp'
        # como se va a ordenar al hacer un listado
        # Descentende -<campo> ej: ['-id']
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria_emp'
        ordering = ['id']


class Employees(models.Model):
    # verbose_name, Cuando mapee este clase a modo de formulario el atributo <Label> se mostrará con el valor de este atributo
    dni = models.CharField(max_length=10, unique=True, verbose_name='DNI', null=True)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro', null=True)
    # Auto_now= Al crear el registro, se agrará la fecha actual
    date_created = models.DateTimeField(auto_now=True)
    # Auto_now_add= Cada vez que la entidad se actualice se cambia
    date_updated = models.DateTimeField(auto_now_add=True)
    age = models.PositiveIntegerField(default=0)
    salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    state = models.BooleanField(default=True)
    # Para guardarlo por fechas
    avatar = models.ImageField(upload_to='avatar/%Y/%m', null=True)
    cvitae = models.FileField(upload_to='cvitae/%Y/%m', null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    categ = models.ManyToManyField(Category)

    # Esto será la representación del objeto cuando lo llames y muestres. Lo mostrará como un STR
    def __str__(self):
        return self.dni

    class Meta:
        # Para cuando registres el modelo en el admin de django
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

        # Como queremos que se llame la tabla
        db_table = 'empleado'
        # como se va a ordenar al hacer un listado
        # Descentende -<campo> ej: ['-id']
        ordering = ['id']
