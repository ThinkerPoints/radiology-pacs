from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox
from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
import numpy as np
from tools.wl_presets import WL_PRESETS

# @ToolPlugin(
#     name="window_level",
#     display_name="Window / Level",
#     category=ToolCategory.NAVIGATION,
#     shortcut="W"
# )
class WindowLevelTool(BaseTool):

    name = "Window / Level"
    category = ToolCategory.NAVIGATION
    shortcut = "W"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.start_pos = None
        self.start_window = None
        self.start_level = None

    def activate(self):
        self.viewport.setCursor(Qt.CrossCursor)

    def deactivate(self):
        self.viewport.unsetCursor()

    def mouse_press(self, event):
        self.start_pos = event.position()
        self.start_window = self.viewport.window
        self.start_level = self.viewport.level

    def mouse_move(self, event):
        if not self.start_pos:
            return

        delta = event.position() - self.start_pos
        new_window = max(1, self.start_window + delta.x())
        new_level = self.start_level + delta.y()

        self.viewport.set_window_level(new_window, new_level)

    def mouse_release(self, event):
        self.start_pos = None

    def draw(self, painter: QPainter):
        pass

    def get_toolbar_widgets(self):
        preset_box = QComboBox()
        preset_box.setMinimumWidth(120)
        preset_box.addItem("WL Presets")

        for name in WL_PRESETS:
            preset_box.addItem(name)

        preset_box.currentTextChanged.connect(self.apply_preset)
        return [preset_box]
    
    def apply_preset(self, name):
        if name in WL_PRESETS:
            window, level = WL_PRESETS[name]
            self.viewport.set_window_level(window, level)
            
