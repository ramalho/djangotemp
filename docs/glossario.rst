
===========
Glossário
===========

.. glossary::

    abstract model
        Em Django um *abstract model* (modelo abstrato) é um :term:`model` que não pode ser instanciado e não tem uma tabela correspodente no banco de dados. Sua utilidade é definir um conjunto de atributos e métodos comuns a vários modelos que serão suas subclasses. Um modelo é definido como abstrato quando tem o atributo ``abstract=True`` em sua classe interna ``Meta``.
        
    application
        Em Django uma *application* (aplicação) é um dos subsistemas que compõe um projeto (:term:`project`). Para criar uma aplicação usa-se o comando ``./manage.py startapp «nome-da-aplicação»``.

    ACID
        Atomicity, Consistency, Isolation, Durability (atomicidade, consistência, isolação e durabilidae): propriedades que asseguram a confiabilidade do processamento de transações.

    callable
        Em Python, um *callable* (invocável) é um objeto que pode ser acionado com o operador de invocação ``()``. Isso inclui funções, métodos, classes e qualquer objeto que implemente um método ``__call__``.
        
    CRUD
        Create, Read, Update, Delete (criar, ler, atualizar, apagar), as quatro operações básicas da persistência de dados.
        
    decorator
        Em Python, um *decorator* é uma função que modifica o comportamento de outra função; por exemplo, um *decorator* pode ser usado para logar todas as chamadas de uma função, ou cachear seus resultados.
        
    DRY
        Don't Repeat Yourself (não se repita): princípio de engenharia de software segundo o qual cada função, dado ou configuração deve aparecer uma e apenas uma vez em um sistema, pois cada duplicação torna muito mais difícil a manutenção e evolução futura do sistema.
        
    iterable
        Em Python um *iterable* (iterável) é uma coleção que pode ser percorrida item a item. Sequências, como listas e tuplas, são iteráveis, mas existem também iteráveis `preguiçosos` que geram seus valores sob demanda, como as expressões geradoras a partir do Python 2.4, ou as instâncias de ``QuerySet`` no Django.
        
    keyword argument
        Em Python um *keyword argument* (argumento nomeado) é um argumento de função passado no formato ``nome=valor`` no momento da invocação. Python vincula tal argumento ao parâmetro de mesmo nome declarado na definição da função. Se não existe parâmetro com este nome, mas existe um parâmetro com prefixo ``**`` (convencionalmente chamado de ``**kwargs), o argumento nomeado é passado para este parâmetro na forma de um item de dicionário. Ou seja, tipicamente o parâmetro ``kwargs`` recebe algo como ``{'nome1':valor1, 'nome2', valor2}``.
        
    KISS
        Keep It Simple, Stupid (preserve a simplicidade, colega [tradução gentil]): princípio de engenharia de software segundo o qual a solução deve ser a mais simples possível capaz de atender aos requisitos do sistema (e não a mais elegante, ou a mais otimizada, ou aquela capaz de resolver um problema que um dia talvez exista). Eistein disse algo como "Things should be as simple as possible, but no simpler" ("As coisas devem ser tão simples quanto possível, mas não simples demais"). http://c2.com/cgi/wiki?EinsteinPrinciple 
        
    manager
        Em Django um *manager* é um objeto presente em cada :term:`model` que permite consultar ou alterar a coleção de instâncias do modelo no banco de dados através de métodos como ``all()``, ``filter()``, ``delete()`` etc. Por default, cada modelo tem um manager chamado ``objects``, mas o programador pode criar modelos adicionais (por exemplo, um modelo chamado ``ativos`` pode limitar as consultas aos objetos considerados ativos em uma dada aplicação). Managers são instâncias de ``django.db.models.manager.Manager`` ou de subclasses desta.
        
    model
        Em Django um *model* (modelo) é uma classe derivada de ``django.db.models.Model`` que representa um tipo de objeto armazenado em uma tabela no banco de dados (exceto quando se trata de um :term:`abstract model`). Por convenção, dentro de uma aplicação (:term:`application`) Django as *views* são criadas em arquivos ``models.py``.
        
    package
        Em Python um *package* (pacote) é um diretório que contém módulos que podem ser importados. Para ser reconhecido como um *package*, o diretório precisa conter um módulo chamado ``__init__.py``, que pode ser um arquivo vazio.
        
    project
        Em Django um *project* (projeto) é um :term:`package` que contém na sua raiz um arquivo `settings.py` com as configurações globais de várias :term:`aplicações<application>`.

    template
        Um *template* (gabarito) é um arquivo que representa genericamente um tipo de página com conteúdo variável. Normalmente o *template* é formado por código HTML com marcações especiais da linguagem de tags do Django. Os *templates* podem ser renderizados, processo pelo qual as marcações do Django são processadas e substituidas por valores específicos, produzindo código HTML puro (sem tags do Django). 
        
    view
        No Django, uma *view* (visão) é uma função que aceita como primeiro parâmetro um objeto ``request`` que representa uma requisição Web (além de outros parâmetros), e trata esta requisição, normalmente produzindo um :term:`template` HTML renderizado. Por convenção, dentro de uma aplicação (:term:`application`) Django as *views* são criadas em arquivos ``views.py``.
                
