from collections import defaultdict

class ToolRegistry:
    _tools = []

    @classmethod
    def register(cls, tool_cls):
        cls._tools.append(tool_cls)

    @classmethod
    def all(cls):
        return cls._tools
