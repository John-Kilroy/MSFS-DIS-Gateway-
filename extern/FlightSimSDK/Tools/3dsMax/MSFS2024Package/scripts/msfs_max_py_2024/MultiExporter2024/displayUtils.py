"""Multi exporter UI display utilities"""

from PySide2.QtWidgets import *

"""
TEXT DISPLAY
"""
# display value as text as value (!)
def errorText(value):
    return "{0} (!)".format(value)

# display value as text as value (Ignored)
def ignoredText(value):
    return "{0} (Ignored)".format(value)

# display value as text as value%
def percentText(value):
    return "{0}%".format(value)

"""
QT STUFF
"""
# Change label text color
def setLabelColor(label, color):
    p = label.palette()
    p.setColor(label.foregroundRole(), color)
    label.setPalette(p)

def newCellWidget(parent):
    newWidget = QWidget()
    newLayout = QHBoxLayout(parent)
    newLayout.setContentsMargins(4, 0, 4, 0)
    newWidget.setLayout(newLayout)
    return newWidget, newLayout

def newHorizontalSpacer():
    return QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
