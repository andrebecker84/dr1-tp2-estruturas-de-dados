# -*- coding: utf-8 -*-
"""Executa os 12 exercícios do DR1-TP2 no WezTerm (Ubuntu/WSL2, shell fish) e captura a janela real.

    uv run --no-project --python 3.14 --with pillow python scripts/capturar_wezterm.py

1. Copia src/ para ~/DR1_TP2 no Ubuntu (estado limpo, sem __pycache__).
2. Abre uma janela nova do WezTerm com a configuração do usuário (tema, fonte, fish e starship).
3. Digita cada comando pelo `wezterm cli send-text` e espera o prompt voltar.
4. Captura a janela com PrintWindow (ctypes, sem PowerShell) e corta a área vazia de baixo.
5. Grava o texto de cada tela em evidencias/saidas/, para conferir os números citados no notebook.
Nada é redigitado nem editado: a imagem é o que a janela mostrou.
"""
import ctypes
import ctypes.wintypes as wt
import os
import subprocess
import time

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TELAS = os.path.join(RAIZ, 'evidencias', 'telas')
SAIDAS = os.path.join(RAIZ, 'evidencias', 'saidas')
WEZ = r'C:\Program Files\WezTerm'
SOCKETS = os.path.join(os.path.expanduser('~'), '.local', 'share', 'wezterm')
LINHAS, COLUNAS = 54, 150
PROMPT = '❯'
DESTINO = '~/DR1_TP2'

# (nome da tela, comandos): Figura N = Exercício N; a 13 são os testes.
ROTEIRO = [
    ('ex01-maior-unico', ['python3 --version', 'python3 ex01_maior_unico.py']),
    ('ex02-intersecao', ['python3 ex02_intersecao.py']),
    ('ex03-primeiro-duplicado', ['python3 ex03_primeiro_duplicado.py']),
    ('ex04-letra-ausente', ['python3 ex04_letra_ausente.py']),
    ('ex05-primeiro-nao-repetido', ['python3 ex05_primeiro_nao_repetido.py']),
    ('ex06-selection-sort', ['python3 ex06_selection_sort.py']),
    ('ex07-insertion-sort', ['python3 ex07_insertion_sort.py']),
    ('ex08-pilha-ou-fila', ['python3 ex08_pilha_ou_fila.py']),
    ('ex09-pilha', ['python3 ex09_pilha.py']),
    ('ex10-fila', ['python3 ex10_fila.py']),
    ('ex11-inverter-string', ['python3 ex11_inverter_string.py']),
    ('ex12-funcoes-hash', ['python3 ex12_funcoes_hash.py']),
    ('testes', ['ls algoritmos tests', 'python3 -m unittest discover -s tests -t .']),
]

RAIZ_WSL = '/mnt/c' + RAIZ[2:].replace('\\', '/')
env = dict(os.environ)
fig = 0

# ------------------------------------------------------------------ captura da janela (Win32)
user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
user32.SetProcessDPIAware()
PW_RENDERFULLCONTENT = 2


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [('biSize', wt.DWORD), ('biWidth', wt.LONG), ('biHeight', wt.LONG), ('biPlanes', wt.WORD),
                ('biBitCount', wt.WORD), ('biCompression', wt.DWORD), ('biSizeImage', wt.DWORD),
                ('biXPelsPerMeter', wt.LONG), ('biYPelsPerMeter', wt.LONG), ('biClrUsed', wt.DWORD),
                ('biClrImportant', wt.DWORD)]


def janela_do_processo(pid):
    """HWND da janela visível principal do processo, ou 0."""
    achada = wt.HWND(0)

    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def visitar(hwnd, _):
        dono = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(dono))
        if dono.value == pid and user32.IsWindowVisible(hwnd) and user32.GetWindowTextLengthW(hwnd):
            achada.value = hwnd
            return False
        return True

    user32.EnumWindows(visitar, 0)
    return achada.value or 0


def capturar_janela(hwnd, destino):
    """Área cliente da janela, como ela é desenhada, mesmo atrás de outras janelas."""
    janela, cliente, origem = wt.RECT(), wt.RECT(), wt.POINT(0, 0)
    user32.GetWindowRect(hwnd, ctypes.byref(janela))
    user32.GetClientRect(hwnd, ctypes.byref(cliente))
    user32.ClientToScreen(hwnd, ctypes.byref(origem))
    largura, altura = janela.right - janela.left, janela.bottom - janela.top

    tela_dc = user32.GetDC(hwnd)
    mem_dc = gdi32.CreateCompatibleDC(tela_dc)
    bitmap = gdi32.CreateCompatibleBitmap(tela_dc, largura, altura)
    gdi32.SelectObject(mem_dc, bitmap)
    user32.PrintWindow(hwnd, mem_dc, PW_RENDERFULLCONTENT)

    info = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), largura, -altura, 1, 32, 0, 0, 0, 0, 0, 0)
    buffer = ctypes.create_string_buffer(largura * altura * 4)
    gdi32.GetDIBits(mem_dc, bitmap, 0, altura, buffer, ctypes.byref(info), 0)
    gdi32.DeleteObject(bitmap)
    gdi32.DeleteDC(mem_dc)
    user32.ReleaseDC(hwnd, tela_dc)

    img = Image.frombuffer('RGB', (largura, altura), buffer, 'raw', 'BGRX', 0, 1)
    x, y = origem.x - janela.left, origem.y - janela.top
    img.crop((x, y, x + cliente.right, y + cliente.bottom)).save(destino)


