# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TT_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_TextureTool(object):
    def setupUi(self, TextureTool):
        if not TextureTool.objectName():
            TextureTool.setObjectName(u"TextureTool")
        TextureTool.resize(1750, 1000)
        TextureTool.setDockNestingEnabled(False)
        self.actionRemoveUnusedTextures = QAction(TextureTool)
        self.actionRemoveUnusedTextures.setObjectName(u"actionRemoveUnusedTextures")
        self.actionRefreshTool = QAction(TextureTool)
        self.actionRefreshTool.setObjectName(u"actionRefreshTool")
        self.actionResetTool = QAction(TextureTool)
        self.actionResetTool.setObjectName(u"actionResetTool")
        self.centralwidget = QWidget(TextureTool)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(7, 7, 7, 7)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 7, -1, 7)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.btnOpenPath = QPushButton(self.groupBox_2)
        self.btnOpenPath.setObjectName(u"btnOpenPath")

        self.horizontalLayout_5.addWidget(self.btnOpenPath)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter_2.setHandleWidth(6)
        self.splitter_2.setChildrenCollapsible(False)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(7, 7, 7, 7)
        self.tabTextureWidget = QTabWidget(self.layoutWidget)
        self.tabTextureWidget.setObjectName(u"tabTextureWidget")
        self.Textures = QWidget()
        self.Textures.setObjectName(u"Textures")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Textures.sizePolicy().hasHeightForWidth())
        self.Textures.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.Textures)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(7, 7, 7, 7)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(7, 5, 7, 5)
        self.splitter = QSplitter(self.Textures)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(11)
        self.splitter.setChildrenCollapsible(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(7, 7, 7, 7)
        self.groupBox_3 = QGroupBox(self.verticalLayoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.ckQualityHigh = QCheckBox(self.groupBox_3)
        self.ckQualityHigh.setObjectName(u"ckQualityHigh")

        self.horizontalLayout_8.addWidget(self.ckQualityHigh)

        self.line_4 = QFrame(self.groupBox_3)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_4)

        self.ckAlphaPreserv = QCheckBox(self.groupBox_3)
        self.ckAlphaPreserv.setObjectName(u"ckAlphaPreserv")

        self.horizontalLayout_8.addWidget(self.ckAlphaPreserv)

        self.line_3 = QFrame(self.groupBox_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_3)

        self.ckNoReduc = QCheckBox(self.groupBox_3)
        self.ckNoReduc.setObjectName(u"ckNoReduc")

        self.horizontalLayout_8.addWidget(self.ckNoReduc)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_2)

        self.ckNoMipmap = QCheckBox(self.groupBox_3)
        self.ckNoMipmap.setObjectName(u"ckNoMipmap")

        self.horizontalLayout_8.addWidget(self.ckNoMipmap)

        self.line_5 = QFrame(self.groupBox_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_5)

        self.ckPreComputedInvAvg = QCheckBox(self.groupBox_3)
        self.ckPreComputedInvAvg.setObjectName(u"ckPreComputedInvAvg")

        self.horizontalLayout_8.addWidget(self.ckPreComputedInvAvg)

        self.line = QFrame(self.groupBox_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line)

        self.ckAnis0 = QCheckBox(self.groupBox_3)
        self.ckAnis0.setObjectName(u"ckAnis0")

        self.horizontalLayout_8.addWidget(self.ckAnis0)

        self.ckAnis2 = QCheckBox(self.groupBox_3)
        self.ckAnis2.setObjectName(u"ckAnis2")

        self.horizontalLayout_8.addWidget(self.ckAnis2)

        self.ckAnis4 = QCheckBox(self.groupBox_3)
        self.ckAnis4.setObjectName(u"ckAnis4")

        self.horizontalLayout_8.addWidget(self.ckAnis4)

        self.ckAnis8 = QCheckBox(self.groupBox_3)
        self.ckAnis8.setObjectName(u"ckAnis8")

        self.horizontalLayout_8.addWidget(self.ckAnis8)

        self.ckAnis16 = QCheckBox(self.groupBox_3)
        self.ckAnis16.setObjectName(u"ckAnis16")

        self.horizontalLayout_8.addWidget(self.ckAnis16)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(7, 7, 7, 7)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.filterBar = QLineEdit(self.verticalLayoutWidget)
        self.filterBar.setObjectName(u"filterBar")

        self.horizontalLayout_7.addWidget(self.filterBar)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.treeTexture = QTreeWidget(self.verticalLayoutWidget)
        self.treeTexture.setObjectName(u"treeTexture")
        sizePolicy1.setHeightForWidth(self.treeTexture.sizePolicy().hasHeightForWidth())
        self.treeTexture.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.treeTexture)

        self.groupBox = QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnAddGroup = QPushButton(self.groupBox)
        self.btnAddGroup.setObjectName(u"btnAddGroup")

        self.horizontalLayout_4.addWidget(self.btnAddGroup)

        self.btnAddTexture = QPushButton(self.groupBox)
        self.btnAddTexture.setObjectName(u"btnAddTexture")

        self.horizontalLayout_4.addWidget(self.btnAddTexture)

        self.btnRemoveGroup = QPushButton(self.groupBox)
        self.btnRemoveGroup.setObjectName(u"btnRemoveGroup")

        self.horizontalLayout_4.addWidget(self.btnRemoveGroup)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.btnExpandAll = QPushButton(self.groupBox)
        self.btnExpandAll.setObjectName(u"btnExpandAll")

        self.horizontalLayout_4.addWidget(self.btnExpandAll)

        self.btnCollapseAll = QPushButton(self.groupBox)
        self.btnCollapseAll.setObjectName(u"btnCollapseAll")

        self.horizontalLayout_4.addWidget(self.btnCollapseAll)


        self.verticalLayout.addWidget(self.groupBox)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(7, 7, 7, 7)
        self.treeFlags = QTreeWidget(self.verticalLayoutWidget_2)
        __qtreewidgetitem = QTreeWidgetItem(self.treeFlags)
        __qtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeFlags)
        __qtreewidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem1.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem2 = QTreeWidgetItem(self.treeFlags)
        __qtreewidgetitem2.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem2.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeFlags)
        __qtreewidgetitem3.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem3.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem4 = QTreeWidgetItem(self.treeFlags)
        __qtreewidgetitem4.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled);
        __qtreewidgetitem5 = QTreeWidgetItem(__qtreewidgetitem4)
        __qtreewidgetitem5.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem5.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem6 = QTreeWidgetItem(__qtreewidgetitem4)
        __qtreewidgetitem6.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem6.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem7 = QTreeWidgetItem(__qtreewidgetitem4)
        __qtreewidgetitem7.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem7.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem8 = QTreeWidgetItem(__qtreewidgetitem4)
        __qtreewidgetitem8.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem8.setCheckState(0, Qt.Unchecked);
        __qtreewidgetitem9 = QTreeWidgetItem(__qtreewidgetitem4)
        __qtreewidgetitem9.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        __qtreewidgetitem9.setCheckState(0, Qt.Unchecked);
        self.treeFlags.setObjectName(u"treeFlags")
        sizePolicy1.setHeightForWidth(self.treeFlags.sizePolicy().hasHeightForWidth())
        self.treeFlags.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.treeFlags)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(7, 11, 7, 11)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btnApplyFlagsTicked = QPushButton(self.verticalLayoutWidget_2)
        self.btnApplyFlagsTicked.setObjectName(u"btnApplyFlagsTicked")

        self.horizontalLayout_2.addWidget(self.btnApplyFlagsTicked)

        self.btnApplyFlags = QPushButton(self.verticalLayoutWidget_2)
        self.btnApplyFlags.setObjectName(u"btnApplyFlags")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btnApplyFlags.sizePolicy().hasHeightForWidth())
        self.btnApplyFlags.setSizePolicy(sizePolicy2)
        self.btnApplyFlags.setAutoRepeat(False)
        self.btnApplyFlags.setAutoExclusive(False)

        self.horizontalLayout_2.addWidget(self.btnApplyFlags)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_6.addWidget(self.splitter)


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.tabTextureWidget.addTab(self.Textures, "")

        self.verticalLayout_3.addWidget(self.tabTextureWidget)

        self.XMLGrpBox = QGroupBox(self.layoutWidget)
        self.XMLGrpBox.setObjectName(u"XMLGrpBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.XMLGrpBox.sizePolicy().hasHeightForWidth())
        self.XMLGrpBox.setSizePolicy(sizePolicy3)
        self.XMLGrpBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.verticalLayout_11 = QVBoxLayout(self.XMLGrpBox)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(-1, 7, -1, 7)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(7, 7, 7, 7)
        self.horizontalSpacer = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnTickedTextures = QPushButton(self.XMLGrpBox)
        self.btnTickedTextures.setObjectName(u"btnTickedTextures")
        sizePolicy2.setHeightForWidth(self.btnTickedTextures.sizePolicy().hasHeightForWidth())
        self.btnTickedTextures.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.btnTickedTextures)

        self.btnSelectedTextures = QPushButton(self.XMLGrpBox)
        self.btnSelectedTextures.setObjectName(u"btnSelectedTextures")

        self.horizontalLayout.addWidget(self.btnSelectedTextures)

        self.btnAllTextures = QPushButton(self.XMLGrpBox)
        self.btnAllTextures.setObjectName(u"btnAllTextures")

        self.horizontalLayout.addWidget(self.btnAllTextures)


        self.verticalLayout_11.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.XMLGrpBox)

        self.splitter_2.addWidget(self.layoutWidget)
        self.scrollArea = QScrollArea(self.splitter_2)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(0, 100))
        self.scrollArea.setSizeIncrement(QSize(0, 0))
        self.scrollArea.setBaseSize(QSize(0, 0))
        self.scrollArea.setFrameShadow(QFrame.Sunken)
        self.scrollArea.setLineWidth(5)
        self.scrollArea.setMidLineWidth(2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1712, 98))
        self.loggerAreaVerticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.loggerAreaVerticalLayout.setObjectName(u"loggerAreaVerticalLayout")
        self.loggerAreaVerticalLayout.setContentsMargins(-1, 7, -1, 7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.splitter_2.addWidget(self.scrollArea)

        self.verticalLayout_4.addWidget(self.splitter_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        TextureTool.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(TextureTool)
        self.statusBar.setObjectName(u"statusBar")
        TextureTool.setStatusBar(self.statusBar)
        self.menuBar = QMenuBar(TextureTool)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1750, 26))
        self.menuTextures = QMenu(self.menuBar)
        self.menuTextures.setObjectName(u"menuTextures")
        TextureTool.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuTextures.menuAction())
        self.menuTextures.addAction(self.actionRefreshTool)
        self.menuTextures.addAction(self.actionRemoveUnusedTextures)
        self.menuTextures.addAction(self.actionResetTool)

        self.retranslateUi(TextureTool)

        self.tabTextureWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TextureTool)
    # setupUi

    def retranslateUi(self, TextureTool):
        TextureTool.setWindowTitle(QCoreApplication.translate("TextureTool", u"Texture Tool", None))
        self.actionRemoveUnusedTextures.setText(QCoreApplication.translate("TextureTool", u"Remove unused textures in scene", None))
        self.actionRefreshTool.setText(QCoreApplication.translate("TextureTool", u"Refresh Tool", None))
