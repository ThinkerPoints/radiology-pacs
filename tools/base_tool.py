# from tools.plugin_registry import ToolRegistry
# from PySide6.QtGui import QAction
# class BaseTool:
#     name = "base"
#     category = "General"
#     toggleable = True

#     def __init__(self, viewport):
#         self.viewport = viewport

#     def activate(self): pass
#     def deactivate(self): pass

#     def mouse_press(self, e): pass
#     def mouse_move(self, e): pass
#     def mouse_release(self, e): pass

#     def draw(self, painter): pass
#     def drawOverlay(self, painter): pass
    
#     def create_action(self, parent):
#         act = QAction(self.name, parent)
#         act.triggered.connect(lambda: parent.viewport.tool_manager.activate(self.name))
#         return act
    


from PySide6.QtGui import QAction
from tools.plugin_registry import ToolRegistry

class BaseTool:
    name = "Base"
    category = "General"
    icon = None
    shortcut = None
    toggle = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ToolRegistry.register(cls)

    def __init__(self, viewport):
        self.viewport = viewport
        self.active = False

    # ---- Life Cycle ----
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    # ---- Events ----
    def mouse_press(self, event): pass
    def mouse_move(self, event): pass
    def mouse_release(self, event): pass
    def wheel(self, event): pass

    # ---- Drawing ----
    def draw(self, painter): pass

    # ---- UI Action ----
    def create_action(self, main_window):
        action = QAction(self.name, main_window)
        if self.shortcut:
            action.setShortcut(self.shortcut)
        action.setCheckable(self.toggle)
        action.triggered.connect(lambda: main_window.viewport.tool_manager.activate(self.name))
        return action
    
    def get_toolbar_widgets(self):
        """
        Return list of QWidget(s) to be added to toolbar.
        Default: no extra widgets.
        """
        return []
