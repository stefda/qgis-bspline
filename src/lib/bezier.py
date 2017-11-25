import math


def distance(p0, p1):
    """ Computes the Euclidean distance of the given points.

    :param p0
    :type p0: float[]

    :param p1
    :type p1: float[]
    """
    return math.sqrt(math.pow(p0[0] - p1[0], 2) + math.pow(p0[1] - p1[1], 2))


def polyLength(points):
    """ Computes the length of the polyline represented by the given points.

    :param points:
    :type points: float[][]

    :return: float
    """
    length = 0
    for i in range(0, len(points) - 1):
        length += distance(points[i], points[i + 1])
    return length


def approxLength(points):
    """ Approximates the length of a cubic bezier specified by the given points.

    :param points:
    :type points: float[][]

    :return: float
    """
    if len(points) != 4:
        raise ValueError('Cannot approximate length other than that of a cubic bezier.')

    pStart = points[0]
    pEnd = points[3]

    lower = distance(pStart, pEnd)
    upper = polyLength(points)

    return lower + (upper - lower) / 2


def vect(p0, p1):
    return [p1[0] - p0[0], p1[1] - p0[1]]


def mv(p0, p1, d):
    v = vect(p0, p1)
    return [d * v[0] + p0[0], d * v[1] + p0[1]]


def bspline(points, start=None, end=None):
    """ Computes the control points of a bezier curve.

    The function expects exactly four points in all of its parameters, e.g. if both `start` and `end` are given then the
    list of points must have precisely two elements.

    :param points:
    :type points: float[][]

    :param start:
    :type start: float[]

    :param end:
    :type end: float[]

    :return: float[][]
    """
    hasStart = start is not None
    hasEnd = end is not None
    if len(points) + int(hasStart) + int(hasEnd) != 4:
        raise ValueError('bpline needs exactly four points.')

    F13 = float(1.0 / 3.0)
    F23 = float(2.0 / 3.0)

    if hasStart:
        c0 = start
    else:
        h0 = mv(points[0], points[1], F23)
        h1 = mv(points[1], points[2], F13)
        c0 = mv(h0, h1, 0.5)

    offset = 0 if hasStart else 1
    c1 = mv(points[0 + offset], points[1 + offset], F13)
    c2 = mv(points[0 + offset], points[1 + offset], F23)

    if hasEnd:
        c3 = end
    else:
        h0 = mv(points[0 + offset], points[1 + offset], F23)
        h1 = mv(points[1 + offset], points[2 + offset], F13)
        c3 = mv(h0, h1, 0.5)

    return [c0, c1, c2, c3]


def bezier(points, t):
    """ Interpolate a bezier curve at t from the given points.

    :param points:
    :type points: float[]

    :param t:
    :type t: float

    :return: float[]
    """
    if t == 0: return points[0]
    if t == 1: return points[-1]

    p = points
    mt = 1 - t

    mt2 = mt * mt
    t2 = t * t

    a = mt2 * mt
    b = mt2 * t * 3
    c = mt * t2 * 3
    d = t * t2

    x = a * p[0][0] + b * p[1][0] + c * p[2][0] + d * p[3][0]
    y = a * p[0][1] + b * p[1][1] + c * p[2][1] + d * p[3][1]

    return [x, y]


class Cubic:
    def __init__(self, points):
        self.points = points

    def evaluate(self, steps):
        steps = steps or 100
        lut = []
        for step in range(0, steps + 1):
            lut.append(bezier(self.points, float(step) / steps))
        return lut
