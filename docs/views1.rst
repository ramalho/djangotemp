===========================================
Views, URLs e templates: o básico
===========================================

.. contents:: Conteúdo


--------------------------------------
Views genéricas
--------------------------------------

Vamos começar o tema das views apresentando as views genéricas que vêm prontas com o Django. A documentação do Django considera as views genéricas um tópico avançado, mas temos três ótimos motivos para começar por elas:

1. usando as views genéricas não precisamos escrever código Python para tratar *requests*, e podemos praticar rapidamente a configuração de URLs e a programação de templates, que são as principais novidades deste capítulo

2. conhecendo bem as views genéricas você evita "reinventar a roda" e escrever código desnecessariamente, seguindo os princípios :term:`DRY` e :term:`KISS`

3. mesmo quando as views genéricas incluídas no Django não resolverem o seu problema, você poderá se inspirar em suas convenções para criar as suas próprias views parametrizadas, tornando mais flexível a sua aplicação e seguindo o princípio :term:`DRY`

A melhor referência para views genéricas ainda é o **Apêndice D** do **Django Book (primeira edição)**: http://djangobook.com/en/1.0/appendixD/

A referência oficial é a mais atualizada mas não tem os exemplos do Django Book, por isso é mais difícil de ler: http://docs.djangoproject.com/en/dev/ref/generic-views/

----------------------------------
Localização dos templates
----------------------------------

.. image:: _static/templates-dir.*
   :align: right

- a busca por templates no sistema de arquivos é feita por funções configuradas em ``settings.py``::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.load_template_source',
        'django.template.loaders.app_directories.load_template_source',
        # 'django.template.loaders.eggs.load_template_source',
    )
    
- a função ``loaders.app_directories.load_template_source`` permite que cada aplicação tenha seu próprio diretório de templates

- as *generic views* por convenção procuram templates em locais como: ``«aplicação»/«modelo»_detail.html``

