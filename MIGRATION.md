# cad-viewer-widget migration plan

## Goal

Maintain a marimo-first CAD viewer with a single implementation model that supports the full demo feature set.

The target architecture must:

- use one runtime path (no split static/preview vs interactive implementations)
- use anywidget best practices for state sync and frontend communication
- preserve the public `show(...)` contract and payload semantics needed for future `jupyter-cadquery` alignment
- keep behavior stable across `marimo edit` and `marimo run`

## Scope and constraints

- no compatibility shims for deprecated Jupyter-only host behavior
- no parallel runtime modes that fork business logic
- keep Python and JavaScript interfaces framework-neutral where possible
- preserve payload compatibility or explicitly version schema changes

Non-goals:

- do not migrate `jupyter-cadquery` in this repository
- do not introduce a second implementation path for the same feature

## Rearchitecture plan

### 1) Adopt a single anywidget runtime

Implement one canonical viewer transport and lifecycle:

- Python side: one `CadViewerWidget` model of truth (traitlets)
- Frontend side: one `CadViewerView` mounted through anywidget
- communication: trait updates + custom messages through anywidget transport
- rendering: incremental updates against one live viewer instance

This replaces snapshot-only patterns that prevent imperative interactions such as animation control, `update_states`, and `export_png`.

### 2) Unify command and state flow

Define one update pipeline:

- declarative state: shapes, states, camera, clipping, materials, options
- imperative commands: play/pause/stop animation, export actions, camera presets, tab selection
- acknowledgements/events: export completion, selection and measure events, error reporting

All commands must route through the same runtime transport; no side channel for different notebook modes.

### 3) Feature parity target from demo contract

Use `notebooks/DEMO.md` as the implementation-independent acceptance target.

- each feature listed in DEMO must work via the single runtime
- behavior must be verifiable in both `marimo edit` and `marimo run`
- feature work should not depend on manual cell ordering side effects

### 4) Notebook interaction model for marimo

Refactor demo interactions to marimo-native control patterns:

- long-lived viewer cells driven by UI state
- explicit controls for animation and visibility steps
- avoid sequencing that only works when running cells one-by-one

### 5) Documentation and cleanup

- keep migration document forward-looking only
- keep demo behavior contract in `notebooks/DEMO.md`
- ensure README matches the single anywidget architecture and test flow

## Implementation guidelines

- keep a single source of truth for viewer state on the model
- apply minimal diffs to frontend scene graph for updates
- avoid host-specific branches in core logic
- isolate transport concerns from geometry/payload processing
- preserve or version payload schema intentionally

## anywidget best practices

- use standard anywidget model/view lifecycle (`render`, teardown cleanup)
- use traitlets for synchronized, observable state
- use custom messages for discrete commands/events where trait sync is not ideal
- ensure listeners are registered once and disposed reliably
- keep frontend mounts idempotent and safe on rerender
- avoid custom ad-hoc transport mechanisms when anywidget already provides one

## Marimo best practices

### Do

- model notebook behavior as reactive state transitions
- keep expensive data preparation separate from rendering cells
- use clear UI controls for operations that were previously implicit in cell order
- keep viewer updates deterministic from model state

### Do not

- rely on `window.postMessage`, parent window APIs, or iframe message bridges
- assume cell execution order as a user interaction primitive
- maintain duplicated runtime behavior by mode
- store authoritative app state only in frontend globals

## Validation plan

Run this matrix on every major change:

1. `python -m py_compile cad_viewer_widget/*.py`
2. `cd js && yarn build`
3. `marimo edit notebooks/Tests-and-demos.py`
4. `marimo run notebooks/Tests-and-demos.py`
5. verify all DEMO contract capabilities in `notebooks/DEMO.md`

## Completion criteria

Migration is complete when:

- one anywidget-based runtime supports all DEMO contract features
- animation, `update_states`, and export interactions work through the same transport
- no second implementation mode exists for equivalent functionality
- docs describe one architecture and one user workflow
