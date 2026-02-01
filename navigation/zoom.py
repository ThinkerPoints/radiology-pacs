from PySide6.QtCore import Qt
from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Zoom", ToolCategory.NAVIGATION)
class ZoomTool(BaseTool):
    name = "Zoom"
    category = ToolCategory.NAVIGATION
    shortcut = "Z"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.step = 1.1

    def activate(self):
        self.viewport.setCursor(Qt.CrossCursor)

    def deactivate(self):
        self.viewport.unsetCursor()

    def wheel(self, event):
        delta = event.angleDelta().y()
        if delta == 0:
            return

        zoom = getattr(self.viewport, "zoom", 1.0)

        if delta > 0:
            zoom *= self.step
        else:
            zoom /= self.step

        zoom = max(0.1, min(zoom, 10.0))

        self.viewport.zoom = zoom
        self.viewport.update()

    def draw(self, painter):
        pass
