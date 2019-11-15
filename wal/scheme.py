import math

from . import lch

# Minimum chroma for red/green (signal colors)
C_RG = 60

# lightness for dark/light colors
# Some general guidelines:
# - dark kcolors should have sufficient contrast to both black and white
# - light colors should have different levels of lightness so they can
#   easily be distinguished
L_DARK = 2, 45, 50, 50, 45, 45, 50, 85
L_LIGHT = 20, 60, 70, 80, 60, 60, 75, 100

# hue for red reference color
OFFSET = math.pi * 2 / 15


def permutate(a, n):
	if n == 0:
		yield ()
	else:
		for i in range(len(a)):
			for rest in permutate(a[:i] + a[i + 1:], n - 1):
				yield (a[i], *rest)


def distance(color, i):
	hue = math.pi / 3 * i + OFFSET
	d = abs(color[2] - hue)
	c = color[1]
	if i in [0, 1]:
		c = max(c, C_RG)
	if d > math.pi:
		d = 2 * math.pi - d
	return d ** 4 * c


def score(colors):
	s = sum(distance(c, i) for i, c in enumerate(colors))
	s /= sum(c[1] for c in colors)
	return s


def scheme(colors, dominant):
	c_grey = min(dominant[1], 8)

	yield L_DARK[0], c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * 1.2
		if i in [0, 1]:
			c = max(c, C_RG)
		yield L_DARK[i + 1], c, colors[i][2]
	yield L_DARK[7], c_grey, dominant[2]

	yield L_LIGHT[0], c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * 1.2
		if i in [0, 1]:
			c = max(c, C_RG)
		yield L_LIGHT[i + 1], c, colors[i][2]
	yield L_LIGHT[7], c_grey, dominant[2]


def colors2scheme(colors):
	colors = [lch.from_hex(c) for c in colors]
	dominant = colors[0]
	colors = min(permutate(colors, 6), key=score)
	colors = [colors[i] for i in [0, 2, 1, 4, 5, 3]]
	return [lch.to_hex(c) for c in scheme(colors, dominant)]
