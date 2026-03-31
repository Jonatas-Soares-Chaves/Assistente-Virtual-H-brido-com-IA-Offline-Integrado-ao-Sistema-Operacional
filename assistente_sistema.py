import os
import webbrowser
import subprocess
import requests
from datetime import datetime

PASTAS_MENU_INICIAR = [
    os.path.join(os.environ["PROGRAMDATA"], r"Microsoft\Windows\Start Menu\Programs"),
    os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs")
]


def procurar_programa(nome):
    nome = nome.lower()

    for pasta in PASTAS_MENU_INICIAR:
        for root, dirs, files in os.walk(pasta):
            for arquivo in files:

                if arquivo.lower().endswith(".lnk"):
                    if nome in arquivo.lower():
                        return os.path.join(root, arquivo)

    return None


def executar_comando(texto):

    texto = texto.lower().strip()

    if texto.startswith("abrir "):

        nome_programa = texto.replace("abrir ", "").strip()

        caminho = procurar_programa(nome_programa)

        if caminho:
            os.startfile(caminho)
            return f"Abrindo {nome_programa}..."

        try:
            subprocess.Popen(nome_programa)
            return f"Tentando abrir {nome_programa}..."
        except:
            return f"Não encontrei o programa {nome_programa}."

    if "hora" in texto:
        agora = datetime.now().strftime("%H:%M:%S")
        return f"Agora são {agora}"

    if "data" in texto or "dia" in texto:
        hoje = datetime.now().strftime("%d/%m/%Y")
        return f"Hoje é {hoje}"

    if "calcular" in texto:
        try:
            conta = texto.replace("calcular", "").strip()
            resultado = eval(conta)
            return f"O resultado é {resultado}"
        except:
            return "Não consegui calcular."

    if "pesquisar" in texto or "pesquisa" in texto:

        busca = (
            texto.replace("pesquisar", "")
            .replace("pesquisa", "")
            .replace("no google", "")
            .strip()
        )

        if busca:
            url = f"https://www.google.com/search?q={busca}"
            webbrowser.open(url)
            return f"Abrindo resultados no Google para: {busca}"

    if "clima" in texto:
        try:
            cidade = texto.replace("clima", "").strip()

            if cidade == "":
                cidade = "Santa Maria"

            resposta = requests.get(f"https://wttr.in/{cidade}?format=3")
            return resposta.text

        except:
            return "Não consegui obter o clima."

    if texto.startswith("executar "):

        comando = texto.replace("executar", "").strip()

        try:
            subprocess.Popen(comando, shell=True)
            return f"Executando {comando}"
        except:
            return "Erro ao executar comando."

    return None
