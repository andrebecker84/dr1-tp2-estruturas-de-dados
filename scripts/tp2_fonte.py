# -*- coding: utf-8 -*-
"""Preenche os blocos automaticos de docs/RELATORIO_TP2.md a partir de src/.

    python scripts/tp2_fonte.py

O docs/RELATORIO_TP2.md e lido direto no GitHub, entao o codigo precisa estar escrito nele. Para nao
copiar a mao (e desatualizar), cada bloco marcado com comentario HTML e regerado aqui:

  <!-- codigo: ARQUIVO f,g -->   ...   <!-- /codigo -->   funcoes ou classes f e g de src/ARQUIVO, sem docstrings
  <!-- inclui: ARQUIVO -->       ...   <!-- /inclui -->   markdown de src/ARQUIVO, secoes rebaixadas
  <!-- video: URL -->            ...   <!-- /video -->    linha com o link do video (ou "a inserir")

O gerador do PDF (gerar_documento.py) chama sincronizar() antes de ler o arquivo.
"""
import ast, io, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, 'src')
TP2 = os.path.join(RAIZ, 'docs', 'RELATORIO_TP2.md')

BLOCO = re.compile(r'<!-- (codigo|inclui|video):[ \t]*(.*?) -->\n.*?<!-- /\1 -->', re.S)


def trecho(arquivo, nomes):
    """Linhas das funcoes e classes pedidas de src/<arquivo>, na ordem do arquivo, sem nenhuma docstring."""
    texto = io.open(os.path.join(SRC, arquivo), encoding='utf-8').read()
    linhas = texto.split('\n')
    saida = []
    for n in ast.parse(texto).body:
        if not (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in nomes):
            continue
        docs = set()
        for no in ast.walk(n):                      # a do proprio no e as dos metodos de uma classe
            if isinstance(no, (ast.FunctionDef, ast.ClassDef)) and _tem_docstring(no):
                docs.update(range(no.body[0].lineno, no.body[0].end_lineno + 1))
        corpo = [l for k, l in enumerate(linhas[n.lineno - 1:n.end_lineno], n.lineno) if k not in docs]
        if len(corpo) > 1 and corpo[0].startswith('class ') and not corpo[1].strip():
            del corpo[1]                            # a linha em branco que vinha depois da docstring da classe
        saida += ([''] if saida else []) + corpo
    return saida


def _tem_docstring(no):
    primeiro = no.body[0]
    return isinstance(primeiro, ast.Expr) and isinstance(primeiro.value, ast.Constant) and isinstance(primeiro.value.value, str)


def _conteudo(tipo, args):
    if tipo == 'codigo':
        arquivo, funcoes = args.split()
        return '```python\n%s\n```\n' % '\n'.join(trecho(arquivo, funcoes.split(',')))
    if tipo == 'inclui':
        md = io.open(os.path.join(SRC, args), encoding='utf-8').read()
        md = re.sub(r'^# .*\n+', '', md)
        return re.sub(r'^## ', '#### ', md, flags=re.M).strip('\n') + '\n'
    if args:
        return '**Link do vídeo:** [assistir no Google Drive](%s)\n' % args
    return '**Link do vídeo:** a inserir.\n'


def sincronizar():
    texto = io.open(TP2, encoding='utf-8').read()

    def troca(m):
        tipo, args = m.group(1), m.group(2).strip()
        abre = '<!-- %s:%s -->' % (tipo, ' ' + args if args else '')
        return '%s\n%s<!-- /%s -->' % (abre, _conteudo(tipo, args), tipo)

    novo = BLOCO.sub(troca, texto)
    if novo != texto:
        io.open(TP2, 'w', encoding='utf-8', newline='\n').write(novo)
    return novo


def para_geradores(texto):
    """Tira o que só serve no GitHub: o bloco so-github (sumário) e as âncoras <a id>."""
    texto = re.sub(r'<!-- so-github -->.*?<!-- /so-github -->\n?', '', texto, flags=re.S)
    return re.sub(r'^<a id="[^"]*"></a>\n', '', texto, flags=re.M)


if __name__ == '__main__':
    sincronizar()
    print('atualizado: %s' % TP2)
