"""Marimo integration helpers for CadViewer."""

import base64
import gzip
import hashlib
from html import escape
from pathlib import Path
from uuid import uuid4

import numpy as np
import orjson


def _ndarray_to_wire(arr: np.ndarray) -> dict:
    """Encode numpy arrays in the JS serializer wire format.

    The frontend already understands objects of the form:
    {buffer, codec, dtype, shape}
    so we reuse that stable schema instead of expanding arrays to JSON lists.
    """
    if arr.dtype in (np.int32, np.int64, np.uint64):
        arr = arr.astype(np.uint32, order="C")
    elif not arr.flags["C_CONTIGUOUS"]:
        arr = np.ascontiguousarray(arr)

    return {
        "buffer": base64.b64encode(arr.ravel().tobytes()).decode("ascii"),
        "codec": "b64",
        "dtype": str(arr.dtype),
        "shape": list(arr.shape),
    }


def _orjson_default(obj):
    """Serialize numpy-heavy viewer state compactly."""
    if isinstance(obj, np.ndarray):
        return _ndarray_to_wire(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    raise TypeError(f"Type is not JSON serializable: {type(obj)}")


def _viewer_state(viewer) -> dict:
    """Collect a stateless snapshot for JS initialization."""
    state = viewer.status(all=True)
    state.setdefault("initialize", False)
    state.setdefault("disposed", False)
    state.setdefault("debug", False)
    state.setdefault("result", "")
    state.setdefault("rendered", False)
    return state


def _gzip_b64(data: bytes) -> str:
    """Return gzip-compressed bytes encoded as ASCII base64."""
    return base64.b64encode(gzip.compress(data, compresslevel=6)).decode("ascii")


def cadviewer_to_html(viewer) -> str:
    """Serialize a CadViewer into compact self-contained marimo HTML."""
    from importlib.resources import files
    _bundle = Path(str(files("cad_viewer_widget").joinpath("static/index.js")))
    bundle = _bundle if _bundle.exists() else None
    state = _viewer_state(viewer)

    state_bytes = orjson.dumps(state, default=_orjson_default)
    state_b64 = _gzip_b64(state_bytes)

    width = state.get("cad_width", 800)
    height = state.get("height", 600)

    container_id = f"cvw-{uuid4().hex}"
    error_id = f"{container_id}-error"

    if bundle is None:
        state_json_escaped = escape(state_bytes.decode("utf-8"))
        return f"""
<div style="border:1px solid #d8d8d8;padding:12px;border-radius:8px;">
  <div style="font-weight:600;">CadViewer bundle not found</div>
  <div style="margin:6px 0 0;">Expected one of: js/dist/index.js or cad_viewer_widget/static/index.js</div>
  <details style="margin-top:10px;">
    <summary>Serialized state</summary>
    <pre style="margin-top:8px;max-height:300px;overflow:auto;">{state_json_escaped}</pre>
  </details>
</div>
"""

    bundle_bytes = bundle.read_bytes()
    bundle_b64 = _gzip_b64(bundle_bytes)
    bundle_hash = hashlib.sha256(bundle_bytes).hexdigest()[:16]

    return f"""
<div id="{container_id}" style="width:{width}px;height:{height}px;max-width:100%;"></div>
<div id="{error_id}" style="display:none;color:#b91c1c;margin-top:8px;"></div>
<script>
(async () => {{
  const host = document.getElementById("{container_id}");
  const errorNode = document.getElementById("{error_id}");

  const fail = (message) => {{
    if (errorNode) {{
      errorNode.style.display = "block";
      errorNode.textContent = message;
    }}
  }};

  const b64ToBytes = (text) => {{
    const binary = atob(text);
    const bytes = new Uint8Array(binary.length);
    for (let index = 0; index < binary.length; index += 1) {{
      bytes[index] = binary.charCodeAt(index);
    }}
    return bytes;
  }};

  const gunzipText = async (text) => {{
    if (typeof DecompressionStream === "undefined") {{
      throw new Error("This browser does not support DecompressionStream for gzip payloads");
    }}
    const bytes = b64ToBytes(text);
    const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    return await new Response(stream).text();
  }};

  const ensureBundle = async () => {{
    if (window.CadViewerWidget && typeof window.CadViewerWidget.mountCadViewer === "function") {{
      return;
    }}

    window.__cadViewerWidgetBundleCache = window.__cadViewerWidgetBundleCache || {{}};
    window.__cadViewerWidgetBundlePromises = window.__cadViewerWidgetBundlePromises || {{}};

    if (window.__cadViewerWidgetBundlePromises["{bundle_hash}"]) {{
      await window.__cadViewerWidgetBundlePromises["{bundle_hash}"];
      return;
    }}

    window.__cadViewerWidgetBundlePromises["{bundle_hash}"] = (async () => {{
      const source = await gunzipText("{bundle_b64}");
      window.__cadViewerWidgetBundleCache["{bundle_hash}"] = source;

      const script = document.createElement("script");
      script.type = "text/javascript";
      script.text = source;
      document.head.appendChild(script);
    }})();

    await window.__cadViewerWidgetBundlePromises["{bundle_hash}"];
  }};

  try {{
    await ensureBundle();
    const state = JSON.parse(await gunzipText("{state_b64}"));
    const api = window.CadViewerWidget;
    if (!api || typeof api.mountCadViewer !== "function") {{
      fail("CadViewerWidget bundle loaded but mount API is unavailable");
      return;
    }}
    api.mountCadViewer(host, state);
  }} catch (error) {{
    fail(`Failed to mount viewer: ${{error.message}}`);
  }}
}})();
</script>
"""

