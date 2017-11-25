from PyQt4.QtGui import QColor
from qgis.core import QGis, QgsMessageLog, QgsPoint
from qgis.gui import QgsRubberBand, QgsVertexMarker
from lib.bezier import bspline
from lib.bezier import Cubic


class BSplineCanvas:
    VERTEX_SHAPE = QgsVertexMarker.ICON_BOX
    VERTEX_SIZE = 11
    VERTEX_PEN_WIDTH = 2
    VERTEX_COLOR = '#f4417d'
    CURVE_PEN_WIDTH = 1
    CURVE_COLOR = '#ff0000'

    def __init__(self, canvas):
        self.canvas = canvas
        self.curves = []
        self.vertices = []
        self.points = []
        self.controlPoints = []
        self.knots = []
        self.wasOverFirstVertex = False

    def pressEvent(self, point):
        """ todo: Doc

        :param point:
        :type point: QPoint

        :return: point: QPoint
        """
        mapCoords = self.getMapCoords(point)
        vertex = self.createVertex(mapCoords)
        point = [mapCoords.x(), mapCoords.y()]

        self.vertices.append(vertex)
        self.points.append(point)
        self.controlPoints.append([point] * 4)
        self.knots.append(point)
        self.curves.append(self.createCurve())

    def moveEvent(self, coords):
        """ todo: Doc

        :param coords:
        :type coords: QPoint
        """
        mapCoords = self.getMapCoords(coords)
        point = [mapCoords.x(), mapCoords.y()]
        if len(self.points) > 0:
            self.controlPoints[-1] = bspline([self.points[-1], point], self.knots[-1], point)

        if len(self.points) > 1:
            self.controlPoints[-2] = bspline([self.points[-2], self.points[-1], point], self.knots[-2], None)
            self.knots[-1] = self.controlPoints[-2][3]

        overFirstVertex = self.isOverFirstVertex(coords)
        if overFirstVertex and not self.wasOverFirstVertex:
            self.vertices[0].setPenWidth(self.VERTEX_SIZE)
            self.vertices[0].setIconSize(self.VERTEX_PEN_WIDTH)
            self.vertices[0].updateCanvas()
            self.wasOverFirstVertex = True
        elif not overFirstVertex and self.wasOverFirstVertex:
            self.vertices[0].setPenWidth(self.VERTEX_PEN_WIDTH)
            self.vertices[0].setIconSize(self.VERTEX_SIZE)
            self.vertices[0].updateCanvas()
            self.wasOverFirstVertex = False

        self.redrawTail()

    def redrawTail(self):
        """ Redraws the last (two) curve(s) of the bspline using the available control points.
        """
        if len(self.curves) == 0:
            # return fast if there are no curves
            return

        # todo: interpolation steps based on estimated curve length
        points = [Cubic(self.controlPoints[-2]).evaluate(10)] if len(self.curves) > 1 else []
        points.append(Cubic(self.controlPoints[-1]).evaluate(10))

        # ensure the first (and last) points are the same as their corresponding knots
        points[-1][0] = self.knots[-1]
        if len(self.curves) > 1:
            points[-2][0] = self.knots[-2]
            points[-2][-1] = self.knots[-1]

        # reset the last (two) curve(s) with the points computed above
        for i, curve in enumerate(self.curves[-2:]):
            curve.reset()
            for j in range(0, len(points[i]) - 1):
                point = points[i][j]
                curve.addPoint(QgsPoint(point[0], point[1]), False)

        # add-redraw the last point of the reset curves
        for i, curve in enumerate(self.curves[-2:]):
            curve.addPoint(QgsPoint(points[i][-1][0], points[i][-1][1]), True)

    def clear(self):
        # remove all vertices
        for vertex in self.vertices:
            self.canvas.scene().removeItem(vertex)
        self.vertices = []

        # remove all curves
        for curve in self.curves:
            self.canvas.scene().removeItem(curve)
        self.vertices = []

        self.vertices = []
        self.curves = []
        self.points = []
        self.knots = []

    def getMapCoords(self, point):
        """ Converts the given point to map coordinates.

        :param point:
        :type point: QPoint

        :return: QPoint
        """
        return self.canvas.getCoordinateTransform().toMapCoordinates(point.x(), point.y())

    def isOverFirstVertex(self, coords):
        """ Decides if the given coords are within the bbox of the first vertex.

        :param coords:
        :type coords: QgsPoint

        :return: bool
        """
        if len(self.vertices) == 0:
            # return fast if there are no vertices
            return False

        vertex = self.vertices[0]
        br = vertex.boundingRect()
        left = vertex.x() + br.left()
        right = vertex.x() + br.right()
        top = vertex.y() + br.top()
        bottom = vertex.y() + br.bottom()
        return left <= coords.x() <= right and top <= coords.y() <= bottom

    def createVertex(self, center):
        """ Creates a new vertex at the given map coordinates.

        :param center:
        :type center: QPoint

        :return: QgsVertexMarker
        """
        vertex = QgsVertexMarker(self.canvas)
        vertex.setIconType(self.VERTEX_SHAPE)
        vertex.setColor(QColor(self.VERTEX_COLOR))
        vertex.setPenWidth(self.VERTEX_PEN_WIDTH)
        vertex.setIconSize(self.VERTEX_SIZE)
        vertex.setCenter(center)
        return vertex

    def createCurve(self):
        """ Creates a new rubber band curve.

        :return: QgsRubberBand
        """
        curve = QgsRubberBand(self.canvas, QGis.Line)
        curve.setColor(QColor(self.CURVE_COLOR))
        curve.setWidth(self.CURVE_PEN_WIDTH)
        return curve
