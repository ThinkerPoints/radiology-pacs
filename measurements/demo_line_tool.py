from tools.base_tool import BaseTool
from PySide6.QtGui import QPen, QColor, QFont
from math import hypot

class DemoLineTool(BaseTool):
    """A simple GUI demo tool that draws a measurement line and shows its length.

    - Click to start a line
    - Drag to update
    - Release to finish (stored as an annotation)
    """
    name = "DemoLine"
    category = "Examples"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.start = None
        self.current = None
        self.annotations = []  # list of ((x1,y1),(x2,y2))

    def activate(self):
        super().activate()
        # no-op: could set cursor here

    def deactivate(self):
        super().deactivate()
        self.start = None
        self.current = None

    def mouse_press(self, event):
        x = event.x() if callable(event.x) else event.x
        y = event.y() if callable(event.y) else event.y
        self.start = (x, y)
        self.current = (x, y)
        if hasattr(self.viewport, "update"):
            self.viewport.update()

    def mouse_move(self, event):
        if not self.start:
            return
        x = event.x() if callable(event.x) else event.x
        y = event.y() if callable(event.y) else event.y
        self.current = (x, y)
        if hasattr(self.viewport, "update"):
            self.viewport.update()

    def mouse_release(self, event):
        if not self.start:
            return
        x = event.x() if callable(event.x) else event.x
        y = event.y() if callable(event.y) else event.y
        self.annotations.append((self.start, (x, y)))
        self.start = None
        self.current = None
        if hasattr(self.viewport, "update"):
            self.viewport.update()

    def _length_text(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length_px = hypot(dx, dy)
        if getattr(self.viewport, "pixel_spacing", None):
            mm = length_px * self.viewport.pixel_spacing
            return f"{mm:.1f} mm"
        return f"{length_px:.1f} px"

    def draw(self, painter):
        pen = QPen(QColor(220, 50, 50), 2)
        painter.setPen(pen)
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        # Active (in-progress) line
        if self.start and self.current:
            x1, y1 = self.start
            x2, y2 = self.current
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            text = self._length_text(self.start, self.current)
            tx = (x1 + x2) / 2
            ty = (y1 + y2) / 2 - 6
            painter.drawText(int(tx), int(ty), text)

        # Finished annotations
        for (sx, sy), (ex, ey) in self.annotations:
            painter.drawLine(int(sx), int(sy), int(ex), int(ey))
            text = self._length_text((sx, sy), (ex, ey))
            tx = (sx + ex) / 2
            ty = (sy + ey) / 2 - 6
            painter.drawText(int(tx), int(ty), text)
