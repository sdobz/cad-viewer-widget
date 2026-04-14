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

### Milestone 1: Python runtime cutover (no compatibility boundary)

Purpose:

- remove Jupyter runtime dependencies from Python in one pass
- establish the marimo-native Python-side contract directly

Touched files:

- `cad_viewer_widget/__init__.py`
- `cad_viewer_widget/widget.py`
- `cad_viewer_widget/sidecar.py`
- `cad_viewer_widget/utils.py`

Work:

- remove `_jupyter_labextension_paths()` and `_jupyter_nbextension_paths()`
- remove `ipywidgets` and `IPython.display` runtime usage
- remove sidecar runtime semantics that depend on Jupyter shell behavior
- defer packaging metadata changes to Milestone 3 to avoid touching packaging files twice
- keep a stable, framework-neutral `show(...)` callable surface for future reuse

Testing step:

1. `python -m py_compile cad_viewer_widget/*.py`
2. `rg -n "ipywidgets|IPython.display|_jupyter_labextension_paths|_jupyter_nbextension_paths" cad_viewer_widget`
3. Confirm all hits are removed from Python runtime files.

Completion check:

- Python runtime files no longer depend on Jupyter constructs
- the Python public API still exposes a reusable show-level entrypoint for upstream callers

### Milestone 2: Frontend runtime cutover (remove Jupyter widget classes)

Purpose:

- replace Jupyter widget frontend classes with marimo-compatible render entrypoint
- keep viewer behavior logic while removing host-specific APIs

Touched files:

- `js/lib/widget.js`
- `js/lib/index.js`
- `js/lib/version.js`
- `js/lib/utils.js`
- `js/lib/serializer.js`
- `js/lib/app.js`

Work:

- remove `DOMWidgetModel` and `DOMWidgetView`
- remove direct shell coupling from viewer lifecycle
- keep state field names aligned with Python-side trait names
- keep rendering behavior, clipping, camera, selection, and animation logic
- document any payload shape changes as explicit schema version deltas

Testing step:

1. `cd js && yarn install`
2. `cd js && yarn build`
3. `rg -n "DOMWidgetModel|DOMWidgetView|@jupyter-widgets/base" js/lib js/package.json`

Completion check:

- JS runtime files do not require Jupyter widget base classes
- payloads produced by Python still map cleanly to frontend runtime fields

### Milestone 3: remove Jupyter plugin artifacts and packaging hooks

Purpose:

- remove JupyterLab and notebook extension packaging in one pass
- make the build produce only marimo-required assets

Touched files:

- `MANIFEST.in`
- `pyproject.toml`
- `js/package.json`
- `js/webpack.config.js`
- `js/lib/labplugin.js`
- `js/lib/extension.js`
- `js/lib/embed.js`
- `js/lib/sidecar.js`
- `cad-viewer-widget.json`
- `install.json`
- `.gitignore`

Work:

- remove hatch Jupyter builder hooks and Jupyter classifiers
- remove Jupyter plugin entry points and extension metadata
- remove sidecar integration files that only exist for notebook shell placement
- align build scripts to the marimo runtime bundle outputs
- keep any backend call points behind a transport abstraction that can be implemented later by non-marimo hosts

Testing step:

1. Create a fresh virtualenv.
2. `python -m pip install -U pip`
3. `python -m pip install -e .`
4. `cd js && yarn build`
5. `rg -n "jupyter|labextension|nbextension|@jupyter" pyproject.toml MANIFEST.in js/package.json install.json cad-viewer-widget.json`

Completion check:

- package metadata no longer defines Jupyter extension install paths
- packaging changes do not remove framework-neutral converter or protocol modules

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

### Milestone 5: final docs pass and repository purge

Purpose:

- make docs match the marimo-only runtime
- remove remaining Jupyter wording or stale references in repository files

Touched files:

- `README.md`
- `js/README.md`
- `RELEASE.md`
- `environment.yml`
- `Makefile`
- `docs/` (either regenerated for marimo or removed)

Work:

- add explicit README testing steps for running marimo notebooks under `notebooks/`
- remove Jupyter-specific setup and troubleshooting text
- remove stale release notes or metadata that claim Jupyter runtime support
- ensure docs do not advertise dual support

Testing step:

1. Follow README from a clean shell.
2. Run `marimo edit notebooks/Tests-and-demos.py`.
3. Run `marimo run notebooks/Tests-and-demos.py`.
4. Confirm steps are complete and accurate with no missing commands.

Completion check:

- a new contributor can run the marimo notebook flow using only README instructions

## Recommended testing matrix

Run this lightweight matrix as you advance:

1. Python syntax check for touched files: `python -m py_compile cad_viewer_widget/*.py`
2. JS build check for touched files: `cd js && yarn build`
3. Search-based purge check: `rg -n "jupyter|ipywidgets|labextension|DOMWidget|nbextension|@jupyter" .`
4. Marimo notebook startup check: `marimo run notebooks/Tests-and-demos.py`
5. One functional render check from `examples/`

## Completion verification

The migration is complete only when all of the following are true:

1. `python -m pip install -e .` works in a fresh virtualenv without installing JupyterLab.
2. `cd js && yarn build` works without any `@jupyter-*` packages.
3. `marimo edit notebooks/Tests-and-demos.py` opens successfully and renders a viewer.
4. `marimo run notebooks/Tests-and-demos.py` completes successfully.
5. `README.md` includes setup instructions and explicit commands for running the marimo notebooks.
6. `rg -n "jupyter|ipywidgets|labextension|DOMWidget|nbextension|@jupyter" .` returns no supported-runtime references.
7. No required code path depends on `IPython.display`, Jupyter shell APIs, or notebook extension registration.
8. `show(...)` and viewer payload contracts are documented and stable enough for a future `jupyter-cadquery` adapter layer.

## Suggested commit order

If you want the shortest safe path, do the milestones in this order:

1. Milestone 1
2. Milestone 2
3. Milestone 3
4. Milestone 4
5. Milestone 5

That order minimizes rework by cutting over each subsystem in a single pass and avoids temporary compatibility code that would otherwise be removed later.
