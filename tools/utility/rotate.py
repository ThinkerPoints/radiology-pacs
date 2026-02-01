from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Rotate", ToolCategory.UTILITY, toggleable=False)
class RotateTool(BaseTool):
    def activate(self):
        self.viewport.rotate_90()

