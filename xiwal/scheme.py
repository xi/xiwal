import functools
import math

from . import lch

# Minimum chroma for red/green (signal colors)
C_RG = 0.15

# MAXIMUM chroma for greys
C_GREY = 0.02

C_FACTOR = 1.2

# lightness for dark/light colors
# Some general guidelines:
# - dark colors should have sufficient contrast to both black and white
# - light colors should have different levels of lightness so they can
#   easily be distinguished
L_DARK = 0.15, 0.50, 0.60, 0.60, 0.55, 0.55, 0.60, 0.90
L_LIGHT = 0.30, 0.65, 0.75, 0.85, 0.65, 0.65, 0.80, 1.00

# hue for red reference color
OFFSET = math.pi * 2 / 14

ORDER = [0, 2, 1, 4, 5, 3]


@functools.cache
def distance(color, i):
    hue = math.pi / 3 * ORDER[i] + OFFSET
    d = abs(color[2] - hue)
    if d > math.pi:
        d = 2 * math.pi - d

    c = color[1]
    if i in [0, 1]:
        c = max(c, C_RG)
        d += (c - color[1]) / (c + color[1])

    return d ** 4 * c, c


def get_best_subset(colors, n):
    # perf: skip some permutations based on their lowest possible score
    pos = 0
    indices = [0] * n
    dists = [0] * n
    weights = [1] * n
    best_score = math.inf
    best_colors = None
    while True:
        dists[pos], weights[pos] = distance(colors[indices[pos]], pos)
        score = sum(dists) / sum(weights)

        if score < best_score and pos + 1 == n:
            best_score = score
            best_colors = [colors[i] for i in indices]

        if score < best_score and pos + 1 < n:
            pos += 1
        else:
            indices[pos] += 1

        while True:
            if indices[pos] == len(colors):
                if pos == 0:
                    return best_colors
                indices[pos] = 0
                dists[pos] = 0
                weights[pos] = 1
                pos -= 1
                indices[pos] += 1
            elif indices[pos] in indices[:pos]:
                indices[pos] += 1
            else:
                break


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
    subset = get_best_subset(colors, 6)
    s = scheme(subset, dominant)
    return [lch.to_hex(c) for c in s]
