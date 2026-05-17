"""ISO 4762 — Hexagon socket head cap screws.

Parametric implementation of the socket head cap screw family defined by
ISO 4762 (equivalent to DIN 912). Geometry is parametric over (thread,
length); dimensions for each thread size come from the standard's
dimension table.

The thread itself is modelled as a smooth cylinder of the nominal thread
diameter (i.e. without the helix profile). This matches ``bd_warehouse``
practice for fasteners and is adequate for assembly modelling, clearance
checks, and visualisation. Real helix-threaded variants are tracked
separately — see the project's GitHub issues.

The dimension table here is the canonical ISO 4762 family. Values cross-
referenced against the FreeCAD Parts Library fixtures (38 variants under
``fcstd2b123d/tests/fixtures/tier3_corpus_c/Screw_M*_ISO4762_8_8_A2K.FCStd``).
"""

from __future__ import annotations

from dataclasses import dataclass

from build123d import (
    Align,
    Cylinder,
    Mode,
    Plane,
    Pos,
    Part,
    RegularPolygon,
    extrude,
)


@dataclass(frozen=True)
class _Iso4762Dims:
    """Dimensions for one ISO 4762 thread size.

    All in millimetres.
    """

    thread_diameter: float  # d, nominal thread diameter
    head_diameter: float    # dk, head outer diameter (max)
    head_height: float      # k, head height (max)
    socket_width: float     # s, hex socket across-flats
    socket_depth: float     # t, socket depth (min)


# ISO 4762 dimension table — values from the standard (ISO 4762:2004).
# Each entry: thread → (d, dk, k, s, t).
_ISO4762_TABLE: dict[str, _Iso4762Dims] = {
    "M3":  _Iso4762Dims(3.0,  5.5,  3.0,  2.5,  1.3),
    "M4":  _Iso4762Dims(4.0,  7.0,  4.0,  3.0,  2.0),
    "M5":  _Iso4762Dims(5.0,  8.5,  5.0,  4.0,  2.5),
    "M6":  _Iso4762Dims(6.0, 10.0,  6.0,  5.0,  3.0),
    "M8":  _Iso4762Dims(8.0, 13.0,  8.0,  6.0,  4.0),
    "M10": _Iso4762Dims(10.0, 16.0, 10.0,  8.0,  5.0),
    "M12": _Iso4762Dims(12.0, 18.0, 12.0, 10.0,  6.0),
    "M16": _Iso4762Dims(16.0, 24.0, 16.0, 14.0,  8.0),
    "M20": _Iso4762Dims(20.0, 30.0, 20.0, 17.0, 10.0),
    "M24": _Iso4762Dims(24.0, 36.0, 24.0, 19.0, 12.0),
    "M30": _Iso4762Dims(30.0, 45.0, 30.0, 22.0, 15.5),
    "M36": _Iso4762Dims(36.0, 54.0, 36.0, 27.0, 19.0),
}


def iso4762_cap_screw(thread: str = "M5", length: float = 20.0) -> Part:
    """Build an ISO 4762 socket head cap screw.

    Parameters
    ----------
    thread:
        Thread designation. One of ``M3`` … ``M36`` (see the keys of
        :data:`_ISO4762_TABLE` for the supported set). Defaults to ``M5``.
    length:
        Shaft length under the head, in millimetres. ISO 4762 standardises
        lengths in discrete steps; this implementation accepts any positive
        value to support assembly modelling. Defaults to ``20`` mm.

    Returns
    -------
    Part:
        The screw modelled with the cylindrical head + hex socket on top
        and a smooth (symbolic) threaded shaft below. Origin is at the
        centre of the screw's head-shaft junction; +Z runs along the shaft
        away from the head.

    Examples
    --------
    >>> screw = iso4762_cap_screw(thread="M5", length=20)
    >>> abs(screw.volume) > 0
    True
    """
    if thread not in _ISO4762_TABLE:
        supported = ", ".join(sorted(_ISO4762_TABLE.keys()))
        raise ValueError(
            f"unsupported thread {thread!r} for ISO 4762; supported: {supported}"
        )
    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")

    d = _ISO4762_TABLE[thread]

    # Head: cylinder sitting on -Z side of the origin (z = -head_height to 0).
    head = Cylinder(
        radius=d.head_diameter / 2,
        height=d.head_height,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    )

    # Hex socket: subtract a hex prism from the head's top face.
    socket_circumradius = d.socket_width / (3**0.5)  # across-flats → circumradius
    socket_face = RegularPolygon(socket_circumradius, side_count=6)
    socket_prism = extrude(socket_face, amount=d.socket_depth)
    socket_at_top = Pos(0, 0, -d.socket_depth) * socket_prism
    head = head - socket_at_top

    # Shaft: smooth cylinder, thread_diameter, from z=0 down to z=length.
    shaft = Cylinder(
        radius=d.thread_diameter / 2,
        height=length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    return head + shaft


__all__ = ["iso4762_cap_screw"]
