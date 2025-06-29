# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meshInspector.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_meshInspector(object):
    def setupUi(self, meshInspector):
        if not meshInspector.objectName():
            meshInspector.setObjectName(u"meshInspector")
        meshInspector.resize(950, 500)
        meshInspector.setMinimumSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(meshInspector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnRefreshList = QToolButton(meshInspector)
        self.btnRefreshList.setObjectName(u"btnRefreshList")
        self.btnRefreshList.setMinimumSize(QSize(0, 30))
        self.btnRefreshList.setLayoutDirection(Qt.RightToLeft)
        self.btnRefreshList.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.btnRefreshList)

        self.line_2 = QFrame(meshInspector)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.lbListOptions = QLabel(meshInspector)
        self.lbListOptions.setObjectName(u"lbListOptions")

        self.horizontalLayout.addWidget(self.lbListOptions)

        self.cbDisplaySubStatsInList = QCheckBox(meshInspector)
        self.cbDisplaySubStatsInList.setObjectName(u"cbDisplaySubStatsInList")

        self.horizontalLayout.addWidget(self.cbDisplaySubStatsInList)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line = QFrame(meshInspector)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.btnExpandAll = QPushButton(meshInspector)
        self.btnExpandAll.setObjectName(u"btnExpandAll")
        self.btnExpandAll.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.btnExpandAll)

        self.btnCollapseAll = QPushButton(meshInspector)
        self.btnCollapseAll.setObjectName(u"btnCollapseAll")
        self.btnCollapseAll.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.btnCollapseAll)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.inspectorTree = QTreeWidget(meshInspector)
        self.inspectorTree.setObjectName(u"inspectorTree")
        self.inspectorTree.setAlternatingRowColors(True)
        self.inspectorTree.setColumnCount(5)
        self.inspectorTree.header().setDefaultSectionSize(100)

        self.verticalLayout.addWidget(self.inspectorTree)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lbUserHintTitle = QLabel(meshInspector)
        self.lbUserHintTitle.setObjectName(u"lbUserHintTitle")

        self.horizontalLayout_2.addWidget(self.lbUserHintTitle)

        self.lbUserHint = QLabel(meshInspector)
        self.lbUserHint.setObjectName(u"lbUserHint")

        self.horizontalLayout_2.addWidget(self.lbUserHint)

        self.buttonBox = QDialogButtonBox(meshInspector)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(meshInspector)
        self.buttonBox.accepted.connect(meshInspector.accept)
        self.buttonBox.rejected.connect(meshInspector.reject)

        QMetaObject.connectSlotsByName(meshInspector)
    # setupUi

    def retranslateUi(self, meshInspector):
        meshInspector.setWindowTitle(QCoreApplication.translate("meshInspector", u"Mesh Inspector", None))
#if QT_CONFIG(tooltip)
        self.btnRefreshList.setToolTip(QCoreApplication.translate("meshInspector", u"Refresh list", None))
#endif // QT_CONFIG(tooltip)
        self.btnRefreshList.setText(QCoreApplication.translate("meshInspector", u"Refresh Statistics", None))
        self.lbListOptions.setText(QCoreApplication.translate("meshInspector", u"List options:", None))
#if QT_CONFIG(tooltip)
        self.cbDisplaySubStatsInList.setToolTip(QCoreApplication.translate("meshInspector", u"Display per-channel infos directly in the list (otherwise accessible by hovering vertex count or name)", None))
#endif // QT_CONFIG(tooltip)
        self.cbDisplaySubStatsInList.setText(QCoreApplication.translate("meshInspector", u"Display per-channel statistics in list", None))
#if QT_CONFIG(tooltip)
        self.btnExpandAll.setToolTip(QCoreApplication.translate("meshInspector", u"Expand all in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnExpandAll.setText(QCoreApplication.translate("meshInspector", u"Expand All", None))
#if QT_CONFIG(tooltip)
        self.btnCollapseAll.setToolTip(QCoreApplication.translate("meshInspector", u"Collapse all in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnCollapseAll.setText(QCoreApplication.translate("meshInspector", u"Collapse All", None))
        ___qtreewidgetitem = self.inspectorTree.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("meshInspector", u"Triangle count", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("meshInspector", u"~Vertex count", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("meshInspector", u"~Draw count", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("meshInspector", u"~Efficiency", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("meshInspector", u"Hierarchy", None));
        self.lbUserHintTitle.setText(QCoreApplication.translate("meshInspector", u"TIP:", None))
        self.lbUserHint.setText(QCoreApplication.translate("meshInspector", u"double click selects object in scene.", None))
    # retranslateUi

