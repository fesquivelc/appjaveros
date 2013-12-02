from django.shortcuts import render_to_response
from django.template.context import RequestContext
from market.models import Producto


def index(request):
    return render_to_response('index.html',{},context_instance=RequestContext(request))

def prueba(request):
    productos = Producto.objects.all()
    return render_to_response('productos.html',{'productos':productos},context_instance=RequestContext(request))

