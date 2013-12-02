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

class Catalogo(models.Model):
    stock = models.CharField(max_length=5)
    precio = models.CharField(max_length= 10)
    supermercado = models.ForeignKey(Supermercado)

    def __unicode__(self):
        return self.stock

class Oferta(models.Model):
    fecha_inicio = models.DateTimeFields()
    fecha_fin = models.DateTimeFields()
    hora_inicio = models.DateTimeFields()
    hora_fin = models.DateTimeFields()
    catalogo = models.ForeignKey(Catalogo)

    def __unicode__(self):
        return self.hora_inicio
        return self.hora_fin
        return self.fecha_inicio
        return self.fecha_fin

class Producto(models.Model):
    descripcion = models.CharField(max_length = 250)
    categoria = models.ForeignKey(Categoria)

    def __unicode__(self):
        return self.descripcion


class Zona(models.Model):
    nombre = models.CharField(max_length = 45)
    descripcion = models.TextField()
    recargo = models.IntegerField()

    def __unicode__(self):
        return self.recargo
        return self.nombre

class Direccion(models.Model):
    tipo = models.CharField(max_length = 2)
    urbanizacion = models.CharField(max_length = 150)
    nombre = models.CharField(max_length = 250)
    numero = models.IntegerField()
    zona = models.ForeignKey(Zona)

    def __unicode__(self):
        return self.numero

class Repartidor(models.Model):
    apellidos = models.CharField(max_length = 100)
    nombre = models.CharField(max_length = 100)
    dni = models.CharField(max_length = 8)
    disponibilidad = models.CharField(max_length = 1)

    def __unicode__(self):
        return self.nombre


class Pedido(models.Model):
    hora_pedido = models.DateTimeFields()
    fecha_pedido = models.DateTimeFields()
    hora_entrega = models.DateTimeFields()
    fecha_entrega = models.DateTimeFields()
    estado = models.CharField(max_length = 1)
    comentario_cliente = models.TextField()
    repartidor = models.ForeignKey(Repartidor)
    zona = models.ForeignKey(Zona)

    def __unicode__(self):
        return self.fecha_entrega
        return self.fecha_pedido
        return self.hora_entrega
        return self.hora_pedido
