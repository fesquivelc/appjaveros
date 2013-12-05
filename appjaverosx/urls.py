from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'appjaverosx.views.home', name='home'),
    # url(r'^appjaverosx/', include('appjaverosx.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$','market.views.login',name='login'),
    url(r'^catalogo/(\d{1,2})/(\d+)/$','market.views.catalogos_view',name='catalogos_view'),
    url(r'^supermercados/$','market.views.supermercados_view',name='supermercados'),
    url(r'^cerrar/$','market.views.cerrar_sesion',name='cerrar_sesion'),
    url(r'add_cart/(\d+)/(\d+)/$','market.views.add_to_cart',name='agregar_carrito'),
    url(r'view_cart/$','market.views.get_cart',name='ver_carrito'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
