"""EN 10058 — geometric validation against FreeCAD source fixtures.

The harness translates each of 22 EN 10058 flat-bar fixtures via
``fcstd2b123d``, exec's the emitted source, and compares
``en_10058_flat_bar(**params).bounding_box() / .volume`` against the
FreeCAD-evaluated geometry.

A flat bar is geometrically the simplest structural profile — a
rectangle extrude — so we enable **both** bbox and volume comparison
with tight tolerance.

Pure-Python sanity checks (no FreeCAD env required) live below the
fixture-validation block.
"""

from __future__ import annotations

import pytest

from bd_freecad_library.standards.en_10058 import en_10058_flat_bar
from bd_freecad_library.standards.en_10058_manifest import FIXTURES
from tests._validation import validate_fixture


# ---------------------------------------------------------------------------
# Fixture-validation suite — one parametrised case per manifest entry
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name,params",
    FIXTURES,
    ids=[f[0] for f in FIXTURES],
)
def test_en_10058_matches_freecad_fixture(fixture_name: str, params: dict) -> None:
    """Bbox-extent AND volume comparison against every EN 10058 fixture.

    Volume tolerance is tight (0.01%) — the parametric form is
    geometrically exact for a rectangular extrude.
    """
    validate_fixture(
        en_10058_flat_bar, fixture_name, params,
        volume_tol_rel=0.0001,
    )


# ---------------------------------------------------------------------------
# Pure-Python sanity checks (no FreeCAD env required)
# ---------------------------------------------------------------------------


def test_en_10058_volume_is_width_times_thickness_times_length() -> None:
    """A flat bar is a pure box extrude — volume is the analytical product."""
    bar = en_10058_flat_bar(width=60, thickness=4, length=100)
    assert abs(bar.volume - 60 * 4 * 100) < 1e-6, bar.volume


def test_en_10058_rejects_nonpositive_dimensions() -> None:
    """Zero or negative width / thickness / length raises ValueError."""
    for kwargs in (
        {"width": 0,  "thickness": 5, "length": 50},
        {"width": -5, "thickness": 5, "length": 50},
        {"width": 5,  "thickness": 0, "length": 50},
        {"width": 5,  "thickness": -1, "length": 50},
        {"width": 5,  "thickness": 5, "length": 0},
        {"width": 5,  "thickness": 5, "length": -10},
    ):
        with pytest.raises(ValueError, match="must all be positive"):
            en_10058_flat_bar(**kwargs)


def test_en_10058_bbox_matches_dimensions() -> None:
    """The bbox extents should be exactly (width, thickness, length) up
    to axis ordering."""
    bar = en_10058_flat_bar(width=100, thickness=10, length=200)
    b = bar.bounding_box()
    extents = sorted([b.size.X, b.size.Y, b.size.Z])
    assert extents == [10.0, 100.0, 200.0]
