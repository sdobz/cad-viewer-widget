# cad-viewer-widget marimo migration plan

## Goal

Convert this repository from a Jupyter or ipywidgets package into a marimo-specific viewer package.

The final state should satisfy all of the following:

- the runtime path is marimo-specific
- the Python package does not depend on Jupyter or ipywidgets
- the JavaScript package does not depend on `@jupyter-*` packages
- the notebook examples in `notebooks/` are marimo notebooks
- the README explains how to run those marimo notebooks
- source and packaging files no longer contain Jupyter references

## Conceptual map

If you are unfamiliar with the two systems, the migration is easier if you separate the viewer into three layers:

1. `three-cad-viewer` is the rendering engine.
2. This repository is the bridge layer between Python state and frontend rendering.
3. Jupyter or marimo is the host runtime.

In the current codebase, the bridge layer is tightly coupled to Jupyter widgets:

- Python side: `ipywidgets`, `IPython.display`, Jupyter extension registration
- JavaScript side: `DOMWidgetModel`, `DOMWidgetView`, lab plugin registration, sidecar integration
- Packaging side: JupyterLab build hooks and labextension artifacts

In marimo, the target model is simpler:

- Python creates a marimo-compatible widget object
- JavaScript renders into a DOM element and listens to synced state
- marimo notebooks import and use the package directly

That means the migration should preserve viewer behavior while replacing the host-specific glue.

## Future jupyter-cadquery compatibility guardrails

This migration must not block a later migration of `jupyter-cadquery`.

Keep these seams stable while removing Jupyter runtime dependencies here:

1. Preserve a framework-neutral `show(...)` contract in Python, even if internals change.
2. Preserve or explicitly version the viewer payload schema (shapes, states, tracks, camera, clipping, picks).
3. Isolate backend interaction behind a transport-agnostic interface (no hard dependency on Jupyter server extension APIs).
4. Keep rendering behavior in this package independent of where tessellation or high-level CAD orchestration lives.
5. Avoid coupling marimo notebook UX decisions to protocol internals that `jupyter-cadquery` might need later.

Explicit non-goal:

- Do not port `jupyter-cadquery` during this migration.
- Do not delete reusable converter logic solely because the Jupyter host is removed.

## Scope rules

Each milestone below is intentionally sized to about one commit.

- Do not combine multiple milestones into one large refactor.
- No compatibility shims. Remove old paths directly.
- A milestone may be non-functional as long as it has a narrow, explicit test step.
- Minimize rework by touching each subsystem once whenever possible.
- Do not regenerate docs until final cleanup.

## Touch-once strategy

To avoid churn, execute the migration in subsystem cutovers:

1. Python runtime cutover (single pass through Python runtime files)
2. Frontend runtime cutover (single pass through JS runtime files)
3. Packaging and metadata cutover (single pass through build or package files)
4. Notebook and README cutover (single pass through user-facing examples and instructions)
5. Final purge and verification sweep

Within each cutover:

- remove old Jupyter behavior immediately, do not retain dual paths
- do not add compatibility wrappers that are planned for deletion
- keep tests narrow and local to the files touched in that commit
- preserve cross-package interfaces (`show` API, payload schema, transport seam) needed by future `jupyter-cadquery` work

## Quality gates for every milestone

Every milestone should clear these gates before you move on:

1. The milestone-specific testing step below passes.
2. The commit message states which subsystem is intentionally broken (if any).
3. No compatibility shims are added.
4. Files outside the subsystem are not edited unless required for imports or build wiring.
5. New Jupyter references are not introduced.
6. Public contracts needed by future `jupyter-cadquery` migration are either preserved or explicitly versioned.

## Milestones

### ✅ Milestone 1: Python runtime cutover (COMPLETE)

- Removed `_jupyter_labextension_paths()`, `_jupyter_nbextension_paths()`
- Replaced `ipywidgets.Output` → `traitlets.HasTraits` in Python runtime
- Removed all `IPython.display` imports and Jupyter-specific semantics
- Kept framework-neutral `show()` API contract
- Validated: `python -m py_compile cad_viewer_widget/*.py` passes