def cortar(caminho):
    """Corta a parte de baixo sem texto. Texto tem brilho alto; o fundo e a imagem do tema, não."""
    img = Image.open(caminho).convert('RGB')
    w, h = img.size
    px = img.load()
    ultima = 0
    for y in range(h - 1, 0, -1):
        if any(sum(px[x, y]) > 330 for x in range(0, w - 40, 2)):
            ultima = y
            break
    img.crop((0, 0, w, min(h, ultima + 34))).save(caminho, optimize=True)


# ------------------------------------------------------------------ terminal
def wsl(cmd):
    subprocess.run(['wsl', '-d', 'Ubuntu', '--exec', 'bash', '-c', cmd], check=True)


def cli(*args):
    r = subprocess.run([os.path.join(WEZ, 'wezterm.exe'), 'cli', *args], env=env,
                       capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout


def texto():
    return [l.rstrip() for l in cli('get-text', '--start-line', '-2000').rstrip().split('\n')]


def prompts(linhas):
    return sum(1 for l in linhas if l.startswith(PROMPT))


def ocioso(linhas):
    return bool(linhas) and linhas[-1].strip() == PROMPT


def esperar(condicao, limite=600):
    fim = time.time() + limite
    while time.time() < fim:
        if condicao(texto()):
            time.sleep(0.6)            # deixa o starship terminar de desenhar o prompt
            return
        time.sleep(0.4)
    raise TimeoutError('o prompt não voltou')


def digita(comando):
    cli('send-text', '--no-paste', comando + '\r')


def cmd(comando):
    antes = prompts(texto())
    digita(comando)
    esperar(lambda l: ocioso(l) and prompts(l) > antes)


def limpa():
    digita('clear')
    time.sleep(1)
    esperar(lambda l: ocioso(l) and prompts(l) == 1)


def tela(nome, hwnd):
    global fig
    fig += 1
    destino = os.path.join(TELAS, f'{fig:02d}-{nome}.png')
    time.sleep(0.8)
    capturar_janela(hwnd, destino)
    cortar(destino)
    with open(os.path.join(SAIDAS, f'{fig:02d}-{nome}.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(texto()) + '\n')


def abrir_wezterm():
    gui = subprocess.Popen([os.path.join(WEZ, 'wezterm-gui.exe'), '--config', f'initial_rows={LINHAS}',
                            '--config', f'initial_cols={COLUNAS}', 'start', '--always-new-process',
                            '--class', 'dr1tp2'])
    socket = os.path.join(SOCKETS, f'gui-sock-{gui.pid}')
    for _ in range(60):
        if os.path.exists(socket):
            break
        time.sleep(0.5)
    env['WEZTERM_UNIX_SOCKET'] = socket
    hwnd = 0
    for _ in range(60):
        hwnd = janela_do_processo(gui.pid)
        if hwnd:
            break
        time.sleep(0.5)
    if not hwnd:
        raise RuntimeError('janela do WezTerm não encontrada')
    esperar(ocioso, 60)
    return gui, hwnd


if __name__ == '__main__':
    os.makedirs(TELAS, exist_ok=True)
    os.makedirs(SAIDAS, exist_ok=True)
    for pasta in (TELAS, SAIDAS):
        for f in os.listdir(pasta):
            if f.endswith(('.png', '.txt')):
                os.remove(os.path.join(pasta, f))

    # Estado limpo no Ubuntu: o código de src/ e a versão do Python fixada no projeto.
    wsl(f'rm -rf {DESTINO} && mkdir -p {DESTINO} && cp -r "{RAIZ_WSL}"/src/. {DESTINO}/ '
        f'&& cp "{RAIZ_WSL}"/.python-version {DESTINO}/ && find {DESTINO} -name __pycache__ -prune -exec rm -rf {{}} + '
        f'&& find {DESTINO} -type d -exec chmod 755 {{}} + && find {DESTINO} -type f -exec chmod 644 {{}} +')

    gui, hwnd = abrir_wezterm()
    try:
        cmd(f'cd {DESTINO}; set -gx PYTHONDONTWRITEBYTECODE 1')
        for nome, comandos in ROTEIRO:
            limpa()
            for c in comandos:
                cmd(c)
            tela(nome, hwnd)
    finally:
        try:
            cli('kill-pane')                         # fecha a janela de captura, sem confirmação
        except Exception:
            gui.terminate()
    print(f'telas capturadas: {fig}')
