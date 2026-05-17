"""Smoke + dimension-sanity tests for the ISO 4762 cap-screw module.

Real geometric regression vs the FreeCAD Parts Library fixtures lives in
``fcstd2b123d`` (38 ``Screw_M*_ISO4762_8_8_A2K.FCStd`` fixtures, all
translating cleanly). The tests here are local sanity checks — they
verify the parametric function builds something with the right shape and
respects its parameters.
"""

from __future__ import annotations

import math

import pytest

from bd_freecad_library.standards.iso4762 import iso4762_cap_screw


# ---------------------------------------------------------------------------
# Basic exec / construction
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "thread", ["M3", "M4", "M5", "M6", "M8", "M10", "M12", "M16", "M20", "M24", "M30", "M36"]
)
def test_iso4762_builds_for_every_supported_thread(thread: str) -> None:
    """Every thread size in the table should produce a non-degenerate part."""
    screw = iso4762_cap_screw(thread=thread, length=20.0)
    assert screw.volume > 0


def test_iso4762_default_thread_is_m5() -> None:
    """Default arguments produce an M5×20 cap screw."""
    default = iso4762_cap_screw()
    m5_20 = iso4762_cap_screw(thread="M5", length=20.0)
    assert math.isclose(default.volume, m5_20.volume, rel_tol=1e-9)


def test_iso4762_rejects_unsupported_thread() -> None:
    """Unsupported thread designation raises a helpful ValueError."""
    with pytest.raises(ValueError, match="unsupported thread"):
        iso4762_cap_screw(thread="M7", length=10.0)


def test_iso4762_rejects_nonpositive_length() -> None:
    """Zero and negative lengths are rejected with a helpful ValueError."""
    for bad in [0, -5, -0.001]:
        with pytest.raises(ValueError, match="length must be positive"):
            iso4762_cap_screw(thread="M5", length=bad)


# ---------------------------------------------------------------------------
# Parameter responsiveness
# ---------------------------------------------------------------------------


def test_iso4762_volume_grows_with_length() -> None:
    """Doubling the shaft length should add roughly the shaft's volume."""
    short = iso4762_cap_screw(thread="M8", length=10.0)
    long = iso4762_cap_screw(thread="M8", length=30.0)
    # Δlength = 20 mm. M8 thread r=4 → expected shaft volume add = π·16·20 ≈ 1005 mm³.
    expected_delta = math.pi * 4**2 * 20
    actual_delta = long.volume - short.volume
    assert math.isclose(actual_delta, expected_delta, rel_tol=1e-3), (
        f"Δvolume {actual_delta:.2f} not ≈ expected {expected_delta:.2f}"
    )


def test_iso4762_bigger_thread_has_bigger_head() -> None:
    """The head dimensions monotonically grow with thread size."""
    m3 = iso4762_cap_screw(thread="M3", length=10.0)
    m12 = iso4762_cap_screw(thread="M12", length=10.0)
    assert m12.bounding_box().size.X > m3.bounding_box().size.X
    assert m12.volume > m3.volume


# ---------------------------------------------------------------------------
# Geometry shape sanity
# ---------------------------------------------------------------------------


def test_iso4762_bbox_extends_along_shaft_axis() -> None:
    """The +Z direction is the shaft; -Z is the head. For an M5×20 cap screw,
    bbox z should run from -head_height (-5 mm) to +length (+20 mm)."""
    screw = iso4762_cap_screw(thread="M5", length=20.0)
    bbox = screw.bounding_box()
    assert math.isclose(bbox.min.Z, -5.0, abs_tol=1e-6), bbox.min.Z
    assert math.isclose(bbox.max.Z, 20.0, abs_tol=1e-6), bbox.max.Z


def test_iso4762_socket_carves_volume_out_of_head() -> None:
    """The hex socket should reduce the head's volume vs an un-socketed
    cylinder of the same dimensions. Sanity check that the subtract fires."""
    from build123d import Align, Cylinder

    # M8: head_d=13, head_h=8, socket_w=6, socket_t=4
    raw_head_volume = math.pi * (13 / 2) ** 2 * 8  # ~1061 mm³
    socket_volume = (3 * math.sqrt(3) / 2) * (6 / math.sqrt(3)) ** 2 * 4  # hex prism
    shaft_volume = math.pi * 4**2 * 20  # M8 shaft, length=20

    screw = iso4762_cap_screw(thread="M8", length=20.0)
    expected = raw_head_volume - socket_volume + shaft_volume
    assert math.isclose(screw.volume, expected, rel_tol=5e-3), (
        f"got {screw.volume:.2f}, expected ≈ {expected:.2f} "
        f"(raw_head - socket + shaft)"
    )
