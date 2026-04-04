import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from measurements.angle_tool import AngleTool
from PySide6.QtCore import QPointF
import json
import math


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


def test_angle_tool_export_json():
    """Test that export_json serializes angles correctly."""
    vp = DummyViewport()
    tool = AngleTool(vp)

    # Add some angles (A, B, C points)
    tool.angles.append((QPointF(10, 10), QPointF(50, 50), QPointF(100, 10)))
    tool.angles.append((QPointF(0, 0), QPointF(100, 100), QPointF(200, 0)))

    # Export to JSON
    exported = tool.export_json()

    # Verify structure
    assert len(exported) == 2
    assert exported[0]["A"] == (10.0, 10.0)
    assert exported[0]["B"] == (50.0, 50.0)
    assert exported[0]["C"] == (100.0, 10.0)
    assert exported[1]["A"] == (0.0, 0.0)
    assert exported[1]["B"] == (100.0, 100.0)
    assert exported[1]["C"] == (200.0, 0.0)

    # Verify it's JSON serializable
    json_str = json.dumps(exported)
    assert json_str is not None
    print("✓ export_json works correctly")


def test_angle_tool_import_json():
    """Test that import_json deserializes angles correctly."""
    vp = DummyViewport()
    tool = AngleTool(vp)

    # Import from JSON data
    data = [
        {"A": (10.0, 10.0), "B": (50.0, 50.0), "C": (100.0, 10.0)},
        {"A": (0.0, 0.0), "B": (100.0, 100.0), "C": (200.0, 0.0)}
    ]
    tool.import_json(data)

    # Verify angles are restored
    assert len(tool.angles) == 2
    A, B, C = tool.angles[0]
    assert isinstance(A, QPointF)
    assert isinstance(B, QPointF)
    assert isinstance(C, QPointF)
    assert A.x() == 10.0 and A.y() == 10.0
    assert B.x() == 50.0 and B.y() == 50.0
    assert C.x() == 100.0 and C.y() == 10.0

    A, B, C = tool.angles[1]
    assert A.x() == 0.0 and A.y() == 0.0
    assert B.x() == 100.0 and B.y() == 100.0
    assert C.x() == 200.0 and C.y() == 0.0
    print("✓ import_json works correctly")


def test_angle_tool_roundtrip():
    """Test that export -> import preserves data (roundtrip test)."""
    vp = DummyViewport()
    tool1 = AngleTool(vp)

    # Add angles
    tool1.angles.append((QPointF(10.5, 10.5), QPointF(50.5, 50.5), QPointF(100.5, 10.5)))
    tool1.angles.append((QPointF(0.75, 0.75), QPointF(100.25, 100.25), QPointF(200.75, 0.75)))

    # Export
    exported = tool1.export_json()

    # Import into a new tool
    tool2 = AngleTool(vp)
    tool2.import_json(exported)

    # Verify all angles match
    assert len(tool1.angles) == len(tool2.angles)
    for (A1, B1, C1), (A2, B2, C2) in zip(tool1.angles, tool2.angles):
        assert abs(A1.x() - A2.x()) < 1e-6
        assert abs(A1.y() - A2.y()) < 1e-6
        assert abs(B1.x() - B2.x()) < 1e-6
        assert abs(B1.y() - B2.y()) < 1e-6
        assert abs(C1.x() - C2.x()) < 1e-6
        assert abs(C1.y() - C2.y()) < 1e-6
    print("✓ roundtrip export/import preserves data")


def test_angle_tool_empty_export():
    """Test that exporting with no angles returns empty list."""
    vp = DummyViewport()
    tool = AngleTool(vp)

    exported = tool.export_json()
    assert exported == []
    print("✓ empty export works correctly")


def test_angle_tool_import_empty():
    """Test that importing empty list works."""
    vp = DummyViewport()
    tool = AngleTool(vp)

    tool.angles.append((QPointF(10, 10), QPointF(50, 50), QPointF(100, 10)))
    tool.import_json([])

    assert len(tool.angles) == 0
    print("✓ empty import works correctly")


def test_angle_tool_calculation():
    """Test that angle calculation matches exported data."""
    vp = DummyViewport()
    tool = AngleTool(vp)

    # Add a 90-degree angle (right angle)
    A = QPointF(0, 0)
    B = QPointF(0, 50)
    C = QPointF(50, 50)
    tool.angles.append((A, B, C))

    # Calculate angle manually
    angle = tool._calculate_angle(A, B, C)
    assert abs(angle - 90.0) < 1.0  # Should be close to 90 degrees

    # Verify it exports and reimports correctly
    exported = tool.export_json()
    tool2 = AngleTool(vp)
    tool2.import_json(exported)
    angle2 = tool2._calculate_angle(tool2.angles[0][0], tool2.angles[0][1], tool2.angles[0][2])
    assert abs(angle - angle2) < 1e-6
    print("✓ angle calculation preserved through persistence")


if __name__ == "__main__":
    test_angle_tool_export_json()
    test_angle_tool_import_json()
    test_angle_tool_roundtrip()
    test_angle_tool_empty_export()
    test_angle_tool_import_empty()
    test_angle_tool_calculation()
    print("\n✅ All angle_tool persistence tests passed!")
