from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from market.models import *
from market.forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def login(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/catalogo')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                usuario = form.cleaned_data['usuario']
                contrasena = form.cleaned_data['password']
                user = authenticate(username=usuario,password=contrasena)
                if user is not None:
                    auth_login(request,user)
                    return HttpResponseRedirect('/catalogo')
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje}
        return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def index(request):
    return render_to_response('index.html',{},context_instance=RequestContext(request))

def prueba(request):
    productos = Producto.objects.all()
    return render_to_response('productos.html',{'productos':productos},context_instance=RequestContext(request))

def catalogo(request):
    catalogos = Catalogo.objects.all()
    return render_to_response('productos.html',{'catalogos':catalogos},context_instance=RequestContext(request))

