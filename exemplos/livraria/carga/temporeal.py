#!/usr/bin/env python
# coding: utf-8

############# encantamentos para ler settings
import sys, os
aqui = os.path.abspath(os.path.split(__file__)[0])
acima = os.path.split(aqui)[0]
sys.path.append(acima)

from django.core.management import setup_environ
import settings
setup_environ(settings)
############# /encantamentos

from livraria.catalogo.models import Livro, Editora, Idioma
from livraria.util.isbn import convertISBN10toISBN13
from random import choice
import pickle
dump = file('carga/produtos.pickle')
prods = pickle.load(dump)
dump.close()

EDITORAS = {31 : {'nome':u'Campus', 'cidade':u'Rio de Janeiro'},
            90 : {'nome':u'Makron Books', 'cidade':u'São Paulo'},
            53 : {'nome':u'Érica', 'cidade':u'São Paulo'},
            108: {'nome':u'Novatec', 'cidade':u'São Paulo'},
            74:  {'nome':u'Wiley', 'cidade':u'New York, NY'},
            159: {'nome':u'Addison-Wesley', 'cidade':u'Reading, MA'},
            112: {'nome':u"O'Reilly", 'cidade':u'Sebastopol, CA'},
            113: {'nome':u"Osborne/McGraw-Hill", 'cidade':u'Berkeley, CA'},
            }
IDIOMAS = {'por':{'sigla':u'pt', 'nome':u'português'},
           'ing':{'sigla':u'en', 'nome':u'inglês'},
           }

#indice = prods.keys()
#shuffle(indice)
#print indice[:120]

indice = set([153836L, 153934L, 153984L, 154123L, 154158L, 154292L, 154367L,
          154411L, 154764L, 154917L, 154923L, 155031L, 155378L, 155487L,
          155811L, 155882L, 156438L, 156988L, 157097L, 157144L, 157207L,
          157218L, 157296L, 157452L, 157517L, 157527L, 157595L, 157641L,
          157700L, 157970L, 158166L, 158290L, 158596L, 158612L, 158756L,
          158904L, 159030L, 159050L, 159195L, 159205L, 159224L, 159291L,
          159308L, 159392L, 159777L, 159818L, 159844L, 160008L, 160106L,
          160125L, 160219L, 160245L, 160378L, 160407L, 160487L, 160804L,
          160919L, 160922L, 160930L, 161088L, 161103L, 161154L, 161451L,
          161487L, 161506L, 161575L, 161705L, 162163L, 162564L, 162810L,
          162953L, 162954L, 163184L, 163245L, 163300L, 163315L, 163379L,
          163637L, 163792L, 163839L, 163867L, 164034L, 164272L, 164312L,
          164540L, 164551L, 164795L, 165115L, 165267L, 165340L, 165450L,
          165475L, 165476L, 165583L, 165867L, 166120L, 166174L, 166240L,
          166613L, 166788L, 167013L, 167296L, 167523L, 167750L, 167814L,
          167829L, 167918L, 167919L, 168238L, 168523L, 168573L, 168638L,
          168661L, 168933L, 168949L, 169096L, 169124L, 169246L, 169285L,
          169316L])

while len(indice) < 200:
    indice.add(choice(prods.keys()))

q = 0
for k in indice:
    prod = prods[k]
    idi = prod['idioma'].lower()[:3]
    if idi in IDIOMAS and prod['id_editora'] in EDITORAS:
        editora = EDITORAS[prod['id_editora']]
        idioma = IDIOMAS[idi]
        print q, prod['isbn'], prod['titulo']
        reg = {}
        reg['titulo'] = prod['titulo'].decode('cp1252')
        reg['isbn'] = convertISBN10toISBN13(prod['isbn'])
        edicao = prod['edicao'].decode('cp1252').strip()
        if idi == 'por' and edicao.isdigit() and int(edicao):
            reg['edicao'] += u'ª'
        else:
            reg['edicao'] += edicao            
        reg['qt_paginas'] = prod['num_paginas']
        reg['dtiso_publicacao'] = prod['ano']
        if prod['encadernacao'].lower().startswith('broc'):
            reg['encadernacao'] = 'br'
        elif prod['encadernacao'].lower().endswith('dura'):
            reg['encadernacao'] = 'du'
        else:
            reg['encadernacao'] = ''
        reg['preco'] = str(prod['preco'])
        reg['editora'] = Editora.objects.get_or_create(**editora)[0]
        reg['idioma'] = Idioma.objects.get_or_create(**idioma)[0]
        livro = Livro(**reg)
        livro.save()
        for nome in prod['nome_autor_texto'].split('/'):
            livro.credito_set.create(nome=nome.strip().decode('cp1252'))
        livro.save()    
        
        q += 1
        if q >= 100: break
