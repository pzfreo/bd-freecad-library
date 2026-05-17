"""ISO 7093 — Plain washers, large series.

Parametric implementation of the ISO 7093:2000 *Plain washers — Large
series* (equivalent to DIN 9021). A washer is a single annulus
extruded along the bolt axis — geometrically the simplest standard
fastener part, which makes this the right first family to ship our
end-to-end validation harness against.

Each variant is fully described by three dimensions: the inner hole
diameter ``d1``, the outer diameter ``d2``, and the thickness ``h``.

Validation manifest in :mod:`iso7093_manifest`; see :mod:`tests._validation`
for the harness. v0.1 ships bbox-extent validation against the four
ISO 7093 fixtures in the ``fcstd2b123d`` corpus.
"""

from __future__ import annotations

from dataclasses import dataclass

from build123d import Circle, Part, extrude


@dataclass(frozen=True)
class _Iso7093Dims:
    """Dimensions for one ISO 7093 washer size, in millimetres."""

    inner_diameter: float   # d1, hole diameter
    outer_diameter: float   # d2, washer outer diameter
    thickness: float        # h


# Dimension table — values matched to the FreeCAD Parts Library's
# ``ISO7093DIN9021_M*FlatWasher.FCStd`` family, which spans ISO 7093
# Part 1 and DIN 9021 (the German precursor). For most sizes the two
# standards agree; the FreeCAD library's M24 (``d1=28``) and M30
# (``d1=33``) values differ from ISO 7093:2000 Part 1 (``d1=25``,
# ``d1=31`` respectively) — we use the FreeCAD library values so
# regression tests match the available fixtures. The values for sizes
# without a FreeCAD fixture are the ISO 7093 Part 1 spec; those are
# tentative and will get cross-referenced if/when fixtures are added.
_ISO7093_TABLE: dict[str, _Iso7093Dims] = {
    "M3":   _Iso7093Dims(3.2,    9.0, 0.8),
    "M3.5": _Iso7093Dims(3.7,   11.0, 0.8),
    "M4":   _Iso7093Dims(4.3,   12.0, 1.0),
    "M5":   _Iso7093Dims(5.3,   15.0, 1.2),   # fixture-validated
    "M6":   _Iso7093Dims(6.4,   18.0, 1.6),
    "M8":   _Iso7093Dims(8.4,   24.0, 2.0),
    "M10":  _Iso7093Dims(10.5,  30.0, 2.5),   # fixture-validated
    "M12":  _Iso7093Dims(13.0,  37.0, 3.0),
    "M14":  _Iso7093Dims(15.0,  44.0, 3.0),
    "M16":  _Iso7093Dims(17.0,  50.0, 3.0),
    "M18":  _Iso7093Dims(19.0,  56.0, 4.0),
    "M20":  _Iso7093Dims(21.0,  60.0, 4.0),
    "M22":  _Iso7093Dims(23.0,  66.0, 5.0),
    "M24":  _Iso7093Dims(28.0,  72.0, 5.0),   # FC library, not ISO 7093 Part 1 (25)
    "M27":  _Iso7093Dims(28.0,  85.0, 6.0),
    "M30":  _Iso7093Dims(33.0,  92.0, 6.0),   # FC library, not ISO 7093 Part 1 (31)
    "M33":  _Iso7093Dims(34.0, 105.0, 6.0),
    "M36":  _Iso7093Dims(37.0, 110.0, 8.0),
}


def iso7093_plain_washer(thread: str = "M5") -> Part:
    """Build an ISO 7093 plain washer (large series).

    Parameters
    ----------
    thread:
        Bolt size the washer fits. One of the keys of
        :data:`_ISO7093_TABLE` — currently ``M3`` through ``M36``.
        Defaults to ``M5``.

    Returns
    -------
    Part:
        The washer modelled as ``Circle(d2/2) − Circle(d1/2)``
        extruded along +Z by the washer thickness. Origin is at the
        washer's centre on its bottom face; +Z runs along the bolt
        axis.

    Examples
    --------
    >>> washer = iso7093_plain_washer(thread="M5")
    >>> abs(washer.volume) > 0
    True
    """
    if thread not in _ISO7093_TABLE:
        supported = ", ".join(_ISO7093_TABLE.keys())
        raise ValueError(
            f"unsupported thread {thread!r} for ISO 7093; supported: {supported}"
        )

    d = _ISO7093_TABLE[thread]
    annulus = Circle(d.outer_diameter / 2) - Circle(d.inner_diameter / 2)
    return extrude(annulus, amount=d.thickness)


__all__ = ["iso7093_plain_washer"]
