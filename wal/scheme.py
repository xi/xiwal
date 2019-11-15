import math

from . import lch

C_BG = 60
L_DARK = 45, 50, 50, 45, 45, 50
L_LIGHT = 60, 70, 80, 60, 60, 75
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
		c = max(c, C_BG)
	if d > math.pi:
		d = 2 * math.pi - d
	return d ** 4 * c


def score(colors):
	s = sum(distance(c, i) for i, c in enumerate(colors))
	s /= sum(c[1] for c in colors)
	return s


def scheme(colors, dominant):
	c_grey = min(dominant[1], 8)

	yield 2, c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * 1.2
		if i in [0, 1]:
			c = max(c, C_BG)
		yield L_DARK[i], c, colors[i][2]
	yield 85, c_grey, dominant[2]

	yield 20, c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * 1.2
		if i in [0, 1]:
			c = max(c, C_BG)
		yield L_LIGHT[i], c, colors[i][2]
	yield 100, c_grey, dominant[2]


def colors2scheme(colors):
	colors = [lch.from_hex(c) for c in colors]
	dominant = colors[0]
	colors = min(permutate(colors, 6), key=score)
	colors = [colors[i] for i in [0, 2, 1, 4, 5, 3]]
	return [lch.to_hex(c) for c in scheme(colors, dominant)]
