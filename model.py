import ollama

class ChatBotLocal:

    def __init__(self):

        self.messages = []

        self.options = {
            "num_predict": 300,
            "num_thread": 6,
            "temperature": 0.7
        }

        self.model = "phi3"


    def responder(self, mensagem):
        """
        Resposta normal
        """

        self.messages.append({"role": "user", "content": mensagem})

        response = ollama.chat(
            model=self.model,
            messages=self.messages,
            options=self.options
        )

        resposta = response["message"]["content"]

        self.messages.append({"role": "assistant", "content": resposta})

        self.messages = self.messages[-6:]

        return resposta


    def responder_stream(self, mensagem):
        """
        Resposta real (stream)
        """

        self.messages.append({"role": "user", "content": mensagem})

        stream = ollama.chat(
            model=self.model,
            messages=self.messages,
            stream=True,
            options=self.options
        )

        resposta_completa = ""

        for chunk in stream:

            parte = chunk["message"]["content"]

            resposta_completa += parte

            yield parte

        self.messages.append({"role": "assistant", "content": resposta_completa})

        self.messages = self.messages[-6:]
