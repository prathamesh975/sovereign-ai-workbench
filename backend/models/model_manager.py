import ollama


class ModelManager:

    def __init__(self):
        self.active_model = None

    def get_installed_models(self):

        response = ollama.list()

        return [
            model.model
            for model in response.models
        ]

    def activate(self, model_name: str):

        installed_models = self.get_installed_models()

        if model_name not in installed_models:
            raise RuntimeError(
                f"Model '{model_name}' is not installed locally."
            )

        self.active_model = model_name

        return {
            "model": model_name,
            "status": "active"
        }

    def get_active_model(self):

        return self.active_model

    def deactivate(self):

        self.active_model = None

        return {
            "status": "inactive"
        }