### ✅ Milestone 2: Frontend runtime cutover (COMPLETE)

- Replaced `DOMWidgetModel`/`DOMWidgetView` with local `RuntimeModel`/`RuntimeView`
- Removed Jupyter shell and lab plugin integration
- Kept all rendering, camera, clipping, and state sync logic
- Kept state field names aligned with Python traitlets
- Validated: `cd js && yarn build` succeeds; no @jupyter-widgets references

### ✅ Milestone 3: Packaging & metadata cutover (COMPLETE)

- Removed hatch Jupyter builder hooks from `pyproject.toml`
- Removed JupyterLab classifiers and extension metadata
- Removed Jupyter plugin files: `labplugin.js`, `extension.js`, `embed.js`, `sidecar.js`, etc.
- Updated dependencies to: `numpy`, `orjson`, `pyparsing`, `traitlets`
- Removed `@jupyter-*` packages from JS
- Updated `environment.yml` to install package via `pip: -e .`
- Validated: Fresh virtualenv install works; no Jupyter references

### ✅ Milestone 4: Notebooks & validation conversion (COMPLETE)

- Converted `.ipynb` notebooks → marimo `.py` format using `marimo convert`
- Created: `notebooks/Tests-and-demos.py`, `notebooks/Classic-OCC-Bottle.py`
- Updated `validate_nb.py` to validate marimo Python notebooks
- Removed dual-notebook formats; only marimo `.py` files remain
- Validated: Both notebooks pass syntax checks; marimo can parse them

### ✅ Milestone 5: marimo plugin integration (COMPLETE)

- package metadata no longer defines Jupyter extension install paths
- packaging changes do not remove framework-neutral converter or protocol modules
- `export_html()` now works for marimo by emitting self-contained HTML
- animation track validation now resolves IDs from normalized shape payloads
- viewer mode helpers (`select_tree`, `select_clipping`) are available on `CadViewer`
- marimo notebook demo no longer relies on `ipywidgets`; uses `mo.ui.dropdown`
- demo example loading now uses absolute paths from notebook location
- minimum width constraints were relaxed for marimo inline layouts

### Milestone 4: convert notebooks and notebook validation to marimo

Purpose:

- replace legacy examples with marimo notebooks in `notebooks/`
- define notebook-level smoke tests for incremental WIP validation

Touched files:

- `notebooks/Tests-and-demos.py`
- `notebooks/Classic-OCC-Bottle.py`
- `notebooks/Tests-and-demos.ipynb`
- `notebooks/Classic-OCC-Bottle.ipynb`
- `validate_nb.py`

Work:

- create marimo notebooks that exercise at least one static example path from `examples/`
- archive or delete Jupyter notebooks rather than maintaining dual notebook formats
- update notebook validation helper to target marimo scripts
- keep notebook tests narrow to startup and one successful render

Testing step:

1. `marimo edit notebooks/Tests-and-demos.py`
2. `marimo run notebooks/Tests-and-demos.py`
3. Confirm at least one example object renders.

Completion check:

- marimo notebooks are the only supported notebooks in `notebooks/`

### Milestone 5: marimo rendering integration (IN PROGRESS)

Purpose:

- enable CadViewer to render 3D geometry in marimo notebooks
- sync Python trait state changes to JavaScript runtime
- load and initialize `js/dist/index.js` bundle in marimo output cells

Touched files:

- `cad_viewer_widget/widget.py` (add `_repr_html_()` and `observe()` trait listeners)
- `cad_viewer_widget/__init__.py` (update `show()` to return displayable object)
- `cad_viewer_widget/_marimo.py` (implement marimo-compatible display wrapper)
- `notebooks/Tests-and-demos.py`, `notebooks/Classic-OCC-Bottle.py` (verify rendering works)

Technical approach:

