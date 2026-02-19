"""Oklab color model.

rgb in range [0, 255]
lab in range [0, 1]
hue in range [-pi, pi]

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

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

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

    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return tuple(map(_rgb2srgb, (r, g, b)))


def lab2lch(lab):
    l, a, b = lab
    c = (a ** 2 + b ** 2) ** 0.5
    h = 0
    if abs(a) > 0.0001 or abs(b) > 0.0001:
        h = math.atan2(b, a)
        h = (h + 4 * math.pi) % (2 * math.pi)
    return l, c, h


def lch2lab(lch):
    l, c, h = lch
    a = math.cos(h) * c
    b = math.sin(h) * c
    return l, a, b


def rgb2lch(rgb):
    return lab2lch(rgb2lab(rgb))


def _lch2rgb(lch):
    return lab2rgb(lch2lab(lch))


def lch2rgb(lch):
    rgb = _lch2rgb(lch)
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


def mix(lch1, lch2, t):
    # mixing hue is hard, so we mix in lab instead
    return lab2lch([x + t * (y - x) for x, y in zip(
        lch2lab(lch1), lch2lab(lch2), strict=True
    )])


def format_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*[int(x) for x in rgb])


def parse_hex(s):
    s = s.lstrip('#')
    if len(s) == 12:
        r = int(s[0:4], 16) / 257
        g = int(s[4:8], 16) / 257
        b = int(s[8:12], 16) / 257
    elif len(s) == 6:
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
    elif len(s) == 3:
        r = int(s[0], 16) * 17
        g = int(s[1], 16) * 17
        b = int(s[2], 16) * 17
    else:
        raise ValueError(f'Invalid hex color: {s}')
    return r, g, b


def from_hex(s):
    return rgb2lch(parse_hex(s))


def to_hex(lch):
    return format_hex(lch2rgb(lch))
