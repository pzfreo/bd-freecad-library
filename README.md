# bd-freecad-library

Parametric build123d Python implementations of parts derived from the
[FreeCAD Parts Library](https://github.com/FreeCAD/FreeCAD-library).

This is a sibling project of [`fcstd2b123d`](https://github.com/pzfreo/fcstd2b123d) —
the translator validates that FreeCAD `.FCStd` files can be mapped to
build123d Python; this library curates the *standards-grade* outputs of
that work into a reusable Python package.

## Status: v0.0 — bootstrap

Currently scaffolded with **EN 10058 hot-rolled flat steel bars** as
the first family — a true category 2a candidate (structural steel
profiles, which `bd_warehouse` doesn't cover today).

Validation harness in place. See `CONTRIBUTING.md` for the five-step
process used to add each family, including the **step 0 bd_warehouse
gate** — anything bd_warehouse already covers is explicitly out of
scope.

## What's in here

- `src/bd_freecad_library/standards/` — parametric implementations of
  internationally standardised parts (ISO / DIN / ANSI / EN).
- `src/bd_freecad_library/curated/` — hand-picked individual designs
  that exemplify common problems.

## Install

```bash
pip install bd-freecad-library
```

## Example

```python
from bd_freecad_library.standards.en_10058 import en_10058_flat_bar

# A 60 × 4 × 100 mm hot-rolled flat steel bar
bar = en_10058_flat_bar(width=60, thickness=4, length=100)
print(bar.volume)  # 24000.0
```

## Validation

Every parts family is regression-tested against the corresponding
fixtures in the [`fcstd2b123d`](https://github.com/pzfreo/fcstd2b123d)
corpus. The harness in `tests/_validation.py` translates each
fixture, exec's the build123d emit, and compares geometry
(bbox-extents + optional volume) against the parametric function.

Run the validation locally:

```bash
export FCSTD2B123D_REPO=$(realpath ../fcd2b123d)
export FCSTD2B123D_FREECAD_PYTHON=$(realpath $FCSTD2B123D_REPO/.conda/envs/freecad/bin/python)
export FCSTD2B123D_FREECAD_PYTHONPATH=$(realpath $FCSTD2B123D_REPO/.conda/envs/freecad/lib)
pip install -e .[dev]
pytest
```

Tests skip cleanly when `FCSTD2B123D_FREECAD_PYTHON` is unset.

## Provenance and licensing

- **Code**: MIT (see `LICENSE`).
- **Dimension tables**: drawn from international standards, cross-referenced
  against the FreeCAD Parts Library (LGPL-2.1-or-later). See `NOTICE`.
- **Validation**: each module's geometry is regression-tested against
  the corresponding `fcstd2b123d` fixtures.

## How this relates to `bd_warehouse`

[`bd_warehouse`](https://github.com/gumyr/bd_warehouse) is the canonical
build123d ecosystem library. It covers ~48% of the FreeCAD Parts Library
already (fasteners, bearings, chains). This project fills the gap:
parametric standards `bd_warehouse` *could* cover but doesn't yet (EN
profiles, tab washers, etc.), and curated individual designs that aren't
parametric families.

Modules here that mature may eventually be contributed upstream to
`bd_warehouse`. See the strategy document in `fcstd2b123d` for the long
view.
