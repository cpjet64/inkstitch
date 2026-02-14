# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..i18n import _
from ..utils import cache

# modern versions of Inkscape use 96 pixels per inch as per the CSS standard
PIXELS_PER_MM = 96 / 25.4


def parse_length_with_units(length):
    parsed = inkex.units.parse_unit(length)
    if parsed is None:
        raise ValueError(_("parseLengthWithUnits: unknown unit %s") % length)

    value, unit = parsed
    if not unit:
        raise ValueError(_("parseLengthWithUnits: unknown unit %s") % length)
    return value, unit


def convert_length(length):
    value, units = parse_length_with_units(length)

    return inkex.units.convert_unit(str(value) + units, 'px')


@cache
def get_viewbox(svg):
    viewbox = svg.get('viewBox')
    if viewbox is None:
        viewbox = "0 0 0 0"
    values = viewbox.strip().replace(',', ' ').split()
    if len(values) < 4:
        values.extend(["0"] * (4 - len(values)))
    return values[:4]


@cache
def get_doc_size(svg):
    width = svg.get('width')
    height = svg.get('height')

    if width == "100%" and height == "100%":
        # Some SVG editors set width and height to "100%".  I can't find any
        # solid documentation on how one is supposed to interpret that, so
        # just ignore it and use the viewBox.  That seems to have the intended
        # result anyway.

        width = None
        height = None

    if width is None or height is None:
        # fall back to the dimensions from the viewBox
        viewbox = get_viewbox(svg)
        width = viewbox[2]
        height = viewbox[3]

    doc_width = convert_length(width)
    doc_height = convert_length(height)

    return doc_width, doc_height


@cache
def get_viewbox_transform(node):
    # somewhat cribbed from inkscape-silhouette
    doc_width, doc_height = get_doc_size(node)

    viewbox = get_viewbox(node)

    dx = -float(viewbox[0])
    dy = -float(viewbox[1])
    transform = inkex.transforms.Transform("translate(%f, %f)" % (dx, dy))

    try:
        sx = doc_width / float(viewbox[2])
        sy = doc_height / float(viewbox[3])

        # preserve aspect ratio
        aspect_ratio = node.get('preserveAspectRatio', 'xMidYMid meet')
        if aspect_ratio != 'none':
            sx = sy = max(sx, sy) if 'slice' in aspect_ratio else min(sx, sy)

        scale_transform = inkex.transforms.Transform("scale(%f, %f)" % (sx, sy))
        transform = transform @ scale_transform
    except ZeroDivisionError:
        pass

    return transform
