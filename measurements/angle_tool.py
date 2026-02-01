from PySide6.QtGui import QPen, QColor, QFont
from PySide6.QtCore import Qt, QPointF
from tools.base_tool import BaseTool
import math

class AngleTool(BaseTool):
    name = "Angle"
    category = "Measurement"
    shortcut = "A"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.points = []
        self.temp_point = None
        self.angles = []   # [(A,B,C), ...]

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            p = event.position()
            self.points.append(p)

            if len(self.points) == 3:
                self.angles.append(tuple(self.points))
                self.points.clear()
                self.temp_point = None
            self.viewport.update()

    def mouse_move(self, event):
        if self.points:
            self.temp_point = event.position()
            self.viewport.update()

    def mouse_release(self, event):
        pass

    def draw(self, painter):
        pen = QPen(QColor(255, 255, 0), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 10))

        # Draw completed angles
        for A, B, C in self.angles:
            self._draw_angle(painter, A, B, C)

        # Rubber band preview
        if len(self.points) == 1 and self.temp_point:
            painter.drawLine(self.points[0], self.temp_point)

        elif len(self.points) == 2 and self.temp_point:
            self._draw_angle(painter, self.points[0], self.points[1], self.temp_point, preview=True)

    def _draw_angle(self, painter, A, B, C, preview=False):
        painter.drawLine(B, A)
        painter.drawLine(B, C)

        angle = self._calculate_angle(A, B, C)
        text = f"{angle:.1f}°"

        mid = B + QPointF(10, -10)
        painter.drawText(mid, text)

    def _calculate_angle(self, A, B, C):
        BA = (A - B)
        BC = (C - B)

        dot = BA.x()*BC.x() + BA.y()*BC.y()
        mag1 = math.hypot(BA.x(), BA.y())
        mag2 = math.hypot(BC.x(), BC.y())

        if mag1 * mag2 == 0:
            return 0.0

        cos_angle = dot / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))
        return math.degrees(math.acos(cos_angle))

    # -------- Persistence --------

    def export_json(self):
        return [
            {
                "A": (A.x(), A.y()),
                "B": (B.x(), B.y()),
                "C": (C.x(), C.y())
            } for A, B, C in self.angles
        ]

    def import_json(self, data):
        self.angles = [
            (QPointF(*d["A"]), QPointF(*d["B"]), QPointF(*d["C"]))
            for d in data
        ]
