"""Oklab color model.

https://bottosson.github.io/posts/oklab/
"""

import math


def _srgb2rgb(c):
    c = c / 255.0
    if c <= 0.04045:
        c = c / 12.92
    else:
        c = ((c + 0.055) / 1.055) ** 2.4
    return c


def _rgb2srgb(c):
    if c <= 0.0031308:
        c = c * 12.92
    else:
        c = 1.055 * (c ** (1 / 2.4)) - 0.055
    return c * 255


def rgb2lab(rgb):
    r, g, b = map(_srgb2rgb, rgb)

    l = 0.4121656120 * r + 0.5362752080 * g + 0.0514575653 * b
    m = 0.2118591070 * r + 0.6807189584 * g + 0.1074065790 * b
    s = 0.0883097947 * r + 0.2818474174 * g + 0.6302613616 * b

    l_ = l ** (1 / 3)
    m_ = m ** (1 / 3)
    s_ = s ** (1 / 3)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    return L, a, b


def lab2rgb(lab):
    L, a, b = lab

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3

    r = +4.0767245293 * l - 3.3072168827 * m + 0.2307590544 * s
    g = -1.2681437731 * l + 2.6093323231 * m - 0.3411344290 * s
    b = -0.0041119885 * l - 0.7034763098 * m + 1.7068625689 * s

    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return tuple(map(_rgb2srgb, (r, g, b)))


def rgb2lch(rgb):
    l, a, b = rgb2lab(rgb)
    c = (a ** 2 + b ** 2) ** 0.5
    h = 0
    if abs(a) > 0.0001 or abs(b) > 0.0001:
        h = math.atan2(b, a)
        h = (h + 4 * math.pi) % (2 * math.pi)
    return l, c, h


def _lch2rgb(lch):
    l, c, h = lch
    a = math.cos(h) * c
    b = math.sin(h) * c
    return lab2rgb((l, a, b))


def lch2rgb(lch):
    rgb = _lch2rgb(lch)

    if any(x < 0 or x > 255 for x in rgb):
        c_min = 0
        c_max = lch[1]

        while c_max - c_min > 0.01:
            c_tmp = (c_min + c_max) / 2
            rgb = _lch2rgb((lch[0], c_tmp, lch[2]))
            if any(x < 0 or x > 255 for x in rgb):
                c_max = c_tmp
            else:
                c_min = c_tmp

    return rgb


def format_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*[int(x) for x in rgb])


def parse_hex(s):
    s = s.lstrip('#')
    if len(s) == 6:
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
    elif len(s) == 3:
        r = int(s[0], 16) * 17
        g = int(s[1], 16) * 17
        b = int(s[2], 16) * 17
    else:
        raise ValueError('Invalid hex color: %s' % s)
    return r, g, b


def from_hex(s):
    return rgb2lch(parse_hex(s))


def to_hex(lch):
    return format_hex(lch2rgb(lch))
