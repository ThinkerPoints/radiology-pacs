from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QDockWidget ,QFileDialog
from tools.auto_loader import load_plugins
from viewer.viewport import Viewport
from viewer.sidebar import DicomSidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Radiology PACS Viewer")
        # self.resize(1400, 900)

        # -------- Central Viewport --------
        self.viewport = Viewport(self)
        self.setCentralWidget(self.viewport)

        # -------- Sidebar (Series Gallery) --------
        self.sidebar = DicomSidebar(self.viewport, self)
        dock = QDockWidget("Series", self)
        dock.setWidget(self.sidebar)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # -------- Load DICOM Folder --------
        self.load_dicom_folder()

        # -------- Tools / Plugin System --------
        load_plugins()
        self.tool_manager = self.viewport.tool_manager
        self.tool_manager.load_plugins()
        self.build_toolbars()

    # ---------- TOOLBARS ----------

    def build_toolbars(self):
        groups = self.tool_manager.grouped_tools()

        for category, tools in groups.items():
            toolbar = self.addToolBar(category)
            toolbar.setMovable(False)

            for tool in tools:
                action = tool.create_action(self)
                toolbar.addAction(action)
                # Add any additional toolbar widgets
                for widget in tool.get_toolbar_widgets():
                    toolbar.addWidget(widget)

    # ---------- DICOM FOLDER LOADING ----------

    def load_dicom_folder(self):
        # folder = QFileDialog.getExistingDirectory(self,"Select DICOM Folder")
        folder = f"C:/DicomSampleImages/592"

        if folder:
            self.sidebar.load_folder(folder)