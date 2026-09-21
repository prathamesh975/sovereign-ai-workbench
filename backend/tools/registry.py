class ToolRegistry:
    """
    Central registry for approved local tools.
    """

    def __init__(self):

        self.tools = {}

    def register(self, name: str, tool):

        self.tools[name] = tool

    def get(self, name: str):

        if name not in self.tools:
            raise ValueError(
                f"Tool '{name}' is not registered."
            )

        return self.tools[name]

    def list_tools(self):

        return list(self.tools.keys())