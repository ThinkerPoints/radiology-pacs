from tools.examples.template_tool import SampleTool
from tools.plugin_registry import ToolRegistry
from tools.tool_manager import ToolManager

class DummyViewport:
    def __init__(self):
        self.updated = 0
    def update(self):
        self.updated += 1

class DummyEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def test_sample_tool_lifecycle_and_events():
    vp = DummyViewport()
    tool = SampleTool(vp)

    # Activate
    tool.activate()
    assert tool.active
    assert tool.points == []

    # Simulate mouse press/move/release
    tool.mouse_press(DummyEvent(10, 20))
    assert tool.points == [(10, 20)]
    assert tool.current == (10, 20)
    assert not tool.finished

    tool.mouse_move(DummyEvent(15, 25))
    assert tool.current == (15, 25)

    tool.mouse_release(DummyEvent(15, 25))
    assert tool.finished
    assert tool.points[-1] == (15, 25)
    assert vp.updated >= 3  # press, move, release triggered updates


def test_tool_registration_and_manager_loading():
    # Ensure SampleTool is registered in ToolRegistry
    classes = [cls.__name__ for cls in ToolRegistry.all()]
    assert "SampleTool" in classes

    vp = DummyViewport()
    tm = ToolManager(vp)
    tm.load_plugins()

    # Ensure ToolManager knows about it and can activate
    assert "SampleTool" in tm.tools
    tm.activate("SampleTool")
    assert isinstance(tm.active_tool, SampleTool)
    assert tm.active_tool.active
