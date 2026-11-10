# -*- coding: utf-8 -*-
"""Monta e executa andre_becker_DR1_TP2.ipynb.

    uv run --no-project --python 3.12 --with nbformat --with nbclient --with ipykernel --with matplotlib python scripts/gerar_notebook.py

O texto fica aqui; os números das tabelas e dos gráficos são calculados ao executar, chamando as
mesmas funções de src/ que geraram as telas do terminal (contagens com semente fixa, então iguais).

Cada exercício segue o mesmo roteiro visual: selos (tema, estrutura, Big O), resumo em citação,
cartões com os números principais e quatro blocos fixos: Fundamentação, Implementação, Execução e
Análise, que termina com o link de volta ao sumário.
"""
import os
import re
import sys
from urllib.parse import quote

import nbformat
from nbclient import NotebookClient

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'src'))
from apoio_notebook import cartoes_html  # noqa: E402  (o mesmo HTML que o notebook usaria)
SAIDA = os.path.join(RAIZ, 'andre_becker_DR1_TP2.ipynb')
REPO = 'https://github.com/andrebecker84/dr1-tp2-estruturas-de-dados'
NBVIEWER = 'https://nbviewer.org/github/andrebecker84/dr1-tp2-estruturas-de-dados/blob/main/andre_becker_DR1_TP2.ipynb'

# Cor do selo de tema: a mesma família de exercícios tem a mesma cor em todo o notebook.
TEMAS = {'hash tables': '2A78D6', 'ordenação': '1BAF7A', 'pilha e fila': 'EB6834', 'funções hash': '6250D6'}

celulas = []


def _inline(t):
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'<i>\1</i>', t)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)


def _tabela(linhas):
    cel = [[c.strip() for c in l.strip().strip('|').split('|')] for l in linhas]
    cab, corpo = cel[0], cel[2:]
    th = ''.join(f'<th style="text-align:left;padding:7px 12px;background:#1E3A8A;color:#fff">{_inline(c)}</th>'
                 for c in cab) if any(cab) else ''
    tr = ''.join('<tr>' + ''.join(f'<td style="text-align:left;padding:6px 12px;border-bottom:1px solid #e4e3df">'
                                  f'{_inline(c)}</td>' for c in l) + '</tr>' for l in corpo)
    thead = f'<thead><tr>{th}</tr></thead>' if th else ''
    return (f'<table style="margin-left:0;margin-right:auto;border-collapse:collapse;font-size:13px">'
            f'{thead}<tbody>{tr}</tbody></table>')


def tabelas_em_html(texto):
    """Tabelas markdown viram HTML alinhado à esquerda (Jupyter e VS Code centralizam as de markdown)."""
    saida, bloco, em_codigo = [], [], False
    for l in texto.split('\n') + ['']:
        if l.startswith('```'):
            em_codigo = not em_codigo
        if l.startswith('|') and not em_codigo:
            bloco.append(l)
            continue
        if bloco:
            saida.append(_tabela(bloco))
            bloco = []
        saida.append(l)
    return '\n'.join(saida[:-1])


def md(t):
    celulas.append(nbformat.v4.new_markdown_cell(tabelas_em_html(t.strip('\n'))))


def py(t, oculto=False):
    """Células que só montam cartões, figuras, tabelas e gráficos ficam com o código recolhido."""
    c = nbformat.v4.new_code_cell(t.strip('\n'))
    if oculto:
        c.metadata['jupyter'] = {'source_hidden': True}
        c.metadata['tags'] = ['hide-input']
    celulas.append(c)


def selo(rotulo, valor, cor):
    """Selo do shields.io: imagem, então aparece igual no GitHub, no nbviewer e no Jupyter."""
    def q(s):
        return quote(s.replace('-', '--').replace('_', '__'), safe='')
    return f'<img src="https://img.shields.io/badge/{q(rotulo)}-{q(valor)}-{cor}?style=flat-square" />'


def secao(ancora, numero, titulo, resumo, tema, estrutura, big_o):
    md(f"""
<a id="{ancora}"></a>

## {numero} · {titulo}

{selo('tema', tema, TEMAS[tema])} {selo('estrutura', estrutura, '52514E')} {selo('Big O', big_o, '1E3A8A')}

> {resumo}
""")


def cartoes(*itens):
    """Cartões gravados como HTML na célula de texto anterior (o título do exercício): sem célula de código,
    eles aparecem limpos também no nbviewer, que não recolhe código."""
    anterior = celulas[-1]
    if anterior.cell_type == 'markdown':
        anterior.source += '\n\n' + cartoes_html(*itens)
    else:
        md(cartoes_html(*itens))


def fundamentacao(texto, titulo='Fundamentação'):
    md(f'#### 📐 {titulo}\n\n' + texto.strip('\n'))


def implementacao(codigo_py, texto=''):
    """O subtítulo entra no fim da célula de texto anterior: um subtítulo sozinho não precisa de célula."""
    titulo = '#### 🧩 Implementação' + (f'\n\n{texto.strip()}' if texto else '')
    anterior = celulas[-1]
    if anterior.cell_type == 'markdown':
        anterior.source += '\n\n' + tabelas_em_html(titulo)
    else:
        md(titulo)
    py(codigo_py)


def execucao(numero, legenda, grafico=None):
    md('#### 🖥️ Execução no terminal')
    py(f"tela({numero}, {legenda!r})", oculto=True)
    if grafico:
        py(grafico, oculto=True)


def analise(texto):
    md('#### 📊 Análise\n\n' + texto.strip('\n') + VOLTAR)


VOLTAR = '\n\n<p align="right" style="text-align:right"><a href="#sumario">⬆ voltar ao sumário</a></p>\n\n---'


