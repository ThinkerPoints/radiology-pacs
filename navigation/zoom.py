from PySide6.QtCore import Qt
from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Zoom", ToolCategory.NAVIGATION)
class ZoomTool(BaseTool):
	name = "Zoom"
	category = ToolCategory.NAVIGATION
	shortcut = "Z"

	def __init__(self, viewport):
		super().__init__(viewport)
		self.start_pos = None
		self.start_scale = 1.0
		self.scale = 1.0

	def activate(self):
		self.viewport.setCursor(Qt.SizeVerCursor)

	def deactivate(self):
		self.viewport.unsetCursor()

	def mouse_press(self, event):
		self.start_pos = event.position().y()
		self.start_scale = getattr(self.viewport, 'zoom_scale', 1.0)

	def mouse_move(self, event):
		if self.start_pos is None:
			return
		dy = event.position().y() - self.start_pos
		factor = 1.0 + dy / 200.0  # Sensitivity
		new_scale = max(0.1, min(10.0, self.start_scale * factor))
		self.viewport.zoom_scale = new_scale
		self.viewport.update()

	def mouse_release(self, event):
		self.start_pos = None

	def draw(self, painter):
		pass
