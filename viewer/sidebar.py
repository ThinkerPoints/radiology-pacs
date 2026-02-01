from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from core.dicom_loader import load_dicom_series, dicom_to_pixmap, load_dicom

class DicomSidebar(QListWidget):

    def __init__(self, viewport, parent=None):
        super().__init__(parent)
        self.viewport = viewport
        self.itemClicked.connect(self.on_item_clicked)

    # ---------- LOAD DICOM FOLDER ----------

    def load_folder(self, folder_path):
        self.clear()
        self.dicom_data = load_dicom_series(folder_path)

        for ds in self.dicom_data:
            pixmap = dicom_to_pixmap(ds, 0).scaled(
                    100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            item = QListWidgetItem()
            item.setIcon(pixmap)
            item.setData(Qt.UserRole, ds)  # 256 = Qt.UserRole
            self.addItem(item)

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
