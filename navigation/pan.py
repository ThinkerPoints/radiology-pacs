from PySide6.QtCore import Qt, QPointF
from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Pan", ToolCategory.NAVIGATION)
class PanTool(BaseTool):
    name = "Pan"
    category = ToolCategory.NAVIGATION
    shortcut = "P"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.start_pos = None
        self.start_offset = QPointF(0, 0)

    def activate(self):
        self.viewport.setCursor(Qt.OpenHandCursor)

    def deactivate(self):
        self.viewport.unsetCursor()
        self.start_pos = None

    def mouse_press(self, event):
        if event.buttons() & Qt.LeftButton:
            self.start_pos = event.position()
            self.start_offset = getattr(self.viewport, "pan_offset", QPointF(0, 0))
            self.viewport.setCursor(Qt.ClosedHandCursor)

    def mouse_move(self, event):
        if self.start_pos is None:
            return

        delta = event.position() - self.start_pos
        self.viewport.pan_offset = self.start_offset + delta
        self.viewport.update()

    def mouse_release(self, event):
        self.start_pos = None
        self.viewport.setCursor(Qt.OpenHandCursor)

    def draw(self, painter):
        pass
