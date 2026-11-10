# -*- coding: utf-8 -*-
"""Apresentação do notebook: tabelas HTML, figuras do terminal, código-fonte e estilo dos gráficos.

Só o notebook usa este arquivo; os exercícios continuam só com a biblioteca padrão.
"""
import base64
import html
import inspect
import os
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import HTML, display

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paleta categórica validada: as três primeiras cores passam em todos os pares, inclusive daltonismo.
AZUL, LARANJA, VERDE_AGUA = '#2a78d6', '#eb6834', '#1baf7a'
CINZA, TINTA, TINTA_2, GRADE = '#8a8985', '#0b0b0b', '#52514e', '#e4e3df'


def estilo():
    mpl.rcParams.update({
        'figure.dpi': 120, 'savefig.dpi': 160, 'figure.facecolor': '#fcfcfb', 'axes.facecolor': '#fcfcfb',
        'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 12, 'axes.titleweight': 'bold',
        'axes.titlelocation': 'left', 'axes.edgecolor': GRADE, 'axes.labelcolor': TINTA_2,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'axes.axisbelow': True,
        'grid.color': GRADE, 'grid.linewidth': 0.8, 'xtick.color': TINTA_2, 'ytick.color': TINTA_2,
        'legend.frameon': False, 'lines.linewidth': 2, 'lines.markersize': 7,
    })


def milhar(n):
    return f'{n:,.0f}'.replace(',', '.')


# ------------------------------------------------------------------ blocos visuais
ESTILO_TAB = ('border-collapse:collapse;margin:6px 0 14px 0;font-size:13px;'
              'font-family:-apple-system,Segoe UI,Roboto,sans-serif')


def tabela(cabecalho, linhas, legenda=None, alinhar=None):
    """Tabela HTML compacta, alinhada à esquerda. alinhar: 'l', 'r' ou 'c' por coluna."""
    alinhar = alinhar or 'l' + 'r' * (len(cabecalho) - 1)
    al = {'l': 'left', 'r': 'right', 'c': 'center'}
    th = ''.join(f'<th style="text-align:{al[a]};padding:7px 12px;background:#1E3A8A;color:#fff;'
                 f'font-weight:600">{c}</th>' for c, a in zip(cabecalho, alinhar))
    corpo = ''
    for i, linha in enumerate(linhas):
        fundo = '#f3f6fc' if i % 2 else '#ffffff'
        corpo += '<tr>' + ''.join(
            f'<td style="text-align:{al[a]};padding:6px 12px;border-bottom:1px solid #e4e3df;'
            f'background:{fundo}">{c}</td>' for c, a in zip(linha, alinhar)) + '</tr>'
    cap = (f'<caption style="caption-side:bottom;text-align:left;color:#52514e;font-size:12px;'
           f'padding-top:6px">{legenda}</caption>') if legenda else ''
    display(HTML(f'<table style="{ESTILO_TAB}">{cap}<thead><tr>{th}</tr></thead><tbody>{corpo}</tbody></table>'))


def cartoes(*itens):
    """Faixa de indicadores: cada item é (valor, rótulo). Abre cada exercício com os números principais."""
    display(HTML(cartoes_html(*itens)))


def cartoes_html(*itens):
    """HTML da faixa de indicadores; o gerador do notebook o grava direto numa célula de texto."""
    blocos = ''.join(
        f'<div style="flex:1 1 170px;padding:10px 14px;border-radius:10px;background:#f6f8fc;'
        f'border-left:4px solid #1E3A8A"><div style="font-size:{19 if len(valor) <= 14 else 16}px;font-weight:700;'
        f'color:#1E3A8A;line-height:1.25">{valor}</div><div style="font-size:12px;color:#52514e;margin-top:3px">'
        f'{rotulo}</div></div>'
        for valor, rotulo in itens)
    return (f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 14px 0;'
            f'font-family:-apple-system,Segoe UI,Roboto,sans-serif">{blocos}</div>')


def figura(caminho, legenda, largura=900):
    """Embute a tela do terminal no notebook (fica no .ipynb) com a legenda abaixo."""
    with open(os.path.join(RAIZ, caminho), 'rb') as f:
        dados = base64.b64encode(f.read()).decode()
    display(HTML(f'<figure style="margin:8px 0 18px 0"><img src="data:image/png;base64,{dados}" '
                 f'style="max-width:{largura}px;width:100%;border-radius:8px;'
                 f'box-shadow:0 2px 10px rgba(0,0,0,.18)"/><figcaption style="color:#52514e;'
                 f'font-size:12px;margin-top:6px">{legenda}</figcaption></figure>'))


def tela(numero, legenda):
    """Figura N: a tela do terminal evidencias/telas/NN-*.png, numerada como o exercício."""
    caminho = next(f for f in sorted(os.listdir(os.path.join(RAIZ, 'evidencias', 'telas'))) if f.startswith(f'{numero:02d}-'))
    figura(f'evidencias/telas/{caminho}', f'Figura {numero}. {legenda}')


def codigo(*objetos):
    """Código-fonte das funções e classes, lido do próprio arquivo em src/, com o intervalo de linhas."""
    for obj in objetos:
        linhas, inicio = inspect.getsourcelines(obj)
        arquivo = os.path.relpath(inspect.getsourcefile(obj), os.path.join(RAIZ, 'src')).replace(os.sep, '/')
        display(HTML(f'<div style="font-size:11px;color:#52514e;margin-top:4px">src/{arquivo} · linhas '
                     f'{inicio}–{inicio + len(linhas) - 1}</div><pre style="background:#0d1117;color:#e6edf3;'
                     f'padding:12px 14px;border-radius:8px;font-size:12px;line-height:1.5;overflow-x:auto;'
                     f'font-family:{MONO}">{realce(textwrap.dedent("".join(linhas)).rstrip())}</pre>'))


MONO = "'Cascadia Code',Consolas,'JetBrains Mono',Menlo,monospace"


def realce(fonte):
    """Realce de sintaxe com estilos inline (o pygments já vem com o IPython); sem ele, texto puro."""
    try:
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer
    except ImportError:
        return html.escape(fonte)
    formatador = HtmlFormatter(style='github-dark', noclasses=True, nowrap=True)
    return highlight(fonte, PythonLexer(), formatador)


def mostrar(nome):
    """Ajusta, grava o gráfico em evidencias/graficos/<nome>.png (usado no README) e exibe."""
    pasta = os.path.join(RAIZ, 'evidencias', 'graficos')
    os.makedirs(pasta, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta, nome + '.png'), bbox_inches='tight')
    plt.show()


def legenda_grafico(texto):
    display(HTML(f'<div style="color:#52514e;font-size:12px;margin:-4px 0 16px 0">{texto}</div>'))
