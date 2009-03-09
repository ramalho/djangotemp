
=====================================================================
Introdução ao Django
=====================================================================

- Luciano Ramalho, Occam Consultoria

- luciano@occam.com.br

---------------------------------------------------------------------
Alguns fatos sobre o Django
---------------------------------------------------------------------

- é o framework favorito do Guido van Rossum, criador de Python

- é largamente utilizado internamente no Google

- é suportado pelo Google App Engine (serviço de hospedagem)

- foi criado num site de notícias, e ciclo de produção reflete isso

---------------------------------------------------------------------
Principais vantagens do Django
---------------------------------------------------------------------

- DDL é gerado a partir do código Python, e não o contrário

- fácil de aprender, porém robusto, flexível e extensível

- interface administrativa auto-gerada feita para usar

.. xxx completar

----------------------------------
Estrutura básica de um projeto
----------------------------------

.. image:: _static/django-proj-dir.*
   :align: right

- o projeto *pizza*: sistemas web para uma pizzaria de bairro

- formado por duas aplicações:

    - ``entrega``: sistema interno para receber e despachar pedidos
    
    - ``portal``: site público da pizzaria

- ``pizza/`` e demais arquivos marcados com o selo foram criados pelo comando::

    $ django-admin.py startproject pizza
        


----------------------------------------
Estrutura básica de um projeto (cont.)
----------------------------------------


.. image:: _static/django-proj-dir.*
   :align: right

- ``pizza/``: o diretório raiz do projeto

    - ``entrega/``: o diretório da aplicação ``entrega``
        
    - ``portal/``: diretório da aplicação ``portal``
    
    - ``static/``: diretório de arquivos estáticos do projeto (.css, .gif)
    
    - ``templates/``: diretório de templates do projeto

    - ``__init__.py``: módulo vazio para marcar o diretório ``pizza/`` como um :term:`package`

    - ``manage.py``: script administrativo

    - ``settings.py``: configurações do projeto
    
    - ``urls.py``: mapeamento de cada tipo de URL para a :term:`view` correspondente

    
----------------------------------------
Estrutura básica de uma aplicação
----------------------------------------

.. image:: _static/django-app-dir.*
   :align: right

- diretório ``pizza/entrega/``

    - diretório de uma das aplicações que formam o sistema

    - ``pizza/entrega/`` e demais arquivos marcados com a estrela foram criados via::
    
        $ ./manage.py startapp entrega

- arquivos da aplicação

    - ``__init__.py``: módulo vazio para marcar o diretório ``entrega/`` como um :term:`package`

    - ``admin.py``: configurações da interface administrativa
    
    - ``models.py``: modelos de dados (classes de persistência)
    
    - ``views.py``: funções de tratamento de requisições
    

