import subprocess
import atexit
import customtkinter as ctk
from model import ChatBotLocal
from assistente_sistema import executar_comando
import style
import re
import threading

ollama_processo = subprocess.Popen(
    ["ollama", "serve"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

def encerrar_ollama():
    try:
        ollama_processo.terminate()
        ollama_processo.wait(timeout=3)
    except:
        pass

atexit.register(encerrar_ollama)

bot = ChatBotLocal()

style.configurar_tema()

app = ctk.CTk()
app.title("Mahnrattan IA")
app.geometry("600x650")

def ao_fechar():
    encerrar_ollama()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", ao_fechar)

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

titulo = ctk.CTkLabel(
    app,
    text="Mahnrattan IA",
    font=style.FONT_TITULO
)
titulo.grid(row=0, column=0, pady=10)

chatbox = ctk.CTkTextbox(
    app,
    font=style.FONT_CHAT,
    wrap="word"
)
chatbox.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

frame_envio = ctk.CTkFrame(app)
frame_envio.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

frame_envio.grid_columnconfigure(0, weight=1)

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


entrada = ctk.CTkEntry(
    frame_envio,
    placeholder_text="Digite sua mensagem..."
)
entrada.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

entrada.bind("<Return>", enviar_mensagem)

botao = ctk.CTkButton(
    frame_envio,
    text="Enviar",
    command=enviar_mensagem,
    width=100
)
botao.grid(row=0, column=1, padx=5, pady=5)

app.mainloop()
