from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Flip", ToolCategory.UTILITY, toggleable=False)
class FlipTool(BaseTool):
    def activate(self):
        self.viewport.flip_horizontal()
