# ISO 7093 — Plain washers, large series

Parametric build123d implementation of the [ISO 7093](https://www.iso.org/standard/22923.html)
*Plain washers — Large series* family (equivalent to DIN 9021).

## What

A flat annular washer with a larger outer diameter than the standard
ISO 7089 series. Distributes bolt load over a wider bearing area,
typical in softer materials or where the through-hole is oversized.

## Standard reference

- **ISO 7093-1:2000** — Plain washers, large series, Part 1: Product
  grade A.
- **DIN 9021** — German equivalent (predates ISO 7093). The FreeCAD
  Parts Library fixtures bridge both standards in their filenames
  (`ISO7093DIN9021_*FlatWasher.FCStd`).

For most sizes the two standards agree to the millimetre. The
FreeCAD library's M24 (`d1=28`) and M30 (`d1=33`) values differ
from ISO 7093 Part 1 (`d1=25` and `d1=31`); we follow the FreeCAD
library values because that's what we validate against.

## Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `thread` | `str` | `"M5"` | Bolt size. `M3` through `M36`. |

Returns: `build123d.Part`. Origin at the washer centre on the bottom
face; +Z runs along the bolt axis.

## Worked example

```python
from bd_freecad_library.standards.iso7093 import iso7093_plain_washer

# M5 washer — the default
w = iso7093_plain_washer()

# Specific variant
w_m12 = iso7093_plain_washer(thread="M12")
```

## Why this default

`thread="M5"` is the modal small-machine-screw size. It's also the
canonical fixture in the FreeCAD library that we use for regression
validation (`ISO7093DIN9021_M5FlatWasher.FCStd`).

## What's modelled

The annulus `Circle(d2/2) − Circle(d1/2)` extruded along +Z by the
washer thickness. Geometrically exact — no approximations.

Edge chamfers / breaks present on real fabricated washers are **not**
modelled. ISO 7093 specifies a "burred-edge-free" finish but no
chamfer dimensions; the FreeCAD library models them as sharp-edged
too, so our match is exact.

## Validated against (4 FreeCAD fixtures)

| Fixture | Thread | Outer Ø | Inner Ø | Thickness | Result |
|---|---|---:|---:|---:|---|
| `ISO7093DIN9021_M5FlatWasher.FCStd` | M5 | 15 | 5.3 | 1.2 | ✓ vol/bbox match |
| `ISO7093DIN9021_M10FlatWasher.FCStd` | M10 | 30 | 10.5 | 2.5 | ✓ |
| `ISO7093DIN9021_M24FlatWasher.FCStd` | M24 | 72 | 28 | 5 | ✓ |
| `ISO7093DIN9021_M30FlatWasher.FCStd` | M30 | 92 | 33 | 6 | ✓ |

Volume match within 0.1% (the parametric form is geometrically
identical to the fixture's `extrude(Circle(d2/2) − Circle(d1/2),
amount=h)` translation).

See `DIMENSIONS.md` for the full dimension table.
