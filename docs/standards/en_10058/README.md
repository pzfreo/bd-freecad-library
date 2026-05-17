# EN 10058 — Hot-rolled flat steel bars

Parametric build123d implementation of [EN 10058:2018](https://www.en-standard.eu/csn-en-10058-hot-rolled-flat-steel-bars-for-general-purposes-dimensions-and-tolerances-on-shape-and-dimensions/)
*Hot rolled flat steel bars for general purposes — Dimensions and
tolerances on shape and dimensions*.

## What

A rectangular cross-section of (width × thickness) extruded along the
bar's longitudinal axis. The simplest structural steel profile —
common in fabricated welded structures, machine bases, fixturing.

## Why it's in this library

EN 10058 falls under category 2a of the project's
[strategy doc](https://github.com/pzfreo/fcd2b123d/blob/main/docs/strategy/derivative-libraries.md):
**structural steel profiles that bd_warehouse doesn't cover today**.
`bd_warehouse` focuses on fasteners/bearings/chains; structural
profiles are the obvious adjacent gap and the FreeCAD library has
22 EN 10058 fixtures we can validate against.

## Standard reference

**EN 10058:2018** — *Hot rolled flat steel bars for general purposes*.

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `width` | `float` | — | Larger cross-section dimension, mm |
| `thickness` | `float` | — | Smaller cross-section dimension, mm |
| `length` | `float` | `50.0` | Bar length along longitudinal axis, mm |

Returns: `build123d.Part`. Origin at the centroid of the bottom face;
+Z runs along the bar's length.

## Standard sizes

EN 10058 specifies discrete preferred dimensions:

- **Widths** (mm): 10, 12, 15, 18, 20, 25, 30, 40, 50, 60, 70, 80, 90,
  100, 110, 120, 130, 140, 150, 160, 180, 200.
- **Thicknesses** (mm): 4, 5, 6, 8, 10, 12, 15, 18, 20, 25, 30, 35,
  40, 50.

The parametric function accepts any positive (width, thickness, length)
to support design-stage modelling. Standard-only enforcement would
needlessly block engineers from defaulting to "close to standard."

## Worked example

```python
from bd_freecad_library.standards.en_10058 import en_10058_flat_bar

# A 60 × 4 × 100 mm flat bar
bar = en_10058_flat_bar(width=60, thickness=4, length=100)
print(bar.volume)  # 24000.0
```

## What's modelled

A pure rectangular extrude — geometrically exact. No rolled-edge
radius, no fillet on the bar ends (real EN 10058 bars have small
edge fillets from the rolling process; the FreeCAD library models
them as sharp-edged too, so the match is exact).

## Validated against (22 FreeCAD fixtures)

| (width × thickness) | Sources |
|---|---|
| 20×12, 25×20, 30×5, 30×8, 50×8, 55×10 | tier3_corpus, tier3_corpus_b, sample_813 |
| 60×4, 60×25, 70×5, 70×30, 70×50, 80×5 | sample_2026 |
| 90×8, 100×6, 110×8, 110×25, 120×20, 120×60 | sample_813, sample_2026 |
| 140×10, 150×8, 150×40, 150×50 | various |

All 22 fixtures validate within **0.01% volume tolerance** (the
parametric form is geometrically identical to the fixture).
