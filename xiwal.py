import glob
import math
import re
import subprocess
import sys

WHITE = (95.05, 100, 108.9)
C_BG = 60


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
	rgb = _lch2rgb(lch);

	if any(x < 0 or x > 255 for x in rgb):
		c_min = 0
		c_max = lch[1]

		while c_max - c_min > 0.01:
			c_tmp = (c_min + c_max) / 2
			rgb = _lch2rgb((lch[0], c_tmp, lch[2]));
			if any(x < 0 or x > 255 for x in rgb):
				c_max = c_tmp
			else:
				c_min = c_tmp

	return rgb


def chex(rgb):
	return '#{:02x}{:02x}{:02x}'.format(*[int(x) for x in rgb])


def im(img, colors=9):
	cmd = ['convert', img, '-alpha', 'deactivate', '-colors', str(colors), '-unique-colors', 'txt:-']
	output = subprocess.check_output(cmd)
	for line in output.splitlines()[1:]:
		line = line.decode('ascii')
		match = re.search('srgb\(([0-9]+),([0-9]+),([0-9]+)\)', line)
		color = [int(i, 10) for i in match.groups()]
		yield color


def permutate(a, n):
	if n == 0:
		yield ()
	else:
		for i in range(len(a)):
			for rest in permutate(a[:i] + a[i + 1:], n - 1):
				yield (a[i], *rest)


def distance(color, i, offset=math.pi * 2 / 12):
	hue = math.pi / 3 * i + offset
	d = abs(color[2] - hue)
	c = color[1]
	if i in [0, 1]:
		c = max(c, C_BG)
	if d > math.pi:
		d = 2 * math.pi - d
	return d ** 2 * c


def score(colors):
	s = sum(distance(c, i) for i, c in enumerate(colors))
	s /= sum(c[1] for c in colors)
	return s


def scheme(colors, dominant):
	l_dark = 45, 50, 50, 45, 45, 50
	l_light = 60, 70, 80, 60, 60, 75
	c_grey = min(dominant[1], 8)

	yield 2, c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * 1.2
		if i in [0, 1]:
			c = max(c, C_BG)
		yield l_dark[i], c, colors[i][2]
	yield 90, c_grey, dominant[2]

	yield 20, c_grey, dominant[2]
	for i in range(6):
		c = colors[i][1] * 1.2
		if i in [0, 1]:
			c = max(c, C_BG)
		yield l_light[i], c, colors[i][2]
	yield 100, c_grey, dominant[2]


def colors2scheme(colors):
	colors = [rgb2lch(c) for c in colors]
	dominant = colors[0]
	colors = min(permutate(colors, 6), key=score)
	colors = [colors[i] for i in [0, 2, 1, 4, 5, 3]]
	return [chex(lch2rgb(c)) for c in scheme(colors, dominant)]


def apply(scheme):
	for path in glob.glob('/dev/pts/[0-9]*'):
		with open(path, 'w') as tty:
			for i in range(0, 16):
				tty.write('\033]4;%s;%s\033\\' % (i, scheme[i]))
			tty.write('\033]%s;%s\033\\' % (11, scheme[0]))
			tty.write('\033]%s;%s\033\\' % (10, scheme[15]))


def palette(scheme):
	s = []
	for i in range(0, 16):
		a = '8;5;%s' % i if i > 7 else i
		s.append('\033[4%sm%s\033[0m' % (a, '   '))
	print(''.join(s[:8]))
	print(''.join(s[8:]))


if __name__ == '__main__':
	# foo
	colors = list(im(sys.argv[1]))
	subprocess.call(['chafa', '-s', '40', sys.argv[1]])
	scheme = colors2scheme(colors)
	print(';'.join(scheme))
	palette(scheme)
	apply(scheme)
