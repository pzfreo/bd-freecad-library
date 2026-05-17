# Contributing — adding a part family

This library follows a repeatable five-step process for each new
standardised parts family or curated design. The workflow is designed
so every family ends up with the same shape: a parametric function (or
class — see issue #1), a regression manifest pinned to FreeCAD source
fixtures, and a per-module README.

## The five steps

### 1. SELECT — pick fixtures from the FreeCAD library

Find fixtures in the [`fcstd2b123d`](https://github.com/pzfreo/fcstd2b123d)
corpus that match the family. The corpus has ~3,194 files; the bulk
are organised under `tests/fixtures/sample_2026/`, `sample_813/`,
and `tier3_corpus*/`.

Inclusion check for the family:

- Internationally standardised (ISO / DIN / ANSI / EN spec exists)
- Dimensionally parametric (a small dimension table covers the family)
- Multiple variants in the FreeCAD library (proves it's worth
  parametrising rather than one-off curating)
- All variants translate cleanly through `fcstd2b123d` today (none
  excluded in its corpus's `EXCLUDED_FROM_TEST`)

If any of these fails, the part is **not** a candidate for
`standards/` — it belongs under `curated/` (if it's good CAD) or
upstream as a `fcstd2b123d` issue (if the translator chokes on it).

### 2. SCAFFOLD — layout

Create the per-family files:

```
src/bd_freecad_library/standards/<family>.py            # parametric function
src/bd_freecad_library/standards/<family>_manifest.py   # validation manifest
tests/test_<family>.py                                  # uses validate_fixture harness
docs/standards/<family>/README.md                       # rationale, params, examples
docs/standards/<family>/DIMENSIONS.md                   # full dimension table
```

`<family>` is a slug like `iso4762` or `en_square_hollow`.

A scaffolding script is planned (issue TBD); for now copy ISO 4762 as
the template.

### 3. IMPLEMENT — write the parametric function

The function:

- Takes a few well-named parameters (e.g. `thread`, `length`).
- Validates inputs with helpful `ValueError`s.
- Looks up dimensions from a private `_TABLE: dict[str, Dims]`
  populated from the standard.
- Returns a `build123d.Part` with a clearly-documented origin
  convention.

Approach hierarchy when the geometry is unclear:

1. **First reach:** the standard's dimension table. Code from spec.
2. **Second reach:** if the standard is ambiguous on a detail (a head
   fillet radius, a chamfer angle), reference the FreeCAD fixture for
   the resolved value — `python -m fcstd2b123d <fixture>` to see how
   it's modelled.
3. **Third reach (rare):** translate a fixture, scaffold from the
   output, then hand-parameterise. Useful when the geometry has
   complex topology (multi-loop sketches, draft angles) that's
   tedious to write from scratch.

What we **don't** do: ship the raw translator output as a "parametric
module." That's a script that produces one variant, not a parametric
function. Always hand-parameterise.

### 4. VALIDATE — the load-bearing piece

Add the manifest:

```python
# src/bd_freecad_library/standards/iso4762_manifest.py
FIXTURES: list[tuple[str, dict]] = [
    ("Screw_M5x20_ISO4762_8_8_A2K.FCStd", {"thread": "M5", "length": 20}),
    # ... one row per fixture in the corpus for this family
]
```

Add the test:

```python
# tests/test_<family>.py
import pytest
from bd_freecad_library.standards.iso4762 import iso4762_cap_screw
from bd_freecad_library.standards.iso4762_manifest import FIXTURES
from tests._validation import validate_fixture

@pytest.mark.parametrize("fixture_name,params", FIXTURES, ids=[f[0] for f in FIXTURES])
def test_iso4762_matches_freecad_fixture(fixture_name, params):
    validate_fixture(iso4762_cap_screw, fixture_name, params)
```

The harness compares bbox extents by default. Per-family you can opt
into volume comparison by passing `volume_tol_rel=0.01` if your
modelling is geometrically exact (no thread approximation, etc.).

Tests skip cleanly when `FCSTD2B123D_FREECAD_PYTHON` is unset — so
non-FreeCAD developers and CI fast lanes don't see failures.

### 5. SHIP — PR

A complete PR for a new family includes:

- `src/.../<family>.py` (parametric function)
- `src/.../<family>_manifest.py` (every FreeCAD fixture covered)
- `tests/test_<family>.py` (uses the harness)
- `docs/standards/<family>/README.md` (params, rationale, worked example)
- `docs/standards/<family>/DIMENSIONS.md` (full dimension table)
- Pure-Python tests pass with no env set
- FreeCAD-side validation passes with `FCSTD2B123D_FREECAD_PYTHON` set

## How the validation harness works

`tests/_validation.py` exposes `validate_fixture(parametric_fn,
fixture_name, params, **opts)`. For each invocation it:

1. Locates the fixture under `fcstd2b123d/tests/fixtures/` (path
   from `$FCSTD2B123D_REPO`, default `../fcd2b123d/`).
2. Translates via `python -m fcstd2b123d <fixture>` in a subprocess
   (FreeCAD env from `$FCSTD2B123D_FREECAD_PYTHON`).
3. `exec()`s the emitted build123d source to capture `result`.
4. Calls `parametric_fn(**params)`.
5. Compares **sorted bbox extents** (rotation-invariant) within
   `bbox_tol_abs` (default 0.5 mm).
6. Optionally compares volume within `volume_tol_rel` (default
   `None` = skip; opt-in per family).

When validation fails, the assertion message includes the fixture
name, the metric that drifted, and both sides' values.

## Environment

| Variable | What | Default |
|---|---|---|
| `FCSTD2B123D_REPO` | Path to fcstd2b123d checkout | `../fcd2b123d/` |
| `FCSTD2B123D_FREECAD_PYTHON` | Python with FreeCAD installed | (unset → tests skip) |
| `FCSTD2B123D_FREECAD_PYTHONPATH` | Extra PYTHONPATH for FreeCAD | (empty) |

Locally (this repo's typical layout):

```bash
export FCSTD2B123D_FREECAD_PYTHON=$(realpath ../fcd2b123d/.conda/envs/freecad/bin/python)
export FCSTD2B123D_FREECAD_PYTHONPATH=$(realpath ../fcd2b123d/.conda/envs/freecad/lib)
pytest
```
