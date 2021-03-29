#!/usr/bin/env python
# https://github.com/datamafia/color-proximity
"""color-proximity module."""

from __future__ import division

from math import sqrt, pow as poww


def hextorgb(hex_value):
    c = hex_value
    r, g, b = 0, 0, 0
    if '#' in hex_value:
        c = hex_value[1:]
    if len(c) == 8:
        # alpha channel
        c = c[2:]
    if len(c) == 3:
        # simplified hex
        c = c[0] * 2 + c[1] * 2 + c[2] * 2
    try:
        r = int(c[:2], 16)
        g = int(c[2:4], 16)
        b = int(c[4:], 16)
    except (ValueError, TypeError):
        return 0, 0, 0
    return r, g, b


class ColorProximity(object):
    """Color Proximity."""

    def proximity(self, a_set, b_set):
        """Return proximity value of a pair RGB tuple or list
        Init, convert list/tupel of int,int,int to color proximity value
        Args:
        a : required, list or tuple containting int, 0-255 RGB color value
        b : required, list or tuple containting int, 0-255 RGB color value
        Returns :
        float
        """
        # support for RBG+alpha, slice to ignore alpha
        if len(a_set) > 3:
            a_set = a_set[:3]
        if len(b_set) > 3:
            b_set = b_set[:3]
        c_1 = self.rgb2lab(a_set)  # int int int
        c_2 = self.rgb2lab(b_set)

        return sqrt(poww(c_1[0] - c_2[0], 2) + poww(c_1[1] - c_2[1], 2) + poww(c_1[2] - c_2[2], 2))

    @classmethod
    def rgb2lab(cls, c_set):
        """RGB to LAB conversion"""

        # """RGB to L.a.b. conversion
        # Transform (int, int, int) from RGB to XYZ (CIE1931) to L.a.b.
        #    http://en.wikipedia.org/wiki/CIE_1931_color_space
        #    http://en.wikipedia.org/wiki/Lab_color_space
        # Args:
        #    c : required, list or tuple of 3 int (RGB)
        # Return :
        #    Lab value as 3 element list
        # """

        rgb = [0, 0, 0]
        xyz = [0, 0, 0]
        lab = [0, 0, 0]

        i = 0
        while len(c_set) > i:
            value = float(c_set[i] / 255)
            if value > 0.04045:
                value = poww(((value + 0.055) / 1.055), 2.4)
            else:
                value = value / 12.92
            rgb[i] = value * 100
            i += 1

        xyz[0] = (rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805) / 95.047
        # // ref_X =  95.047   Observer= 2deg, Illuminant= D65
        xyz[1] = (rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722) / 100.0
        # // ref_Y = 100.000
        xyz[2] = (rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505) / 108.883
        # // ref_Z = 108.883

        i = 0
        while len(xyz) > i:
            value = xyz[i]
            if value > 0.008856:
                value = poww(value, 1 / 3)
            else:
                value = (7.787 * value) + (16 / 116)
            xyz[i] = value
            i += 1

        lab[0] = round(((116 * xyz[1]) - 16), 3)
        lab[1] = round((500 * (xyz[0] - xyz[1])), 3)
        lab[2] = round((200 * (xyz[1] - xyz[2])), 3)

        return lab
