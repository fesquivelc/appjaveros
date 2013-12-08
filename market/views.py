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
                           '<p>%s</p>' %(email,titulo,contenido)

            to = 'fesquivelc@gmail.com'
            msje = EmailMultiAlternatives('Correo de contacto',html_content,'from@server.com',[to])
            msje.attach_alternative(html_content,'text/html')
            msje.send()
    else:
        formulario = ContactoForm()
    ctx = {'enviado': info_enviado, 'email':email,'titulo':titulo,'contenido':contenido,'form':formulario}
    return render_to_response('contacto.html',ctx,context_instance=RequestContext(request))


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
                user = authenticate(username=usuario,password=contrasena)
                if user is not None:
                    if user.is_active:
                        auth_login(request,user)

                        #variable de sesion que contiene el carrito
                        request.session['carrito_compra'] = []
                        return HttpResponseRedirect(rutaCorrecto)
                    else:
                        mensaje = "Cuenta inactiva"
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje}
        return render_to_response('login.html',ctx,context_instance=RequestContext(request))



def catalogos_view(request,market,cat):
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
         catalogos = Catalogo.objects.filter(supermercado=supermercado).filter(producto__in=Producto.objects.filter(nombre__contains=nombreProducto).filter(categoria=Categoria.objects.get(id=int(cat))))
    else:
        catalogos = Catalogo.objects.filter(supermercado=supermercado).filter(producto__in=Producto.objects.filter(nombre__contains=nombreProducto))
    ctx = {'mnuCategorias':mnuCategorias,'catalogos':catalogos,'form':form,'supermercado':supermercado,'catActual':int(cat)}
    return render_to_response('catalogos.html',ctx,context_instance=RequestContext(request))

def supermercados_view(request):
    markets = Supermercado.objects.all()
    return render_to_response('supermercados.html',{'markets':markets},context_instance=RequestContext(request))

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_to_cart(request, catalogo_id, cantidad):
    catalogo = Catalogo.objects.get(id = catalogo_id)
    cart = Cart(request)
    cart.add(catalogo,catalogo.precio,1)
    print len(dict(cart=Cart(request)))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_from_cart(request, catalogo_id):
    catalogo = Catalogo.objects.get(id = catalogo_id)
    cart = Cart(request)
    cart.remove(catalogo)

def get_cart(request):
    lista = []
    shop =  dict(cart=Cart(request))

    print shop.get('cart')

    for i in shop.get('cart'):
        print i.product

    return render_to_response('carrito.html', dict(cart=Cart(request)),context_instance=RequestContext(request))