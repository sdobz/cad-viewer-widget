"""
Marimo integration helpers for CadViewer.

Provides utilities to display CadViewer objects in marimo notebooks.
"""

import json
import uuid
from typing import Optional
from pathlib import Path


def cadviewer_to_html(viewer) -> str:
    """
    Convert a CadViewer to HTML for marimo display.
    
    Usage:
        import marimo as mo
        from cad_viewer_widget import show
        from cad_viewer_widget._marimo import cadviewer_to_html
        
        cv = show(shapes, ...)
        mo.Html(cadviewer_to_html(cv))
    
    Parameters
    ----------
    viewer : CadViewer
        The viewer object to render
        
    Returns
    -------
    str
        HTML string with embedded viewer
    """
    from .widget import CadViewer
    
    if not isinstance(viewer, CadViewer):
        raise TypeError(f"Expected CadViewer, got {type(viewer)}")
    
    container_id = f"cad-{uuid.uuid4().hex[:8]}"
    
    # Prepare viewer state
    viewer_state = {
        "id": viewer.widget.id,
        "shapes": dict(viewer.widget.shapes) if viewer.widget.shapes else {},
        "states": dict(viewer.widget.states) if viewer.widget.states else {},
        "tracks": [t.__dict__ if hasattr(t, '__dict__') else t for t in viewer.tracks],
        # Camera
        "position": list(viewer.widget.position) if viewer.widget.position else None,
        "quaternion": list(viewer.widget.quaternion) if viewer.widget.quaternion else None,
        "target": list(viewer.widget.target) if viewer.widget.target else None,
        "zoom": float(viewer.widget.zoom),
        # UI  
        "cad_width": int(viewer.widget.cad_width),
        "height": int(viewer.widget.height),
        "glass": bool(viewer.widget.glass),
        "tools": bool(viewer.widget.tools),
        "theme": str(viewer.widget.theme),
        "grid": viewer.widget.grid,
        "axes": bool(viewer.widget.axes),
        "ortho": bool(viewer.widget.ortho),
        "control": str(viewer.widget.control),
        "up": str(viewer.widget.up),
    }
    
    # Build HTML with inline JS initialization
    html = f'''<div id="{container_id}" style="width: {viewer.widget.cad_width}px; height: {viewer.widget.height}px; border: 1px solid #ddd; position: relative; background: #f5f5f5;">
  <div style="padding: 20px; text-align: center; color: #666;">
    <p>CAD Viewer (WIP: marimo integration in progress)</p>
    <p>Shapes: {len(viewer.widget.shapes)} | Tracks: {len(viewer.tracks)}</p>
    <details>
      <summary>Viewer State</summary>
      <pre style="background: #f9f9f9; padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 11px;">{json.dumps(viewer_state, indent=2, default=str)}</pre>
    </details>
  </div>
</div>'''
    
    return html


def make_cadviewer_displayable(viewer):
    """
    Wrap a CadViewer for marimo display via mo.Html().
    
    Usage:
        import marimo as mo
        from cad_viewer_widget import show
        from cad_viewer_widget._marimo import make_cadviewer_displayable
        
        cv = show(shapes, ...)
        mo.Html(make_cadviewer_displayable(cv))
    
    Parameters
    ----------
    viewer : CadViewer
        The viewer object to wrap
        
    Returns
    -------
    str
        HTML representation suitable for mo.Html()
    """
    return cadviewer_to_html(viewer)
