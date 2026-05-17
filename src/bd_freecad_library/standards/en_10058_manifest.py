"""Validation manifest for EN 10058 flat steel bars.

Each entry pairs a FreeCAD fixture filename with the parametric call.
The harness in :mod:`tests._validation` translates each fixture and
compares against ``en_10058_flat_bar(**params)``.

The FreeCAD library models each fixture at a 50 mm length (a modelling
convenience — EN 10058 doesn't fix length).
"""

from __future__ import annotations

# 22 EN 10058 fixtures spanning a wide range of (width, thickness)
# combinations. All translate cleanly through fcstd2b123d.
# Length is 50 mm in every fixture (FreeCAD library convention).
FIXTURES: list[tuple[str, dict]] = [
    ("Flat_Bar_20x12_EN10058_S235JR.FCStd",  {"width": 20,  "thickness": 12, "length": 50}),
    ("Flat_Bar_25x20_EN10058_S235JR.FCStd",  {"width": 25,  "thickness": 20, "length": 50}),
    ("Flat_Bar_30x5_EN10058_S235JR.FCStd",   {"width": 30,  "thickness": 5,  "length": 50}),
    ("Flat_Bar_30x8_EN10058_S235JR.FCStd",   {"width": 30,  "thickness": 8,  "length": 50}),
    ("Flat_Bar_50x8_EN10058_S235JR.FCStd",   {"width": 50,  "thickness": 8,  "length": 50}),
    ("Flat_Bar_55x10_EN10058_S235JR.FCStd",  {"width": 55,  "thickness": 10, "length": 50}),
    ("Flat_Bar_60x4_EN10058_S235JR.FCStd",   {"width": 60,  "thickness": 4,  "length": 50}),
    ("Flat_Bar_60x25_EN10058_S235JR.FCStd",  {"width": 60,  "thickness": 25, "length": 50}),
    ("Flat_Bar_70x5_EN10058_S235JR.FCStd",   {"width": 70,  "thickness": 5,  "length": 50}),
    ("Flat_Bar_70x30_EN10058_S235JR.FCStd",  {"width": 70,  "thickness": 30, "length": 50}),
    ("Flat_Bar_70x50_EN10058_S235JR.FCStd",  {"width": 70,  "thickness": 50, "length": 50}),
    ("Flat_Bar_80x5_EN10058_S235JR.FCStd",   {"width": 80,  "thickness": 5,  "length": 50}),
    ("Flat_Bar_90x8_EN10058_S235JR.FCStd",   {"width": 90,  "thickness": 8,  "length": 50}),
    ("Flat_Bar_100x6_EN10058_S235JR.FCStd",  {"width": 100, "thickness": 6,  "length": 50}),
    ("Flat_Bar_110x8_EN10058_S235JR.FCStd",  {"width": 110, "thickness": 8,  "length": 50}),
    ("Flat_Bar_110x25_EN10058_S235JR.FCStd", {"width": 110, "thickness": 25, "length": 50}),
    ("Flat_Bar_120x20_EN10058_S235JR.FCStd", {"width": 120, "thickness": 20, "length": 50}),
    ("Flat_Bar_120x60_EN10058_S235JR.FCStd", {"width": 120, "thickness": 60, "length": 50}),
    ("Flat_Bar_140x10_EN10058_S235JR.FCStd", {"width": 140, "thickness": 10, "length": 50}),
    ("Flat_Bar_150x8_EN10058_S235JR.FCStd",  {"width": 150, "thickness": 8,  "length": 50}),
    ("Flat_Bar_150x40_EN10058_S235JR.FCStd", {"width": 150, "thickness": 40, "length": 50}),
    ("Flat_Bar_150x50_EN10058_S235JR.FCStd", {"width": 150, "thickness": 50, "length": 50}),
]