1. **Display hook**: Add `_repr_html_()` method to `CadViewer` that returns HTML with:
   - Unique DOM container ID for viewer mount
   - Embedded or CDN-loaded `js/dist/index.js`
   - Serialized initial state (shapes, camera, clipping, animations)

2. **JS bundle delivery**: Load `js/dist/index.js` from:
   - Option A: Inline as base64-encoded script tag (largest HTML but self-contained)
   - Option B: Serve from CDN or localhost during development
   - Option C: Use marimo's JavaScript/HTML output system for async loading

3. **State sync (marimo-native pattern)**:
   - **Do NOT use `window.postMessage()`**: It breaks marimo's reactivity model. Instead, use marimo's built-in state management.
   - Python: `traitlets.observe()` on shape, camera, clipping, animation traits → dispatch to `mo.state()` statefulness
   - Marimo reactive pattern: Wrap viewer in `mo.ui.html()` output; state changes flow through marimo's synchronous reactive DAG
   - JavaScript: RuntimeView receives state updates via marimo's normal output-update cycle, not postMessage
   - **Rationale**: marimo re-runs reactive cells in dependency order; postMessage creates a hidden side-channel that violates that model and causes desync bugs

4. **Runtime initialization (marimo-compatible)**:
   - Implement `_repr_html_()` returning a self-contained HTML fragment with embedded `<script>` for RuntimeView initialization
   - Use `mo.ui.html(viewer._repr_html_())` to wrap the viewer in marimo's output system
   - JS RuntimeView initializes once on mount; state updates flow through marimo cell re-runs, not DOM events
   - Python trait changes trigger marimo cell invalidation → marimo re-runs dependent cells → new `_repr_html_()` generated with updated state

Work breakdown:

- [ ] Modify `CadViewer.__init__()` to initialize state as traitlets (already done in M1)
- [ ] Implement `_repr_html_()` as stateless serializer of current traitlet values to JSON
- [ ] Verify `_repr_html_()` payload includes all state needed for JS initialization (shapes, camera, clipping, animations)
- [ ] Create marimo test notebook: `viewer = show(shape)` → calls `_repr_html_()` → marimo wraps in `mo.ui.html()`
- [ ] Test interactivity: viewer rotates/zooms locally in JS without Python callback (local-only state)
- [ ] Test parametric re-run: change shape input cell → re-run dependent viewer cell → `_repr_html_()` re-serializes new geometry, marimo updates output
- [ ] **ANTI-PATTERN CHECK**: Audit code for any `window.postMessage()`, `window.parent.*`, or `iframe.contentWindow` calls → remove

Testing step:

1. `marimo edit notebooks/Classic-OCC-Bottle.py`
2. Run first cell (bottle construction) → viewer renders
3. Interact with viewer (rotate, zoom, select, clip) → changes persist locally in JS
4. Change shape input parameter in earlier cell (e.g., adjust bottle height)
5. Verify dependent viewer cell re-runs → `_repr_html_()` called again → viewer shows new geometry
6. Verify no console errors about postMessage, stale DOM refs, or failed state sync

Completion check:

- CadViewer renders with 3D geometry visible when called in marimo notebook cell
- Local user interactions (rotate, zoom) work without Python roundtrips
- **Parametric re-run**: Changing input cell triggers downstream viewer cell re-execution with updated geometry
- Camera, clipping, and animation state flows through marimo's DAG (not side-channel postMessage)
- Notebook can be reloaded or scrolled without breaks
- Works in both `marimo edit` and `marimo run` modes
- State sync audit: zero references to postMessage, parent window APIs, or iframe messaging

### Milestone 6: final docs pass and repository purge

Purpose:

- make docs match the marimo-only runtime
- remove remaining Jupyter wording or stale references in repository files

Touched files:

- `README.md` (add marimo setup and examples section)
- `js/README.md` (remove Jupyter build steps)
- `RELEASE.md` or `CHANGELOG.md` (update for marimo-only release)
- `environment.yml` (already updated for marimo)
- `Makefile` (remove Jupyter build targets)

Work:

