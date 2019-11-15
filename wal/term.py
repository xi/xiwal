import glob

from . import lch


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
		r, g, b = lch.parse_hex(scheme[i])
		s.append('\033[48;2;%i;%i;%im    \033[0m' % (r, g, b))
	print(''.join(s[:8]))
	print(''.join(s[8:]))
