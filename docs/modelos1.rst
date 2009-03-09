
===============================
Modelos de dados: o básico
===============================

.. image:: _static/django-app-dir.*
   :align: right

- por convenção cada aplicação tem o seu ``models.py``

- o ``models.py`` determina o esquema de dados (e não o BD)

- este arquivo contém praticamente só definições de classes derivadas de ``models.Model``

------------------------------
Exemplo de ``Model``
------------------------------

::

    class Livro(models.Model):
        titulo = models.CharField(max_length=256)
        isbn = models.CharField(max_length=16, blank=True)
        edicao = models.CharField(max_length=64, blank=True)
        qt_paginas = models.PositiveIntegerField(default=0)
        dt_catalogacao = models.DateField(auto_now_add=True)
        editora = models.ForeignKey('Editora')
        categoria = models.CharField(max_length=8, blank=True, 
                                     choices=CATEGORIAS)

        class Meta:
            ordering = ('titulo', 'isbn', 'id')
        
        def __unicode__(self):
            return self.titulo

------------------------------
Tipos de campos primitivos
------------------------------

- campos que emulam tipos básicos de SQL

    - CharField, TextField, BooleanField, NullBooleanField
    
    - DateField, DateTimeField, TimeField

    - IntegerField, SmallIntegerField, AutoField
    
    - DecimalField, FloatField 

    
- campos que acrescentam validações sobre tipos básicos

    - EmailField, URLField, IPAddressField, SlugField, XMLField

    - PositiveIntegerField, PositiveSmallIntegerField, CommaSeparatedIntegerField

- campos para armazenar arquivos

    - FileField, FilePathField, ImageField
    
    - nos três casos, os dados são armazenados no sistema de arquivos, e o campo no banco de dados registra apenas o nome do arquivo ou o caminho
    
.. _fk-intro:
    
-----------------------------------------
Campo de referência: ``ForeignKey``
-----------------------------------------

- ``ForeignKey``: referência a objeto (chave estrangeira)

    - relação muitos-para-um::

        class Livro(models.Model):
            titulo = models.CharField(max_length=256)
            editora = models.ForeignKey('Editora')
            
        class Editora(models.Model):
            nome = models.CharField(max_length=128)
            cidade = models.CharField(max_length=128)

    
    - objeto referente (editora) ganha um atributo dinâmico ``«modelo»_set`` onde ``«modelo»`` é o nome do modelo relacionado em caixa baixa (livro). Ex: objeto ``ed`` instância de ``Editora`` ganha ``ed.livro_set``)::

        >>> ed = Editora.objects.get(nome__icontains='norton')
        >>> ed
        <Editora: W. W. Norton & Company>
        >>> for l in ed.livro_set.all(): print l
        ... 
        Colors of the World
        The Annotated Alice
        
-----------------------------------------
Campo de referência: ``OneToOneField``
-----------------------------------------

- ``OneToOneField``: referência a objeto (chave estrangeira)

    - relação um-para-um::
    
        class Criador(models.Model):
            nome = models.CharField(max_length=128)
            dt_nascimento = models.DateField(null=True, blank=True)
            livros = models.ManyToManyField(Livro, through='Credito')
        
        class Biografia(models.Model):
            sobre = models.OneToOneField(Criador)
            texto = models.TextField()

    - objeto referente (criador) ganha um atributo dinâmico com o nome do modelo relacionado em caixa baixa (ex: instância ``c`` de ``Criador`` ganha ``c.biografia``)::
            
        >>> lc = Criador.objects.get(id=1)
        >>> print lc.biografia.texto
        Charles Lutwidge Dodgson, ou Lewis Carrol foi um escritor e um matemático britânico...
        
-----------------------------------------
Campo de referência: ``ManyToManyField``
-----------------------------------------
        
