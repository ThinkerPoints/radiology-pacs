from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStyle
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor, QMovie
from core.dicom_loader import load_dicom_series, dicom_to_pixmap, load_dicom

class DicomSidebar(QListWidget):

    def __init__(self, viewport, parent=None):
        super().__init__(parent)
        self.viewport = viewport
        self.itemClicked.connect(self.on_item_clicked)

    # ---------- LOAD DICOM FOLDER ----------

    def load_folder(self, folder_path):
        self.clear()
        # Show loading icon
        loading_item = QListWidgetItem()
        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_layout.setContentsMargins(0, 0, 0, 0)
        loading_label = QLabel()
        loading_label.setAlignment(Qt.AlignCenter)
        # Use a built-in spinner or fallback to text
        try:
            movie = QMovie(self.style().standardIcon(QStyle.SP_BrowserReload).pixmap(32, 32))
            loading_label.setMovie(movie)
            movie.start()
        except Exception:
            loading_label.setText("Loading...")
        loading_layout.addWidget(loading_label)
        loading_item.setSizeHint(loading_widget.sizeHint())
        self.addItem(loading_item)
        self.setItemWidget(loading_item, loading_widget)

        def finish_loading():
            self.clear()
            self.dicom_data = load_dicom_series(folder_path)
            for ds in self.dicom_data:
                pixmap = dicom_to_pixmap(ds, 0).scaled(
                    100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                # Draw frame counter if multi-frame
                total_frames = 1
                if hasattr(ds, 'NumberOfFrames'):
                    try:
                        total_frames = int(ds.NumberOfFrames)
                    except Exception:
                        total_frames = 1
                if total_frames > 1:
                    thumb = pixmap.copy()
                    painter = QPainter(thumb)
                    painter.setRenderHint(QPainter.Antialiasing)
                    font = QFont()
                    font.setPointSize(10)
                    font.setBold(True)
                    painter.setFont(font)
                    text = f"{total_frames} frames"
                    rect = thumb.rect().adjusted(0, thumb.height() - 24, 0, 0)
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(0, 0, 0, 160))
                    painter.drawRect(rect)
                    painter.setPen(Qt.white)
                    painter.drawText(rect, Qt.AlignCenter, text)
                    painter.end()
                    pixmap = thumb
                # Custom widget for gallery view
                widget = QWidget()
                layout = QVBoxLayout(widget)
                layout.setContentsMargins(2, 2, 2, 2)
                thumb_label = QLabel()
                thumb_label.setPixmap(pixmap)
                thumb_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(thumb_label)
                # Optionally, show file name or other info here
                item = QListWidgetItem()
                item.setData(Qt.UserRole, ds)
                item.setSizeHint(widget.sizeHint())
                self.addItem(item)
                self.setItemWidget(item, widget)

        # Simulate async loading for UI feedback
        QTimer.singleShot(100, finish_loading)

    # ---------- CLICK HANDLER ----------

    # def on_item_clicked(self, item):
    #     ds = load_dicom(item.data(Qt.UserRole))
    #     ds = item.data(Qt.UserRole)
    #     if ds:
    #         self.viewport.set_dicom(ds)

    def on_item_clicked(self, item):
        ds = item.data(Qt.UserRole)

        spacing = None
        if "PixelSpacing" in ds:
            spacing = (
                float(ds.PixelSpacing[0]),
                float(ds.PixelSpacing[1])
            )

        self.viewport.set_dicom(ds, spacing)
