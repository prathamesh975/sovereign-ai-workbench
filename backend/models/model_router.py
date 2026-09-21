from backend.models.model_registry import ModelRegistry, ModelInfo


class ModelRouter:

    def __init__(self):
        self.registry = ModelRegistry()

    def route(self, task_type: str) -> ModelInfo:
        return self.registry.get_model(task_type)