# bd-freecad-library

Parametric build123d Python implementations of parts derived from the
[FreeCAD Parts Library](https://github.com/FreeCAD/FreeCAD-library).

This is a sibling project of [`fcstd2b123d`](https://github.com/pzfreo/fcstd2b123d) —
the translator validates that FreeCAD `.FCStd` files can be mapped to
build123d Python; this library curates the *standards-grade* outputs of
that work into a reusable Python package.

## Status: v0.0 — bootstrap

Currently scaffolded with ISO 4762 (socket head cap screws) as the first
family. Many more to come. Expect API churn in v0.x.

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
from bd_freecad_library.standards.iso4762 import iso4762_cap_screw

# An M5×20 socket head cap screw
screw = iso4762_cap_screw(thread="M5", length=20)
print(screw.volume)
```

## Threading note (v0.1 / v0.2 split)

v0.1 modelling: threaded shafts are **smooth cylinders** of the thread's
nominal diameter — geometrically correct except for the thread profile
itself. This matches `bd_warehouse`'s approach and is sufficient for
most assembly modelling.

v0.2 will add real helix-threaded variants once
[`fcstd2b123d#33`](https://github.com/pzfreo/fcstd2b123d/issues/33)
(Part::Helix translation) is closed. Tracked as a separate issue here.

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
