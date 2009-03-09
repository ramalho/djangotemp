# coding: utf-8

from django.db import models

CATEGORIAS = (('', u'(indefinida)'), 
              ('FIC', u'Ficção'), 
              ('NFIC', u'Não-Ficção'), 
              ('AAE', u'Autoajuda/Esoterismo'))

class Livro(models.Model):
    titulo = models.CharField(verbose_name=u'Título', max_length=256)
    isbn = models.CharField(max_length=16, blank=True)
    edicao = models.CharField(verbose_name=u'Edição', max_length=64, blank=True)
    qt_paginas = models.PositiveIntegerField(verbose_name=u'Num. páginas', 
                                             default=0)
    # dt_publicacao ISO-8601: pode ser apenas '1980' ou '1980-12'
    dt_publicacao = models.CharField(u'Data de publicação', max_length=16, blank=True)
    dt_catalogacao = models.DateField(auto_now_add=True, editable=False)
    editora = models.ForeignKey('Editora')
    categoria = models.CharField(max_length=8, blank=True, 
                                 choices=CATEGORIAS, 
                                 default=CATEGORIAS[0][0])                                                                        
    class Meta:
        ordering = ('titulo', 'isbn', 'id')

    def __unicode__(self):
        return self.titulo
    
    @models.permalink
    def get_absolute_url(self):
        #return '/cat/livro/%s/' % self.id
        return ('catalogo-livro-detalhe', (), {'object_id':self.id})


class Editora(models.Model):
    nome = models.CharField(max_length=128)
    cidade = models.CharField(max_length=128, blank=True)
    
    def __unicode__(self):
        return self.nome

class Criador(models.Model):
    nome = models.CharField(max_length=128)
    dt_nascimento = models.DateField(null=True, blank=True)
    livros = models.ManyToManyField(Livro, through='Credito')

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = u'Criadores'
    
class Biografia(models.Model):
    sobre = models.OneToOneField(Criador)
    #sobre = models.ForeignKey(Criador, unique=True) # funciona com databrowse    
    texto = models.TextField()

    def __unicode__(self):
        return u'Biografia de ' + self.sobre.nome    
    
class Credito(models.Model):
    livro = models.ForeignKey(Livro)
    criador = models.ForeignKey('Criador')
    papel = models.CharField(max_length=64, blank=True)
    
    class Meta:
        verbose_name = u'Crédito'
        verbose_name_plural = u'Créditos'
        order_with_respect_to = 'livro'
        
    def __unicode__(self):
        livro_criador = u'%s: %s' % (self.livro, self.criador)
        if self.papel:
            return livro_criador + u' (%s)' % self.papel
        else:
            return livro_criador
