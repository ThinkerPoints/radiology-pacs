from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QFont, QColor, QFontMetrics
from PySide6.QtWidgets import (
    QInputDialog,
    QColorDialog,
    QFontDialog
)

from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

# ---------------------------------------------------------
# Data Model
# ---------------------------------------------------------
class TextItem:
    def __init__(self, image_pos, text, font, color):
        self.image_pos = image_pos      # QPointF (image space)
        self.text = text
        if isinstance(font, QFont):
            self.font = QFont(font)
        elif isinstance(font, str):
            self.font = QFont(font)
        else:
            self.font = QFont("Arial", 12)
        self.color = QColor(color)


# ---------------------------------------------------------
# Tool Plugin
# ---------------------------------------------------------
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

        # Default style
        self.default_font = QFont("Arial", 12)
        self.default_color = QColor(255, 255, 0)

    # -----------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------
    def activate(self):
        self.viewport.setCursor(Qt.IBeamCursor)

    def deactivate(self):
        self.viewport.unsetCursor()
        self.active_item = None

    # -----------------------------------------------------
    # Coordinate conversion
    # -----------------------------------------------------
    def screen_to_image(self, pos: QPointF) -> QPointF:
        zoom = self.viewport.zoom_scale
        pan = self.viewport.pan_offset
        cx = self.viewport.width() / 2
        cy = self.viewport.height() / 2
        return (pos - QPointF(cx, cy) - pan) / zoom

    def image_to_screen(self, pos: QPointF) -> QPointF:
        zoom = self.viewport.zoom_scale
        pan = self.viewport.pan_offset
        cx = self.viewport.width() / 2
        cy = self.viewport.height() / 2
        return pos * zoom + pan + QPointF(cx, cy)

    # -----------------------------------------------------
    # Mouse Events
    # -----------------------------------------------------
    def mouse_press(self, event):
        pos = event.position()

        # ---------------- Right Click → Delete
        if event.button() == Qt.RightButton:
            item = self.hit_test(pos)
            if item:
                self.items.remove(item)
                self.viewport.update()
            return

        # ---------------- Left Click
        item = self.hit_test(pos)
        if item:
            self.active_item = item
            screen_pos = self.image_to_screen(item.image_pos)
            self.drag_offset = screen_pos - pos
            self.viewport.setCursor(Qt.SizeAllCursor)
            return

        # ---------------- Create new text
        text, ok = QInputDialog.getText(
            self.viewport,
            "Add Text Annotation",
            "Enter text:"
        )

        if not ok or not text.strip():
            return

        # Optional: font chooser
        font = self.default_font
        if not isinstance(font, QFont):
            font = QFont(str(font))
        font, ok_font = QFontDialog.getFont(font, self.viewport)
        if ok_font:
            self.default_font = font

        # Optional: color chooser
        color = QColorDialog.getColor(self.default_color, self.viewport)
        if color.isValid():
            self.default_color = color

        image_pos = self.screen_to_image(pos)
        self.items.append(
            TextItem(image_pos, text, self.default_font, self.default_color)
        )
        self.viewport.update()

    def mouse_move(self, event):
        pos = event.position()

        # Dragging active text
        if self.active_item:
            new_screen_pos = pos + self.drag_offset
            self.active_item.image_pos = self.screen_to_image(new_screen_pos)
            self.viewport.update()
            return

        # Hover feedback
        if self.hit_test(pos):
            self.viewport.setCursor(Qt.SizeAllCursor)
        else:
            self.viewport.setCursor(Qt.IBeamCursor)

    def mouse_release(self, event):
        self.active_item = None
        self.drag_offset = None
        self.viewport.setCursor(Qt.IBeamCursor)

    def mouse_double_click(self, event):
        item = self.hit_test(event.position())
        if not item:
            return

        text, ok = QInputDialog.getText(
            self.viewport,
            "Edit Text",
            "Update text:",
            text=item.text
        )

        if ok and text.strip():
            item.text = text
            self.viewport.update()

    # -----------------------------------------------------
    # Keyboard Events
    # -----------------------------------------------------
    def key_press(self, event):
        if event.key() == Qt.Key_Delete and self.active_item:
            self.items.remove(self.active_item)
            self.active_item = None
            self.viewport.update()

    # -----------------------------------------------------
    # Hit Testing
    # -----------------------------------------------------
    def hit_test(self, screen_pos: QPointF):
        for item in reversed(self.items):
            metrics = QFontMetrics(item.font)
            pos = self.image_to_screen(item.image_pos)
            rect = metrics.boundingRect(item.text)
            rect.moveTopLeft(pos.toPoint())
            if rect.contains(screen_pos.toPoint()):
                return item
        return None

    # -----------------------------------------------------
    # Drawing
    # -----------------------------------------------------
    def draw(self, painter):
        for item in self.items:
            painter.setFont(item.font)
            painter.setPen(item.color)
            painter.drawText(
                self.image_to_screen(item.image_pos),
                item.text
            )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------
    def export_json(self):
        """Export annotations for saving / DICOM SR mapping"""
        return [
            {
                "type": "TEXT",
                "text": item.text,
                "x": item.image_pos.x(),
                "y": item.image_pos.y(),
                "font": item.font.toString(),
                "color": item.color.name()
            }
            for item in self.items
        ]
