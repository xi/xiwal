import sys

from . import image
from . import scheme
from . import term


solarized = ['#002b36', '#eee8d5', '#b58900', '#cb4b16', '#dc322f', '#d33682', '#6c71c4', '#268bd2', '#2aa198', '#859900']
gruvbox = ['#3c3836', '#cc241d', '#98971a', '#d79921', '#458588', '#b16286', '#689d6a', '#d65d0e']
tango = ['#555753', '#ef2929', '#8ae234', '#fce94f', '#739fcf', '#ad7fa8', '#34e2e2']


if __name__ == '__main__':
	colors = list(image.extract_colors(sys.argv[1], 9))
	# colors = solarized
	scheme = scheme.colors2scheme(colors)
	print(';'.join(scheme))
	term.palette()
	term.apply(scheme)
