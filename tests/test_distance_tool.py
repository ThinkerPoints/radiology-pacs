import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from measurements.distance_tool import DistanceTool
from PySide6.QtCore import QPointF
import json


class DummyViewport:
    def __init__(self):
        self.updated = 0
        self.pixel_spacing = 0.5  # mm/pixel

    def update(self):
        self.updated += 1


class DummyEvent:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def button(self):
        from PySide6.QtCore import Qt
        return Qt.LeftButton
    
    def position(self):
        return QPointF(self._x, self._y)


def test_distance_tool_export_json():
    """Test that export_json serializes measurements correctly."""
    vp = DummyViewport()
    tool = DistanceTool(vp)

    # Add some measurements
    tool.measurements.append((QPointF(10, 20), QPointF(50, 80)))
    tool.measurements.append((QPointF(100, 100), QPointF(200, 150)))

    # Export to JSON
    exported = tool.export_json()

    # Verify structure
    assert len(exported) == 2
    assert exported[0]["start"] == (10.0, 20.0)
    assert exported[0]["end"] == (50.0, 80.0)
    assert exported[1]["start"] == (100.0, 100.0)
    assert exported[1]["end"] == (200.0, 150.0)

    # Verify it's JSON serializable
    json_str = json.dumps(exported)
    assert json_str is not None
    print("✓ export_json works correctly")


def test_distance_tool_import_json():
    """Test that import_json deserializes measurements correctly."""
    vp = DummyViewport()
    tool = DistanceTool(vp)

    # Import from JSON data
    data = [
        {"start": (10.0, 20.0), "end": (50.0, 80.0)},
        {"start": (100.0, 100.0), "end": (200.0, 150.0)}
    ]
    tool.import_json(data)

    # Verify measurements are restored
    assert len(tool.measurements) == 2
    p1, p2 = tool.measurements[0]
    assert isinstance(p1, QPointF)
    assert isinstance(p2, QPointF)
    assert p1.x() == 10.0 and p1.y() == 20.0
    assert p2.x() == 50.0 and p2.y() == 80.0

    p1, p2 = tool.measurements[1]
    assert p1.x() == 100.0 and p1.y() == 100.0
    assert p2.x() == 200.0 and p2.y() == 150.0
    print("✓ import_json works correctly")


def test_distance_tool_roundtrip():
    """Test that export -> import preserves data (roundtrip test)."""
    vp = DummyViewport()
    tool1 = DistanceTool(vp)

    # Add measurements
    tool1.measurements.append((QPointF(10.5, 20.5), QPointF(50.5, 80.5)))
    tool1.measurements.append((QPointF(100.75, 100.75), QPointF(200.25, 150.25)))

    # Export
    exported = tool1.export_json()

    # Import into a new tool
    tool2 = DistanceTool(vp)
    tool2.import_json(exported)

    # Verify all measurements match
    assert len(tool1.measurements) == len(tool2.measurements)
    for (p1_orig, p2_orig), (p1_new, p2_new) in zip(tool1.measurements, tool2.measurements):
        assert abs(p1_orig.x() - p1_new.x()) < 1e-6
        assert abs(p1_orig.y() - p1_new.y()) < 1e-6
        assert abs(p2_orig.x() - p2_new.x()) < 1e-6
        assert abs(p2_orig.y() - p2_new.y()) < 1e-6
    print("✓ roundtrip export/import preserves data")


def test_distance_tool_empty_export():
    """Test that exporting with no measurements returns empty list."""
    vp = DummyViewport()
    tool = DistanceTool(vp)

    exported = tool.export_json()
    assert exported == []
    print("✓ empty export works correctly")


def test_distance_tool_import_empty():
    """Test that importing empty list works."""
    vp = DummyViewport()
    tool = DistanceTool(vp)

    tool.measurements.append((QPointF(10, 20), QPointF(50, 80)))
    tool.import_json([])

    assert len(tool.measurements) == 0
    print("✓ empty import works correctly")


if __name__ == "__main__":
    test_distance_tool_export_json()
    test_distance_tool_import_json()
    test_distance_tool_roundtrip()
    test_distance_tool_empty_export()
    test_distance_tool_import_empty()
    print("\n✅ All distance_tool persistence tests passed!")