# =====================================================================================  CAPA
md(f"""
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E3A8A,100:2A78D6&height=190&section=header&text=Hash%20Tables%2C%20Pilhas%20e%20Filas&fontSize=46&fontColor=ffffff&fontAlignY=36&desc=DR1-TP2%20%C2%B7%20notebook&descAlignY=60&descSize=17" width="100%" />

# #️⃣ Hash Tables, Pilhas e Filas

**Da solução correta à solução eficiente: laços aninhados trocados por hash tables, Selection e Insertion Sort instrumentados, pilha e fila de capacidade fixa e a qualidade de funções hash, com Big O medido em cada passo**

<img src="https://img.shields.io/badge/Python-3.15.2-3776AB?style=flat-square&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Ubuntu-24.04%20(WSL2)-E95420?style=flat-square&logo=ubuntu&logoColor=white" /> <img src="https://img.shields.io/badge/depend%C3%AAncias-s%C3%B3%20biblioteca%20padr%C3%A3o-3776AB?style=flat-square" /> <img src="https://img.shields.io/badge/unittest-29%20passando-1BAF7A?style=flat-square" /> <img src="https://img.shields.io/badge/Big%20O-O(1)%20%C2%B7%20O(N)%20%C2%B7%20O(N%C2%B2)-6250D6?style=flat-square" />

| | |
|---|---|
| **Aluno** | André Luis Becker |
| **Professor** | Ian Monteiro Nunes |
| **Disciplina** | DR1 · Velocidade e Qualidade com Estruturas de Dados e Algoritmos |
| **Bloco · Trimestre** | Ciência da Computação · 26E4 |
| **Repositório** | [{REPO.split('github.com/')[1]}]({REPO}) · [versão renderizada no nbviewer]({NBVIEWER}) |
| **Entrega** | `andre_becker_DR1_TP2.pdf` · código em [`src/`]({REPO}/tree/main/src) · telas em [`evidencias/telas/`]({REPO}/tree/main/evidencias/telas) |
""")

md(f"""
<a id="sumario"></a>

## 📚 Sumário

| | Seção | | Seção |
|:-:|---|:-:|---|
| 1 | [Visão geral](#visao) | 10 | [Ex. 9 · Pilha com controle de erros](#ex09) |
| 2 | [Ex. 1 · Maior número único](#ex01) | 11 | [Ex. 10 · Fila com ponteiros](#ex10) |
| 3 | [Ex. 2 · Interseção de arrays](#ex02) | 12 | [Ex. 11 · Inversão de string com pilha](#ex11) |
| 4 | [Ex. 3 · Primeiro valor duplicado](#ex03) | 13 | [Ex. 12 · Funções hash e distribuição](#ex12) |
| 5 | [Ex. 4 · Letra ausente do alfabeto](#ex04) | 14 | [Testes automatizados](#testes) |
| 6 | [Ex. 5 · Primeiro caractere não repetido](#ex05) | 15 | [Atendimento ao enunciado e à rubrica](#rubrica) |
| 7 | [Ex. 6 · Selection Sort](#ex06) | 16 | [Conclusão](#conclusao) |
| 8 | [Ex. 7 · Insertion Sort](#ex07) | 17 | [Referências](#referencias) |
| 9 | [Ex. 8 · Pilha ou fila](#ex08) | | |

{selo('tema', 'hash tables', TEMAS['hash tables'])} Ex. 1 a 5 &nbsp; {selo('tema', 'ordenação', TEMAS['ordenação'])} Ex. 6 e 7 &nbsp; {selo('tema', 'pilha e fila', TEMAS['pilha e fila'])} Ex. 8 a 11 &nbsp; {selo('tema', 'funções hash', TEMAS['funções hash'])} Ex. 12
""")

# =====================================================================================  1. VISÃO GERAL
md("""
<a id="visao"></a>

## 1 · Visão geral

Como no TP1, meço eficiência **contando passos** (comparações, trocas, deslocamentos e acessos a
estruturas), não tempo: a contagem não depende da máquina e mostra direto a forma do crescimento
(NUNES, 2026a). Cada exercício é um script em `src/` que confere o próprio resultado com `[OK]` ou
`[FALHA]`. As telas são da execução real no **WezTerm**, com o Ubuntu 24.04 do WSL2, shell fish e
Python 3.15.2.
""")

py("""
import sys
sys.path.insert(0, 'src')
from apoio_notebook import *              # tabelas, cartões, figuras e estilo dos gráficos
from algoritmos.metricas import medir
import matplotlib.pyplot as plt
estilo()
print('src/ importado: as células abaixo chamam as mesmas funções que rodaram no terminal')
""")
cartoes(('12', 'exercícios, cada um com verificação [OK]'), ('29', 'testes automatizados passando'),
        ('13', 'telas do terminal real'), ('1.901×', 'menos passos no melhor ganho (Ex. 1)'))

md("""
#### Quadro-resumo

| Ex. | Problema | Estrutura | Resultado principal | Big O |
|:-:|---|---|---|---|
| 1 | Maior número único | hash table | 25.000.000 → 13.148 passos (N = 5.000) | O(N²) → O(N) |
| 2 | Interseção de arrays | hash table | 2 × 1.000.000 elementos em 2,3 milhões de acessos | O(N·M) → O(N + M) |
| 3 | Primeiro duplicado | hash table | 2N − 1 acessos no pior caso | O(N) |
| 4 | Letra ausente | array de presença (26) | acentos, dígitos e pontuação tratados | O(N), espaço O(1) |
| 5 | Primeiro não repetido | hash table | 3N acessos no pior caso | O(N) |
| 6 | Selection Sort | array | N(N−1)/2 comparações em qualquer estado | Θ(N²) |
| 7 | Insertion Sort | array | 999 passos (ordenada) × 999.000 (invertida) | O(N) a O(N²) |
| 8 | Atendimento por ordem de chegada | **fila** | A espera 2 instantes na fila e 9 na pilha | O(1) por operação |
| 9 | Pilha de capacidade fixa | array + topo | overflow e underflow sem corromper o estado | O(1) |
| 10 | Fila com ponteiros | array circular | 100.000 operações sem violar o FIFO | O(1) |
| 11 | Inversão de string | pilha | N push + N pop, sem slicing | O(N) |
| 12 | Funções hash com M = 10 | | h₃ só alcança 6 dos 10 baldes | |

#### Como ler cada exercício

| Bloco | O que mostra |
|---|---|
| Selos e cartões | tema, estrutura, Big O e os números principais |
| 📐 Fundamentação | a teoria, com a aula ou o livro de referência, e as decisões tomadas |
| 🧩 Implementação | o código do núcleo, lido direto de `src/` |
| 🖥️ Execução no terminal | a tela real do WezTerm e, quando ajuda, um gráfico calculado aqui |
| 📊 Análise | o que os números mostram e a complexidade em Big O |

#### Organização do código

O núcleo (`src/algoritmos/`) não tem `print`: recebe dados, devolve o resultado e soma os passos num
objeto `Metricas`. Os scripts `exNN_*.py` montam as entradas e mostram a saída (`src/apresentacao/`),
e os testes (`src/tests/`) conferem o núcleo.

```
src/
├── algoritmos/      unicos · intersecao · duplicados · texto · ordenacao · pilha · fila · hashing · metricas · erros
├── apresentacao/    tabelas e cores do terminal
├── tests/           29 testes (unittest)
├── dados.py         entradas com semente fixa (42)
└── ex01 … ex12      um script por exercício
```
""" + VOLTAR)