#if QT_CONFIG(tooltip)
        self.actionRefreshTool.setToolTip(QCoreApplication.translate("TextureTool", u"Refresh the Tool", None))
#endif // QT_CONFIG(tooltip)
        self.actionResetTool.setText(QCoreApplication.translate("TextureTool", u"Reset Tool", None))
#if QT_CONFIG(tooltip)
        self.actionResetTool.setToolTip(QCoreApplication.translate("TextureTool", u"Reset Tool's saved DATA from scene", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("TextureTool", u"Utilities", None))
#if QT_CONFIG(tooltip)
        self.btnOpenPath.setToolTip(QCoreApplication.translate("TextureTool", u"Open the path of selected texture", None))
#endif // QT_CONFIG(tooltip)
        self.btnOpenPath.setText(QCoreApplication.translate("TextureTool", u"Open Texture Path", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("TextureTool", u"Filters", None))
        self.ckQualityHigh.setText(QCoreApplication.translate("TextureTool", u"Quality High", None))
        self.ckAlphaPreserv.setText(QCoreApplication.translate("TextureTool", u"Alpha Preservation", None))
        self.ckNoReduc.setText(QCoreApplication.translate("TextureTool", u"No Reduction", None))
        self.ckNoMipmap.setText(QCoreApplication.translate("TextureTool", u"No Mipmaps", None))
        self.ckPreComputedInvAvg.setText(QCoreApplication.translate("TextureTool", u"PreComputed Inverse Average", None))
        self.ckAnis0.setText(QCoreApplication.translate("TextureTool", u"Anisotropic x0", None))
        self.ckAnis2.setText(QCoreApplication.translate("TextureTool", u"Anisotropic x2", None))
        self.ckAnis4.setText(QCoreApplication.translate("TextureTool", u"Anisotropic x4", None))
        self.ckAnis8.setText(QCoreApplication.translate("TextureTool", u"Anisotropic x8", None))
        self.ckAnis16.setText(QCoreApplication.translate("TextureTool", u"Anisotropic x16", None))
        self.label.setText(QCoreApplication.translate("TextureTool", u"Search :", None))
        self.filterBar.setPlaceholderText(QCoreApplication.translate("TextureTool", u"Enter a texture name to filter", None))
        ___qtreewidgetitem = self.treeTexture.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("TextureTool", u"Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("TextureTool", u"Texture", None));
        self.groupBox.setTitle(QCoreApplication.translate("TextureTool", u"Options", None))
#if QT_CONFIG(tooltip)
        self.btnAddGroup.setToolTip(QCoreApplication.translate("TextureTool", u"Add an empty Group or a Group applied to the setected Texture(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddGroup.setText(QCoreApplication.translate("TextureTool", u"Add Group", None))
#if QT_CONFIG(tooltip)
        self.btnAddTexture.setToolTip(QCoreApplication.translate("TextureTool", u"Add new Texture(s) item(s) if Texture(s) with the same name and different path is referenced in the scene.", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddTexture.setText(QCoreApplication.translate("TextureTool", u"Add Texture(s)", None))
#if QT_CONFIG(tooltip)
        self.btnRemoveGroup.setToolTip(QCoreApplication.translate("TextureTool", u"Remove the selected Group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnRemoveGroup.setText(QCoreApplication.translate("TextureTool", u"Remove Group(s)", None))
#if QT_CONFIG(tooltip)
        self.btnExpandAll.setToolTip(QCoreApplication.translate("TextureTool", u"Expand all the \"Groups\"", None))
#endif // QT_CONFIG(tooltip)
        self.btnExpandAll.setText(QCoreApplication.translate("TextureTool", u"Expand All", None))
#if QT_CONFIG(tooltip)
        self.btnCollapseAll.setToolTip(QCoreApplication.translate("TextureTool", u"Collapse all the \"Groups\"", None))
#endif // QT_CONFIG(tooltip)
        self.btnCollapseAll.setText(QCoreApplication.translate("TextureTool", u"Collapse All", None))
        ___qtreewidgetitem1 = self.treeFlags.headerItem()
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("TextureTool", u"Flags", None));

        __sortingEnabled = self.treeFlags.isSortingEnabled()
        self.treeFlags.setSortingEnabled(False)
        ___qtreewidgetitem2 = self.treeFlags.topLevelItem(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("TextureTool", u"Quality High", None));
        ___qtreewidgetitem3 = self.treeFlags.topLevelItem(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("TextureTool", u"Alpha Preservation", None));
#if QT_CONFIG(tooltip)
        ___qtreewidgetitem3.setToolTip(0, QCoreApplication.translate("TextureTool", u"*IMPORTANT* To be checked only if the texture has 4 slots (RGBA)", None));
#endif // QT_CONFIG(tooltip)
        ___qtreewidgetitem4 = self.treeFlags.topLevelItem(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("TextureTool", u"No Reduction", None));
        ___qtreewidgetitem5 = self.treeFlags.topLevelItem(3)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("TextureTool", u"No Mipmaps", None));
        ___qtreewidgetitem6 = self.treeFlags.topLevelItem(4)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("TextureTool", u"Anisotrpic", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem6.child(0)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("TextureTool", u"0x (Standard)", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem6.child(1)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("TextureTool", u"2x (High)", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem6.child(2)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("TextureTool", u"4x (Very High)", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem6.child(3)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("TextureTool", u"8x (Extreme)", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem6.child(4)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("TextureTool", u"16x (Insane)", None));
        self.treeFlags.setSortingEnabled(__sortingEnabled)

#if QT_CONFIG(tooltip)
        self.btnApplyFlagsTicked.setToolTip(QCoreApplication.translate("TextureTool", u"Apply ticked FLAGS to ticked Texture(s) and Group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnApplyFlagsTicked.setText(QCoreApplication.translate("TextureTool", u"Apply To Ticked", None))
#if QT_CONFIG(tooltip)
        self.btnApplyFlags.setToolTip(QCoreApplication.translate("TextureTool", u"Apply ticked FLAGS to selected Texture(s) and Group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnApplyFlags.setText(QCoreApplication.translate("TextureTool", u"Apply To Selected", None))
        self.tabTextureWidget.setTabText(self.tabTextureWidget.indexOf(self.Textures), QCoreApplication.translate("TextureTool", u"Textures", None))
        self.XMLGrpBox.setTitle(QCoreApplication.translate("TextureTool", u"Generate Texture Lib XML", None))
#if QT_CONFIG(tooltip)
        self.btnTickedTextures.setToolTip(QCoreApplication.translate("TextureTool", u"Generate XML for ticked Texture(s) and Group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnTickedTextures.setText(QCoreApplication.translate("TextureTool", u"Ticked Textures", None))
#if QT_CONFIG(tooltip)
        self.btnSelectedTextures.setToolTip(QCoreApplication.translate("TextureTool", u"Generate XML for selected Texture(s) and Group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnSelectedTextures.setText(QCoreApplication.translate("TextureTool", u"Selected Textures", None))
#if QT_CONFIG(tooltip)
        self.btnAllTextures.setToolTip(QCoreApplication.translate("TextureTool", u"Generate XML for all Texture(s) and Group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnAllTextures.setText(QCoreApplication.translate("TextureTool", u"All Textures", None))
        self.menuTextures.setTitle(QCoreApplication.translate("TextureTool", u"Tool", None))
    # retranslateUi

