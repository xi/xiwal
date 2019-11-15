import math

WHITE = (95.05, 100, 108.9)


def _srgb2rgb(c):
	c = c / 255.0
	if c <= 0.04045:
		c = c / 12.92
	else:
		c = ((c + 0.055) / 1.055) ** 2.4
	return c * 100


def _rgb2srgb(c):
	c = c / 100.0
	if c <= 0.0031308:
		c = c * 12.92
	else:
		c = 1.055 * (c ** (1 / 2.4)) - 0.055
	return c * 255


def _xyz2lab(t):
	if t > 216.0 / 24389:
		return t ** (1.0 / 3)
	else:
		return 841.0 / 108 * t + 4.0 / 29


def _lab2xyz(t):
	if t > 6.0 / 29:
		return t ** 3
	else:
		return 108.0 / 841 * (t - 4.0 / 29)


def rgb2lab(rgb):
	r, g, b = map(_srgb2rgb, rgb)

	x = _xyz2lab((0.4124 * r + 0.3576 * g + 0.1805 * b) / WHITE[0])
	y = _xyz2lab((0.2126 * r + 0.7152 * g + 0.0722 * b) / WHITE[1])
	z = _xyz2lab((0.0193 * r + 0.1192 * g + 0.9505 * b) / WHITE[2])

	l = 116 * y - 16
	a = 500 * (x - y)
	b = 200 * (y - z)

	return l, a, b


def lab2rgb(lab):
	l, a, b = lab

	l = (l + 16) / 116.0

	x = WHITE[0] * _lab2xyz(l + a / 500)
	y = WHITE[1] * _lab2xyz(l)
	z = WHITE[2] * _lab2xyz(l - b / 200)

	r =  3.2406 * x - 1.5372 * y - 0.4986 * z
	g = -0.9689 * x + 1.8758 * y + 0.0415 * z
	b =  0.0557 * x - 0.2040 * y + 1.0570 * z

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
	r = int(s[1:3], 16)
	g = int(s[3:5], 16)
	b = int(s[5:7], 16)
	return r, g, b


def from_hex(s):
	return rgb2lch(parse_hex(s))


def to_hex(lch):
	return format_hex(lch2rgb(lch))
