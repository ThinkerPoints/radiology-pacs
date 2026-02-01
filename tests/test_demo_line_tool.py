from measurements.demo_line_tool import DemoLineTool
from tools.tool_manager import ToolManager


class DummyViewport:
    def __init__(self):
        self.updated = 0
        self.pixel_spacing = 0.5  # mm/pixel

    def update(self):
        self.updated += 1


class DummyEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def test_demo_line_tool_draw_and_store():
    vp = DummyViewport()
    t = DemoLineTool(vp)

    t.activate()
    assert t.active

    # start line
    t.mouse_press(DummyEvent(10, 10))
    assert t.start == (10, 10)
    assert t.current == (10, 10)

    # move
    t.mouse_move(DummyEvent(20, 10))
    assert t.current == (20, 10)

    # release
    t.mouse_release(DummyEvent(20, 10))
    assert len(t.annotations) == 1
    assert vp.updated >= 3

    # length text uses mm conversion due to pixel_spacing
    txt = t._length_text((10, 10), (20, 10))
    assert "mm" in txt


def test_tool_manager_integration():
    vp = DummyViewport()
    tm = ToolManager(vp)
    tm.load_plugins()

    # Ensure DemoLine is loaded
    assert "DemoLine" in tm.tools
    tm.activate("DemoLine")
    assert tm.active_tool.name == "DemoLine"
    assert tm.active_tool.active
