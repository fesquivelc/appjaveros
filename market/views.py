from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from market.models import *
from market.forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

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
                    auth_login(request,user)
                    return HttpResponseRedirect(rutaCorrecto)
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje}
        return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def catalogo(request,market):
    catalogos = Supermercado.objects.get(id=market).catalogo_set.all()
    return render_to_response('catalogos.html',{'catalogos':catalogos},context_instance=RequestContext(request))

def catalogo_categoria(request,market,cat):
    if int(cat) == 0:
        catalogos = Supermercado.objects.get(id=market).catalogo_set.all()
    else:
        categoria = Categoria.objects.get(int(cat))
        productos = categoria.producto_set.filter

    categorias = Categoria.objects.all()

    return render_to_response('catalogos.html',{'catalogos':catalogos,'categorias':categorias},context_instance=RequestContext(request))


def supermercados(request):
    markets = Supermercado.objects.all()
    return render_to_response('supermercados.html',{'markets':markets},context_instance=RequestContext(request))


