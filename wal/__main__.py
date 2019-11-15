import sys
import argparse

from . import image
from . import scheme
from . import term


solarized = ['#002b36', '#eee8d5', '#b58900', '#cb4b16', '#dc322f', '#d33682', '#6c71c4', '#268bd2', '#2aa198', '#859900']
gruvbox = ['#3c3836', '#cc241d', '#98971a', '#d79921', '#458588', '#b16286', '#689d6a', '#d65d0e']
tango = ['#555753', '#ef2929', '#8ae234', '#fce94f', '#739fcf', '#ad7fa8', '#34e2e2']


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--image', '-i')
	parser.add_argument('-n', type=int, default=8)
	parser.add_argument('colors', nargs='*')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()

	colors = []
	if args.image:
		colors += list(image.extract_colors(args.image, args.n))
	colors += args.colors

	if len(colors) < 6:
		sys.exit('Need at least 6 colors')

	scheme = scheme.colors2scheme(colors)

	print(';'.join(scheme))
	term.palette()
	term.apply(scheme)
