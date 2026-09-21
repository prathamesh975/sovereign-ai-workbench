import ollama


class OllamaClient:
    """
    Client for communicating with the
    locally running Ollama server.
    """

    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Ollama and
        return the generated response.
        """

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]