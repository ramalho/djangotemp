from django.conf.urls.defaults import *
from django.views.generic import list_detail

from biblio.catalogo.models import Livro

livros_info = {
    'queryset' : Livro.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', list_detail.object_list, livros_info),
    (r'^livro/(?P<object_id>\d+)/$', list_detail.object_detail, livros_info,
     'catalogo-livro-detalhe'),
)



