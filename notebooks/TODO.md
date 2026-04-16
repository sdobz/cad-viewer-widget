# Marimo Missing Features

This note compares the original demo notebook in `Tests-and-demos.ipynb`, the auto-converted marimo version, and the migration notes in `MARIMO.md`.

The goal is to list features that existed in the Jupyter plugin workflow and are still missing, incomplete, or semantically degraded in marimo.

## Observed in `marimo run Tests-and-demos.py`

The current marimo run produces concrete failures that confirm several of the gaps below:

- `export_html()` raises `NotImplementedError`
- animation track validation fails because `self.widget.states` is empty when `add_track()` validates paths
- `select_clipping()` is missing on `CadViewer`
- `select_tree()` is missing on `CadViewer`
- repeated sidecar reuse emits warnings such as `Parameter 'anchor' cannot be changed after sidecar with title 'CVW 2' has been openend`
- multiple examples trigger `cad_width cannot be smaller than 780`, which is inherited Jupyter-era sizing behavior and not a good fit for marimo's inline layout

The rest of this document lists those failures by feature area.

## 1. Real sidecar panels and anchor placement

The original notebook spends a large part of the demo on sidecar behavior:

- `open_viewer("Test")`
- `show(..., title="CVW 1", anchor="right")`
- `anchor="split-right"`
- `anchor="split-top"`
- `set_default_sidecar("CVW 1")`
- `get_sidecar(...)`, `get_sidecars()`, `close_sidecar(...)`, `close_sidecars()`

In JupyterLab, these APIs meant a real docked output area or side panel managed by the shell. That is not available in marimo.

Current marimo state:

- the viewer renders inline in the cell output
- `title` and `anchor` do not create real docked panels
- split placements like `right`, `split-right`, and `split-top` have no marimo-native equivalent
- `close_*` and `get_*sidecar*` can still manage Python-side viewer objects, but not actual notebook UI panes

Why this matters:

- the sections `# The Viewer`, `# Sidecar handling`, and `## Use default sidecar` in `Tests-and-demos.ipynb` are fundamentally about multi-panel JupyterLab UX
- the converted marimo notebook can preserve API calls, but not the original behavior those calls demonstrated

What is missing:

- a marimo-native replacement for docked viewers
- a clear semantic rewrite of `anchor` so it is either implemented with marimo layout primitives or explicitly documented as ignored
- viewer reuse across cells in a single persistent named panel
- removal of stale sidecar warnings when the frontend is already falling back to inline rendering

## 2. Sidecar registry APIs still exist, but their old meaning is gone

The public API still exports the Jupyter-era sidecar helpers:

- `open_viewer`
- `get_sidecar`
- `get_sidecars`
- `set_default_sidecar`
- `close_sidecar`
- `close_sidecars`

These functions are central in the original notebook, but in marimo they no longer correspond to an actual shell-managed sidecar lifecycle.

Current marimo state:

- the helpers still maintain viewer objects and titles
- the frontend falls back to inline rendering when no real sidecar host exists
- notebook examples that test sidecar lookup and disposal are no longer testing a real UI feature

What is missing:

- either a real marimo implementation of named viewer regions
- or a reduced marimo API surface that removes the Jupyter-specific sidecar illusion
- a consistent marimo behavior for reusing named viewers without pretending that `anchor` is still meaningful

Until that is resolved, the sidecar-related parts of `Tests-and-demos.ipynb` are only partially portable.

## 3. `export_html()` is still unavailable

The original demo includes an export section with:

- `cv.export_png("boxes2.png")`
- `cv.export_html()`
- `cv.pin_as_png()`

Current marimo state:

- `export_png()` is still wired through widget messages
- `pin_as_png()` is still wired through widget messages
- `export_html()` raises `NotImplementedError`

Why this matters:

- `MARIMO.md` explicitly calls out HTML export as a remaining migration task
- the original notebook treats HTML export as a normal part of the viewer workflow

What is missing:

- a marimo-compatible standalone HTML export path
- replacement for the old Jupyter embedding mechanism used by `embed_minimal_html`
- a notebook-safe demo path so the export section can run without stopping the rest of the marimo notebook

## 4. `timeit` diagnostics are not confirmed working

The original notebook has an explicit status note:

- `timeit=FAIL`

That note appears in both the original `Tests-and-demos.ipynb` and the converted marimo version.

Current marimo state:

- the Python API still exposes `timeit`
- the JavaScript view still creates a `Timer("addShapes", ...)`
- the demo notebook still records the feature as failing

What is missing:

- confirmation that timing output is visible and useful in marimo
- if timing is only printed to a browser console, a better user-facing reporting path
- an updated demo showing the expected output, or removal of the option if it is no longer meant to work

## 5. Animation track validation is not working in the marimo demo flow

The original notebook includes animation demos that call `add_track()` on paths like:

- `/hexapod/right_back_leg`
- `/hexapod/left_middle_leg`
- `/hexapod/left_middle_leg/left_middle_lower_leg`

Current marimo run result:

- `add_track()` fails with `ValueError: ... is not a valid subpath of any of []`
- the failure comes from `_check_track()`, which validates track paths against `self.widget.states.keys()`
- in the failing marimo run, `self.widget.states` is empty at validation time

Why this matters:

- the animation sections in `Tests-and-demos.ipynb` were part of the original supported workflow
- this is not just a missing convenience feature; it breaks the animation demos outright

What is missing:

- correct population and synchronization of `widget.states` before animation track validation runs
- or a different validation strategy that does not require `states` to be fully populated before tracks can be added
- an updated marimo animation demo proving that `add_track()`, `animate()`, `play()`, and `stop()` work end to end

## 6. UI-mode switching helpers are missing from `CadViewer`

The demo notebook calls:

- `select_clipping()`
- `select_tree()`

Current marimo run result:

- both raise `AttributeError` because those methods do not exist on `CadViewer`

Why this matters:

- these are not sidecar-only features; they are part of the interaction workflow demonstrated by the original notebook
- their absence means the clipping and tree-navigation sections are incomplete in marimo today

What is missing:

- a Python API for switching the active viewer tool or tab in the migrated widget
- or a rewrite of the demo to avoid methods that no longer exist

## 7. The demo notebook still contains Jupyter-specific narratives that do not match marimo behavior

Several sections in `Tests-and-demos.ipynb` describe behavior that was true for the Jupyter plugin but is misleading in marimo, especially:

- `# Sidecar handling`
- `## openviewer and add_shapes`
- `## Use default sidecar`
- parts of the camera and viewer reuse demos that rely on named viewers bound to shell panels

What is missing:

- a marimo-specific demo narrative that explains which viewer APIs are fully supported inline
- explicit callouts where behavior is degraded or emulated
- separation between:
  - features that work identically in marimo
  - features that work with changed semantics
  - features that remain Jupyter-only

## Suggested next work

1. Decide whether sidecars are a real marimo feature target or should be removed from the marimo-facing API.
2. Implement a marimo-compatible `export_html()` path.
3. Fix animation-track path validation so the hexapod animation demos run.
4. Add or restore the viewer-mode helpers used by the clipping and tree sections, or remove those calls from the marimo demo.
5. Verify `timeit` end-to-end and either fix it or document it as unsupported.
6. Split the demo notebook into `works in marimo` and `Jupyter-only / not yet migrated` sections.
