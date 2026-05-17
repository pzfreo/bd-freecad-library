# ISO 7093 / DIN 9021 dimension table

All values from ISO 7093-1:2000 and DIN 9021. Dimensions in
millimetres. Values marked **(FC)** follow the FreeCAD Parts Library
where it diverges from ISO 7093 Part 1.

| Thread | d1 (inner Ø) | d2 (outer Ø) | h (thickness) | Source |
|---|---:|---:|---:|---|
| M3   |  3.2 |   9 | 0.8 | ISO 7093 |
| M3.5 |  3.7 |  11 | 0.8 | ISO 7093 |
| M4   |  4.3 |  12 | 1.0 | ISO 7093 |
| M5   |  5.3 |  15 | 1.2 | ISO 7093 / FC ✓ |
| M6   |  6.4 |  18 | 1.6 | ISO 7093 |
| M8   |  8.4 |  24 | 2.0 | ISO 7093 |
| M10  | 10.5 |  30 | 2.5 | ISO 7093 / FC ✓ |
| M12  | 13.0 |  37 | 3.0 | ISO 7093 |
| M14  | 15.0 |  44 | 3.0 | ISO 7093 |
| M16  | 17.0 |  50 | 3.0 | ISO 7093 |
| M18  | 19.0 |  56 | 4.0 | ISO 7093 |
| M20  | 21.0 |  60 | 4.0 | ISO 7093 |
| M22  | 23.0 |  66 | 5.0 | ISO 7093 |
| **M24** | **28.0** |  72 | 5.0 | **FC** (ISO 7093 Part 1: d1=25) |
| M27  | 28.0 |  85 | 6.0 | ISO 7093 |
| **M30** | **33.0** |  92 | 6.0 | **FC** (ISO 7093 Part 1: d1=31) |
| M33  | 34.0 | 105 | 6.0 | ISO 7093 |
| M36  | 37.0 | 110 | 8.0 | ISO 7093 |

## Column glossary

- **d1** — inner (hole) diameter.
- **d2** — outer diameter.
- **h** — washer thickness.

## On the M24 / M30 discrepancy

ISO 7093:2000 Part 1 specifies d1=25 (M24) and d1=31 (M30) — values
slightly larger than the bolt's clearance hole. The FreeCAD Parts
Library models these with d1=28 (M24) and d1=33 (M30) — closer to
DIN 9021 / ISO 7093 Part 2 dimensions. Reasons documented in the
parts library's own history vary by source; for this implementation
we follow what the FreeCAD library models because that's the
geometric baseline our tests validate against.

If you need strict ISO 7093 Part 1 dimensions, file an issue and
we'll add a separate `iso7093_part1_plain_washer` function (or accept
a `strict_iso=True` flag), driven by fixtures of that exact spec.

## Source

- ISO 7093-1:2000 *Plain washers — Large series — Part 1: Product
  grade A*.
- DIN 9021 *Plain washers — Outside diameter approximately 3 × inside
  diameter*.

Cross-referenced against the FreeCAD Parts Library
(`Fasteners/Washer/ISO7093DIN9021_*FlatWasher.FCStd`).
