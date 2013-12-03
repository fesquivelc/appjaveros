from django.contrib.auth.models import User # LOS USUARIOS SON MANEJADOS POR DJANGO AUTOMATICAMENTE =)
from django.db import models

# Create your models here.
class Supermercado(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=10)
    web = models.CharField(max_length=200,null=True)
    logo = models.FileField(upload_to='static/images/supermercados')

    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ('nombre',)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=150,null=True)

    def __unicode__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length = 250,null=True)
    categoria = models.ForeignKey(Categoria)

    def __unicode__(self):
        return self.descripcion



class Catalogo(models.Model):
    stock = models.CharField(max_length=5)
    precio = models.DecimalField(max_digits=8,decimal_places=2,default='0.00')
    supermercado = models.ForeignKey(Supermercado)
    producto = models.ForeignKey(Producto)
    imagen = models.ImageField(upload_to='static/images/productos')

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
        return self.nombre + ' ' +str(self.recargo)


class Direccion(models.Model):
    tipo = models.CharField(max_length = 2)
    urbanizacion = models.CharField(max_length = 150)
    nombre = models.CharField(max_length = 250)
    numero = models.IntegerField()
    telefono = models.CharField(max_length=10)
    zona = models.ForeignKey(Zona)
    usuario = models.ManyToManyField(User)
    def __unicode__(self):
        return self.numero

    class Meta:
        ordering = ('nombre',)

class Repartidor(models.Model):
    dni = models.CharField(max_length = 8,primary_key=True)
    apellidos = models.CharField(max_length = 100)
    nombre = models.CharField(max_length = 100)
    disponibilidad = models.CharField(max_length = 1)

    def __unicode__(self):
        return self.nombre
    class Meta:
        ordering = ('apellidos',)


class Pedido(models.Model):
    hora_pedido = models.DateTimeField()
    fecha_pedido = models.DateTimeField()
    hora_entrega = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    estado = models.CharField(max_length = 1)
    comentario_cliente = models.TextField()
    repartidor = models.ForeignKey(Repartidor)
    zona = models.ForeignKey(Zona)
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.repartidor.nombre + ' ' + str(self.fecha_pedido) + ' ' + self.hora_fin
