from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QWheelEvent, QImage,QPixmap
from tools.tool_manager import ToolManager
from core.dicom_loader import dicom_to_pixmap, get_rescaled_pixels
import numpy as np

class Viewport(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tool_manager = ToolManager(self)

        self.image = None
        self.pixel_spacing = None  # mm per pixel

        self.dataset = None
        self.current_frame = 0
        self.total_frames = 1
        self.pixmap = None

        # Window / Level
        self.pixel_array = None
        self.window = 400
        self.level = 40

        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)

    # ---------- IMAGE SETTING ----------

    def set_image(self, qimage, spacing=None):
        self.image = qimage
        self.pixel_spacing = spacing
        self.update()

    # ---------- DICOM LOADING ----------

    def set_dicom(self, ds, spacing=None):
        print("Viewport received:", type(ds))
        self.dataset = ds
        self.current_frame = 0
        self.pixel_spacing = spacing

        pixel_array = get_rescaled_pixels(ds)
        if pixel_array.ndim in (3, 4):
            self.total_frames = pixel_array.shape[0]
        else:
            self.total_frames = 1
        
        self.update_frame()

    def update_frame(self):
        if not self.dataset:
            return

        self.pixel_array = get_rescaled_pixels(self.dataset)[self.current_frame]
        self.apply_window_level()
        
        self.pixmap = dicom_to_pixmap(self.dataset, self.current_frame)
        self.update()

    # def update_frame(self):
    #     if not self.dataset:
    #         return

    #     arr = get_rescaled_pixels(self.dataset)

    #     if arr.ndim == 2:
    #         self.pixel_array = arr

    #     elif arr.ndim == 3:
    #         self.pixel_array = arr[self.current_frame]

    #     elif arr.ndim == 4:
    #         self.pixel_array = arr[self.current_frame, :, :, 0]

    #     else:
    #         raise ValueError(f"Unsupported DICOM shape {arr.shape}")

    #     if not hasattr(self, "_wl_initialized"):
    #         self.auto_window_level()
    #         self._wl_initialized = True

    #     self.apply_window_level()

    # ---------- SLICE SCROLLING ----------

    def wheelEvent(self, event: QWheelEvent):
        self.tool_manager.handle_wheel(event)
        if not self.dataset or self.total_frames <= 1:
            return

        delta = event.angleDelta().y()
        if delta > 0:
            self.current_frame = min(self.total_frames - 1, self.current_frame + 1)
        else:
            self.current_frame = max(0, self.current_frame - 1)

        self.update_frame()

    # ---------- TOOL EVENT ROUTING ----------

    def mousePressEvent(self, event):
        self.tool_manager.handle_mouse_press(event)

    def mouseMoveEvent(self, event):
        self.tool_manager.handle_mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.tool_manager.handle_mouse_release(event)

    # ---------- PAINT PIPELINE ----------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        if self.pixmap:
            painter.drawPixmap(self.rect(), self.pixmap)

        # Draw active tool overlay
        if self.tool_manager.active_tool:
            self.tool_manager.active_tool.draw(painter)

    # ---------- WINDOW / LEVEL ADJUSTMENT ----------
    
    def set_window_level(self, window, level):
        self.window = window
        self.level = level
        self.apply_window_level()

    def auto_window_level(self):
        """Auto WL from pixel statistics (RadiAnt-style)."""
        img = self.pixel_array

        p1, p99 = np.percentile(img, (1, 99))
        self.level = (p1 + p99) / 2
        self.window = (p99 - p1)

    def apply_window_level(self):
        if self.pixel_array is None:
            return

        img = self.pixel_array.astype(np.float32)

        low = self.level - self.window / 2
        high = self.level + self.window / 2

        img = np.clip(img, low, high)
        img = (img - low) / (high - low)
        img = np.clip(img, 0, 1)

        if getattr(self.dataset, "PhotometricInterpretation", "") == "MONOCHROME1":
            img = 1.0 - img

        img = (img * 255).astype(np.uint8)

        h, w = img.shape

        if img.ndim == 2:
            h, w = img.shape
            bytes_per_line = w
            qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_Grayscale8).copy()

        if img.ndim == 3 and img.shape[2] == 3:
            h, w, _ = img.shape
            bytes_per_line = 3 * w
            qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
        else:
            qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8).copy()

        self.pixmap = QPixmap.fromImage(qimg)
        self.update()



    