# =====================================================================================  EX 1
secao('ex01', 2, 'Exercício 1 · Maior número único com hash table',
      'Mesmo problema, duas estruturas: a escolha certa troca N² comparações por no máximo 3N acessos.',
      'hash tables', 'dict', 'O(N²) → O(N)')
cartoes(('O(N²) → O(N)', 'complexidade'), ('25.000.000 → 13.148', 'passos com N = 5.000'),
        ('1.901×', 'menos passos'), ('10 / 10', 'listas com o mesmo resultado nas duas versões'))
fundamentacao("""
Um laço dentro de outro sobre os mesmos dados é o padrão clássico de O(N²): para cada um dos N
elementos, o laço interno percorre os N de novo (NUNES, 2026a; WENGROW, 2023, cap. 4). A saída é
responder "quantas vezes este valor aparece?" sem varrer a lista, guardando as contagens numa
**hash table**, que calcula a posição a partir da própria chave e lê ou grava em **O(1) no caso
médio** (WENGROW, 2023, cap. 8). Em Python, o `dict` é uma hash table (PYTHON SOFTWARE FOUNDATION, 2024b).

Na versão aninhada conto cada `arr[j] == arr[i]`. Na versão com hash conto cada acesso ao dicionário:
2 por elemento na contagem (`get` + gravação) e 1 por par na escolha do maior.
""")
implementacao("""
from algoritmos.unicos import maior_unico_aninhado, maior_unico_hash
codigo(maior_unico_aninhado, maior_unico_hash)
""")
execucao(1, 'Exercício 1 no WezTerm: exemplos com o mesmo resultado e crescimento de 10 a 5.000 elementos.', """
from dados import inteiros_com_repetidos
tamanhos = [100, 250, 500, 1000, 2000, 4000]
aninhado = [medir(maior_unico_aninhado, inteiros_com_repetidos(n))[1].comparacoes for n in tamanhos]
hash_ = [medir(maior_unico_hash, inteiros_com_repetidos(n))[1].acessos for n in tamanhos]
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.loglog(tamanhos, aninhado, marker='o', color=LARANJA, label='laços aninhados: N² comparações')
ax.loglog(tamanhos, hash_, marker='o', color=AZUL, label='hash table: até 3N acessos')
ax.set_title('Maior número único: passos em função de N')
ax.set_xticks(tamanhos, [milhar(n) for n in tamanhos]); ax.minorticks_off()
ax.set_xlabel('N (escala log)'); ax.set_ylabel('passos (escala log)'); ax.legend()
mostrar('ex01_aninhado_x_hash')
legenda_grafico('Gráfico 1. Em escala log-log a inclinação é o expoente: 2 para N² e 1 para N.')
""")
analise("""
O gargalo está no laço interno, que nunca para antes do fim: a versão aninhada faz N² comparações em
qualquer entrada. Na versão com hash table, as duas passadas vêm uma depois da outra, e não uma dentro
da outra, somando 2N + U acessos (U = valores distintos, no máximo N). O custo é **O(N)**.

Multiplicar N por 10 multiplica as comparações por 100 e os acessos por 10. O preço da melhoria é a
memória extra do dicionário, O(U).
""")

# =====================================================================================  EX 2
secao('ex02', 3, 'Exercício 2 · Interseção de arrays em tempo linear',
      'O primeiro array vai para uma hash table, e cada valor do segundo é consultado em um passo.',
      'hash tables', 'dict', 'O(N·M) → O(N + M)')
cartoes(('O(N·M) → O(N + M)', 'complexidade'), ('2 × 1.000.000', 'elementos validados'),
        ('1,17', 'acessos por elemento'), ('0,94 s', 'no Ubuntu, contra 10¹² comparações no aninhado'))
fundamentacao("""
A Aula 5 mostra a interseção com laços aninhados: N × M comparações, que a saída antecipada (`break`)
só melhora no melhor caso (NUNES, 2026b). Com o primeiro array numa hash table, "este valor está em
`a`?" vira uma consulta O(1), e o total cai para **N inserções + M consultas** (WENGROW, 2023, cap. 8).

> **Decisões.** Sem `set`, `&` nem `intersection`: só um `dict` montado à mão. O valor de cada chave
> indica se ela ainda pode entrar no resultado (`True`) ou se já entrou (`False`), então repetidos não
> se duplicam. O resultado segue a ordem do segundo array.
""")
implementacao("""
from algoritmos.intersecao import intersecao, intersecao_aninhada
codigo(intersecao)
""")
execucao(2, 'Exercício 2: exemplos, comparação com a versão aninhada e validação com até 1.000.000 de elementos por array.', """
import ex02_intersecao as ex02
tamanhos = [250, 500, 1000, 2000, 4000]
casos = [ex02.pares_e_multiplos_de_3(n)[:2] for n in tamanhos]
aninhado = [medir(intersecao_aninhada, a, b)[1].comparacoes for a, b in casos]
hash_ = [medir(intersecao, a, b)[1].acessos for a, b in casos]
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.plot(tamanhos, [c / 1e6 for c in aninhado], marker='o', color=LARANJA, label='laços aninhados (com break)')
ax.plot(tamanhos, [c / 1e6 for c in hash_], marker='o', color=AZUL, label='hash table')
ax.set_title('Interseção: passos para N = M')
ax.set_xticks(tamanhos, [milhar(n) for n in tamanhos])
ax.set_xlabel('N = M'); ax.set_ylabel('milhões de passos'); ax.legend()
mostrar('ex02_intersecao')
legenda_grafico('Gráfico 2. A curva do aninhado é uma parábola; a da hash table fica colada no zero, crescendo em linha reta.')
""")
analise("""
Para validar em escala, `a` recebe os pares e `b` os múltiplos de 3, embaralhados. A resposta é
conhecida por construção (os múltiplos de 6 menores que 2N), e o script confere a quantidade, os
valores e a ausência de repetidos.

Os acessos por elemento ficam constantes em **1,17** de 10 mil a 1 milhão de elementos, o sinal de um
custo linear. A versão aninhada precisaria de até 10¹² comparações: mesmo a 10 milhões por segundo,
seriam mais de 27 horas.
""")