- ``ManyToManyField``: referência a múltiplos objetos via tabela de ligação

    - relação muitos-para-muitos
    
    - objeto referente ganha um atributo dinâmico ``«modelo»_set`` (ver :ref:`fk-intro`)
    
    - a tabela de ligação pode ser implícita ou explícita via parâmetro ``through``
    
::

    class Livro(models.Model):
        titulo = models.CharField(max_length=256)
        editora = models.ForeignKey('Editora')
        assuntos = models.ManyToManyField('Assunto')
        criadores = models.ManyToManyField('Criador', through='Credito')
        
    class Credito(models.Model):
        livro = models.ForeignKey(Livro)
        criador = models.ForeignKey('Criador')
        papel = models.CharField(max_length=64)
        
    class Criador(models.Model):
        nome = models.CharField(max_length=128)
        dt_nascimento = models.DateField(null=True, blank=True)
        

--------------------------------------------
Parâmetros comuns para campos
--------------------------------------------

- fonte: ``django/db/models/fields/__init__.py``::

    class Field(object):
        '...'
        def __init__(self, verbose_name=None, name=None, primary_key=False,
                max_length=None, unique=False, blank=False, null=False,
                db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
                serialize=True, unique_for_date=None, unique_for_month=None,
                unique_for_year=None, choices=None, help_text='', 
                db_column=None, db_tablespace=None, auto_created=False):
            '...'
                
- parâmetros que definem o esquema no banco de dados:

    - primary_key, unique, null, db_index, db_column, db_tablespace

- parâmetros que definem a validação e a apresentação do campo para o usuário:

    - verbose_name, blank, default, unique_for_date, unique_for_month, unique_for_year, choices, help_text
    
--------------------------------------
Parâmetros que definem o esquema
--------------------------------------

Em ordem de utilidade (subjetiva).

``null=False``
    Determina se o campo aceitará valores nulos (``NULL`` em SQL; ``None`` em Python). O default implica em ``NOT NULL``.

``unique=False``
    Determina se o campo terá uma restrição de unicidade. Caso ``True`` implica também na criação de um índice.

``db_index=False``
    Determina se o campo será indexado. O default é ``False`` para a maioria dos tipos de campos, mas é ``True`` em alguns casos (ex. ``SlugField``).

``primary_key=False``
    Determina se o campo é a chave primária. Pouco usado, porque a melhor prática é deixar o Django criar um ``AutoField`` com o nome ``id``. Implica na criação de um índice.
    
``db_column=None``
    Determina o nome da coluna no banco de dados SQL. O default ``None`` implica que a coluna terá o mesmo nome do campo, exceto no caso dos campos referenciais que ganham o sufixo ``_id`` (ex. ``editora_id``). 

``db_tablespace=None``
    Em servidores Oracle, determina o `tablespace` a ser usado para os índices do campo. O parâmetro não tem efeito no PostgreSQL, no MySQL e no SQLite.

----------------------------------------------------
Parâmetros que definem a apresentação
----------------------------------------------------

Em ordem de utilidade (subjetiva).

``verbose_name=None``
    Rótulo (`label`) do campo em formulários gerados pelo Django. Usado principalmente para associar rótulos acentuados (ex. ``u"edição"``). Recomendável usar ``unicode``.

``help_text=''``
    Texto de ajuda do campo. Usado em formulário gerados pelo Django. Útil para exibir exemplo de preenchimento (ex. ``help_text=u'ex. (11)8432-0333'``). Recomendável usar ``unicode``.

``default=NOT_PROVIDED``
    Valor default do campo. Se for um valor simples, pode ser implementado na DDL. Mas também pode ser um :term:`callable`, que será invocado sempre que o objeto for instanciado.
    
----------------------------------------------------
Parâmetros que definem a validação
----------------------------------------------------

Em ordem de utilidade (subjetiva).

``max_length=None``
    Tamanho máximo do conteúdo do campo para validação. Parâmetro obrigatório em campos ``CharField`` e derivados; não usado em vários tipos de campos. Pode ser implementado na DDL como o tamanho do ``VARCHAR``.

