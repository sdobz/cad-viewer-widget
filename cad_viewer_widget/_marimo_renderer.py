"""
Marimo renderer for CadViewerWidget.

Provides a marimo-compatible representation of CadViewer objects for display in marimo notebooks.
"""

import json
import uuid
from pathlib import Path

from .widget import CadViewer


def _get_js_bundle_path() -> str:
    """Get path to the compiled JS bundle."""
    bundle = Path(__file__).parent.parent / "js" / "dist" / "index.js"
    if not bundle.exists():
        raise FileNotFoundError(
            f"JS bundle not found at {bundle}. Run: cd js && yarn build"
        )
    return str(bundle)


def _marimo_icon():
    """Register marimo plugin for CadViewer display."""
    try:
        import marimo as mo
        
        # Register a custom object renderer for CadViewer
        def render_cadviewer(viewer: CadViewer) -> mo.Html:
            """Render a CadViewer object in marimo."""
            container_id = f"cad-viewer-{uuid.uuid4().hex[:8]}"
            
            # Prepare viewer state for JS
            viewer_state = {
                "id": viewer.widget.id,
                "shapes": dict(viewer.widget.shapes) if viewer.widget.shapes else {},
                "states": dict(viewer.widget.states) if viewer.widget.states else {},
                "tracks": viewer.tracks,
                # Camera state
                "position": viewer.widget.position,
                "quaternion": viewer.widget.quaternion,
                "target": viewer.widget.target,
                "zoom": viewer.widget.zoom,
                # Rendering options
                "cad_width": viewer.widget.cad_width,
                "height": viewer.widget.height,
                "glass": viewer.widget.glass,
                "tools": viewer.widget.tools,
                "theme": viewer.widget.theme,
                "grid": viewer.widget.grid,
                "axes": viewer.widget.axes,
                "ortho": viewer.widget.ortho,
                "control": viewer.widget.control,
            }
            
            # Create HTML container with embedded viewer
            html = f'''
            <div id="{container_id}" style="width: {viewer.widget.cad_width}px; height: {viewer.widget.height}px; position: relative; border: 1px solid #ccc;"></div>
            <script type="module">
              import {{ CadViewerModel, CadViewerView }} from "/js/dist/index.js";
              
              const container = document.getElementById("{container_id}");
              const state = {json.dumps(viewer_state)};
              
              // Create viewer instance
              const viewer = new CadViewerView({{
                el: container,
                model: new CadViewerModel(),
                state: state
              }});
              
              // Populate with shapes and state
              if (state.shapes && Object.keys(state.shapes).length > 0) {{
                viewer.render();
              }}
            </script>
            '''
            
            return mo.Html(html)
        
        # Try to register the renderer (marimo 0.8.0+ API)
        try:
            mo.ui.register_renderer(CadViewer, render_cadviewer)
        except AttributeError:
            # Older marimo versions may not support register_renderer
            pass
        
        return render_cadviewer
    except ImportError:
        # marimo not installed, skip registration
        return None


# Register on import if marimo is available
_cadviewer_renderer = _marimo_icon()
