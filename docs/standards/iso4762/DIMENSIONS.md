# ISO 4762 dimension table

Values for the ISO 4762:2004 socket head cap screw family. All
dimensions in millimetres.

| Thread | d (thread Ø) | dk (head Ø max) | k (head height max) | s (socket A/F) | t (socket depth min) |
|---|---:|---:|---:|---:|---:|
| M3  |  3.0 |  5.5 |  3.0 |  2.5 |  1.3 |
| M4  |  4.0 |  7.0 |  4.0 |  3.0 |  2.0 |
| M5  |  5.0 |  8.5 |  5.0 |  4.0 |  2.5 |
| M6  |  6.0 | 10.0 |  6.0 |  5.0 |  3.0 |
| M8  |  8.0 | 13.0 |  8.0 |  6.0 |  4.0 |
| M10 | 10.0 | 16.0 | 10.0 |  8.0 |  5.0 |
| M12 | 12.0 | 18.0 | 12.0 | 10.0 |  6.0 |
| M16 | 16.0 | 24.0 | 16.0 | 14.0 |  8.0 |
| M20 | 20.0 | 30.0 | 20.0 | 17.0 | 10.0 |
| M24 | 24.0 | 36.0 | 24.0 | 19.0 | 12.0 |
| M30 | 30.0 | 45.0 | 30.0 | 22.0 | 15.5 |
| M36 | 36.0 | 54.0 | 36.0 | 27.0 | 19.0 |

## Column glossary

- **d** — nominal thread diameter (the screw's "size").
- **dk** — head outer diameter, maximum permitted value.
- **k** — head height (along the screw axis), maximum permitted value.
- **s** — hex socket across-flats dimension (the hex key size).
- **t** — minimum hex socket depth (axial).

## Source

Values from ISO 4762:2004 *Hexagon socket head cap screws*.

Cross-referenced against the FreeCAD Parts Library
(`Fasteners/Screw_*_ISO4762_8_8_A2K.FCStd`), which provided 38 fixture
variants for regression testing.

## Out-of-scope sizes

ISO 4762 also defines M1.6, M2, M2.5, M14, M22, and M27. These are
geometrically valid but currently absent from the FreeCAD Parts
Library — and therefore aren't in our cross-reference set. If you need
them, they can be added with confidence; the dimension table is in the
standard.
