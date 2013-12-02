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

class Producto(models.Model):
    descripcion = models.CharField(max_length = 250)
    categoria = models.ForeignKey(Categoria)

    def __unicode__(self):
        return self.descripcion



class Catalogo(models.Model):
    stock = models.CharField(max_length=5)
    precio = models.CharField(max_length= 10)
    supermercado = models.ForeignKey(Supermercado)
    producto = models.ForeignKey(Producto)

    def __unicode__(self):
        return self.producto.descripcion + self.supermercado.nombre

class Oferta(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    catalogo = models.ForeignKey(Catalogo)

    def __unicode__(self):
        return 'oferta: '+str(self.fecha_inicio) + self.catalogo.producto.descripcion +  self.catalogo.supermercado.nombre




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
    hora_pedido = models.DateTimeField()
    fecha_pedido = models.DateTimeField()
    hora_entrega = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    estado = models.CharField(max_length = 1)
    comentario_cliente = models.TextField()
    repartidor = models.ForeignKey(Repartidor)
    zona = models.ForeignKey(Zona)

    def __unicode__(self):
        return self.repartidor.nombre + ' ' + str(self.fecha_pedido) + ' ' + self.hora_fin
