from tools.base_tool import BaseTool
from tools.tool_plugin import ToolPlugin
from tools.tool_category import ToolCategory

@ToolPlugin("Text", ToolCategory.ANNOTATION)
class TextTool(BaseTool): pass

