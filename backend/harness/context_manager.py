class ContextManager:
    """
    Stores the state and information collected
    during an agent execution.
    """

    def __init__(self):

        self.data = {}

    def set(self, key: str, value):

        self.data[key] = value

    def get(self, key: str, default=None):

        return self.data.get(
            key,
            default
        )

    def get_all(self):

        return self.data

    def clear(self):

        self.data.clear()