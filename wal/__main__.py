import sys
import argparse

from . import image
from . import scheme
from . import term


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--image', '-i')
	parser.add_argument('-n', type=int, default=8)
	parser.add_argument('colors', nargs='*')
	return parser.parse_args()


def main():
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


if __name__ == '__main__':
	main()