``blank=False``
    Determina se o campo pode ser validado com seu conteúdo vazio ``""``. Os autores do Django sempre preferem usar campos tipo caractere que aceitam brancos em vez de nulos.

``choices``
    Conjunto de valores válidos para o campo. Veja como em `Parâmetro choices`_.

``unique_for_date=None`` ``unique_for_month=None`` ``unique_for_year=None``
    Determina que o valor deste campo deve ser único em relação ao campo data especificado.


--------------------------
Parâmetro ``choices``
--------------------------

- O parâmetro deve ser um iterável (:term:`iterable`) que produz duplas ``(valor,legenda)`` onde o valor será o conteúdo da escolha (ex. ``'cafe'``) e legenda é o que será exibido para o usuário (ex. ``u'Café expresso'``))

::

    BEBIDAS = (('cafe',u'Café expresso'), ('mate',u'Chá mate'), ('chocolate',u'Chocolate quente'))

    class Pedido(models.Model):
        bebida = models.CharField(max_length=16, choices=BEBIDAS)
        
- Em HTML, as opções acima podem ser exibidas assim:

.. code-block:: html
    
    <select name="bebidas">
        <option value="cafe">Café expresso</option>
        <option value="mate">Chá mate</option>
        <option value="chocolate">Chocolate quente</option>
    </select>

- Para cada campo ``x`` com parâmetro ``choices``, o modelo ganha dinamicamente um método ``get_x_display(v)`` para obter a legenda corresponende a um valor.


------------------------------
Meta-opções para modelos (1)
------------------------------

Em ordem de utilidade (subjetiva).

``ordering``
    Estabelece a ordenação padrão dos resultados consultas a este modelo. O valor deste atributo é uma sequência de nomes de campos. Use ``-`` como prefixo de um campo para definir ordem descendente:: 
    
        ordering = ['-dt_publicacao', 'editoria']

``unique_together``
    Estabelece a restrição de unicidade para conjuntos de campos.
    
``verbose_name``, ``verbose_name_plural``
    Define o nome do modelo (singular e plural) para apresentação na interface administrativa.

``get_latest_by``
    Estabelece o campo ``DateTime`` a ser usado como critério para o método de consulta ``latest``.

.. _meta-mod-2:
        
----------------------------------
Meta-opções para modelos (2)
----------------------------------

``order_with_respect_to``
    Estabelece qual campo ``ForeignKey`` determina a ordem relativa dos itens. Ver :ref:`ordenar-relacionados`.
        
``abstract``
    Define que este é um modelo abstrato (:term:`abstract model`), que não será persistido em uma tabela mas será usado para definir um esquema reutilizável por herança.
    
``db_table``
    Define o nome da tabela que corresponde ao modelo. Quando esta opção não é usada o nome da tabela é ``aplicao_modelo`` (ex.: ``catalogo_livro`` é o modelo ``Livro`` da aplicação ``catalogo``.    

``db_tablespace``
    Estabelece o *tablespace* que será usado para armazenar os dados deste modelo. Não tem efeito na maioria dos bancos de dados suportados pelo Django 1.0.

------------------------------------
Métodos especiais
------------------------------------

Os seguintes métodos, se definidos em um modelo, são utilizados pelo Django:

``__unicode__``
    Devolve a representação em unicode do objeto; por exemplo, para um livro esta representação pode ser o seu título. Usado em várias partes do admin do Django para representar o objeto em listagens e combos.
    
``get_absolute_url``
    Devolve o camiho a partir da raiz do site até o objeto. Usado pelo admin do Django para exibir um botão **View on site** com link para a página pública do objeto. Essencial para qualquer view que precisa gerar links para objetos, por exemplo, uma página de resultados de busca. Veja exemplo em :ref:`primeiro-template`.

