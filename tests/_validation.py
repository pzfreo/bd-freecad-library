"""Validation harness: parametric output vs FreeCAD source fixtures.

Each family declares a manifest of ``(fixture_filename, params)`` pairs.
This harness:

1. Locates the fixture in the ``fcstd2b123d`` sibling repo.
2. Translates it via ``python -m fcstd2b123d <fixture>`` (subprocess into
   the FreeCAD env).
3. Exec's the emitted build123d source to get the FreeCAD-side ``result``
   ``Part``.
4. Calls the parametric function with ``params`` to get our side's
   ``Part``.
5. Compares geometric invariants (bbox by default; volume opt-in).

Tests skip cleanly when ``FCSTD2B123D_FREECAD_PYTHON`` is unset (CI's
fast lane). The slow lane (with FreeCAD) runs the full validation.

Environment variables:
    FCSTD2B123D_REPO              path to fcstd2b123d checkout
                                  (default: ../fcd2b123d/ next to this repo)
    FCSTD2B123D_FREECAD_PYTHON    Python with FreeCAD installed
    FCSTD2B123D_FREECAD_PYTHONPATH  extra PYTHONPATH for FreeCAD
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Callable

import pytest


def fcstd2b123d_repo() -> Path:
    """Locate the fcstd2b123d checkout we validate against."""
    p = os.environ.get("FCSTD2B123D_REPO")
    if p:
        return Path(p)
    # Default: sibling directory.
    sibling = Path(__file__).resolve().parent.parent.parent / "fcd2b123d"
    return sibling


def freecad_python() -> str:
    """The FreeCAD-enabled Python; skip cleanly if unset."""
    p = os.environ.get("FCSTD2B123D_FREECAD_PYTHON")
    if not p:
        pytest.skip(
            "FCSTD2B123D_FREECAD_PYTHON not set; geometric validation needs "
            "a FreeCAD-enabled Python to translate the source fixtures"
        )
    return p


def fixtures_root() -> Path:
    """Where the FCStd fixtures live in fcstd2b123d."""
    return fcstd2b123d_repo() / "tests" / "fixtures"


def _find_fixture(name: str) -> Path:
    """Locate a fixture by basename under the fcstd2b123d fixtures tree."""
    root = fixtures_root()
    matches = list(root.rglob(name))
    if not matches:
        pytest.fail(f"fixture {name!r} not found under {root}")
    if len(matches) > 1:
        pytest.fail(
            f"fixture {name!r} matched {len(matches)} files; manifest names "
            f"must be unique. Matches: {matches}"
        )
    return matches[0]


def _translate_fixture(fcstd_path: Path) -> str:
    """Run ``python -m fcstd2b123d <fixture>`` and return the emit source."""
    py = freecad_python()
    repo = fcstd2b123d_repo()
    fc_pp = os.environ.get("FCSTD2B123D_FREECAD_PYTHONPATH", "")
    pythonpath = ":".join(p for p in (str(repo / "src"), fc_pp) if p)
    env = {**os.environ, "PYTHONPATH": pythonpath}
    result = subprocess.run(
        [py, "-m", "fcstd2b123d", str(fcstd_path)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail(
            f"fcstd2b123d failed on {fcstd_path.name}:\n"
            f"stdout:\n{result.stdout[-500:]}\n"
            f"stderr:\n{result.stderr[-500:]}"
        )
    return result.stdout


def _exec_emit(source: str) -> Any:
    """Exec emitted build123d source; return the bound ``result`` Part."""
    namespace: dict[str, Any] = {}
    try:
        exec(source, namespace)
    except Exception as exc:
        pytest.fail(f"emitted source failed to exec: {exc}\n\nSource tail:\n{source[-800:]}")
    if "result" not in namespace:
        pytest.fail("emitted source did not bind `result`")
    return namespace["result"]


def _bbox_signature(part: Any) -> tuple[float, float, float]:
    """Sorted bbox extents — invariant under axis-aligned rotation.

    For a screw, this collapses orientation differences between the
    FreeCAD fixture and our parametric output: ``(head_diameter,
    head_diameter, head_height + length)`` in either orientation
    sorts to the same triple.
    """
    b = part.bounding_box()
    sizes = sorted([b.size.X, b.size.Y, b.size.Z])
    return (sizes[0], sizes[1], sizes[2])


def validate_fixture(
    parametric_fn: Callable[..., Any],
    fixture_name: str,
    params: dict[str, Any],
    *,
    bbox_tol_abs: float = 0.5,
    volume_tol_rel: float | None = None,
) -> None:
    """Validate one fixture against the parametric function.

    Parameters
    ----------
    parametric_fn:
        The family's parametric function, e.g. ``iso4762_cap_screw``.
    fixture_name:
        Basename of the .FCStd fixture (located by rglob under
        ``fcstd2b123d/tests/fixtures/``).
    params:
        Keyword arguments to pass to ``parametric_fn``.
    bbox_tol_abs:
        Absolute tolerance for each bbox extent (mm). Default 0.5 mm
        allows for head fillet and thread approximation differences.
    volume_tol_rel:
        Optional relative tolerance for volume comparison. ``None``
        (default) skips volume — appropriate when the parametric form
        approximates FreeCAD geometry (smooth cylinder vs. helix
        thread, no head fillet, etc.). Set to a small value once the
        family's modelling is exact.
    """
    fcstd_path = _find_fixture(fixture_name)
    source = _translate_fixture(fcstd_path)
    fc_part = _exec_emit(source)
    our_part = parametric_fn(**params)

    fc_bbox = _bbox_signature(fc_part)
    our_bbox = _bbox_signature(our_part)
    for axis, (fc_dim, our_dim) in enumerate(zip(fc_bbox, our_bbox)):
        delta = abs(fc_dim - our_dim)
        assert delta <= bbox_tol_abs, (
            f"{fixture_name}: bbox axis {axis} (sorted) differs by "
            f"{delta:.3f} mm > {bbox_tol_abs} mm tol (FC={fc_dim:.3f}, "
            f"ours={our_dim:.3f})"
        )

    if volume_tol_rel is not None:
        fc_vol = abs(fc_part.volume)
        our_vol = abs(our_part.volume)
        if fc_vol > 0:
            rel_err = abs(fc_vol - our_vol) / fc_vol
            assert rel_err <= volume_tol_rel, (
                f"{fixture_name}: volume rel.err {rel_err:.3%} > "
                f"{volume_tol_rel:.3%} tol (FC={fc_vol:.2f}, ours={our_vol:.2f})"
            )