# =====================================================================================  EX 3
secao('ex03', 4, 'Exercício 3 · Primeiro valor duplicado',
      'Uma passada na ordem de leitura, com uma hash table dos valores já vistos.',
      'hash tables', 'dict', 'O(N)')
cartoes(('O(N)', 'tempo · memória O(N)'), ('2N − 1', 'acessos no pior caso'),
        ('12.497.501 → 10.001', 'passos com N = 5.001'), ('3 acessos', 'quando o par está no início'))
fundamentacao("""
Guardar como chaves os valores já processados transforma "já vi este valor?" de uma busca linear em
uma consulta O(1) (WENGROW, 2023, cap. 8). Como a leitura segue a ordem do array e para na primeira
repetição, o resultado é o valor cuja **segunda ocorrência aparece primeiro**, sem reprocessar nada.
""")
implementacao("""
from algoritmos.duplicados import primeiro_duplicado
codigo(primeiro_duplicado)
""")
execucao(3, 'Exercício 3: cinco entradas com um par repetido e o pior caso (par nas pontas) contra a versão aninhada.')
analise("""
Cada valor novo custa 2 acessos (consulta e gravação) e o repetido custa 1, então o pior caso, com o
par nas pontas, faz 2N − 1 acessos: **O(N)**. Os exemplos mostram que strings diferenciam maiúsculas
(`'Ana'` ≠ `'ana'`) e que a string vazia é uma chave válida. O enunciado garante exatamente um par,
mas, sem repetição, a função devolve `None` em vez de falhar.
""")

# =====================================================================================  EX 4
secao('ex04', 5, 'Exercício 4 · Letra ausente do alfabeto',
      'Normalizo cada caractere e marco a presença num array de 26 posições.',
      'hash tables', 'array de presença', 'O(N)')
cartoes(('O(N)', 'tempo'), ('O(1)', 'espaço: sempre 26 posições'), ('7 / 7', 'textos com a resposta esperada'),
        ('Ç → c · Á → a', 'normalização'))
fundamentacao("""
As chaves possíveis são conhecidas e contíguas (`a` a `z`), então a estrutura auxiliar pode ser um
array indexado por `ord(letra) − ord('a')`: é o **endereçamento direto**, uma hash table cuja função
hash não tem colisões (CORMEN et al., 2012, seção 11.1).

> **Decisões.** `casefold()` ignora maiúsculas. A decomposição Unicode (NFD) separa o acento da letra,
> então `ç` conta como `c` e `ã` como `a` (PYTHON SOFTWARE FOUNDATION, 2024c). Espaços, dígitos e
> pontuação ficam fora do intervalo `a`–`z` e são descartados. A função devolve **todas** as letras
> ausentes; quando falta uma só, a lista tem um elemento.
""")
implementacao("""
from algoritmos.texto import letras_ausentes, sem_acento
codigo(sem_acento, letras_ausentes)
""")
execucao(4, 'Exercício 4: frases em inglês e português, com acentos, dígitos e pontuação, e textos de até 1.000.000 de caracteres.')
analise("""
T(N) = N leituras + até N marcações + 26 verificações = **O(N)**. A memória extra é o array de 26
posições, que não depende do tamanho do texto, então o espaço é **O(1)**. A última frase do exemplo
foi escrita antes de o alfabeto incluir k, w e y, e a função devolve as três.
""")

# =====================================================================================  EX 5
secao('ex05', 6, 'Exercício 5 · Primeiro caractere não repetido',
      'Primeiro conto as frequências; depois verifico na ordem original.',
      'hash tables', 'dict', 'O(N)')
cartoes(('O(N)', 'tempo · memória O(K), K caracteres distintos'), ('2 passadas', 'contagem e verificação'),
        ('3N', 'acessos no pior caso'), ('9 / 9', 'exemplos corretos'))
fundamentacao("""
Um caractere só é "não repetido" depois de visto o texto inteiro, então a solução separa as duas
etapas (WENGROW, 2023, cap. 8):

1. a **contagem** grava a frequência de cada caractere na hash table, numa passada;
2. a **verificação** percorre **o texto**, e não o dicionário, e devolve o primeiro caractere com
   frequência 1. Assim a ordem original é preservada de forma explícita.
""")
implementacao("""
from algoritmos.texto import primeiro_nao_repetido
codigo(primeiro_nao_repetido)
""")
execucao(5, 'Exercício 5: nove exemplos e o pior caso, com o único caractere no fim, até 1.000.000 de caracteres.')
analise("""
São 2 acessos por caractere na contagem e no máximo 1 na verificação, logo **3N**: a tabela de
crescimento mostra exatamente 3N de 1 mil a 1 milhão de caracteres. Maiúscula e minúscula são
caracteres diferentes (`'Infnet'` → `'I'`), e um texto sem caractere único devolve `None`.
""")

# =====================================================================================  EX 6
secao('ex06', 7, 'Exercício 6 · Selection Sort',
      'Cada travessia acha o menor do trecho não ordenado e faz no máximo uma troca.',
      'ordenação', 'array', 'Θ(N²)')
cartoes(('Θ(N²)', 'melhor, médio e pior caso'), ('499.500', 'comparações com N = 1.000, em qualquer estado'),
        ('≤ N − 1', 'trocas'), ('10 + 2', 'comparações e trocas no exemplo da Aula 4'))
fundamentacao("""
A travessia *i* compara o menor encontrado com os N − 1 − *i* elementos seguintes, e a soma dá
**(N² − N)/2 comparações** com **até N − 1 trocas**. Sem o termo de menor grau e sem a constante,
fica **O(N²)** (NUNES, 2026a; WENGROW, 2023, cap. 5). Como nada encerra uma travessia mais cedo, o
custo é o mesmo em toda entrada: **Θ(N²)**, um limite justo (NUNES, 2026b).
""")
implementacao("""
from algoritmos.ordenacao import selection_sort, insertion_sort
codigo(selection_sort)
""")
execucao(6, 'Exercício 6: passo a passo no array da Aula 4 e listas de 10, 100 e 1.000 elementos em quatro estados iniciais.')
analise("""
As comparações deram N(N−1)/2 nos quatro estados, como prevê a análise. Só as trocas mudam com o
estado inicial (N = 1.000):

| Estado inicial | Trocas | Motivo |
|---|---|---|
| ordenada | 0 | o menor já está no lugar, e o código não troca |
| quase ordenada | 44 | só os pares fora do lugar trocam |
| invertida | 500 | cada troca põe dois elementos no lugar |
| aleatória | 995 | quase toda travessia termina com uma troca |

O passo a passo de `[4 2 7 1 3]` reproduz o slide da Aula 4: 10 comparações e 2 trocas.
""")

