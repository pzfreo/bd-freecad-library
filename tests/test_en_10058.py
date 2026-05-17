"""EN 10058 — geometric validation against FreeCAD source fixtures.

Since #8 the implementation in ``src/bd_freecad_library/standards/
en_10058.py`` is **generated** by ``fcstd2b123d.family_extract``
from ``families/en_10058.yaml``. The Python file is committed so
library consumers don't need ``fcstd2b123d`` at install time.

This test loads the YAML manifest, discovers the matching fixtures
in the ``fcstd2b123d`` corpus, and validates that instantiating
``EN10058FlatBar(**params)`` produces geometry matching each fixture.

Pure-Python sanity checks (no FreeCAD env required) live below the
fixture-validation block.
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import pytest

from bd_freecad_library.standards.en_10058 import EN10058FlatBar
from tests._validation import validate_fixture


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "families" / "en_10058.yaml"


def _load_manifest_fixtures() -> list[tuple[str, dict]]:
    """Discover the fixtures via the YAML manifest using ``fcstd2b123d``'s
    family-extraction helpers.

    Skips cleanly when fcstd2b123d isn't importable or the FreeCAD
    fixtures root can't be located.
    """
    fcstd2b123d_repo = Path(
        os.environ.get(
            "FCSTD2B123D_REPO",
            str(REPO_ROOT.parent / "fcd2b123d"),
        )
    )
    if not (fcstd2b123d_repo / "src" / "fcstd2b123d").is_dir():
        return []
    sys.path.insert(0, str(fcstd2b123d_repo / "src"))
    try:
        from fcstd2b123d.family import load_manifest
        from fcstd2b123d.family_extract import discover_fixtures
    except ImportError:
        return []

    manifest = load_manifest(MANIFEST_PATH)
    records = discover_fixtures(manifest, fcstd2b123d_repo / "tests" / "fixtures")
    return [
        (rec.path.name, {k: float(v) if isinstance(v, (int, float)) else v
                          for k, v in rec.params.items()})
        for rec in records
    ]


_FIXTURE_DATA = _load_manifest_fixtures()


# ---------------------------------------------------------------------------
# Fixture-validation suite — one parametrised case per manifest fixture
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name,params",
    _FIXTURE_DATA or [("__placeholder__", {})],
    ids=[f[0] for f in _FIXTURE_DATA] or ["__no_fixtures__"],
)
def test_en_10058_matches_freecad_fixture(fixture_name: str, params: dict) -> None:
    """Bbox-extent AND volume comparison against every EN 10058 fixture
    discovered via the YAML manifest.

    Volume tolerance is tight (0.01%) — the generated parametric class
    is geometrically exact for a rectangular extrude.
    """
    if fixture_name == "__placeholder__":
        pytest.skip("fcstd2b123d corpus not available; cannot discover fixtures")
    # extrude_amount params (e.g. ``length``) aren't pre-discoverable from
    # the manifest's filename pattern — fill in the canonical 50 mm here.
    params = {**params}
    params.setdefault("length", 50)
    validate_fixture(
        EN10058FlatBar, fixture_name, params,
        volume_tol_rel=0.0001,
    )


# ---------------------------------------------------------------------------
# Pure-Python sanity checks (no FreeCAD env required)
# ---------------------------------------------------------------------------


def test_en_10058_volume_is_width_times_thickness_times_length() -> None:
    """A flat bar is a pure box extrude — volume is the analytical product."""
    bar = EN10058FlatBar(width=60, thickness=4, length=100)
    assert abs(bar.volume - 60 * 4 * 100) < 1e-6, bar.volume


def test_en_10058_bbox_matches_dimensions() -> None:
    """The bbox extents should be exactly (width, thickness, length) up
    to axis ordering."""
    bar = EN10058FlatBar(width=100, thickness=10, length=200)
    b = bar.bounding_box()
    extents = sorted([b.size.X, b.size.Y, b.size.Z])
    assert extents == [10.0, 100.0, 200.0]


def test_en_10058_default_instantiation_succeeds() -> None:
    """Constructing without args uses the generated defaults (the first
    fixture's parameters)."""
    bar = EN10058FlatBar()
    assert abs(bar.volume) > 0


def test_en_10058_is_a_basepartobject() -> None:
    """The generated class subclasses ``BasePartObject`` so it behaves
    like other build123d / bd_warehouse parts (rotation, align, mode)."""
    from build123d import BasePartObject
    assert issubclass(EN10058FlatBar, BasePartObject)
