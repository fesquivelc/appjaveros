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
                        return HttpResponseRedirect(rutaCorrecto)
                    else:
                        mensaje = "Cuenta inactiva"
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje}
        return render_to_response('login.html',ctx,context_instance=RequestContext(request))


def catalogos_view(request,market,cat):
    mensaje=""
    supermercado = Supermercado.objects.get(id=market)
    mnuCategorias = supermercado.catalogo_set.all()
    ctx = {}
    if request.method == "POST":
        form = BusquedaProductoForm(request.POST)
        if form.is_valid():
            nombreProducto = form.cleaned_data['nombreProducto']
            mensaje = nombreProducto
            if cat != 0:
                catalogos = Catalogo.objects.filter(supermercado=supermercado).filter(categoria=cat).filter(producto__in=Producto.objects.filter(nombre__contains=nombreProducto))
            else:
                catalogos = Catalogo.objects.filter(supermercado=supermercado).filter(producto__in=Producto.objects.filter(nombre__contains=nombreProducto))
            form = BusquedaProductoForm()
            ctx = {'mnuCategorias':mnuCategorias,'catalogos':catalogos,'mensaje':mensaje,'form':form}
    else:
        form = BusquedaProductoForm()
        ctx = {'mnuCategorias':mnuCategorias,'mensaje':mensaje,'form':form}
    print form
    return render_to_response('catalogos.html',ctx,context_instance=RequestContext(request))

#def catalogo_categoria(request,market,cat):
#    mensaje = ""
#    if request.method == "POST":
#        mensaje = "ay papi"
#    #if int(cat) == 0:
#    catalogos = Supermercado.objects.get(id=market).catalogo_set.all()
#    #else:
#    #    categoria = Categoria.objects.get(int(cat))
#    #    productos = categoria.producto_set.filter
#
#    categorias = Categoria.objects.all()
#
#    return render_to_response('catalogos.html',{'catalogos':catalogos,'categorias':categorias,'mensaje':mensaje},context_instance=RequestContext(request))


def supermercados(request):
    markets = Supermercado.objects.all()
    return render_to_response('supermercados.html',{'markets':markets},context_instance=RequestContext(request))

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')
