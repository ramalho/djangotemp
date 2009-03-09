
===============================
Django ORM: o básico
===============================

- O que o ORM oferece

    - independência em relação ao banco de dados SQL
    
    - acesso direto a objetos relacionados
    
    - implementação fácil e flexível de operações :term:`CRUD`
    
    - validação de campos
    
    - transações :term:`ACID`

---------------------------------------
API do ORM: exemplo de interação
---------------------------------------

Os modelos ganham por default um atributo ``«Modelo».objects`` que é um :term:`manager`, através do qual você acessa toda a coleção de objetos do modelo (ou seja, operações no banco de dados a nível de tabela, e não registro). 

A maioria dos métodos de managers na verdade são delegados para um ``QuerySet``, e devolvem instâncias de ``QuerySet``. Por exemplo, a chamada ``Livro.objects.all()`` devolve um ``QuerySet`` que engloba todos os registros da tabela de livros. 

- usando ``./manage.py shell``

::

    >>> from biblio.catalogo.models import *
    >>> alice = Livro.objects.get(isbn='9780393048476')
    >>> for c in alice.criador_set.all(): print 
    ... 
    Lewis Carroll
    Martin Gardner
    John Tenniel
    >>> lc = alice.criador_set.get(nome__contains='Carroll')
    >>> print lc.biografia.texto
    Charles Lutwidge Dodgson, ou Lewis Carrol (Cheshire, 27 de janeiro de 1832 — Guildford, 14 de Janeiro de 1898) foi um escritor e matemático britânico. Lecionava matemática no Christ College, em Oxford).
    >>> 
    
----------------------------------
Métodos de Managers e QuerySets
----------------------------------

Os mais usados são:

``«qs».all()``
    Devolve um ``QuerySet`` com todos os objetos do modelo (isto é, todos os registros da tabela correspondente).

``«qs».filter(«critério1», «critério2», ...)``
    Devolve um ``QuerySet`` com todos os objetos do modelo selecionados pelo critério, ou seja, gerando uma em SQL uma cláusula ``WHERE`` com os critérios combinados por ``AND``. Ver :ref:`criterios`.
        
``«qs».get(«critério1», «critério2», ...)``
    Devolve **o único** objeto do modelo selecionado pelos critérios. Se nenhum objeto é encontrado, é levantada uma exceção ``«modelo».DoesNotExist``. Se mais de um objeto é encontrado, é levantada uma exceção ``«modelo».MultipleObjectsReturned``.
    
    
``«qs».order_by(«campo1», «campo2», ...)``
    Determina a ordenação do resultado pelos campos indicados. Se o nome de um campo for precedido de **-** então a ordem é descendente. Ex. para obter as 5 notícias mais recentes: ``noticias.objects.order_by('-dt_public')[:5]``.
    

.. _select-related:

-----------------------------------
Seleção de objetos referentes
-----------------------------------

``«qs».select_related(«campo1», «campo2», ..., depth=0)``
    Força o ORM a realizar *joins* para buscar os objetos referentes e evitar acessos posteriores ao banco de dados. 
    
    Os «campos» são nomes de campos de referência (``ForeignKey`` etc.). Pode-se usar a sintaxe ``referente__campo``.
    
    O único parâmetro nomeado aceito é ``depth``, e serve para limitar a extensão dos relacionamentos a serem recuperados. ``*fields`` e ``depth`` não podem ser usados ao mesmo tempo.


.. _criterios:

-------------------------------
Critérios para buscar objetos
-------------------------------

Os critérios de busca usados em métodos de ``QuerySet`` são :term:`argumentos nomeados <keyword argument>`, com nomes formados por atributos do modelo e operadores como ``contains``, ``in`` ou ``isnull``, unidos por ``__`` (dois underscores)::

    >>> lc = alice.criador_set.get(nome__icontains='Carroll') # operador __icontains

Alguns exemplos de critérios:

``«campo»__exact=«valor»``
    Corresponde ao SQL ``SELECT ... WHERE «campo» = «valor»``. Por conveniência, o operador ``__exact`` pode ser omitido, ou seja, a busca exata pode ser escrita assim::

        >>> alice = Livro.objects.get(isbn='9780393048476') # busca exata

