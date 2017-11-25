from PyQt4.QtGui import QIcon, QAction
from qgis.gui import QgsMapTool
from bspline_canvas import BSplineCanvas


class BSpline(QgsMapTool):
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.bsplineCanvas = BSplineCanvas(self.canvas)

        QgsMapTool.__init__(self, self.canvas)

        # create toolbar
        self.toolbar = self.iface.addToolBar(u'BSpline')
        self.toolbar.setObjectName(u'BSpline')

        # initialize action
        self.action = None

    def initGui(self):
        icon = QIcon(':/plugins/BSpline/icon.png')
        self.action = QAction(icon, u'B-Spline', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.action.setEnabled(True)

        self.toolbar.addAction(self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.bsplineCanvas.clear()

        # remove button from the toolbar
        self.iface.removeToolBarIcon(self.action)

        # remove the toolbar
        del self.toolbar

    def run(self, action):
        self.canvas.setMapTool(self)
        self.action.setChecked(True)

    def canvasPressEvent(self, event):
        self.bsplineCanvas.pressEvent(event.pos())

    def canvasMoveEvent(self, event):
        self.bsplineCanvas.moveEvent(event.pos())