# =====================================================================================  EX 7
secao('ex07', 8, 'Exercício 7 · Insertion Sort',
      'Adaptativo: quase nada a fazer numa lista quase ordenada, o máximo numa lista invertida.',
      'ordenação', 'array', 'O(N) a O(N²)')
cartoes(('O(N) → O(N²)', 'melhor → pior caso'), ('999 × 999.000', 'passos: ordenada × invertida (N = 1.000)'),
        ('deslocamentos = inversões', 'em todas as 12 listas'), ('22 passos', 'no exemplo da Aula 5'))
fundamentacao("""
O valor da posição vai para `temp`, os maiores à esquerda deslocam uma casa e `temp` entra no espaço
vazio (NUNES, 2026b; WENGROW, 2023, cap. 6):

| Caso | Entrada | Comparações | Deslocamentos | Big O |
|---|---|---|---|---|
| Melhor | ordenada | N − 1 | 0 | O(N) |
| Médio | aleatória | ≈ N²/4 | ≈ N²/4 | O(N²) |
| Pior | invertida | N(N−1)/2 | N(N−1)/2 | O(N²) |

Cada deslocamento desfaz exatamente uma **inversão** (par fora de ordem). Por isso o custo real é
O(N + I), em que I é o número de inversões, e uma lista quase ordenada custa quase O(N).
""")
implementacao("codigo(insertion_sort)")
execucao(7, 'Exercício 7: passo a passo da Aula 5, quatro estados iniciais e comparação com o Selection Sort.', """
from dados import Cenario, lista_no_cenario
estados = list(Cenario)
insercao, selecao = [], []
for estado in estados:
    lista = lista_no_cenario(1000, estado)
    m = medir(insertion_sort, lista)[1]; insercao.append(m.comparacoes + m.deslocamentos)
    m = medir(selection_sort, lista)[1]; selecao.append(m.comparacoes + m.trocas)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
x = range(len(estados))
for desloc, valores, cor, nome in ((-0.2, insercao, VERDE_AGUA, 'Insertion Sort'), (0.2, selecao, LARANJA, 'Selection Sort')):
    barras = ax.bar([i + desloc for i in x], valores, 0.38, color=cor, label=nome)
    for b, v in zip(barras, valores):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.15, milhar(v), ha='center', fontsize=8, color=TINTA_2)
ax.set_yscale('log'); ax.set_ylim(500, 1.2e7)
ax.set_xticks(list(x), [str(e) for e in estados])
ax.set_title('Passos com N = 1.000 por estado inicial'); ax.set_ylabel('passos (escala log)'); ax.legend(loc='upper left', ncol=2)
mostrar('ex07_insertion_x_selection')
legenda_grafico('Gráfico 3. Comparações + deslocamentos (Insertion) e comparações + trocas (Selection).')
""")
analise("""
A lista quase ordenada custou 1.043 comparações e 44 deslocamentos, quase linear; a invertida custou
499.500 de cada, o pior caso exato. Contra o Selection Sort, o Insertion vence na lista ordenada, na
quase ordenada e, por pouco, na aleatória, e perde na invertida (999 mil contra 500 mil passos), como
no quadro da Aula 5.

O Insertion Sort é a escolha para dados pequenos ou quase ordenados. O Selection Sort compensa quando
escrever na memória é caro, porque faz no máximo N − 1 trocas.
""")

# =====================================================================================  EX 8
secao('ex08', 9, 'Exercício 8 · Pilha ou fila?',
      'Um sistema que atende estritamente na ordem de chegada precisa de uma fila.',
      'pilha e fila', 'fila (FIFO)', 'O(1) por operação')
cartoes(('Fila (FIFO)', 'escolha'), ('O(1)', 'enqueue, dequeue e peek'),
        ('2 × 9', 'espera da 1ª solicitação: fila × pilha'), ('A B C D E', 'ordem de atendimento da fila'))
fundamentacao("""
A regra "atender estritamente na ordem de chegada" é a definição de **FIFO** (*first in, first out*):
quem chega primeiro sai primeiro, como numa fila de cinema (WENGROW, 2023, cap. 9). A **pilha** é
LIFO e sempre atende o último que chegou. Ela viola a regra e pode deixar o primeiro esperando
indefinidamente enquanto chegam novas solicitações (*starvation*). Com uma estrutura restrita, a
própria estrutura impõe a regra de negócio: não existe operação que atenda fora de ordem.

| Operação | O que faz no sistema | Custo |
|---|---|---|
| `enqueue(s)` | registra a solicitação que chegou, no **fim** da fila | O(1) |
| `dequeue()` | retira a mais antiga, do **início**, para atendimento | O(1) |
| `peek()` | consulta quem é o próximo sem retirar | O(1) |
| `is_empty()` / `is_full()` | evita atender sem solicitações e aceitar além da capacidade | O(1) |

> **Detalhe de implementação.** Retirar do início de uma `list` do Python (`pop(0)`) custa O(N), porque
> todos os elementos se deslocam (PYTHON SOFTWARE FOUNDATION, 2024a). A fila do Exercício 10 usa um
> array circular com ponteiros e mantém o `dequeue` em O(1).
""", titulo='Justificativa da escolha')
implementacao("""
from algoritmos.fila import Queue
from algoritmos.pilha import Stack
import ex08_pilha_ou_fila as ex08
codigo(ex08.simular)
""", 'A simulação aplica os mesmos eventos às duas estruturas, usando a `Queue` do Exercício 10 e a `Stack` do Exercício 9.')
execucao(8, 'Exercício 8: os mesmos eventos aplicados a uma fila e a uma pilha. A fila respeita a ordem de chegada; a pilha não.')
analise("""
Com chegadas e atendimentos intercalados, a fila atende **A B C D E**, exatamente a ordem de chegada,
e a maior espera é de 4 instantes. A pilha atende **B D E C A**: a solicitação A, a primeira a chegar,
só é atendida no fim, depois de 9 instantes.
""")

