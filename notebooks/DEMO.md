# Demo feature contract

This document defines the implementation-independent behavior demonstrated by `notebooks/Tests-and-demos.py`.

Use this as the product contract during refactors.

## Purpose

The demo should prove that the viewer supports interactive CAD exploration and control, not just static rendering.

## Feature areas

### 1) Basic viewer rendering

- open a viewer and render tessellated examples from `examples/*.json`
- support multiple object types (solids/faces/edges/assemblies)
- show object tree and tools when enabled
- expose viewer status and model metadata

### 2) Viewer configuration

- apply rendering options: edge color, opacity, lighting, material settings, normal display
- apply camera and control options: trackball/orbit, up-axis, ortho/perspective
- apply scene options: axes, grids, transparency, black edges, explode, collapse modes
- support viewer sizing controls for CAD area, tree area, and height

### 3) Export and snapshot actions

- export current view to PNG file
- export standalone HTML for the current view
- pin current view as PNG in the viewer UI

### 4) Viewer reuse and update

- reuse an existing named viewer
- replace or add shapes in an existing viewer
- maintain camera behavior according to reset policy (`reset`, `keep`, `center`)

### 5) Camera interactions

- set/get camera position, target, quaternion, and zoom
- preserve or reset camera state based on user choice
- support camera preset operations and direct rotations

### 6) Runtime widget interaction

- mutate viewer options at runtime and observe changes
- read selection and measure-related data (`last_pick`, selected IDs)
- toggle UI and render parameters without recreating unrelated notebook state

### 7) Tree and clipping interactions

- switch between tree and clipping tabs/tools
- update clipping normals, sliders, plane helpers, and intersection mode
- apply object visibility updates by path (`update_states`)

### 8) Programmatic rotations

- rotate objects with trackball controls (`rotate_x/y/z`)
- rotate view with orbit controls (`rotate_up/left`)

### 9) Animation lifecycle

- define tracks by object path with time/value sequences
- validate track paths against available model paths
- send tracks, set animation speed, and run animation
- support playback controls: play, pause, stop
- support track lifecycle operations: add, clear, replace

### 10) Multi-viewer handling

- manage multiple concurrent viewers in one notebook
- close/dispose viewers cleanly

## Behavior requirements across marimo modes

All capabilities above should be available in both:

- `marimo edit`
- `marimo run`

The interaction model must not rely on manual one-cell-at-a-time execution order.

## Acceptance checklist

- each feature area has at least one runnable demo interaction
- no feature requires hidden host-specific behavior to work
- failures are surfaced with actionable errors
- notebook still serves as a practical manual QA script for the viewer
