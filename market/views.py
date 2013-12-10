# coding=utf-8
from django.core.mail.message import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from market.models import *
from market.forms import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from cart import Cart

def add_to_cart(request, catalogo_id, cantidad):
    catalogo = Catalogo.objects.get(id=catalogo_id)
    cart = Cart(request)
    cart.add(catalogo, catalogo.precio, 1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def catalogos_view(request, market, cat):
    supermercado = Supermercado.objects.get(id=int(market))
    mnuCategorias = Categoria.objects.all()
    nombreProducto = ''
    if request.method == "POST":
        form = BusquedaProductoForm(request.POST)
        if form.is_valid():
            print 'Es valido'
            nombreProducto = form.cleaned_data['nombreProducto']
    else:
        form = BusquedaProductoForm()
    if int(cat):
        catalogos = Catalogo.objects.filter(supermercado=supermercado).filter(
            producto__in=Producto.objects.filter(nombre__contains=nombreProducto).filter(
                categoria=Categoria.objects.get(id=int(cat))))
    else:
        catalogos = Catalogo.objects.filter(supermercado=supermercado).filter(
            producto__in=Producto.objects.filter(nombre__contains=nombreProducto))
    ctx = {'mnuCategorias': mnuCategorias, 'catalogos': catalogos, 'form': form, 'supermercado': supermercado,
           'catActual': int(cat)}
    return render_to_response('catalogos.html', ctx, context_instance=RequestContext(request))


def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')


def contacto_view(request):
    info_enviado = False
    email = ''
    titulo = ''
    contenido = ''

    if request.method == 'POST':
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['email']
            titulo = formulario.cleaned_data['titulo']
            contenido = formulario.cleaned_data['contenido']

            #configuracion para enviar el mensaje a GMAIL
            html_content = 'Informacion recibida <br/> <br/> <h3> ******* Mensaje de %s ******* </h3> <br/> <br/>' \
                           '<h4>Titulo: %s </h4>' \
                           '<p>%s</p>' % (email, titulo, contenido)

            to = 'project.pythonisa@gmail.com'
            msje = EmailMultiAlternatives('Correo de contacto', html_content, 'from@server.com', [to])
            msje.attach_alternative(html_content, 'text/html')
            msje.send()
    else:
        formulario = ContactoForm()
    ctx = {'enviado': info_enviado, 'email': email, 'titulo': titulo, 'contenido': contenido, 'form': formulario}
    return render_to_response('contacto.html', ctx, context_instance=RequestContext(request))


def get_cart(request):
    if request.method == 'POST':
        pedido = Pedido()

        tamano = int(request.POST['tamano'])
        id_direccion = int(request.POST['direccion'])
        precio_total = float(request.POST['precio_total'])

        #LLENAMOS LOS DATOS BASICOS PARA EL PEDIDO
        pedido.direccion = Direccion.objects.get(id = id_direccion)
        pedido.usuario = request.user
        pedido.precio_total = precio_total

        #GUARDAMOS EL PEDIDO
        pedido.save()

        for i in range(1, tamano):
            #INSTANCIAMOS UN DETALLEPEDIDO
            detallePedido = DetallePedido()

            #RECUPERAMOS EL VALOR DEL ID DEL CATALOGO
            id_catalogo = int(request.POST['catalogo-%s' % i])

            #RECUPERAMOS LA CANTIDAD DE PRODUCTO PEDIDO
            cantidad = int(request.POST['cantidad-%s' % i])

            #OBTENEMOS UN OBJETO CATALOGO
            catalogo = Catalogo.objects.get(id=id_catalogo)

            #UTILIZAMOS ESTA INFORMACION PARA EL DETALLEPEDIDO
            detallePedido.pedido = pedido
            detallePedido.catalogo = catalogo
            detallePedido.cantidad = cantidad

            #GUARDAMOS EL DETALLE
            detallePedido.save()

        ruta = '/pedidos/detalle/%s/' % pedido.id

        return HttpResponseRedirect(ruta)


    else:
        return render_to_response('carrito.html', dict(cart=Cart(request)), context_instance=RequestContext(request))


def login(request):
    mensaje = ""
    rutaCorrecto = '/supermercados'
    if request.user.is_authenticated():
        return HttpResponseRedirect(rutaCorrecto)
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                usuario = form.cleaned_data['usuario']
                contrasena = form.cleaned_data['password']
                user = authenticate(username=usuario, password=contrasena)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return HttpResponseRedirect(rutaCorrecto)
                    else:
                        mensaje = "Cuenta inactiva"
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx = {'form': form, 'mensaje': mensaje}
        return render_to_response('login.html', ctx, context_instance=RequestContext(request))


def remove_from_cart(request, catalogo_id):
    catalogo = Catalogo.objects.get(id=catalogo_id)
    cart = Cart(request)
    cart.remove(catalogo)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def supermercados_view(request):
    markets = Supermercado.objects.all()
    return render_to_response('supermercados.html', {'markets': markets}, context_instance=RequestContext(request))


def pedidos_view(request):
    #OBTENEMOS LOS PEDIDOS DEL USUARIO
    pedidos = request.user.pedido_set.all()

    #VALORES DE CONTEXTO
    ctx = {'pedidos':pedidos}
    return render_to_response('pedidos.html',ctx,context_instance=RequestContext(request))


def detalle_pedido_view(request, id_pedido):
    #OBTENEMOS EL PEDIDO
    pedido = Pedido.objects.get(id = int(id_pedido))
    #OBTENEMOS TODOS LOS DETALLES DE DICHO PEDIDO
    detalles = pedido.detallepedido_set.all()

    #VALORES DE CONTEXTO
    ctx = {'pedido':pedido,'detalles':detalles}

    #LLENAMOS CON ESTOS VALORES EL TEMPLATE 'detalle_pedido.html'
    return render_to_response('detalle_pedido.html',ctx,context_instance=RequestContext(request))