# =====================================================================================  EX 9
secao('ex09', 10, 'Exercício 9 · Pilha com controle de erros',
      'Array de tamanho fixo e um índice de topo, encapsulados numa classe.',
      'pilha e fila', 'Stack (LIFO)', 'O(1)')
cartoes(('O(1)', 'push, pop e peek'), ('Overflow · Underflow', 'exceções próprias'),
        ('estado intacto', 'após cada erro'), ('14 operações', 'com o estado registrado'))
fundamentacao("""
O objeto `Stack` guarda o que precisa sobreviver entre as operações: o array `_dados`, criado uma vez
com a capacidade fixa (`[None] * capacidade`), e o índice `_topo` (−1 = vazia). Nada é recriado a
cada chamada, e o tamanho e a capacidade são derivados desses dois atributos
(GOODRICH; TAMASSIA; GOLDWASSER, 2013, cap. 6).

`push` em pilha cheia levanta `Overflow`; `pop` e `peek` em pilha vazia levantam `Underflow`. A
verificação vem **antes** de qualquer alteração, então um erro nunca deixa a pilha num estado
inconsistente. Usei exceções, e não um valor de retorno especial, para que o uso indevido não passe
despercebido.
""", titulo='Persistência do estado e erros')
implementacao("""
from algoritmos.erros import Overflow, Underflow
codigo(Stack.push, Stack.pop, Stack.peek)
""")
execucao(9, 'Exercício 9: Stack(4) com o array interno, o topo e o tamanho após cada uma das 14 operações, incluindo overflow e underflow.')
analise("""
O passo 6 tenta empilhar o 50 com a pilha cheia: o `Overflow` é tratado e o array continua
`[10 20 30 40]`. Os passos 13 e 14 operam na pilha vazia, e o topo continua −1. Cada `pop` devolve o
último valor inserido (LIFO) e libera a posição (`·`).
""")

# =====================================================================================  EX 10
secao('ex10', 11, 'Exercício 10 · Fila com ponteiros',
      'Dois ponteiros andam em círculo sobre um array fixo: nada é deslocado.',
      'pilha e fila', 'Queue (FIFO)', 'O(1)')
cartoes(('O(1)', 'enqueue, dequeue e peek'), ('início · fim · tamanho', 'estado da fila'),
        ('100.000', 'operações aleatórias validadas'), ('0', 'violações do FIFO'))
fundamentacao("""
`inicio` aponta o próximo a sair e `fim` a posição livre onde entra o próximo. Os dois avançam com
`(i + 1) % capacidade` e, ao chegar ao fim do array, voltam para a posição 0 (**array circular**).
Sem isso, as posições liberadas no começo nunca seriam reusadas (GOODRICH; TAMASSIA; GOLDWASSER, 2013,
seção 6.2). O `tamanho` resolve a ambiguidade de `inicio == fim`, que acontece tanto na fila vazia
quanto na cheia.

```
 passo 8: fila cheia depois de o fim dar a volta
 índice     0    1    2    3
          ┌────┬────┬────┬────┐
          │ 50 │ 60 │ 30 │ 40 │    tamanho 4/4
          └────┴────┴────┴────┘
                      ▲
               início = fim = 2      próximo a sair: 30 (o mais antigo)
```
""", titulo='Funcionamento')
implementacao("codigo(Queue.enqueue, Queue.dequeue)")
execucao(10, 'Exercício 10: Queue(4) com início, fim e tamanho após cada operação, e a validação FIFO com 100.000 operações aleatórias.')
analise("""
Para validar o FIFO, entram os inteiros 1, 2, 3, … e cada `dequeue` precisa devolver exatamente o
próximo da sequência. Em 100.000 operações aleatórias com capacidade 8, os 44.425 `dequeue` saíram em
ordem, e os 5.505 `Overflow` e 5.641 `Underflow` foram tratados sem alterar a fila.
""")

# =====================================================================================  EX 11
secao('ex11', 12, 'Exercício 11 · Inversão de string com pilha',
      'O último caractere a entrar é o primeiro a sair: a pilha inverte a ordem por definição.',
      'pilha e fila', 'Stack (LIFO)', 'O(N)')
cartoes(('O(N)', 'tempo e memória'), ('N push + N pop', 'operações O(1)'), ('8 / 8', 'strings conferidas'),
        ('sem slicing', 'nem reversed()'))
fundamentacao("""
Reaproveito a `Stack` do Exercício 9 com capacidade igual ao tamanho da string. Empilho os N
caracteres e desempilho todos; como a pilha é LIFO, eles saem na ordem inversa (WENGROW, 2023,
cap. 9). O `"".join` só concatena os caracteres na ordem em que saíram da pilha.
""")
implementacao("""
from algoritmos.texto import inverter
codigo(inverter)
""")
execucao(11, 'Exercício 11: pilha e saída a cada push e pop para "Infnet", e testes com palíndromo, acentos, string unitária e vazia.')
analise("""
A conferência não usa slicing: para cada posição *i*, verifico que `invertida[i] == texto[N − 1 − i]` e
que inverter duas vezes devolve o original. Os casos de borda passaram: a string vazia (pilha com
capacidade mínima 1 e nenhum push), a de um caractere e o palíndromo `arara`.
""")

# =====================================================================================  EX 12
secao('ex12', 13, 'Exercício 12 · Análise de funções hash',
      'Com M = 10, uma função hash só enxerga o último dígito da chave, e isso decide tudo.',
      'funções hash', 'M = 10', 'colisões')
cartoes(('6 de 10', 'baldes que h₃ consegue usar'), ('h₂ ≡ h₁', 'mesma distribuição, baldes renomeados'),
        ('50 em 1 balde', 'múltiplos de 10 em qualquer das três'), ('M = 11', 'distribui os mesmos conjuntos'))