- add explicit README testing steps for running marimo notebooks under `notebooks/`
- remove Jupyter-specific setup and troubleshooting text
- remove stale release notes or metadata that claim Jupyter runtime support
- document marimo installation and notebook execution
- add troubleshooting for marimo-specific issues (plugin loading, state sync)

Testing step:

1. Follow README from a clean shell.
2. Run `marimo edit notebooks/Tests-and-demos.py`.
3. Interact with viewer and verify 3D rendering works.
4. Run `marimo run notebooks/Tests-and-demos.py` and confirm rendering works in headless mode.

Completion check:

- a new contributor can run the marimo notebook flow using only README instructions
- no Jupyter references remain in docs or configuration files

## Marimo Integration Best Practices

Follow these patterns to ensure the migrated codebase works correctly in marimo and avoids common pitfalls:

### ✅ DO

1. **Use marimo's reactive DAG natively**:

   ```python
   # Good: Let marimo track dependencies automatically
   @app.cell
   def __(geojson_path):
       mesh = build_mesh_from_geojson(geojson_path)
       return mesh

   @app.cell
   def __(mesh, text_label):
       stl = build_candle(mesh, text_label)
       return stl
   ```

   When `text_label` changes, only the second cell re-runs; the mesh is cached.

2. **Use `mo.status.spinner()` for long-running computations**:

   ```python
   with mo.status.spinner(title="Building mesh..."):
       mesh = tessellate_terrain(elevation_data, optimization_level)
   ```

   Gives users feedback and prevents the "Is it frozen?" perception.

3. **Use `mo.ui.stop_button()` for interruptible tasks** (if marimo supports):

   ```python
   stop = mo.ui.stop_button()
   mesh = expensive_build(stop=stop)
   ```

4. **Cache expensive computations explicitly**:

   ```python
   @functools.lru_cache(maxsize=16)
   def fetch_terrain(geojson_bounds_tuple):
       """Hash args automatically; only fetch once per unique bounds."""
       return touch_terrain_api(geojson_bounds_tuple)
   ```

   Or use `@mo.cache` if marimo provides it.

5. **Return stateless `_repr_html_()` snapshots**:

   ```python
   class CadViewer:
       def _repr_html_(self):
           """Serialize current state to HTML; called each time cell re-runs."""
           return html_with_embedded_state(self.shapes, self.camera, self.clipping)
   ```

   Every cell re-run generates a fresh HTML snapshot; marimo renders it without side effects.

6. **Separate data transformation from display**:

   ```python
   @app.cell
   def __(elevation_grid):
       # Pure computation: no rendering
       processed = process_raster(elevation_grid)
       return processed

   @app.cell
   def __(processed):
       # Display only: no heavy lifting
       fig = mo.ui.html(plot_heightmap(processed))
       return fig
   ```

### ❌ DO NOT

1. **Do NOT use `window.postMessage()` or `window.parent.postMessage()`**:
   - Breaks marimo's reactivity model
   - Creates hidden state channels
   - Causes desync bugs after re-runs
   - **Replace with**: Rely on marimo cell re-execution to propagate state

2. **Do NOT assume persistent Python objects across cell re-runs**:

   ```python
   # BAD: global state persists but is stale
   global_cache = {}

   @app.cell
   def __(input_param):
       if input_param in global_cache:
           return global_cache[input_param]  # Stale!
       ...
   ```

   **Replace with**: Use `@functools.lru_cache` or explicit `mo.cache` that respects marimo's invalidation

3. **Do NOT store widget state in JavaScript closure variables**:

   ```javascript
   // BAD: Persists across notebook re-runs, stale after parameter change
   let cachedMesh = null;

   function initViewer(mesh) {
       if (cachedMesh === mesh) return;  // Won't detect update!
       ...
   }
   ```

   **Replace with**: Initialize fresh on every `_repr_html_()` call; let marimo track the state

