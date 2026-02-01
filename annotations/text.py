from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QInputDialog
from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory


@ToolPlugin("Text", ToolCategory.ANNOTATION)
class TextTool(BaseTool):
    name = "Text"
    category = ToolCategory.ANNOTATION
    shortcut = "T"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.text_items = []     # [(pos, text)]
        self.current_pos = None

        self.font = QFont("Arial", 12)
        self.color = QColor(255, 255, 0)  # PACS yellow

    def activate(self):
        self.viewport.setCursor(Qt.IBeamCursor)

    def deactivate(self):
        self.viewport.unsetCursor()
        self.current_pos = None

    def mouse_press(self, event):
        if event.button() != Qt.LeftButton:
            return

        self.current_pos = event.position()

        text, ok = QInputDialog.getText(
            self.viewport,
            "Add Text",
            "Enter annotation text:"
        )

        if ok and text.strip():
            self.text_items.append((self.current_pos, text))
            self.viewport.update()

        self.current_pos = None

    def mouse_move(self, event):
        pass

    def mouse_release(self, event):
        pass

    def draw(self, painter):
        painter.setFont(self.font)
        painter.setPen(self.color)

        for pos, text in self.text_items:
            painter.drawText(pos, text)
