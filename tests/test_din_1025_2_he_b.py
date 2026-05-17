"""DIN 1025-2 HE-B — geometric validation against FreeCAD source fixtures.

Like en_10058, the implementation is **generated** by
``fcstd2b123d.family_extract`` from ``families/din_1025_2_he_b.yaml``.

Three fixtures in the corpus (HE-B 280, 320, 900). For each, the
generated ``DIN1025HEBProfile(h, b, tw, tf, r, length)`` instantiated
with those parameters should produce geometry matching the FreeCAD
source.

Pure-Python sanity checks live below the fixture-validation block.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from bd_freecad_library.standards.din_1025_2_he_b import DIN1025HEBProfile
from tests._validation import validate_fixture


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "families" / "din_1025_2_he_b.yaml"


def _load_manifest_fixtures() -> list[tuple[str, dict]]:
    """Discover HE-B fixtures via the YAML manifest."""
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
# Fixture-validation suite — one parametrised case per HE-B fixture
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name,params",
    _FIXTURE_DATA or [("__placeholder__", {})],
    ids=[f[0] for f in _FIXTURE_DATA] or ["__no_fixtures__"],
)
def test_he_b_matches_freecad_fixture(fixture_name: str, params: dict) -> None:
    """Bbox-extent comparison against every HE-B fixture.

    For HE-B the cross-section has rounded fillets between web and
    flange; the bbox is dominated by (b, h) so we use bbox validation.
    Volume is also tight (cross-section area × length, no thread
    approximations).
    """
    if fixture_name == "__placeholder__":
        pytest.skip("fcstd2b123d corpus not available; cannot discover fixtures")
    params = {**params}
    params.setdefault("length", 50)
    validate_fixture(
        DIN1025HEBProfile, fixture_name, params,
        volume_tol_rel=0.001,
    )


# ---------------------------------------------------------------------------
# Pure-Python sanity checks
# ---------------------------------------------------------------------------


def test_he_b_default_instantiation_succeeds() -> None:
    """Defaults are the first fixture's dimensions; constructor works."""
    beam = DIN1025HEBProfile()
    assert abs(beam.volume) > 0


def test_he_b_280_bbox_matches_size() -> None:
    """HE-B 280 has h = b = 280 (square outer envelope)."""
    beam = DIN1025HEBProfile(h=280, b=280, tw=10.5, tf=18, r=24, length=100)
    bbox = beam.bounding_box()
    extents = sorted([bbox.size.X, bbox.size.Y, bbox.size.Z])
    assert extents == pytest.approx([100.0, 280.0, 280.0], abs=1e-6)


def test_he_b_320_bbox_matches_size() -> None:
    """HE-B 320+ has b=300, h=320 (non-square)."""
    beam = DIN1025HEBProfile(h=320, b=300, tw=11.5, tf=20.5, r=27, length=100)
    bbox = beam.bounding_box()
    extents = sorted([bbox.size.X, bbox.size.Y, bbox.size.Z])
    assert extents == pytest.approx([100.0, 300.0, 320.0], abs=1e-6)


def test_he_b_volume_scales_linearly_with_length() -> None:
    """Doubling the length doubles the volume."""
    short = DIN1025HEBProfile(h=280, b=280, tw=10.5, tf=18, r=24, length=50)
    long = DIN1025HEBProfile(h=280, b=280, tw=10.5, tf=18, r=24, length=100)
    assert abs(long.volume - 2 * short.volume) < 1e-6


def test_he_b_is_a_basepartobject() -> None:
    from build123d import BasePartObject
    assert issubclass(DIN1025HEBProfile, BasePartObject)