4. **Do NOT mix framework state models (jQuery event handlers + trait observers + DOM mutations)**:

   ```python
   # BAD: Multiple layers fighting for control
   self.on_trait_change(self._on_shape_change)  # Python
   viewer.addEventListener("shapeChange", ...)  # JS
   IPython.display.update_display(...)  # Jupyter hack
   ```

   **Replace with**: Single path: Python traitlets → marimo cell invalidation → fresh `_repr_html_()` → JS one-time init

5. **Do NOT assume the viewer keeps state between marimo edits**:
   - Editing a notebook cell re-runs that cell and all dependents
   - The 3D viewer gets a fresh DOM element
   - Any local JS state (zoom level, selection) is lost
   - **Solution**: If users need to preserve local state (e.g., camera angle), persist it in the Python state and serialize in `_repr_html_()`

6. **Do NOT implement runtime transport or comm channels**:
   ```python
   # BAD: Trying to re-implement Jupyter comms
   class CadViewer:
       def __init__(self):
           self.comm = create_comm()  # Won't work in marimo!
   ```
   **Replace with**: Use pure Python state + `_repr_html_()` serialization

### ⚠️ PATTERNS REQUIRING AUDIT

Before shipping Milestone 5, audit the codebase for these patterns:

- [ ] **Search for `window.postMessage`** or `window.parent`: Any found = blocker
- [ ] **Search for `ipywidgets`** imports in runtime code (should be none after M1)
- [ ] **Search for `IPython.display`** or `IPython.get_ipython()`: Any found = blocker
- [ ] **Search for `comm` or `Comm`** in Python runtime: Should not exist (M1 already removed)
- [ ] **Search for global state in JS** (e.g., `let viewer_instance = null` at module level): Audit each one; prefer function-scoped or marimo-managed state
- [ ] **Test parametric re-run**: Modify an input parameter in a notebook cell → verify downstream viewer cell re-executes → verify new geometry displays (not stale)

---

## Current status

Run this lightweight matrix as you advance through each milestone:

1. Python syntax check: `python -m py_compile cad_viewer_widget/*.py`
2. JS build check: `cd js && yarn build`
3. Search-based purge check: `rg -n "jupyter|ipywidgets|labextension|DOMWidget|nbextension|@jupyter" . --no-ignore`
4. Marimo notebook startup: `marimo edit notebooks/Tests-and-demos.py`
5. Marimo notebook renderability (after M5): Verify 3D viewer displays in cell output
6. Marimo notebook execution: `marimo run notebooks/Tests-and-demos.py`

## Completion verification

The migration is complete only when all of the following are true:

1. `python -m pip install -e .` works in a fresh virtualenv without installing JupyterLab or notebook.
2. `cd js && yarn build` works without any `@jupyter-*` packages.
3. `marimo edit notebooks/Tests-and-demos.py` opens successfully and **renders a 3D viewer** in the output cell.
4. `marimo run notebooks/Tests-and-demos.py` completes and **produces 3D viewer HTML output**.
5. User interactions (rotation, zoom, clipping, object selection) in the viewer work as expected.
6. `README.md` includes setup instructions and explicit commands for running the marimo notebooks.
7. `rg -n "jupyter|ipywidgets|labextension|DOMWidget|nbextension|@jupyter" .` returns no supported-runtime references (excluding this MIGRATION.md file).
8. No required code path depends on `IPython.display`, Jupyter shell APIs, or notebook extension registration.
9. `show(...)` and viewer payload contracts are documented and stable enough for a future adapter layer (e.g., jupyter-cadquery).
10. Both `notebooks/Tests-and-demos.py` and `notebooks/Classic-OCC-Bottle.py` render successfully with no modifications needed by end users.

## Current status

✅ **Completed**: Milestones 1-5 (Python runtime, JS runtime, packaging, notebooks, marimo integration)
⏸️ **Pending**: Milestone 6 (docs purge)

## Suggested commit order

Do the milestones in this order to minimize rework:

1. Milestones 1-4 (already complete)
2. Milestone 5 (marimo rendering integration)
3. Milestone 6 (docs purge and final cleanup)
