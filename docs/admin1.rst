===========================================
Configuração da interface administrativa
===========================================

.. contents:: Conteúdo


--------------------------------------
O mínimo necessário
--------------------------------------

Para habilitar a interface administrativa do Django:

1. em ``settings.py``, instale a aplicação ``django.contrib.admin``::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',  # <----
    )

2. em ``urls.py``, descomente as linhas ligadas ao admin::

    from django.contrib import admin  # <----
    admin.autodiscover()              # <----

    urlpatterns = patterns('',
        '...'
        (r'^admin/', include(admin.site.urls)),   # <----
        '...'    
    )

3. execute o comando ``./manage.py syncdb`` para que o Django crie as tabelas administrativas


---------------------------------------
Estrutura do arquivo ``admin.py``
---------------------------------------

Exemplo:

::

    from django.contrib import admin
    from pizza.entrega.models import Pedido, Pizza, Entregador
     
    class PizzaInline(admin.TabularInline):
        model = Pizza
     
    class PedidoAdmin(admin.ModelAdmin):
        inlines = [PizzaInline]
        list_display = ('entrou', 'cliente',
                        'nome_entregador', 'partiu', 'despachado')
        list_display_links = ('entrou', 'cliente')
        
    class PizzaAdmin(admin.ModelAdmin):
        list_display = ('pedido', '__unicode__')
     
    admin.site.register(Pedido, PedidoAdmin)
    admin.site.register(Pizza, PizzaAdmin)
    admin.site.register(Entregador)

------------------------------------------
Opções na definição do ``ModelAdmin``
------------------------------------------

Na instância de ``ModelAdmin``:

::

    class ClienteAdmin(admin.ModelAdmin):
        list_display = ('fone', 'contato', 'endereco')
        list_display_links = ('fone', 'contato')
        search_fields = ('fone', 'contato', 'logradouro', 'numero')
        
.. _admin-lists:
        
--------------------------
Formatação de listas
--------------------------

``list_display=«tupla-de-atributos»``
    Transforma a listagem em uma tabela onde cada atributo é uma coluna. Os atributos podem ser campos ou métodos do ``Model``, métodos do ``ModelAdmin`` ou simples funções que aceitam um objeto como argumento e devolvem o valor a ser exibido. É comum colocar um atributo ``short_description`` em tais métodos e funções para rotular o cabeçalho da coluna. Ver :ref:`admin-model-ops`.

``list_display_links=«tupla-de-atributos»``
    Determina quais campos na listagem ganham links para o form de edição do item. Por default, apenas o campo da primeira coluna ganha link.
    
``list_per_page=«int»``
    Determina o número máximo de itens por página na listagem. O default é 100.

``list_select_related=«bool»``
    Determina se o Django ORM deve buscar os objetos relacionados ao modelo da listagem, realizando *joins* para reduzir o número de consultas ao banco de dados. O default é ``False``. Ver :ref:`select-related`.

``ordering=«tupla-de-campos»``
    Determina o critério de ordenação padrão da listagem. No admin do Django 1.0x, apenas o primeiro item é levado em conta.
    
-----------------------------
Filtros e listas hierárquicas
-----------------------------

``search_fields=«tupla-de-campos»``
    Faz surgir no topo da listagem uma caixa de busca para selecionar os resultados buscando nos campos indicados na «tupla-de-campos»
    
``date_hierarchy=«campo-data»``
    Quebra a listagem por uma hierarquia de datas (ano, dia, mês...)

``list_filter=«tupla-de-campos»``
    Faz surgir uma barra lateral esquerda que permite a filtrar os resultados segundo o valor dos campos indicados na «tupla-de-campos». Os campos podem ser ``BooleanField``, ``CharField``, ``DateField``, ``DateTimeField``, ``IntegerField`` ou ``ForeignKey``.
    
.. image:: _static/admin-filter.*
    
    
.. _admin-model-ops:

---------------------------------------
Opções na definição do ``Model``
---------------------------------------

Alguns metadados aplicados a métodos no modelo ou funções em ``admin.py`` alteram a exibição de resultados no admin.

``«func».boolean``
    Se ``True``, o admin exibe um marcador verde se o resultado for verdadeiro, ou vermelho se não for.    

    ::
    
        class Pedido(models.Model):
            '...'        
            def despachado(self):
                return self.entregador and self.partida
            despachado.boolean = True 

``«func».allow_tags``
    Se ``True``, os tags HTML contidos no resutado ficam intactos; do contrário, eles são suprimidos (suprimir tags é o comportamento padrão, por motivos de segurança). 
    
    ::

        class Tarefa(models.Model):
            '...'
        
            def rotulo(self):
                fmt = '''<span style="color: #%s;">%s</span>'''
                return fmt % (self.cor(), self.prioridade)
            rotulo.allow_tags = True
            rotulo.short_description = u'rótulo'
            rotulo.admin_order_field = 'prioridade'

``«func».short_description``
    Define o nome da coluna onde o resultado será exibido nas listagens do admin. Ver :ref:`admin-lists`.

``«func».admin_order_field``
    Define o campo do modelo a ser usado para ordenar os resultados quando o usuário pedir a ordenação por esta coluna no admin. Sem este atributo, colunas geradas por métodos não podem ser usadas para ordenação, pois o admin utiliza o banco de dados para fazer a ordenação.
    
-----------------------------------------
Opções na definição do ``Model`` (cont.)
-----------------------------------------

::

    class Pedido(models.Model):
        inclusao = models.DateTimeField(auto_now_add=True)
        cliente = models.ForeignKey(Cliente)
        entregador = models.ForeignKey('Entregador', null=True, blank=True)
        partida = models.TimeField(null=True, blank=True)
        
        class Meta:
            ordering = ['-inclusao']
             
        def despachado(self):
            return (self.entregador is not None) and (self.partida is not None)
        despachado.boolean = True 

- no admin, apenas o primeiro criério de ordenação defindo em ``Meta.ordering`` é usado (fonte:  http://docs.djangoproject.com/en/dev/ref/models/options/#ordering)