fundamentacao(r"""
Tabela de tamanho fixo M = 10 e chaves inteiras k ≥ 0:

| Função | Definição | Depende de |
|---|---|---|
| h₁ | k mod 10 | último dígito de k |
| h₂ | 7k mod 10 | último dígito de k |
| h₃ | k² mod 10 | último dígito de k |

Como (a · b) mod M = ((a mod M) · (b mod M)) mod M, as três funções dependem apenas de **r = k mod 10**.
Basta então ver para onde cada um dos 10 restos vai:

| r = k mod 10 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | baldes atingíveis |
|---|---|---|---|---|---|---|---|---|---|---|---|
| h₁ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | **10** |
| h₂ | 0 | 7 | 4 | 1 | 8 | 5 | 2 | 9 | 6 | 3 | **10** |
| h₃ | 0 | 1 | 4 | 9 | 6 | 5 | 6 | 9 | 4 | 1 | **6** |

- **h₂ é uma permutação de h₁.** Como mdc(7, 10) = 1, multiplicar por 7 só embaralha os rótulos dos
  baldes: as chaves que colidem em h₁ colidem também em h₂. O fator 7 não espalha nada.
- **h₃ nunca atinge os baldes 2, 3, 7 e 8**, porque nenhum quadrado termina nesses dígitos. Os pares
  de restos 1 e 9, 2 e 8, 3 e 7 e 4 e 6 caem no mesmo balde, porque r² ≡ (10 − r)².
""", titulo='As funções e o que elas enxergam')
implementacao("""
from algoritmos.hashing import colisoes, distribuicao, h1, h2, h3, imagem
codigo(h1, h2, h3, distribuicao, colisoes)
""", 'Não é uma hash table: as funções só calculam o balde de cada chave, como pede o enunciado.')
execucao(12, 'Exercício 12: imagem das três funções, distribuição de cinco conjuntos de chaves e o contraste com M = 11.', """
import random
conjuntos = {'200 chaves aleatórias (0 a 9.999)': random.Random(42).sample(range(10_000), 200),
             '200 chaves pares': list(range(0, 400, 2))}
funcoes = {'h₁ = k mod 10': h1, 'h₂ = 7k mod 10': h2, 'h₃ = k² mod 10': h3}
fig, eixos = plt.subplots(2, 3, figsize=(11, 5.2), sharey='row')
for linha, (titulo, chaves) in enumerate(conjuntos.items()):
    for coluna, (nome, funcao) in enumerate(funcoes.items()):
        ax = eixos[linha][coluna]
        baldes = distribuicao(chaves, funcao)
        ax.bar(range(10), baldes, color=[AZUL, LARANJA, VERDE_AGUA][coluna], width=0.7)
        ax.axhline(len(chaves) / 10, color=CINZA, ls='--', lw=1.2)
        ax.set_xticks(range(10)); ax.grid(axis='x', visible=False)
        ax.set_title(nome if linha == 0 else '', fontsize=11)
        if coluna == 0:
            ax.set_ylabel(titulo.replace(' (', '\\n('), fontsize=9)
fig.suptitle('Chaves por balde (linha tracejada: distribuição ideal)', x=0.01, ha='left', fontweight='bold')
mostrar('ex12_distribuicao_hash')
legenda_grafico('Gráfico 4. h₂ só reordena as barras de h₁; h₃ deixa quatro baldes sempre vazios e dobra a carga dos demais.')
""")
analise(r"""
**Distribuição medida.** O ideal são 5 chaves por balde. Com 50 chaves em 10 baldes há no mínimo 40
colisões, então o **maior balde** mostra melhor o desequilíbrio:

| Conjunto de 50 chaves | h₁ (maior balde) | h₂ (maior balde) | h₃ (maior balde) |
|---|---|---|---|
| sequenciais 0..49 | 5 (ideal) | 5 (ideal) | 10 |
| aleatórias 0..9999 | 12 | 12 | 15 |
| pares | 10 (5 baldes) | 10 (5 baldes) | 20 (3 baldes) |
| múltiplos de 5 | 25 (2 baldes) | 25 (2 baldes) | 25 (2 baldes) |
| múltiplos de 10 | **50 (1 balde)** | **50 (1 balde)** | **50 (1 balde)** |

**Maior risco de colisão.**

1. h₃ é a pior, e o defeito é estrutural: não depende dos dados. 40% da tabela nunca é usada, e mesmo
   com chaves perfeitamente uniformes os baldes 1, 4, 6 e 9 recebem o dobro dos baldes 0 e 5.
2. h₁ e h₂ empatam. São boas quando o último dígito das chaves é uniforme, mas qualquer padrão nesse
   dígito vira colisão: pares usam metade da tabela, múltiplos de 5 usam 2 baldes e múltiplos de 10
   usam 1, o que transforma a busca num balde em O(N).

**Justificativa técnica.** O problema de fundo é **M = 10 ser a base do sistema decimal**: k mod 10
descarta todos os dígitos, menos o último. Os textos clássicos recomendam evitar M que seja potência
ou múltiplo da base e preferir **um primo** longe dessas potências (KNUTH, 1998, seção 6.4; CORMEN et
al., 2012, seção 11.3.1). Com **M = 11**, os mesmos múltiplos de 5 e de 10 ocupam os 11 baldes, com
no máximo 5 por balde (Figura 12). Numa tabela com encadeamento, a busca custa em média O(1 + α), com
α = N/M, mas só se a função espalhar as chaves; concentradas num balde, ela degrada para O(N)
(WENGROW, 2023, cap. 8).
""")

# =====================================================================================  TESTES
md("""
<a id="testes"></a>

## 14 · Testes automatizados

> 29 testes (`unittest`, biblioteca padrão) conferem o núcleo independentemente dos scripts.

| Arquivo | Testes | O que confere |
|---|:-:|---|
| `tests/test_algoritmos.py` | 19 | hash × aninhado iguais em 100 listas aleatórias; contadores (N², ≤ 3N, 2N − 1, 3N); interseção sem repetidos e na ordem de `b`; letras ausentes com acentos; as duas ordenações (resultado, entrada intacta, N(N−1)/2, exemplo dos slides, melhor e pior caso, deslocamentos = inversões); imagens e permutação das funções hash |
| `tests/test_estruturas.py` | 10 | LIFO, FIFO com volta no array, overflow e underflow sem alterar o estado, capacidade inválida, 5.000 operações aleatórias na fila, inversão com a sequência exata de push e pop |
""")
py("tela(13, 'Módulos do núcleo e dos testes, e a execução dos 29 testes no Ubuntu.')", oculto=True)
md(VOLTAR.strip())

