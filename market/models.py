from django.db import models

# Create your models here.
class Supermercado(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=10)
    web = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150)

    def __unicode__(self):
        return self.nombre

