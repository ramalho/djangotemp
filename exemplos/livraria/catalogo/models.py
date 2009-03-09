# coding: utf-8

from django.db import models

ENCADERNACOES = (('', u'(indefinida)'), 
                 ('br', u'brochura'), 
                 ('du', u'capa dura'), 
                 ('es', u'especial'))

class Livro(models.Model):
    titulo = models.CharField(verbose_name=u'Título', max_length=256, db_index=True)
    isbn = models.CharField(max_length=16, unique=True, null=True)
    edicao = models.CharField(verbose_name=u'Edição', max_length=64, blank=True)
    qt_paginas = models.PositiveIntegerField(verbose_name=u'Num. páginas', 
                                             default=0)
    # dtiso_publicacao ISO-8601: pode ser apenas '1980' ou '1980-12'
    dtiso_publicacao = models.CharField(u'Data de publicação', 
                                     max_length=16, blank=True)
    dt_catalogacao = models.DateField(auto_now_add=True, editable=False, db_index=True)
    editora = models.ForeignKey('Editora')
    encadernacao = models.CharField(max_length=2, blank=True, 
                                    choices=ENCADERNACOES)
    preco = models.DecimalField(verbose_name=u'preço', 
                                max_digits=6, decimal_places=2, db_index=True)
    idioma = models.ForeignKey('Idioma')
    
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
    nome = models.CharField(max_length=128, db_index=True)
    # dtiso_* ISO-8601: pode ser apenas '1980' ou '1980-12'
    dtiso_nascimento = models.CharField(u'Nascimento', 
                                     max_length=16, blank=True)
    dtiso_falecimento = models.CharField(u'Falecimento', 
                                     max_length=16, blank=True)
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
    criador = models.ForeignKey('Criador', null=True)
    nome = models.CharField(max_length=128, blank=True)
    papel = models.CharField(max_length=64, blank=True)
    
    class Meta:
        verbose_name = u'Crédito'
        verbose_name_plural = u'Créditos'
        order_with_respect_to = 'livro'
        
    def __unicode__(self):
        return u'%s (%s)' % (self.nome, self.livro)

class Idioma(models.Model):
    sigla = models.CharField(max_length='8')
    nome = models.CharField(max_length='32')
    
    def __unicode__(self):
        return unicode(self.nome)
