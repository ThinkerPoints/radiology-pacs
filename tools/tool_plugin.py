from tools.plugin_registry import ToolRegistry

def ToolPlugin(name, category, icon=None, toggleable=True):
    def decorator(cls):
        cls.name = name
        cls.category = category
        cls.icon = icon
        cls.toggleable = toggleable
        ToolRegistry.register(cls)
        return cls
    return decorator
