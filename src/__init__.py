# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BSpline
                                 A QGIS plugin
 Tool to digitize b-splines
                             -------------------
        begin                : 2017-10-29
        copyright            : (C) 2017 by Pocketsail Ltd.
        email                : stefda@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load BSpline class from file BSpline.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .bspline import BSpline
    return BSpline(iface)
