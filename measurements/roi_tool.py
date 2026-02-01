from PySide6.QtGui import QPen, QColor, QFont
from PySide6.QtCore import Qt, QPointF, QRectF
from tools.base_tool import BaseTool
import numpy as np

class ROITool(BaseTool):
    name = "ROI"
    category = "Measurement"
    shortcut = "R"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.start = None
        self.end = None
        self.rois = []   # list of QRectF

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.position()
            self.end = self.start
            self.viewport.update()

    def mouse_move(self, event):
        if self.start:
            self.end = event.position()
            self.viewport.update()

    def mouse_release(self, event):
        if self.start and self.end:
            rect = QRectF(self.start, self.end).normalized()
            self.rois.append(rect)
            self.start = None
            self.end = None
            self.viewport.update()

    def draw(self, painter):
        pen = QPen(QColor(0, 255, 0), 2, Qt.DashLine)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 10))

        # Draw completed ROIs
        for rect in self.rois:
            self._draw_roi(painter, rect)

        # Rubber band
        if self.start and self.end:
            rect = QRectF(self.start, self.end).normalized()
            painter.drawRect(rect)

    def _draw_roi(self, painter, rect):
        painter.drawRect(rect)

        area_mm2 = self._calculate_area_mm2(rect)
        text = f"{area_mm2:.2f} mm²"

        painter.drawText(rect.topLeft() + QPointF(5, -5), text)

    def _calculate_area_mm2(self, rect):
        if not self.viewport.pixel_spacing:
            return 0.0

        sx, sy = self.viewport.pixel_spacing
        width_mm = rect.width() * sx
        height_mm = rect.height() * sy
        return width_mm * height_mm

    # ---------- Persistence ----------

    def export_json(self):
        return [
            {
                "x": r.x(),
                "y": r.y(),
                "w": r.width(),
                "h": r.height()
            } for r in self.rois
        ]

    def import_json(self, data):
        self.rois = [QRectF(d["x"], d["y"], d["w"], d["h"]) for d in data]
