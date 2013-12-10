from django.conf import settings
from django.contrib.auth.models import User # LOS USUARIOS SON MANEJADOS POR DJANGO AUTOMATICAMENTE =)
from django.db import models
import datetime

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
    unidad = models.CharField(max_length=10,choices=(
                                                        ('Kg','Kilogramos'),
                                                        ('g','gramos'),
                                                        ('uni','unidades'),
                                                        ('caj','cajas')
                                                    ))

    def __unicode__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = 'Productos'
        ordering=('nombre','descripcion',)


class Catalogo(models.Model):
    stock = models.IntegerField(max_length=5,default='0')
    precio = models.DecimalField(max_digits=8,decimal_places=2,default='0.00')
    supermercado = models.ForeignKey(Supermercado)
    producto = models.ForeignKey(Producto)
    imagen = models.ImageField(upload_to='static/images/productos')

    def __unicode__(self):
        return self.producto.descripcion + ' ' + self.supermercado.nombre

class Oferta(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField(null=True)
    catalogo = models.ForeignKey(Catalogo)
    estado = models.CharField(max_length=1,choices=(
                                                    ('A','Activo'),
                                                    ('N','No activo'),
                                                ))

    def __unicode__(self):
        return 'oferta: '+str(self.fecha_inicio) + self.catalogo.producto.descripcion +  self.catalogo.supermercado.nombre

class Zona(models.Model):
    nombre = models.CharField(max_length = 45)
    descripcion = models.TextField()
    recargo = models.IntegerField()

    def __unicode__(self):
        return 'nombre: %s - recargo: %s' % (self.nombre,self.recargo)

    class Meta:
        ordering = ('recargo','nombre',)

class Urbanizacion(models.Model):
    nombre = models.CharField(max_length=150)
    zona = models.ForeignKey(Zona)

    def __unicode__(self):
        return 'Zona: %s - Nombre: %s' % (self.nombre,self.zona)

    class Meta:
        verbose_name_plural = 'Urbanizaciones'
        ordering = ('zona','nombre',)

class Calle(models.Model):
    urbanizacion = models.ForeignKey(Urbanizacion)
    tipo = models.CharField(max_length = 2, choices=(('Av','Avenida'),('Jr','Jiron')))
    nombre = models.CharField(max_length=150)

    def __unicode__(self):
        return '%s %s Urb. %s' % (self.tipo,self.nombre,self.urbanizacion.nombre)
class Direccion(models.Model):
    numero = models.IntegerField()
    telefono = models.CharField(max_length=10)
    calle = models.ForeignKey(Calle)
    usuario = models.ManyToManyField(settings.AUTH_USER_MODEL)
    def __unicode__(self):
        return '%s %s %s Urb. %s' % (self.calle.tipo,self.calle.nombre,self.numero,self.calle.urbanizacion.nombre)

    class Meta:
        verbose_name_plural = 'Direcciones'
        ordering = ('calle',)

class Repartidor(models.Model):
    dni = models.CharField(max_length = 8,primary_key=True)
    apellidos = models.CharField(max_length = 100)
    nombre = models.CharField(max_length = 100)
    disponibilidad = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = 'Repartidores'
        ordering = ('apellidos',)


class Pedido(models.Model):
    hora_pedido = models.TimeField(default=datetime.datetime.now())
    fecha_pedido = models.DateField(default=datetime.datetime.now())
    hora_entrega = models.TimeField(null=True)
    fecha_entrega = models.DateField(null=True)
    estado = models.CharField(max_length = 1, default='S', choices=(
                                                        ('S', 'Sin salir'),
                                                        ('A', 'Atendiendo'),
                                                        ('E', 'Entregado'),
                                                    ))
    direccion = models.ForeignKey(Direccion)
    comentario_cliente = models.TextField(null=True)
    confirmacion_cliente = models.BooleanField(default=False)
    repartidor = models.ForeignKey(Repartidor, null=True)
    usuario = models.ForeignKey(User)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return 'usuario: %s - fecha de pedido: %s - hora de pedido: %s' % (self.usuario.get_username(),self.fecha_pedido,self.hora_pedido)

    class Meta:
        ordering = ('fecha_pedido',)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    catalogo = models.ForeignKey(Catalogo)
    cantidad = models.IntegerField()

    def __unicode__(self):
        return 'pedido: %s - producto: %s' % (self.pedido.id,self.catalogo.producto.nombre)