import math
import functools

from . import lch

# Minimum chroma for red/green (signal colors)
C_RG = 60

# MAXIMUM chroma for greys
C_GREY = 8

C_FACTOR = 1.2

# lightness for dark/light colors
# Some general guidelines:
# - dark kcolors should have sufficient contrast to both black and white
# - light colors should have different levels of lightness so they can
#   easily be distinguished
L_DARK = 2, 45, 50, 50, 45, 45, 50, 85
L_LIGHT = 20, 60, 70, 80, 60, 60, 75, 100

# hue for red reference color
OFFSET = math.pi * 2 / 15

ORDER = [0, 2, 1, 4, 5, 3]


def permutate(a, n):
	if n == 0:
		yield ()
	else:
		for i in range(len(a)):
			for rest in permutate(a[:i] + a[i + 1:], n - 1):
				yield (a[i], *rest)


@functools.lru_cache(maxsize=32)
def distance(color, i):
	hue = math.pi / 3 * i + OFFSET
	d = abs(color[2] - hue)
	if d > math.pi:
		d = 2 * math.pi - d

	c = color[1]
	if i in [0, 1]:
		c = max(c, C_RG)

	return d ** 4 * c, c


def score(colors):
	sum_score = 0
	sum_chroma = 0

	for i, color in enumerate(colors):
		score, chroma = distance(color, ORDER[i])
		sum_score += score
		sum_chroma += chroma

	return sum_score / sum_chroma


def scheme(colors, dominant):
	c_grey = min(dominant[1], C_GREY)

	yield L_DARK[0], c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * C_FACTOR
		if i in [0, 1]:
			c = max(c, C_RG)
		yield L_DARK[i + 1], c, colors[i][2]
	yield L_DARK[7], c_grey, dominant[2]

	yield L_LIGHT[0], c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * C_FACTOR
		if i in [0, 1]:
			c = max(c, C_RG)
		yield L_LIGHT[i + 1], c, colors[i][2]
	yield L_LIGHT[7], c_grey, dominant[2]


def colors2scheme(colors):
	colors = [lch.from_hex(c) for c in colors]
	dominant = colors[0]
	colors = min(permutate(colors, 6), key=score)
	s = scheme(colors, dominant)
	return [lch.to_hex(c) for c in s]
