import glob
import os

from . import lch


def apply(scheme, cachefile='~/.cache/wal/sequences'):
    cachefile = os.path.expanduser(cachefile)
    os.makedirs(os.path.dirname(cachefile), exist_ok=True)

    for path in [cachefile, *glob.glob('/dev/pts/[0-9]*')]:
        with open(path, 'w') as tty:
            for i in range(16):
                tty.write(f'\033]4;{i};{scheme[i]}\033\\')
            tty.write(f'\033]11;{scheme[0]}\033\\')
            tty.write(f'\033]10;{scheme[15]}\033\\')


def palette(scheme):
    s = []
    for i in range(16):
        r, g, b = lch.parse_hex(scheme[i])
        s.append(f'\033[48;2;{r};{g};{b}m    \033[0m')
    print(''.join(s[:8]))
    print(''.join(s[8:]))


def palette_256(scheme):
    palette(scheme)

    print()

    for y in range(6):
        line = []
        for z in range(6):
            for x in range(6):
                r, g, b = lch.parse_hex(scheme[16 + 36 * y + 6 * z + x])
                line.append(f'\033[48;2;{r};{g};{b}m    \033[0m')
            line.append('  ')
        print(''.join(line))

    print()

    line = []
    for i in range(24):
        r, g, b = lch.parse_hex(scheme[232 + i])
        line.append(f'\033[48;2;{r};{g};{b}m    \033[0m')
    print(''.join(line))