# =====================================================================================  RUBRICA
md("""
<a id="rubrica"></a>

## 15 · Atendimento ao enunciado e à rubrica

> Cada critério da rubrica, com a seção em que é atendido.

| Critério da rubrica | Onde está |
|---|---|
| Identificou gargalos em implementações iniciais | [Ex. 1](#ex01): laço interno completo · [Ex. 2](#ex02): N × M comparações · [Ex. 3](#ex03): comparação com todos os anteriores |
| Reduziu a complexidade, justificando a melhoria | [Ex. 1](#ex01), [2](#ex02), [3](#ex03) e [5](#ex05): O(N²) → O(N), com o mesmo resultado nas duas versões |
| Implementou corretamente Selection Sort e Insertion Sort | [Ex. 6](#ex06) e [Ex. 7](#ex07), com o passo a passo dos slides e [testes](#testes) |
| Mensurou a complexidade usando Big O | contadores em todos os algoritmos, conferidos contra N², 3N, 2N − 1 e N(N−1)/2 |
| Comparou algoritmos em diferentes cenários de entrada | quatro estados iniciais nos [Ex. 6](#ex06) e [7](#ex07); de 10 a 1.000.000 de elementos nos Ex. 1 a 5 |
| Utilizou hash tables para recuperação eficiente | [Ex. 1](#ex01), [2](#ex02), [3](#ex03) e [5](#ex05) com `dict`; [Ex. 4](#ex04) com endereçamento direto |
| Escolheu corretamente entre pilha e fila | [Ex. 8](#ex08): fila, com simulação contra a pilha |
| Implementou pilha com overflow e underflow explícitos | [Ex. 9](#ex09): exceções `Overflow` e `Underflow`, estado preservado |
| Implementou fila garantindo o FIFO | [Ex. 10](#ex10): ponteiros circulares e 100.000 operações validadas |
| Aplicou pilhas a problemas algorítmicos concretos | [Ex. 11](#ex11): inversão de string com push e pop explícitos |
| Organizou o notebook de forma clara e estruturada | [sumário](#sumario) e o mesmo roteiro em todos os exercícios ([como ler](#visao)) |
| Documentou decisões técnicas de forma objetiva | blocos "Decisões" dos Ex. 2 e 4, justificativa do Ex. 8 e análise do Ex. 12 |
| Apresentou evidências completas de execução | 13 telas do WezTerm, saídas em texto em `evidencias/saidas/` e o PDF de entrega |
| Manteve consistência entre código, resultados e análise | as células chamam as mesmas funções que rodaram no terminal; os números coincidem com as telas |

Os cinco itens de tarefa de cada exercício do enunciado estão cobertos na seção do exercício; o
texto completo está em [`docs/context/enunciado-DR1-TP2.md`](docs/context/enunciado-DR1-TP2.md).
""" + VOLTAR)

# =====================================================================================  CONCLUSÃO
md("""
<a id="conclusao"></a>

## 16 · Conclusão

1. Os laços aninhados que só procuram ou contam algo foram trocados por hash tables. Nos Exercícios 1
   a 5 o custo caiu para **O(N)** sem mudar o resultado, ao preço de memória O(N) para a tabela.
2. Selection e Insertion Sort são O(N²) no pior caso, mas a entrada decide o que se paga na prática.
   O Selection faz sempre N(N−1)/2 comparações; o Insertion paga pelas inversões e chega a O(N) numa
   lista ordenada.
3. A escolha entre pilha e fila vem da regra de acesso: a ordem de chegada pede **FIFO**, desfazer
   pede **LIFO**. As duas implementações guardam o estado no objeto, rejeitam o uso indevido com
   exceções e fazem tudo em O(1).
4. Uma função hash vale pela distribuição que produz. Com M = 10, h₃ desperdiça 40% da tabela, e h₁ e
   h₂ herdam qualquer padrão do último dígito; um M primo resolve os dois problemas.
""" + VOLTAR)

# =====================================================================================  REFERÊNCIAS
md("""
<a id="referencias"></a>

## 17 · Referências

CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. **Algoritmos: teoria e prática**. Tradução da 3. ed. americana. Rio de Janeiro: Elsevier, 2012.

GOODRICH, M. T.; TAMASSIA, R.; GOLDWASSER, M. H. **Data structures and algorithms in Python**. Hoboken: Wiley, 2013.

KNUTH, D. E. **The art of computer programming**: volume 3: sorting and searching. 2. ed. Reading: Addison-Wesley, 1998.

NUNES, I. M. **Aula 4**: análise de complexidade: algoritmo selection sort e otimização de código usando a notação Big O. Rio de Janeiro: Instituto Infnet, 2026a. Slides da disciplina Velocidade e Qualidade com Estruturas de Dados e Algoritmos.

NUNES, I. M. **Aula 5**: análise de complexidade do insertion sort: melhor caso, caso médio e pior caso. Rio de Janeiro: Instituto Infnet, 2026b. Slides da disciplina Velocidade e Qualidade com Estruturas de Dados e Algoritmos.

PYTHON SOFTWARE FOUNDATION. **TimeComplexity**. Python Wiki, 2024a. Disponível em: https://wiki.python.org/moin/TimeComplexity. Acesso em: 9 nov. 2026.

PYTHON SOFTWARE FOUNDATION. **Built-in types: mapping types (dict)**. 2024b. Disponível em: https://docs.python.org/3/library/stdtypes.html#mapping-types-dict. Acesso em: 9 nov. 2026.

PYTHON SOFTWARE FOUNDATION. **unicodedata: Unicode database**. 2024c. Disponível em: https://docs.python.org/3/library/unicodedata.html. Acesso em: 9 nov. 2026.

WENGROW, J. **A common-sense guide to data structures and algorithms in Python**: volume 1: level up your core programming skills. Raleigh: The Pragmatic Bookshelf, 2023.

---

<sub>Reprodução: `scripts/capturar_wezterm.py` abre o WezTerm, digita os comandos no fish do Ubuntu e grava as telas;
`scripts/gerar_notebook.py` monta e executa este notebook chamando as mesmas funções de `src/`.</sub>

<p align="right" style="text-align:right"><a href="#sumario">⬆ voltar ao sumário</a></p>
""")

nb = nbformat.v4.new_notebook(cells=celulas)
nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
nb.metadata['language_info'] = {'name': 'python'}
nb.metadata['title'] = 'andre_becker_DR1_TP2'

if __name__ == '__main__':
    NotebookClient(nb, timeout=900, kernel_name='python3', resources={'metadata': {'path': RAIZ}}).execute()
    nbformat.write(nb, SAIDA)
    print('gerado: %s | celulas: %d' % (SAIDA, len(nb.cells)))
