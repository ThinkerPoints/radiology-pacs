from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Arrow", ToolCategory.ANNOTATION)
class ArrowTool(BaseTool): pass


