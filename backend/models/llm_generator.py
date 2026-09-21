import requests


class LLMGenerator:

    def __init__(self, model="qwen2.5-coder:3b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]