- assim, a melhor forma de organizar os templates no sistema de arquivos é em diretórios como segue (sim, «aplicação» aparece duas vezes)::

    «projeto»/«aplicação»/«templates»/«aplicação»/*.html 

-----------------------------------
Configuração das URLs
-----------------------------------

- Django usa expressões regulares configuradas no módulo ``urls.py`` para analisar as URLs das requisições e invocar a *view* apropriada para cada padrão de URL

- em um projeto modular, recomenda-se que cada aplicação tenha seu próprio módulo ``«aplicação»/urls.py``, estes são incluídos no ``urls.py`` principal na raiz do projeto::

    urlpatterns = patterns('',
        (r'^cat/', include('biblio.catalogo.urls')),
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'^db/(.*)', databrowse.site.root),
    )

- em ``«aplicação»/urls.py`` a análise dos caminhos de URLs continua::

    urlpatterns = patterns('',
        (r'^$', list_detail.object_list, livros_info),
        (r'^livro/(?P<object_id>\d+)/$', list_detail.object_detail, livros_info),
    )

- no exemplo acima, a URL ``http://exemplo.com/cat/`` aciona a *view* ``object_list``

- no mesmo exemplo, a URL ``http://exemplo.com/cat/livro/3/`` aciona ``object_detail`` 

-------------------------------------------
Configuração de *views* genéricas
-------------------------------------------

- ``urls.py`` é o único código Python necessário para uma *generic view* funcionar; por exemplo, veja o módulo ``biblio/catalogo/urls.py``:

.. code-block:: python
    :linenos:

    from django.conf.urls.defaults import *
    from django.views.generic import list_detail
    
    from biblio.catalogo.models import Livro
    
    livros_info = {
        'queryset' : Livro.objects.all(),
    }
    
    urlpatterns = patterns('',
        (r'^$', list_detail.object_list, livros_info),
        (r'^livro/(?P<object_id>\d+)/$', list_detail.object_detail, livros_info),
    )
    
- **linha 2:** importação do módulo ``views.generic.list_detail``

- **linhas 6 a 8:** dicionário com parâmetro para as *generic views*

- **linhas 10 a 13:** configuração das *generic views*

- **linha 12:** o grupo nomeado ``(?P<object_id>\d+)`` é passado para a *view* como um parâmetro de mesmo nome

.. _primeiro-template:

----------------------------------------
Primeiro template: ``livro_list.html``
----------------------------------------

- o caminho do template para a view genérica ``list_detail.object_list`` segue a convenção ``«aplicação»/«modelo»_list.html``, em caixa baixa; os nomes da aplicação e do modelo são obtidos por introspecção do parâmetro ``queryset``

- o contexto do template inclui a variável ``object_list``, referência ao parâmetro ``queryset``

.. code-block:: html
    :linenos:

    <h1>Livros</h1>

    <table border="1">
      <tr><th>ISBN</th><th>Título</th></tr>
      {% for livro in object_list %}
        <tr>
          <td>{{ livro.isbn }}</td>
          <td>
            <a href="{{ livro.get_absolute_url }}">{{ livro.titulo }}</a>
          </td>
        </tr>
      {% endfor %}
    </table>

----------------------------------------
Segundo template: ``livro_detail.html``
----------------------------------------

- o nome do template para a view genérica ``list_detail.object_detail`` segue a convenção ``«aplicação»/«modelo»_detail.html``, sempre em caixa baixa

- o contexto do template inclui a variável ``object``, referência ao objeto localizado através de ``queryset.get(id=object_id)``

.. code-block:: html
    :linenos:

    <h1>Ficha catalográfica</h1>
    
    <dl>
        <dt>Título</dt>
            <dd>{{ object.titulo }}</dd>
        <dt>ISBN</dt>
            <dd>{{ object.isbn }}</dd>
    </dl>
    
    
---------------------------------------------
O problema do caminho da aplicação nas URLs
---------------------------------------------

O funcionamento das *views* genéricas de listagem/detalhe dependem do método ``get_absolute_url`` para produzir os links da listagem para a página de detalhe. Eis uma implementação fácil de entender::

    class Livro(models.Model):
        '...'   
        def get_absolute_url(self):
            return '/cat/livro/%s/' % self.id

Este código é simples, mas viola o princípio :term:`DRY`, pois o prefixo `cat/` da URL está definido no módulo ``urls.py`` do projeto::

    urlpatterns = patterns('',
        '...'
        (r'^cat/', include('biblio.catalogo.urls')),
        '...'    
    )


Isto significa que se um administrador decidir mudar o prefixo das URLs da aplicação ``catalogo``, o método ``get_absolute_url`` do livro deixará de funcionar. 


-----------------------------------------------------
Solução: views nomeadas e o *decorator* ``permalink``
-----------------------------------------------------

A solução do problema envolve duas alterações, ambas dentro da aplicação ``catalogo``:

1. no módulo ``urls.py`` da aplicação, a configuração da view de detalhe recebe um nome (último item na linha 4 do trecho abaixo):

.. code-block:: python
    :linenos:
    
    urlpatterns = patterns('',
        (r'^$', list_detail.object_list, livros_info), 
        (r'^livro/(?P<object_id>\d+)/$', list_detail.object_detail, 
            livros_info, 'catalogo-livro-detalhe'),
    )

2. no módulo ``models.py`` da aplicação, o método ``get_absolute_url`` recebe o :term:`decorator` ``permalink`` e é alterado para devolver uma tupla no formato ``(«nome-da-view-url», «parâmetros-posicionais», «parâmetros-nomeados»)``::

    class Livro(models.Model):
        '...'   
        @models.permalink
        def get_absolute_url(self):
            #return '/cat/livro/%s/' % self.id
            return ('catalogo-livro-detalhe', (), {'object_id':self.id})

------------------------------------------------
*Views* genéricas incluídas com o Django (1)
------------------------------------------------

- as *generic views* ficam todas no pacote ``django.views.generic``, ou seja, o nome completo da primeira mencionada abaixo é ``django.views.generic.list_detail.object_list``

- *generic views* para listagem/detalhe (acabamos de ver)

    - ``list_detail.object_list``

    - ``list_detail.object_detail``
    
- *generic views* “simples”

    - ``simple.direct_to_template``
    
    - ``simple.redirect_to``
    
- *generic views* para criar/alterar/deletar objetos

    - ``create_update.create_object``
    
    - ``create_update.update_object``
    
    - ``create_update.delete_object``

------------------------------------------------
*Views* genéricas incluídas com o Django (2)
------------------------------------------------

- estas *generic views* também ficam no pacote ``django.views.generic``

- *generic views* para navegar por arquivos cronológicos
    
    - ``date_based.archive_index``

    - ``date_based.archive_year``

    - ``date_based.archive_month``

    - ``date_based.archive_week``

    - ``date_based.archive_day``

    - ``date_based.archive_today``

    - ``date_based.object_detail``

