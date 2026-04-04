import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from measurements.roi_tool import ROITool
from PySide6.QtCore import QPointF, QRectF
import json


class DummyViewport:
    def __init__(self):
        self.updated = 0
        self.pixel_spacing = (0.5, 0.5)  # mm/pixel (sx, sy)

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


def test_roi_tool_export_json():
    """Test that export_json serializes ROIs correctly."""
    vp = DummyViewport()
    tool = ROITool(vp)

    # Add some ROIs
    tool.rois.append(QRectF(10, 20, 100, 50))
    tool.rois.append(QRectF(200, 150, 80, 100))

    # Export to JSON
    exported = tool.export_json()

    # Verify structure
    assert len(exported) == 2
    assert exported[0]["x"] == 10.0
    assert exported[0]["y"] == 20.0
    assert exported[0]["w"] == 100.0
    assert exported[0]["h"] == 50.0
    
    assert exported[1]["x"] == 200.0
    assert exported[1]["y"] == 150.0
    assert exported[1]["w"] == 80.0
    assert exported[1]["h"] == 100.0

    # Verify it's JSON serializable
    json_str = json.dumps(exported)
    assert json_str is not None
    print("✓ export_json works correctly")


def test_roi_tool_import_json():
    """Test that import_json deserializes ROIs correctly."""
    vp = DummyViewport()
    tool = ROITool(vp)

    # Import from JSON data
    data = [
        {"x": 10.0, "y": 20.0, "w": 100.0, "h": 50.0},
        {"x": 200.0, "y": 150.0, "w": 80.0, "h": 100.0}
    ]
    tool.import_json(data)

    # Verify ROIs are restored
    assert len(tool.rois) == 2
    rect1 = tool.rois[0]
    assert isinstance(rect1, QRectF)
    assert rect1.x() == 10.0
    assert rect1.y() == 20.0
    assert rect1.width() == 100.0
    assert rect1.height() == 50.0

    rect2 = tool.rois[1]
    assert rect2.x() == 200.0
    assert rect2.y() == 150.0
    assert rect2.width() == 80.0
    assert rect2.height() == 100.0
    print("✓ import_json works correctly")


def test_roi_tool_roundtrip():
    """Test that export -> import preserves data (roundtrip test)."""
    vp = DummyViewport()
    tool1 = ROITool(vp)

    # Add ROIs
    tool1.rois.append(QRectF(10.5, 20.5, 100.75, 50.25))
    tool1.rois.append(QRectF(200.125, 150.875, 80.5, 100.5))

    # Export
    exported = tool1.export_json()

    # Import into a new tool
    tool2 = ROITool(vp)
    tool2.import_json(exported)

    # Verify all ROIs match with floating point precision
    assert len(tool1.rois) == len(tool2.rois)
    for rect1, rect2 in zip(tool1.rois, tool2.rois):
        assert abs(rect1.x() - rect2.x()) < 1e-6
        assert abs(rect1.y() - rect2.y()) < 1e-6
        assert abs(rect1.width() - rect2.width()) < 1e-6
        assert abs(rect1.height() - rect2.height()) < 1e-6
    print("✓ roundtrip export/import preserves data")


def test_roi_tool_empty_export():
    """Test that exporting with no ROIs returns empty list."""
    vp = DummyViewport()
    tool = ROITool(vp)

    exported = tool.export_json()
    assert exported == []
    print("✓ empty export works correctly")


def test_roi_tool_import_empty():
    """Test that importing empty list works."""
    vp = DummyViewport()
    tool = ROITool(vp)

    tool.rois.append(QRectF(10, 20, 100, 50))
    tool.import_json([])

    assert len(tool.rois) == 0
    print("✓ empty import works correctly")


def test_roi_tool_area_calculation():
    """Test that area calculation works with exported/imported ROIs."""
    vp = DummyViewport()
    tool = ROITool(vp)

    # Add a 100x100 pixel ROI (50x50 mm with 0.5 spacing)
    tool.rois.append(QRectF(0, 0, 100, 100))

    # Calculate area
    area_mm2 = tool._calculate_area_mm2(tool.rois[0])
    expected_area = 100 * 0.5 * 100 * 0.5  # 2500 mm²
    assert abs(area_mm2 - expected_area) < 1e-6

    # Export and reimport
    exported = tool.export_json()
    tool2 = ROITool(vp)
    tool2.import_json(exported)

    # Verify area calculation on imported ROI
    area_mm2_2 = tool2._calculate_area_mm2(tool2.rois[0])
    assert abs(area_mm2 - area_mm2_2) < 1e-6
    print("✓ area calculation preserved through persistence")


def test_roi_tool_zero_spacing():
    """Test area calculation with zero pixel spacing."""
    vp = DummyViewport()
    vp.pixel_spacing = None  # No spacing
    tool = ROITool(vp)

    tool.rois.append(QRectF(0, 0, 100, 100))
    area_mm2 = tool._calculate_area_mm2(tool.rois[0])
    assert area_mm2 == 0.0
    print("✓ handles zero/none pixel spacing correctly")


if __name__ == "__main__":
    test_roi_tool_export_json()
    test_roi_tool_import_json()
    test_roi_tool_roundtrip()
    test_roi_tool_empty_export()
    test_roi_tool_import_empty()
    test_roi_tool_area_calculation()
    test_roi_tool_zero_spacing()
    print("\n✅ All roi_tool persistence tests passed!")
