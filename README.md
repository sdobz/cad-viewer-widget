# cad-viewer-widget

A marimo-focused CAD viewer widget built on top of [three-cad-viewer](https://github.com/bernhard-42/three-cad-viewer).

This fork is taking the original JupyterLab or ipywidgets wrapper and reshaping it into a widget layer that can run cleanly in marimo. The rendering engine remains the same. The work in this repository is about replacing notebook-specific integration with a smaller, framework-neutral widget bridge.

## Project layout

The viewer stack is still split into three layers:

1. **[three-cad-viewer](https://github.com/bernhard-42/three-cad-viewer)**
   The WebGL CAD renderer. This is the core viewer and is already independent of Jupyter.

2. **cad-viewer-widget** (this repository)
   The Python and JavaScript bridge that exposes the viewer to notebook or app frontends. In this fork, the goal is marimo compatibility via a lighter widget protocol.

3. **[jupyter-cadquery](https://github.com/bernhard-42/jupyter-cadquery)**
   Higher-level CadQuery or build123d integration. That layer is separate from this repository and should treat this package as a viewer backend.

## Status

This repository is in transition from a JupyterLab-specific package to a marimo-oriented widget package.

- The rendering path is still based on `three-cad-viewer`.
- The existing source still contains Jupyter or ipywidgets-specific pieces.
- The target architecture is an `anywidget`-style bridge that can render inside marimo.
- Legacy notebooks under `notebooks/` are still useful as behavior references, but they are not the target runtime.

## Development environment

This fork uses Nix only to provide the system runtime and frontend toolchain. Python libraries come from your virtual environment, driven by `pyproject.toml` and `environment.yml`.

Requirements:

- Python
- Node.js
- Yarn 1.x
- A virtual environment for Python dependencies

If you use the included flake:

```bash
nix develop
```

Then create and populate the Python environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
cd js && yarn install && cd ..
```

If you are not using Nix, provide equivalent system tools yourself and then run the same virtualenv setup.

## Build workflow

Build the JavaScript bundle and the labextension artifacts:

```bash
cd js
yarn build:prod
cd ..
```

For active frontend development:

```bash
cd js
yarn build
yarn watch
```

Build the Python package:

```bash
hatch build
```

## marimo direction

The intended end state for this fork is:

- replace the Jupyter widget glue with a marimo-compatible widget layer
- preserve the existing viewer protocol and renderer behavior
- keep Python package installation in a normal virtualenv
- keep Nix limited to interpreter and toolchain provisioning

This repository is the viewer bridge, not the final application. A marimo notebook or app should import this package and use it as the rendering surface for tessellated CAD data.

## Legacy references

The following files remain useful while porting behavior:

- `notebooks/Tests-and-demos.ipynb`
- `notebooks/Classic-OCC-Bottle.ipynb`
- `examples/`

They document expected viewer behavior, but the long-term goal is to replace Jupyter-centric examples with marimo-native ones.
