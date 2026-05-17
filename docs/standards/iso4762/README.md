# ISO 4762 — Socket head cap screws

Parametric build123d implementation of the [ISO 4762](https://www.iso.org/standard/34460.html)
socket head cap screw family (equivalent to DIN 912).

## What

Cylindrical-head fastener with a hexagonal socket recess in the head top
and a single threaded shaft. Tightened with a hex key. The most common
machine screw in modern mechanical design.

## Standard reference

**ISO 4762:2004** — *Hexagon socket head cap screws*.

Dimensional data cross-referenced against:
- The FreeCAD Parts Library (38 variants of
  `Screw_M{size}x{length}_ISO4762_8_8_A2K.FCStd` in `Fasteners/`).
- The `fcstd2b123d` translator's regression corpus
  (`tests/fixtures/tier3_corpus_c/`), where all 38 variants translate
  cleanly to build123d Python.

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `thread` | `str` | `"M5"` | Thread designation. One of `M3, M4, M5, M6, M8, M10, M12, M16, M20, M24, M30, M36`. |
| `length` | `float` | `20.0` | Shaft length under the head, in millimetres. Accepts any positive value (ISO 4762 standardises discrete steps, but for assembly modelling we accept arbitrary lengths). |

Returns: `build123d.Part`. Origin at the head/shaft junction; +Z runs
along the shaft away from the head.

## Worked example

```python
from bd_freecad_library.standards.iso4762 import iso4762_cap_screw

# An M5×20 cap screw — the default
screw = iso4762_cap_screw()

# Specific variant
m12_x_50 = iso4762_cap_screw(thread="M12", length=50)

# Position into an assembly: head at origin, shaft along +Z
from build123d import Pos, Rot
mounted = Pos(10, 10, 0) * Rot(X=180) * iso4762_cap_screw(thread="M6", length=15)
```

## Why these defaults

**`thread="M5"`** is the modal thread size in the FreeCAD library's
Fasteners corpus (~6 of 38 ISO 4762 variants are M5) and a sensible
"if you don't know, this works" default for hobbyist/maker-scale work.

**`length=20`** sits in the middle of the common-length range (the
library corpus spans M3×5 to M36×220); 20 mm avoids both the very-short
"head only" pathology and the very-long "thread bending" edge case.

## What's modelled vs not

**Modelled:**
- Cylindrical head with correct outer diameter and height per ISO 4762.
- Hex socket on the head top with correct across-flats and depth.
- Shaft of the nominal thread diameter and given length.

**Not modelled (v0.1):**
- The thread helix. The shaft is a smooth cylinder of the nominal
  thread diameter — geometrically correct for clearance and assembly
  checks, but the helix profile itself is absent. This matches
  `bd_warehouse` practice.
- Head-shaft fillet (currently a sharp transition).
- Drive marks / manufacturer stamping on the head top.

Real helix threading is planned for v0.2 — see the project's open
issues. It gates on `fcstd2b123d#33` (Part::Helix translation support).

## Validated against

| FreeCAD file | Thread | Length | Notes |
|---|---|---|---|
| `Screw_M3x12_ISO4762_8_8_A2K.FCStd` | M3 | 12 mm | corpus tier3_c |
| `Screw_M5x12_ISO4762_8_8_A2K.FCStd` | M5 | 12 mm | corpus tier3_c |
| `Screw_M6x45_ISO4762_8_8_A2K.FCStd` | M6 | 45 mm | corpus tier3_c |
| `Screw_M8x160_ISO4762_8_8_A2K.FCStd` | M8 | 160 mm | corpus tier3_c |
| `Screw_M24x55_ISO4762_8_8_A2K.FCStd` | M24 | 55 mm | corpus tier3_c |
| `Screw_M36x110_ISO4762_8_8_A2K.FCStd` | M36 | 110 mm | corpus tier3_c |

…and 32 other size/length variants. All translate cleanly through
`fcstd2b123d` (volume / centre-of-mass / principal moment of inertia
within 1e-6 relative tolerance vs FreeCAD's evaluated BRep).

See `DIMENSIONS.md` for the full per-thread-size table.
