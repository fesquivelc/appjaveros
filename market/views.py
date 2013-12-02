from django.shortcuts import render_to_response
from django.template.context import RequestContext


def index(request):
    return render_to_response('index.html',{},context_instance=RequestContext(request))

def prueba(request):
    return render_to_response('principal.html',{},context_instance=RequestContext(request))