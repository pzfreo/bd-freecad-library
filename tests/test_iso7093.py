"""ISO 7093 — geometric validation against FreeCAD source fixtures.

The harness in :mod:`tests._validation` translates each fixture in
:mod:`iso7093_manifest` via ``fcstd2b123d``, exec's the emit, and
compares ``iso7093_plain_washer(**params).bounding_box()`` against
the FreeCAD-evaluated geometry.

For washers the FreeCAD fixture is a complete annulus extrude — both
bbox **and** volume are tightly comparable, so we enable both checks
(unlike screw families that defer volume until thread modelling is
exact).

Pure-Python sanity checks (no FreeCAD env required) live below the
fixture-validation block.
"""

from __future__ import annotations

import math

import pytest

from bd_freecad_library.standards.iso7093 import iso7093_plain_washer
from bd_freecad_library.standards.iso7093_manifest import FIXTURES
from tests._validation import validate_fixture


# ---------------------------------------------------------------------------
# Fixture-validation suite — one parametrised case per manifest entry
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name,params",
    FIXTURES,
    ids=[f[0] for f in FIXTURES],
)
def test_iso7093_matches_freecad_fixture(fixture_name: str, params: dict) -> None:
    """Bbox-extent AND volume comparison against every ISO 7093 fixture.

    Volume tolerance is tight (0.1%) — the parametric form is
    geometrically exact for a plain washer.
    """
    validate_fixture(
        iso7093_plain_washer, fixture_name, params,
        volume_tol_rel=0.001,
    )


# ---------------------------------------------------------------------------
# Pure-Python sanity checks (no FreeCAD env required)
# ---------------------------------------------------------------------------


def test_iso7093_default_thread_is_m5() -> None:
    """Default arguments produce an M5 washer."""
    default = iso7093_plain_washer()
    m5 = iso7093_plain_washer(thread="M5")
    assert math.isclose(default.volume, m5.volume, rel_tol=1e-9)


def test_iso7093_rejects_unsupported_thread() -> None:
    """Unsupported thread designation raises a helpful ValueError."""
    with pytest.raises(ValueError, match="unsupported thread"):
        iso7093_plain_washer(thread="M7")


def test_iso7093_volume_matches_analytical_annulus() -> None:
    """The washer volume should equal the analytical annulus * thickness."""
    # M10: d1=10.5, d2=30, h=2.5
    expected = math.pi * ((30 / 2) ** 2 - (10.5 / 2) ** 2) * 2.5
    actual = iso7093_plain_washer(thread="M10").volume
    assert math.isclose(actual, expected, rel_tol=1e-6), (
        f"M10 washer volume {actual:.3f} != analytical {expected:.3f}"
    )


def test_iso7093_bigger_thread_has_bigger_outer_diameter() -> None:
    """Outer diameter monotonically grows with thread size."""
    m5 = iso7093_plain_washer(thread="M5").bounding_box()
    m24 = iso7093_plain_washer(thread="M24").bounding_box()
    assert m24.size.X > m5.size.X
    assert m24.size.Y > m5.size.Y
