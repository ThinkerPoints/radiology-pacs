from PySide6.QtGui import QPen, QColor, QFont
from PySide6.QtCore import Qt, QPointF
from tools.base_tool import BaseTool
import math

class DistanceTool(BaseTool):
    name = "Distance"
    category = "Measurement"
    shortcut = "D"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.start = None
        self.end = None
        self.temp_end = None
        self.measurements = []

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.position()
            self.temp_end = self.start

    def mouse_move(self, event):
        if self.start:
            self.temp_end = event.position()
            self.viewport.update()

    def mouse_release(self, event):
        if self.start and self.temp_end:
            self.end = self.temp_end
            self.measurements.append((self.start, self.end))
            self.start = None
            self.temp_end = None
            self.viewport.update()

    def draw(self, painter):
        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 10))

        # Draw completed measurements
        for p1, p2 in self.measurements:
            self._draw_line(painter, p1, p2)

        # Draw rubber band
        if self.start and self.temp_end:
            self._draw_line(painter, self.start, self.temp_end)

    def _draw_line(self, painter, p1, p2):
        painter.drawLine(p1, p2)

        dist_px = self._pixel_distance(p1, p2)
        dist_mm = self._mm_distance(dist_px)

        mid = (p1 + p2) / 2
        label = f"{dist_px:.1f}px / {dist_mm:.2f}mm"

        painter.drawText(mid + QPointF(5, -5), label)

    def _pixel_distance(self, p1, p2):
        return math.hypot(p2.x() - p1.x(), p2.y() - p1.y())

    def _mm_distance(self, px):
        spacing = self.viewport.pixel_spacing
        if spacing:
            return px * spacing
        return 0
