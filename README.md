# Radiology PACS Viewer 🩺🖼️

**Purpose:** A compact, modular DICOM viewer with measurement and annotation tools, a plugin-based tool system, and a performant image rendering pipeline.

---

## Architecture Overview 🔧

- **Entry point:** `app.py` starts the application and initializes core systems.
- **Core DICOM I/O:** `core/dicom_loader.py` handles reading DICOM files (via `pydicom`) and converting pixel data to numpy arrays.
- **Viewer & UI:** `viewer/` contains `main_window.py`, `viewport.py` and `sidebar.py` which manage rendering and UI interactions.
- **Tools & Plugins:** `tools/` provides the base tool abstractions (`base_tool.py`), plugin registration (`plugin_registry.py`), and management (`tool_manager.py`). Individual tools live in `tools/` and `measurements/`.
- **Annotations & Measurements:** `annotations/` and `measurements/` implement drawing primitives and measurement logic (distance, angle, ROI, etc.).
- **Navigation & Interaction:** `navigation/` exposes interactions like pan (`pan.py`), zoom (`zoom.py`), and `window_level.py`.

---

## Folder Structure 📁

Top-level structure (brief):

- `app.py` - Application entry point
- `requirements.txt` - Dependencies
- `core/` - DICOM loading and core image utilities (`core/dicom_loader.py`)
- `viewer/` - UI windows, viewports, and rendering
- `annotations/` - Drawing primitives (arrows, text)
- `measurements/` - Measurement tool implementations (`distance_tool.py`, `angle_tool.py`, `roi_tool.py`)
- `navigation/` - Navigation tools (pan/zoom/window/level)
- `tools/` - Tool plugin system and utilities
- `pacs_env/` - Local virtualenv and 3rd-party deps (OpenCV, numpy, PyQt, pydicom, pynetdicom)
- `tools/utility` - Helper utilities (flip/reset/rotate)

> Tip: To add a new tool, implement a subclass of `BaseTool` in `tools/` or `measurements/` and register it in the plugin registry.

---

## Image Rendering Pipeline 🖥️➡️🖼️

1. **DICOM Read** - `core/dicom_loader.py` reads DICOM dataset using `pydicom`, returns raw pixel data (numpy array) and metadata (rescale slope/intercept, modality LUT).
2. **Preprocessing** - Apply rescale (slope/intercept), modality LUT, and convert to Hounsfield or intensity units when needed.
3. **Window/Level** - `window_level` logic maps intensities into display range; this step supports different presets and dynamic updates.
4. **Transforms** - Apply geometric transforms (zoom, pan, rotation, flip) either by transforming coordinates or resampling the pixel buffer.
5. **Color mapping & Enhancements** - Optional LUT/colormap or contrast enhancements using OpenCV (`cv2`) if required.
6. **Buffer Conversion** - Convert the processed numpy array to a GUI-friendly image format (e.g., `QImage`/`QPixmap`) for Qt rendering.
7. **Overlay Rendering** - Draw annotations, measurements and UI overlays (scale bars, crosshair) on top of the image in `viewport.py`.
8. **Present** - Paint combined framebuffer to the screen. Use double buffering and redraw only on state change to keep UI responsive.

Performance notes:
- Cache scaled/resampled images for repeated zoom/pan operations.
- Use lower-resolution buffers while interacting (smooth interaction) and refine on mouse release.
- Leverage OpenCV/Numpy for fast pixel ops and PyQt for efficient blitting.

---

## Tool Plugin System Lifecycle 🔁

The tool system is designed for modular, pluggable tools that follow a clear lifecycle:

1. **Discovery & Registration**
   - At startup `tools/plugin_registry.py` (or `tools/auto_loader.py`) discovers tool classes and registers them with `ToolManager`.
2. **Initialization**
   - `ToolManager` instantiates tool objects and calls initialization hooks (e.g., `initialize()` or `activate()` on a plugin).
3. **Activation / Equip**
   - When user selects a tool, `ToolManager` sets the active tool and calls `on_activate()` (sets cursors, state, UI hints).
4. **Interaction**
   - The active tool receives user events (mouse press/move/release, key events) through well-defined callbacks (e.g., `on_mouse_press`, `on_mouse_move`, `on_mouse_release`).
   - Tools update temporary overlay/state while the user interacts (rubberband lines, live measurements).
5. **Commit / Cancel**
   - On completion, tool commits results (creates annotation objects or measurement records saved to memory or disk), or cancels and discards temporary state.
6. **Deactivation / Cleanup**
   - `on_deactivate()` cleans up UI state and unsubscribes from events.
7. **Persistence & Undo**
   - The `undo_redo.py` system receives commands from tools for undo/redo support. Measurements/annotations are stored in centralized model layers.

How to add a tool (high-level):
- Subclass `BaseTool` or implement the `ToolPlugin` interface in `tools/`.
- Implement lifecycle methods (`initialize`, `on_activate`, event handlers, `on_deactivate`).
- Register the tool via `plugin_registry` or ensure the auto-loader finds it.

---

## Quick Start 🚀

- Run the application: `python app.py`
- Open a DICOM series and use the sidebar to select tools (distance, angle, ROI, window/level, pan/zoom).

---

## Contributing & Extending 💡

- Add new measurement/annotation under `measurements/` or `annotations/`.
- For UI or rendering changes, modify `viewer/viewport.py` and ensure overlays are drawn in device coordinates.
- Use `tools/plugin_registry.py` to add plugin registration points and unit-test lifecycle hooks.

---

## Examples & Diagrams 🧩

- Tool lifecycle diagram: `docs/tool_lifecycle.puml` (PlantUML source). Render with PlantUML to export an SVG/PNG.
- Sample tool template: `tools/examples/template_tool.py` demonstrates a minimal `BaseTool` implementation and lifecycle.
- GUI demo tool: `measurements/demo_line_tool.py` is a runnable example that draws a measurement line overlay and displays length in mm or px.
- Unit tests: `tests/test_sample_tool.py` and `tests/test_demo_line_tool.py` show how to test registration, activation, and event handling.

How to run tests:

1. Install dev deps: `pip install pytest`
2. Run: `pytest -q`

GUI demo

- Start the app: `python app.py`
- In the toolbar look for the **Examples** category and select **DemoLine**. Click-drag on the image to draw a measurement line; the length will display near the line.

Diagrams

- PlantUML source: `docs/tool_lifecycle.puml`
- Rendered SVG: `docs/tool_lifecycle.svg`

If you'd like, I can also add an automated script to render PlantUML to PNG/SVG using PlantUML (`plantuml.jar`) or help generate a more detailed diagram. Reply with **"render script"** or **"detailed diagram"**.
