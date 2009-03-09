from django.contrib import admin, databrowse
from livraria.catalogo.models import *
 
admin.site.register(Livro)
admin.site.register(Editora)
admin.site.register(Criador)
admin.site.register(Biografia)
admin.site.register(Credito)
admin.site.register(Idioma)
databrowse.site.register(Livro)
databrowse.site.register(Editora)
databrowse.site.register(Criador)
databrowse.site.register(Biografia)
databrowse.site.register(Credito)
databrowse.site.register(Idioma)
