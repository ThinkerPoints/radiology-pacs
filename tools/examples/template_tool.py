from tools.base_tool import BaseTool

class SampleTool(BaseTool):
    """Sample tool demonstrating the plugin lifecycle.

    Behavior:
    - Click to set start point
    - Move to update current point
    - Release to finalize and store the measurement
    """
    name = "SampleTool"
    category = "Examples"

    def __init__(self, viewport):
        super().__init__(viewport)
        self.points = []  # list of (x, y) tuples
        self.current = None
        self.finished = False

    def _get_xy(self, event):
        # Try a few common event shapes used by tests and Qt
        if hasattr(event, "x") and hasattr(event, "y"):
            x = event.x() if callable(event.x) else event.x
            y = event.y() if callable(event.y) else event.y
            return x, y
        if hasattr(event, "pos"):
            p = event.pos()
            x = p.x() if callable(p.x) else getattr(p, "x", p[0])
            y = p.y() if callable(p.y) else getattr(p, "y", p[1])
            return x, y
        raise AttributeError("Unknown event type for coordinates")

    # ---- Lifecycle ----
    def activate(self):
        super().activate()
        self.points = []
        self.current = None
        self.finished = False

    def deactivate(self):
        super().deactivate()
        # Cleanup if needed

    # ---- Events ----
    def mouse_press(self, event):
        x, y = self._get_xy(event)
        self.points = [(x, y)]
        self.current = (x, y)
        self.finished = False
        # Signal viewport to update overlay
        if hasattr(self.viewport, "update"):
            self.viewport.update()

    def mouse_move(self, event):
        if not self.points:
            return
        x, y = self._get_xy(event)
        self.current = (x, y)
        if hasattr(self.viewport, "update"):
            self.viewport.update()

    def mouse_release(self, event):
        if not self.points:
            return
        x, y = self._get_xy(event)
        self.points.append((x, y))
        self.current = None
        self.finished = True
        if hasattr(self.viewport, "update"):
            self.viewport.update()

    # ---- Draw (no real Qt painter required for tests, but defined for integration) ----
    def draw(self, painter):
        # In real integration this would draw on the viewport using QPainter
        pass
