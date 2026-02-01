from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QInputDialog
from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory


class TextItem:
    def __init__(self, image_pos, text):
        self.image_pos = image_pos
        self.text = text


@ToolPlugin("Text", ToolCategory.ANNOTATION)
class TextTool(BaseTool):
    name = "Text"
    category = ToolCategory.ANNOTATION
    shortcut = "T"

    def __init__(self, viewport):
        super().__init__(viewport)

        self.items = []
        self.active_item = None
        self.drag_offset = None

        self.font = QFont("Arial", 12)
        self.color = QColor(255, 255, 0)

    # --------------------
    # Tool lifecycle
    # --------------------
    def activate(self):
        self.viewport.setCursor(Qt.IBeamCursor)

    def deactivate(self):
        self.viewport.unsetCursor()
        self.active_item = None

    # --------------------
    # Coordinate helpers
    # --------------------
    def screen_to_image(self, pos):
        zoom = self.viewport.zoom_scale
        pan = self.viewport.pan_offset
        cx = self.viewport.width() / 2
        cy = self.viewport.height() / 2
        return (pos - QPointF(cx, cy) - pan) / zoom

    def image_to_screen(self, pos):
        zoom = self.viewport.zoom_scale
        pan = self.viewport.pan_offset
        cx = self.viewport.width() / 2
        cy = self.viewport.height() / 2
        return pos * zoom + pan + QPointF(cx, cy)

    # --------------------
    # Mouse events
    # --------------------
    def mouse_press(self, event):
        pos = event.position()

        # Check if clicking existing text
        item = self.hit_test(pos)
        if item:
            self.active_item = item
            screen_pos = self.image_to_screen(item.image_pos)
            self.drag_offset = screen_pos - pos
            self.viewport.setCursor(Qt.SizeAllCursor)
            return

        # Create new text
        text, ok = QInputDialog.getText(
            self.viewport, "Add Text", "Enter annotation text:"
        )

        if ok and text.strip():
            image_pos = self.screen_to_image(pos)
            self.items.append(TextItem(image_pos, text))
            self.viewport.update()

    def mouse_move(self, event):
        if not self.active_item:
            return

        new_screen_pos = event.position() + self.drag_offset
        self.active_item.image_pos = self.screen_to_image(new_screen_pos)
        self.viewport.update()

    def mouse_release(self, event):
        self.active_item = None
        self.drag_offset = None
        self.viewport.setCursor(Qt.IBeamCursor)

    def mouse_double_click(self, event):
        item = self.hit_test(event.position())
        if not item:
            return

        text, ok = QInputDialog.getText(
            self.viewport, "Edit Text", "Update annotation text:",
            text=item.text
        )

        if ok and text.strip():
            item.text = text
            self.viewport.update()

    # --------------------
    # Hit testing
    # --------------------
    def hit_test(self, screen_pos):
        from PySide6.QtGui import QFontMetrics
        metrics = QFontMetrics(self.font)
        for item in reversed(self.items):
            pos = self.image_to_screen(item.image_pos)
            rect = metrics.boundingRect(pos.x(), pos.y(), 1000, 1000, Qt.AlignLeft, item.text)
            if rect.contains(screen_pos.toPoint()):
                return item
        return None

    # --------------------
    # Drawing
    # --------------------
    def draw(self, painter):
        painter.setFont(self.font)
        painter.setPen(self.color)

        for item in self.items:
            screen_pos = self.image_to_screen(item.image_pos)
            painter.drawText(screen_pos, item.text)
