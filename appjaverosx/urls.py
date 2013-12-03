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
    url(r'^catalogo/(\d{1,2})/$','market.views.catalogo',name='catalogo'),
    url(r'^catalogo/(\d{1,2})/(\d+)$','market.views.catalogo_categoria',name='catalogo'),
    url(r'^supermercados/$','market.views.supermercados',name='supermercados'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
