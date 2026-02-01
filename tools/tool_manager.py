from tools.plugin_registry import ToolRegistry

# class ToolManager:
#     def __init__(self, viewport):
#         self.viewport = viewport
#         self.tools = {}
#         self.active_tool = None

#     def load_plugins(self):
#         for tool_cls in ToolRegistry.all():
#             tool = tool_cls(self.viewport)
#             self.tools[tool.name] = tool

#     def grouped_tools(self):
#         groups = {}
#         for tool in self.tools.values():
#             groups.setdefault(tool.category, []).append(tool)
#         return groups

#     def activate(self, name):
#         if self.active_tool:
#             self.active_tool.deactivate()

#         tool = self.tools.get(name)
#         if tool:
#             self.active_tool = tool
#             tool.activate()
#             self.viewport.update()

#     def handle_mouse_press(self, event):
#         if self.active_tool:
#             self.active_tool.mouse_press(event)

#     def handle_mouse_move(self, event):
#         if self.active_tool:
#             self.active_tool.mouse_move(event)

#     def handle_mouse_release(self, event):
#         if self.active_tool:
#             self.active_tool.mouse_release(event)

#     def draw_overlay(self, painter):
#         if self.active_tool:
#             self.active_tool.drawOverlay(painter)



class ToolManager:
    def __init__(self, viewport):
        self.viewport = viewport
        self.tools = {}
        self.active_tool = None

    def load_plugins(self):
        for tool_cls in ToolRegistry.all():
            tool = tool_cls(self.viewport)
            self.tools[tool.name] = tool

    def grouped_tools(self):
        groups = {}
        for tool in self.tools.values():
            groups.setdefault(tool.category, []).append(tool)
        return groups

    def activate(self, name):
        if self.active_tool:
            self.active_tool.deactivate()

        tool = self.tools.get(name)
        if tool:
            self.active_tool = tool
            tool.activate()
            self.viewport.update()

    # ---- Event Routing ----
    def handle_mouse_press(self, event):
        if self.active_tool:
            self.active_tool.mouse_press(event)

    def handle_mouse_move(self, event):
        if self.active_tool:
            self.active_tool.mouse_move(event)

    def handle_mouse_release(self, event):
        if self.active_tool:
            self.active_tool.mouse_release(event)

    def handle_wheel(self, event):
        if self.active_tool:
            self.active_tool.wheel(event)

