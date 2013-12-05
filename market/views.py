from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from market.models import *
from market.forms import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.db.models import Q


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
                        request.session['carrito_compra'] = {}
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


def add_cart(request, id_catalogo):
    detalle = DetallePedido()
    catalogo = Catalogo.objects.get(id=id_catalogo)

    detalle.cantidad = 1
    detalle.catalogo = catalogo

    request.session['carrito_compra'] = detalle
    #carrito = request.session['carrito_compra']
    #if detalle not in carrito:
    #    carrito.append(detalle)
    return HttpResponseRedirect('../../')

def get_cart(request):
    productos = request.session['carrito_compra']
    ctx = {'productos':productos}

    return render_to_response('carrito.html',ctx,context_instance=RequestContext(request))