``«campo»__icontains=«valor»``
    Corresponde ao SQL ``SELECT ... WHERE «campo» LIKE '%«valor»%'``. O prefixo ``i`` significa que este operador é indiferente a caixa alta ou baixa (*case insensitive*).

``«campo»__lt=«valor»``
    Operador *menor que* (*less than*). Corresponde ao SQL ``SELECT ... WHERE «campo» < '%«valor»%'``. O operador ``lte`` é *menor ou igual que* (*less than or equal*). Há também os operadores ``gt`` e ``gte``.

    >>> livros_curtos = Livro.objects.filter(qt_paginas__lt=100) # <100 pgs.
    
-----------------------
Atributos dinâmicos
-----------------------

O ORM do Django cria dinamicamente os seguintes atributos em cada instância ``i`` de um :term:`model`:

``i.pk``
    Nome alternativo para o campo ``id``. Útil para acessar um campo de chave primária com outro nome, criado com o parâmetro ``primary_key``.

``i.«relacionado»_set``
    Um :term:`manager` para acessar o conjunto de objetos relacionados que fazem referência a este, através de campos ``ForeignKeyField`` ou ``ManyToManyField``. O nome deste atributo pode ser configurado pelo parâmetro ``related_name`` na definição do campo ``ForeignKeyField`` ou ``ManyToManyField``.

``i.«relacionado»``
    Acesso direto ao objeto que faz referência a este através de um ``OneToOneField``.
    
``i.«referente»_id``
    Valor da chave estrangeira de um campo ``ForeignKeyField``, ``ManyToManyField`` ou ``OneToOneField``. Para acessar diretamente o objeto apontado pelo campo, use ``i.«referente»``.

-----------------------
Métodos dinâmicos
-----------------------

O ORM do Django cria dinamicamente os seguintes métodos em cada instância ``i`` de um :term:`model`:

``i.get_«opção»_display(valor)``
    Devolve a legenda que corresponde ao valor em um campo «opção» criado com o parâmetro ``choices``. 

``i.get_«objeto»_order()``
    Devolve uma lista com as chaves primárias dos objetos relacionados, em ordem.

``i.set_«objeto»_order(lista)``
    Dada de uma lista de chaves primárias, redefine a ordem dos objetos relacionados.    
    
``i.get_next_by_«datahora»()``
    Devolve a próxima instância em ordem cronológica de acordo com o campo «datahora». 

``i.get_previous_by_«datahora»()``
    Devolve a instância anterior em ordem cronológica de acordo com o campo «datahora». 

.. _ordenar-relacionados:

-----------------------------------
Ordenação de objetos relacionados
-----------------------------------
    
Às vezes a ordem dos objetos em um ``«relacionado»_set`` é importante (por exemplo, os autores de um livro devem ser citados na ordem correta). 

O parâmetro ``order_with_respect_to`` estabelece que os objetos relacionados devem manter sua ordem em relação aos seus referentes (ex. créditos em relação a livros).

::

    class Credito(models.Model):
        livro = models.ForeignKey(Livro)
        criador = models.ForeignKey('Criador')
        papel = models.CharField(max_length=64, blank=True)
        
        class Meta:
            order_with_respect_to = 'livro'

A ordem é mantida através de um campo ``_order`` (integer) criado automaticamente na tabela deste modelo. 

--------------------------------------------
Ordenação de objetos relacionados (cont.)
--------------------------------------------

O modelo referente (apontado pela ``ForeignKey``) ganha os métodos dinâmicos ``get_«item»_order`` e ``set_«item»_order`` que permitem ler e alterar a ordem relativa dos itens relacionados.
        
::

    >>> from biblio.catalogo.models import *
    >>> livro = Livro.objects.get(isbn='9780393048476')
    >>> livro
    <Livro: The Annotated Alice>
    >>> livro.get_credito_order()
    [1, 2, 3]
    >>> for c in livro.credito_set.all(): print c
    The Annotated Alice: Lewis Carroll (autor)
    The Annotated Alice: Martin Gardner (editor)
    The Annotated Alice: John Tenniel (ilustrador)
    >>> livro.set_credito_order([1,3,2])
    >>> for c in alice.credito_set.all(): print c
    The Annotated Alice: Lewis Carroll (autor)
    The Annotated Alice: John Tenniel (ilustrador)
    The Annotated Alice: Martin Gardner (editor)

    
    
