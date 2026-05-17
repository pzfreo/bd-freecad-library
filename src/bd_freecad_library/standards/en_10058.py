"""EN 10058 — Hot-rolled flat steel bars.

Parametric implementation of EN 10058 *Hot rolled flat steel bars for
general purposes* — a rectangular cross-section of (width × thickness)
extruded along the bar's length. Geometrically the simplest structural
profile in the EN 10058 family, and the cleanest place to start
because:

* The FreeCAD Parts Library has 22 fixtures spanning the standard
  width × thickness combinations, all translating cleanly through
  ``fcstd2b123d``.
* The geometry is exact — no thread approximation, no fillet
  discrepancies, no boolean composition.
* bd_warehouse doesn't yet cover structural steel profiles, so this
  is genuinely category 2a (something the warehouse could carry but
  doesn't).

Validation manifest in :mod:`en_10058_manifest`; see
:mod:`tests._validation` for the harness.
"""

from __future__ import annotations

from build123d import Part, Rectangle, extrude


def en_10058_flat_bar(
    width: float,
    thickness: float,
    length: float = 50.0,
) -> Part:
    """Build an EN 10058 hot-rolled flat steel bar.

    Parameters
    ----------
    width:
        Bar width (the larger cross-section dimension), in mm. EN 10058
        standardises discrete sizes (10, 12, 15, 18, 20, 25, 30, 40,
        50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200);
        any positive value is accepted for design-stage parametric work.
    thickness:
        Bar thickness (the smaller cross-section dimension), in mm.
        Standard thicknesses are 4, 5, 6, 8, 10, 12, 15, 18, 20, 25,
        30, 35, 40, 50.
    length:
        Bar length along its longitudinal axis, in mm. EN 10058 doesn't
        fix this — it's a continuous parameter. Defaults to 50 mm
        (matches the FreeCAD library's modelling convention).

    Returns
    -------
    Part:
        A rectangular prism of the given (width, thickness) cross-section
        extruded by ``length``. Origin at the centroid of the bottom
        face; +Z runs along the bar's length.

    Examples
    --------
    >>> bar = en_10058_flat_bar(width=60, thickness=4, length=100)
    >>> abs(bar.volume - 60*4*100) < 1e-6
    True
    """
    if width <= 0 or thickness <= 0 or length <= 0:
        raise ValueError(
            f"width, thickness, length must all be positive; "
            f"got width={width}, thickness={thickness}, length={length}"
        )
    cross_section = Rectangle(width, thickness)
    return extrude(cross_section, amount=length)


__all__ = ["en_10058_flat_bar"]
