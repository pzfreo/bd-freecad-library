"""Validation manifest for ISO 7093 plain washers.

Each entry pairs a FreeCAD fixture filename with the parametric call
that should produce equivalent geometry. The harness in
:mod:`tests._validation` translates each fixture, exec's the emit, and
compares against ``iso7093_plain_washer(**params)``.

Fixtures live in ``fcstd2b123d/tests/fixtures/`` (located via the
``FCSTD2B123D_REPO`` env var; default ``../fcd2b123d/``).
"""

from __future__ import annotations

# Four ISO 7093 fixtures present in the fcstd2b123d corpus. Each
# translates cleanly to a complete-washer Part (annulus extrude).
FIXTURES: list[tuple[str, dict]] = [
    ("ISO7093DIN9021_M5FlatWasher.FCStd",  {"thread": "M5"}),
    ("ISO7093DIN9021_M10FlatWasher.FCStd", {"thread": "M10"}),
    ("ISO7093DIN9021_M24FlatWasher.FCStd", {"thread": "M24"}),
    ("ISO7093DIN9021_M30FlatWasher.FCStd", {"thread": "M30"}),
]
