import subprocess
import atexit
import customtkinter as ctk
from model import ChatBotLocal
from assistente_sistema import executar_comando
import style
import re
import threading

# 🔹 Inicia o servidor do Ollama
ollama_processo = subprocess.Popen(
    ["ollama", "serve"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# 🔹 Função para encerrar o Ollama
def encerrar_ollama():
    try:
        ollama_processo.terminate()
        ollama_processo.wait(timeout=3)
    except:
        pass

atexit.register(encerrar_ollama)

# Inicializa bot
bot = ChatBotLocal()

# Configura tema
style.configurar_tema()

#Cria a janela principal
app = ctk.CTk()
app.title("Mahnrattan IA")
app.geometry("600x650")

#Função ao fechar janela
def ao_fechar():
    encerrar_ollama()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", ao_fechar)

# 🔹 Permite redimensionamento
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

# Título
titulo = ctk.CTkLabel(
    app,
    text="Mahnrattan IA",
    font=style.FONT_TITULO
)
titulo.grid(row=0, column=0, pady=10)

# Caixa de chat
chatbox = ctk.CTkTextbox(
    app,
    font=style.FONT_CHAT,
    wrap="word"
)
chatbox.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

# Frame de envio
frame_envio = ctk.CTkFrame(app)
frame_envio.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

frame_envio.grid_columnconfigure(0, weight=1)

# 🔹 Formatar resposta
def formatar_resposta(texto):

    texto = texto.strip()
    texto = re.sub(r'\n(\d+\.)', r'\n\n\1', texto)
    texto = re.sub(r'\n(- )', r'\n\n\1', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)

    return texto


def enviar_mensagem(event=None):

    user_text = entrada.get().strip()

    if not user_text:
        return

    entrada.delete(0, "end")

    chatbox.insert("end", f"Você: {user_text}\n")
    chatbox.see("end")

    resposta_sistema = executar_comando(user_text)

    if resposta_sistema:
        chatbox.insert("end", f"IA: {resposta_sistema}\n\n")
        chatbox.see("end")
        return

    def resposta_bot():

        resposta_completa = ""

        for parte in bot.responder_stream(user_text):
            resposta_completa += parte

        resposta_formatada = formatar_resposta(resposta_completa)

        chatbox.insert("end", f"IA: {resposta_formatada}\n\n")
        chatbox.see("end")

    threading.Thread(target=resposta_bot, daemon=True).start()


# Entrada de texto
entrada = ctk.CTkEntry(
    frame_envio,
    placeholder_text="Digite sua mensagem..."
)
entrada.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

entrada.bind("<Return>", enviar_mensagem)

# Botão enviar
botao = ctk.CTkButton(
    frame_envio,
    text="Enviar",
    command=enviar_mensagem,
    width=100
)
botao.grid(row=0, column=1, padx=5, pady=5)

# Inicia app
app.mainloop()