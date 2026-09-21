from dataclasses import dataclass


@dataclass
class ModelInfo:
    name: str
    task_type: str
    description: str


class ModelRegistry:

    def __init__(self):

        self.models = {

            "coding": ModelInfo(
                name="qwen2.5-coder:3b",
                task_type="coding",
                description="Local model for coding and programming tasks."
            ),

            "general": ModelInfo(
                name="qwen2.5-coder:3b",
                task_type="general",
                description="Local fallback model for general reasoning."
            ),

            "vision": ModelInfo(
                name="qwen2.5vl:3b",
                task_type="vision",
                description="Local vision-language model for images and scanned documents."
            )
        }

    def get_model(self, task_type: str) -> ModelInfo:

        return self.models.get(
            task_type,
            self.models["general"]
        )