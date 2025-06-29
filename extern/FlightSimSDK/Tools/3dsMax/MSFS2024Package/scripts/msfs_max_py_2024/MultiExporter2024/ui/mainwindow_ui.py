# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MultiExporter(object):
    def setupUi(self, MultiExporter):
        if not MultiExporter.objectName():
            MultiExporter.setObjectName(u"MultiExporter")
        MultiExporter.resize(1498, 867)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MultiExporter.sizePolicy().hasHeightForWidth())
        MultiExporter.setSizePolicy(sizePolicy)
        MultiExporter.setMinimumSize(QSize(500, 773))
        self.openTextureToolAction = QAction(MultiExporter)
        self.openTextureToolAction.setObjectName(u"openTextureToolAction")
        self.resolveUniqueIDsAction = QAction(MultiExporter)
        self.resolveUniqueIDsAction.setObjectName(u"resolveUniqueIDsAction")
        self.importglTFConfigurationAction = QAction(MultiExporter)
        self.importglTFConfigurationAction.setObjectName(u"importglTFConfigurationAction")
        self.saveglTFConfigurationAction = QAction(MultiExporter)
        self.saveglTFConfigurationAction.setObjectName(u"saveglTFConfigurationAction")
        self.saveglTFConfigurationAction.setVisible(True)
        self.runResolveUniqueIDsAction = QAction(MultiExporter)
        self.runResolveUniqueIDsAction.setObjectName(u"runResolveUniqueIDsAction")
        self.actionRefresh = QAction(MultiExporter)
        self.actionRefresh.setObjectName(u"actionRefresh")
        self.centralwidget = QWidget(MultiExporter)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter_areas = QSplitter(self.centralwidget)
        self.splitter_areas.setObjectName(u"splitter_areas")
        sizePolicy.setHeightForWidth(self.splitter_areas.sizePolicy().hasHeightForWidth())
        self.splitter_areas.setSizePolicy(sizePolicy)
        self.splitter_areas.setMinimumSize(QSize(0, 0))
        self.splitter_areas.setOrientation(Qt.Vertical)
        self.splitter_areas.setChildrenCollapsible(False)
        self.scrollArea = QScrollArea(self.splitter_areas)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 500))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1474, 685))
        self.scrollAreaWidgetContents.setMinimumSize(QSize(300, 400))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.headerBox = QGroupBox(self.scrollAreaWidgetContents)
        self.headerBox.setObjectName(u"headerBox")
        sizePolicy1.setHeightForWidth(self.headerBox.sizePolicy().hasHeightForWidth())
        self.headerBox.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.headerBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btnRefresh = QToolButton(self.headerBox)
        self.btnRefresh.setObjectName(u"btnRefresh")
        self.btnRefresh.setMinimumSize(QSize(80, 30))
        self.btnRefresh.setLayoutDirection(Qt.RightToLeft)
        self.btnRefresh.setIconSize(QSize(20, 20))
        self.btnRefresh.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnRefresh)

        self.lbQuickOptions = QLabel(self.headerBox)
        self.lbQuickOptions.setObjectName(u"lbQuickOptions")

        self.horizontalLayout_2.addWidget(self.lbQuickOptions)

        self.cbAlwaysSelectInScene = QCheckBox(self.headerBox)
        self.cbAlwaysSelectInScene.setObjectName(u"cbAlwaysSelectInScene")

        self.horizontalLayout_2.addWidget(self.cbAlwaysSelectInScene)

        self.cbSelectInSceneSelectsChildren = QCheckBox(self.headerBox)
        self.cbSelectInSceneSelectsChildren.setObjectName(u"cbSelectInSceneSelectsChildren")
        self.cbSelectInSceneSelectsChildren.setChecked(True)

        self.horizontalLayout_2.addWidget(self.cbSelectInSceneSelectsChildren)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.lbCoin = QLabel(self.headerBox)
        self.lbCoin.setObjectName(u"lbCoin")

        self.horizontalLayout_2.addWidget(self.lbCoin)

        self.coin = QToolButton(self.headerBox)
        self.coin.setObjectName(u"coin")
        self.coin.setMinimumSize(QSize(30, 30))
        self.coin.setAutoRaise(True)

        self.horizontalLayout_2.addWidget(self.coin)

        self.horizontalSpacer_4 = QSpacerItem(673, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.btnOpenExportFolder = QToolButton(self.headerBox)
        self.btnOpenExportFolder.setObjectName(u"btnOpenExportFolder")
        self.btnOpenExportFolder.setMinimumSize(QSize(150, 30))
        self.btnOpenExportFolder.setLayoutDirection(Qt.RightToLeft)
        self.btnOpenExportFolder.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.btnOpenExportFolder)


        self.verticalLayout.addWidget(self.headerBox)

        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.tabWidget.setTabsClosable(False)
        self.tabObjects = QWidget()
        self.tabObjects.setObjectName(u"tabObjects")
        sizePolicy.setHeightForWidth(self.tabObjects.sizePolicy().hasHeightForWidth())
        self.tabObjects.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.tabObjects)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(7, 5, 7, -1)
        self.btnHierarchyViewFilter = QToolButton(self.tabObjects)
        self.btnHierarchyViewFilter.setObjectName(u"btnHierarchyViewFilter")
        self.btnHierarchyViewFilter.setCheckable(True)
        self.btnHierarchyViewFilter.setChecked(True)

        self.horizontalLayout_3.addWidget(self.btnHierarchyViewFilter)

        self.cbFilterExportableOnly = QCheckBox(self.tabObjects)
        self.cbFilterExportableOnly.setObjectName(u"cbFilterExportableOnly")
        self.cbFilterExportableOnly.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.cbFilterExportableOnly)

        self.cbFilterVisibleOnly = QCheckBox(self.tabObjects)
        self.cbFilterVisibleOnly.setObjectName(u"cbFilterVisibleOnly")
        self.cbFilterVisibleOnly.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.cbFilterVisibleOnly)

        self.cbFilterLodsOnly = QCheckBox(self.tabObjects)
        self.cbFilterLodsOnly.setObjectName(u"cbFilterLodsOnly")
        self.cbFilterLodsOnly.setEnabled(True)
        self.cbFilterLodsOnly.setChecked(False)

        self.horizontalLayout_3.addWidget(self.cbFilterLodsOnly)

        self.sbFilterLodsNumber = QSpinBox(self.tabObjects)
        self.sbFilterLodsNumber.setObjectName(u"sbFilterLodsNumber")
        self.sbFilterLodsNumber.setEnabled(False)
        self.sbFilterLodsNumber.setMinimum(-1)
        self.sbFilterLodsNumber.setValue(-1)

        self.horizontalLayout_3.addWidget(self.sbFilterLodsNumber)

        self.filterObjects = QLineEdit(self.tabObjects)
        self.filterObjects.setObjectName(u"filterObjects")
        self.filterObjects.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.filterObjects)

        self.line_8 = QFrame(self.tabObjects)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_8)

        self.btnExpandAll = QPushButton(self.tabObjects)
        self.btnExpandAll.setObjectName(u"btnExpandAll")
        self.btnExpandAll.setMinimumSize(QSize(100, 0))
        self.btnExpandAll.setBaseSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.btnExpandAll)

        self.btnCollapseAll = QPushButton(self.tabObjects)
        self.btnCollapseAll.setObjectName(u"btnCollapseAll")
        self.btnCollapseAll.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.btnCollapseAll)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.treeLODs = QTreeWidget(self.tabObjects)
        self.treeLODs.setObjectName(u"treeLODs")
        sizePolicy.setHeightForWidth(self.treeLODs.sizePolicy().hasHeightForWidth())
        self.treeLODs.setSizePolicy(sizePolicy)
        self.treeLODs.setAlternatingRowColors(True)
        self.treeLODs.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeLODs.setIndentation(20)
        self.treeLODs.header().setDefaultSectionSize(80)

        self.verticalLayout_4.addWidget(self.treeLODs)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, -1, -1, 5)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(7, 0, 7, -1)
        self.lbLineProperty = QLabel(self.tabObjects)
        self.lbLineProperty.setObjectName(u"lbLineProperty")

        self.horizontalLayout_6.addWidget(self.lbLineProperty)

        self.line_12 = QFrame(self.tabObjects)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.VLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line_12)

        self.cbAutoLODs = QCheckBox(self.tabObjects)
        self.cbAutoLODs.setObjectName(u"cbAutoLODs")
        self.cbAutoLODs.setEnabled(True)
        self.cbAutoLODs.setLayoutDirection(Qt.LeftToRight)
        self.cbAutoLODs.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.cbAutoLODs)

        self.line = QFrame(self.tabObjects)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line)

        self.lbLodValue = QLabel(self.tabObjects)
        self.lbLodValue.setObjectName(u"lbLodValue")

        self.horizontalLayout_6.addWidget(self.lbLodValue)

        self.lodValue = QLineEdit(self.tabObjects)
        self.lodValue.setObjectName(u"lodValue")
        self.lodValue.setMaximumSize(QSize(50, 16777215))
        self.lodValue.setAutoFillBackground(False)

        self.horizontalLayout_6.addWidget(self.lodValue)

        self.btnAdjustLodValue = QToolButton(self.tabObjects)
        self.btnAdjustLodValue.setObjectName(u"btnAdjustLodValue")
        self.btnAdjustLodValue.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_6.addWidget(self.btnAdjustLodValue)

        self.line_6 = QFrame(self.tabObjects)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line_6)

        self.lbExportTransforms = QLabel(self.tabObjects)
        self.lbExportTransforms.setObjectName(u"lbExportTransforms")

        self.horizontalLayout_6.addWidget(self.lbExportTransforms)

        self.btnExportPosition = QToolButton(self.tabObjects)
        self.btnExportPosition.setObjectName(u"btnExportPosition")
        self.btnExportPosition.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.btnExportPosition)

        self.btnExportRotation = QToolButton(self.tabObjects)
        self.btnExportRotation.setObjectName(u"btnExportRotation")
        self.btnExportRotation.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.btnExportRotation)

        self.btnExportScale = QToolButton(self.tabObjects)
        self.btnExportScale.setObjectName(u"btnExportScale")
        self.btnExportScale.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.btnExportScale)

        self.line_14 = QFrame(self.tabObjects)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setFrameShape(QFrame.VLine)
        self.line_14.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line_14)

        self.lbObjectOptionPreset = QLabel(self.tabObjects)
        self.lbObjectOptionPreset.setObjectName(u"lbObjectOptionPreset")

        self.horizontalLayout_6.addWidget(self.lbObjectOptionPreset)

        self.cbObjectOptionPreset = QComboBox(self.tabObjects)
        self.cbObjectOptionPreset.addItem("")
        self.cbObjectOptionPreset.setObjectName(u"cbObjectOptionPreset")

        self.horizontalLayout_6.addWidget(self.cbObjectOptionPreset)

        self.line_9 = QFrame(self.tabObjects)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.VLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line_9)

        self.lbExportPath = QLabel(self.tabObjects)
        self.lbExportPath.setObjectName(u"lbExportPath")

        self.horizontalLayout_6.addWidget(self.lbExportPath)

        self.btnAddExportPath = QPushButton(self.tabObjects)
        self.btnAddExportPath.setObjectName(u"btnAddExportPath")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btnAddExportPath.sizePolicy().hasHeightForWidth())
        self.btnAddExportPath.setSizePolicy(sizePolicy2)
        self.btnAddExportPath.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.btnAddExportPath)

        self.btnRemoveExportPath = QPushButton(self.tabObjects)
        self.btnRemoveExportPath.setObjectName(u"btnRemoveExportPath")
        sizePolicy2.setHeightForWidth(self.btnRemoveExportPath.sizePolicy().hasHeightForWidth())
        self.btnRemoveExportPath.setSizePolicy(sizePolicy2)
        self.btnRemoveExportPath.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.btnRemoveExportPath)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.line_7 = QFrame(self.tabObjects)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_6.addWidget(self.line_7)

        self.btnConformLayers = QPushButton(self.tabObjects)
        self.btnConformLayers.setObjectName(u"btnConformLayers")

        self.horizontalLayout_6.addWidget(self.btnConformLayers)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.tabObjects, "")
        self.tabPresets = QWidget()
        self.tabPresets.setObjectName(u"tabPresets")
        sizePolicy.setHeightForWidth(self.tabPresets.sizePolicy().hasHeightForWidth())
        self.tabPresets.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.tabPresets)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 7)
        self.splitter = QSplitter(self.tabPresets)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_presets = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_presets.setObjectName(u"verticalLayout_presets")
        self.verticalLayout_presets.setContentsMargins(0, 0, 7, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(7, 5, 7, -1)
        self.btnAddPreset = QPushButton(self.layoutWidget)
        self.btnAddPreset.setObjectName(u"btnAddPreset")
        self.btnAddPreset.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_15.addWidget(self.btnAddPreset)

        self.btnAddExistingPresets = QToolButton(self.layoutWidget)
        self.btnAddExistingPresets.setObjectName(u"btnAddExistingPresets")
        self.btnAddExistingPresets.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_15.addWidget(self.btnAddExistingPresets)

        self.btnAddGroup = QToolButton(self.layoutWidget)
        self.btnAddGroup.setObjectName(u"btnAddGroup")
        self.btnAddGroup.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_15.addWidget(self.btnAddGroup)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_5)

        self.line_3 = QFrame(self.layoutWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_15.addWidget(self.line_3)

        self.btnPresetViewFilter = QToolButton(self.layoutWidget)
        self.btnPresetViewFilter.setObjectName(u"btnPresetViewFilter")
        self.btnPresetViewFilter.setCheckable(True)
        self.btnPresetViewFilter.setChecked(True)

        self.horizontalLayout_15.addWidget(self.btnPresetViewFilter)

        self.filterPresets = QLineEdit(self.layoutWidget)
        self.filterPresets.setObjectName(u"filterPresets")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.filterPresets.sizePolicy().hasHeightForWidth())
        self.filterPresets.setSizePolicy(sizePolicy3)
        self.filterPresets.setClearButtonEnabled(True)

        self.horizontalLayout_15.addWidget(self.filterPresets)

        self.line_16 = QFrame(self.layoutWidget)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setFrameShape(QFrame.VLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_15.addWidget(self.line_16)

        self.btnPresetExpandAll = QPushButton(self.layoutWidget)
        self.btnPresetExpandAll.setObjectName(u"btnPresetExpandAll")
        self.btnPresetExpandAll.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_15.addWidget(self.btnPresetExpandAll)

        self.btnPresetCollapseAll = QPushButton(self.layoutWidget)
        self.btnPresetCollapseAll.setObjectName(u"btnPresetCollapseAll")
        self.btnPresetCollapseAll.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_15.addWidget(self.btnPresetCollapseAll)


        self.verticalLayout_9.addLayout(self.horizontalLayout_15)

        self.treePresets = QTreeWidget(self.layoutWidget)
        self.treePresets.setObjectName(u"treePresets")
        self.treePresets.setEnabled(True)
        sizePolicy.setHeightForWidth(self.treePresets.sizePolicy().hasHeightForWidth())
        self.treePresets.setSizePolicy(sizePolicy)
        self.treePresets.setDragEnabled(True)
        self.treePresets.setDragDropMode(QAbstractItemView.InternalMove)
        self.treePresets.setDefaultDropAction(Qt.MoveAction)
        self.treePresets.setAlternatingRowColors(True)
        self.treePresets.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treePresets.header().setDefaultSectionSize(49)

        self.verticalLayout_9.addWidget(self.treePresets)


        self.verticalLayout_presets.addLayout(self.verticalLayout_9)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(7, -1, 7, -1)
        self.lbPresetsLineProperty = QLabel(self.layoutWidget)
        self.lbPresetsLineProperty.setObjectName(u"lbPresetsLineProperty")

        self.horizontalLayout_9.addWidget(self.lbPresetsLineProperty)

        self.line_5 = QFrame(self.layoutWidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_9.addWidget(self.line_5)

        self.btnDuplicatePreset = QPushButton(self.layoutWidget)
        self.btnDuplicatePreset.setObjectName(u"btnDuplicatePreset")

        self.horizontalLayout_9.addWidget(self.btnDuplicatePreset)

        self.btnRemovePreset = QPushButton(self.layoutWidget)
        self.btnRemovePreset.setObjectName(u"btnRemovePreset")

        self.horizontalLayout_9.addWidget(self.btnRemovePreset)

        self.line_4 = QFrame(self.layoutWidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_9.addWidget(self.line_4)

        self.lbPresetsOptionPreset = QLabel(self.layoutWidget)
        self.lbPresetsOptionPreset.setObjectName(u"lbPresetsOptionPreset")

        self.horizontalLayout_9.addWidget(self.lbPresetsOptionPreset)

        self.cbOptionPreset = QComboBox(self.layoutWidget)
        self.cbOptionPreset.addItem("")
        self.cbOptionPreset.setObjectName(u"cbOptionPreset")

        self.horizontalLayout_9.addWidget(self.cbOptionPreset)

        self.line_15 = QFrame(self.layoutWidget)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setFrameShape(QFrame.VLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_9.addWidget(self.line_15)

        self.lbPresetsExportPath = QLabel(self.layoutWidget)
        self.lbPresetsExportPath.setObjectName(u"lbPresetsExportPath")

        self.horizontalLayout_9.addWidget(self.lbPresetsExportPath)

        self.btnEditPresetPath = QPushButton(self.layoutWidget)
        self.btnEditPresetPath.setObjectName(u"btnEditPresetPath")
        self.btnEditPresetPath.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_9.addWidget(self.btnEditPresetPath)

        self.btnEditGroupPath = QPushButton(self.layoutWidget)
        self.btnEditGroupPath.setObjectName(u"btnEditGroupPath")
        self.btnEditGroupPath.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_9.addWidget(self.btnEditGroupPath)

        self.horizontalSpacer_7 = QSpacerItem(30, 26, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)


        self.verticalLayout_presets.addLayout(self.horizontalLayout_9)

        self.splitter.addWidget(self.layoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_layers = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_layers.setObjectName(u"verticalLayout_layers")
        self.verticalLayout_layers.setContentsMargins(7, 0, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(7, 5, 7, -1)
        self.reloadLayersButton = QPushButton(self.verticalLayoutWidget_2)
        self.reloadLayersButton.setObjectName(u"reloadLayersButton")
        self.reloadLayersButton.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_16.addWidget(self.reloadLayersButton)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_9)

        self.btnLayerExpandAll = QPushButton(self.verticalLayoutWidget_2)
        self.btnLayerExpandAll.setObjectName(u"btnLayerExpandAll")
        self.btnLayerExpandAll.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_16.addWidget(self.btnLayerExpandAll)

        self.btnLayerCollapseAll = QPushButton(self.verticalLayoutWidget_2)
        self.btnLayerCollapseAll.setObjectName(u"btnLayerCollapseAll")
        self.btnLayerCollapseAll.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_16.addWidget(self.btnLayerCollapseAll)


        self.verticalLayout_11.addLayout(self.horizontalLayout_16)

        self.treeLayer = QTreeWidget(self.verticalLayoutWidget_2)
        self.treeLayer.setObjectName(u"treeLayer")
        self.treeLayer.setAlternatingRowColors(True)
        self.treeLayer.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_11.addWidget(self.treeLayer)


        self.verticalLayout_layers.addLayout(self.verticalLayout_11)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(7, -1, 7, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.btnApplyPresetLayer = QPushButton(self.verticalLayoutWidget_2)
        self.btnApplyPresetLayer.setObjectName(u"btnApplyPresetLayer")

        self.horizontalLayout_5.addWidget(self.btnApplyPresetLayer)


        self.verticalLayout_layers.addLayout(self.horizontalLayout_5)

        self.splitter.addWidget(self.verticalLayoutWidget_2)

        self.verticalLayout_2.addWidget(self.splitter)

        self.tabWidget.addTab(self.tabPresets, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(7)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 5, 5, 0)
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.btnOptions = QToolButton(self.groupBox_2)
        self.btnOptions.setObjectName(u"btnOptions")
        self.btnOptions.setMinimumSize(QSize(0, 30))
        self.btnOptions.setLayoutDirection(Qt.LeftToRight)
        self.btnOptions.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_13.addWidget(self.btnOptions)

        self.btnSceneInspector = QToolButton(self.groupBox_2)
        self.btnSceneInspector.setObjectName(u"btnSceneInspector")
        self.btnSceneInspector.setMinimumSize(QSize(0, 30))
        self.btnSceneInspector.setLayoutDirection(Qt.RightToLeft)
        self.btnSceneInspector.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_13.addWidget(self.btnSceneInspector)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_13)

        self.line_11 = QFrame(self.groupBox_2)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShadow(QFrame.Sunken)
        self.line_11.setLineWidth(1)
        self.line_11.setFrameShape(QFrame.HLine)

        self.verticalLayout_8.addWidget(self.line_11)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.lbTipTitle = QLabel(self.groupBox_2)
        self.lbTipTitle.setObjectName(u"lbTipTitle")

        self.horizontalLayout_14.addWidget(self.lbTipTitle)

        self.lbTip = QLabel(self.groupBox_2)
        self.lbTip.setObjectName(u"lbTip")

        self.horizontalLayout_14.addWidget(self.lbTip)

        self.horizontalSpacer_8 = QSpacerItem(40, 30, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_8)


        self.verticalLayout_8.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_10.addLayout(self.verticalLayout_8)


        self.horizontalLayout_11.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.btnExportTicked = QPushButton(self.groupBox_3)
        self.btnExportTicked.setObjectName(u"btnExportTicked")
        self.btnExportTicked.setMinimumSize(QSize(150, 30))

        self.horizontalLayout_12.addWidget(self.btnExportTicked)

        self.btnExportSelected = QPushButton(self.groupBox_3)
        self.btnExportSelected.setObjectName(u"btnExportSelected")
        self.btnExportSelected.setMinimumSize(QSize(150, 30))

        self.horizontalLayout_12.addWidget(self.btnExportSelected)

        self.btnExportAll = QPushButton(self.groupBox_3)
        self.btnExportAll.setObjectName(u"btnExportAll")
        self.btnExportAll.setMinimumSize(QSize(150, 30))

        self.horizontalLayout_12.addWidget(self.btnExportAll)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.line_10 = QFrame(self.groupBox_3)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line_10)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cbGltfExport = QCheckBox(self.groupBox_3)
        self.cbGltfExport.setObjectName(u"cbGltfExport")
        self.cbGltfExport.setChecked(True)

        self.horizontalLayout_4.addWidget(self.cbGltfExport)

        self.cbXmlExport = QCheckBox(self.groupBox_3)
        self.cbXmlExport.setObjectName(u"cbXmlExport")
        self.cbXmlExport.setChecked(True)

        self.horizontalLayout_4.addWidget(self.cbXmlExport)

        self.cbTextureLib = QCheckBox(self.groupBox_3)
        self.cbTextureLib.setObjectName(u"cbTextureLib")
        self.cbTextureLib.setEnabled(True)
        self.cbTextureLib.setChecked(False)

        self.horizontalLayout_4.addWidget(self.cbTextureLib)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addLayout(self.verticalLayout_6)


        self.horizontalLayout_11.addWidget(self.groupBox_3)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(5, 5, 5, -1)
        self.lbProgressBar = QLabel(self.scrollAreaWidgetContents)
        self.lbProgressBar.setObjectName(u"lbProgressBar")

        self.horizontalLayout_7.addWidget(self.lbProgressBar)

        self.progressBar = QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximumSize(QSize(16777215, 20))
        self.progressBar.setStyleSheet(u"")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)

        self.horizontalLayout_7.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.splitter_areas.addWidget(self.scrollArea)
        self.scrollArea_2 = QScrollArea(self.splitter_areas)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setMinimumSize(QSize(0, 101))
        self.scrollArea_2.setStyleSheet(u"")
        self.scrollArea_2.setWidgetResizable(True)
        self.loggerArea = QWidget()
        self.loggerArea.setObjectName(u"loggerArea")
        self.loggerArea.setGeometry(QRect(0, 0, 1474, 99))
        self.loggerAreaVLayout = QVBoxLayout(self.loggerArea)
        self.loggerAreaVLayout.setObjectName(u"loggerAreaVLayout")
        self.scrollArea_2.setWidget(self.loggerArea)
        self.splitter_areas.addWidget(self.scrollArea_2)

        self.verticalLayout_3.addWidget(self.splitter_areas)

        MultiExporter.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MultiExporter)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1498, 26))
        self.menuUtils = QMenu(self.menubar)
        self.menuUtils.setObjectName(u"menuUtils")
        self.menuUtils.setMinimumSize(QSize(235, 0))
        MultiExporter.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MultiExporter)
        self.statusbar.setObjectName(u"statusbar")
        MultiExporter.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuUtils.menuAction())
        self.menuUtils.addSeparator()
        self.menuUtils.addAction(self.openTextureToolAction)
        self.menuUtils.addSeparator()
        self.menuUtils.addAction(self.runResolveUniqueIDsAction)
        self.menuUtils.addSeparator()
        self.menuUtils.addAction(self.saveglTFConfigurationAction)
        self.menuUtils.addAction(self.importglTFConfigurationAction)

        self.retranslateUi(MultiExporter)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MultiExporter)
    # setupUi

    def retranslateUi(self, MultiExporter):
        MultiExporter.setWindowTitle(QCoreApplication.translate("MultiExporter", u"Multi Exporter", None))
        self.openTextureToolAction.setText(QCoreApplication.translate("MultiExporter", u"Open Texture Tool", None))
        self.resolveUniqueIDsAction.setText(QCoreApplication.translate("MultiExporter", u"Resolve Unique IDs", None))
        self.importglTFConfigurationAction.setText(QCoreApplication.translate("MultiExporter", u"Import glTF configuration (*.mep)", None))
        self.saveglTFConfigurationAction.setText(QCoreApplication.translate("MultiExporter", u"Save glTF configuration (*.mep)", None))
        self.runResolveUniqueIDsAction.setText(QCoreApplication.translate("MultiExporter", u"Run resolve unique IDs", None))
        self.actionRefresh.setText(QCoreApplication.translate("MultiExporter", u"Refresh", None))
        self.headerBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.btnRefresh.setToolTip(QCoreApplication.translate("MultiExporter", u"Refresh list", None))
#endif // QT_CONFIG(tooltip)
        self.btnRefresh.setText(QCoreApplication.translate("MultiExporter", u"Refresh", None))
        self.lbQuickOptions.setText(QCoreApplication.translate("MultiExporter", u"List options:", None))
#if QT_CONFIG(tooltip)
        self.cbAlwaysSelectInScene.setToolTip(QCoreApplication.translate("MultiExporter", u"Select element in list will select in scene too\n"
"Note that double click and right click also allows to select in scene by default", None))
#endif // QT_CONFIG(tooltip)
        self.cbAlwaysSelectInScene.setText(QCoreApplication.translate("MultiExporter", u"Always select in scene", None))
#if QT_CONFIG(tooltip)
        self.cbSelectInSceneSelectsChildren.setToolTip(QCoreApplication.translate("MultiExporter", u"Double click an element in the list or right click it to select in scene\n"
"Use this option to select children too", None))
#endif // QT_CONFIG(tooltip)
        self.cbSelectInSceneSelectsChildren.setText(QCoreApplication.translate("MultiExporter", u"Select in scene selects children", None))
        self.lbCoin.setText("")
#if QT_CONFIG(tooltip)
        self.coin.setToolTip(QCoreApplication.translate("MultiExporter", u"If you click me, I'll run away.", None))
#endif // QT_CONFIG(tooltip)
        self.coin.setText("")
#if QT_CONFIG(tooltip)
        self.btnOpenExportFolder.setToolTip(QCoreApplication.translate("MultiExporter", u"Open export path of selected object", None))
#endif // QT_CONFIG(tooltip)
        self.btnOpenExportFolder.setText(QCoreApplication.translate("MultiExporter", u"Open Export Folder", None))
#if QT_CONFIG(tooltip)
        self.btnHierarchyViewFilter.setToolTip(QCoreApplication.translate("MultiExporter", u"Enable display filters", None))
#endif // QT_CONFIG(tooltip)
        self.btnHierarchyViewFilter.setText(QCoreApplication.translate("MultiExporter", u"...", None))
#if QT_CONFIG(tooltip)
        self.cbFilterExportableOnly.setToolTip(QCoreApplication.translate("MultiExporter", u"Display only exportable object(s)", None))
#endif // QT_CONFIG(tooltip)
        self.cbFilterExportableOnly.setText(QCoreApplication.translate("MultiExporter", u"Only Exportable", None))
#if QT_CONFIG(tooltip)
        self.cbFilterVisibleOnly.setToolTip(QCoreApplication.translate("MultiExporter", u"Display only visible object(s)", None))
#endif // QT_CONFIG(tooltip)
        self.cbFilterVisibleOnly.setText(QCoreApplication.translate("MultiExporter", u"Only Visible in Scene", None))
#if QT_CONFIG(tooltip)
        self.cbFilterLodsOnly.setToolTip(QCoreApplication.translate("MultiExporter", u"Display only LODs object(s)", None))
#endif // QT_CONFIG(tooltip)
        self.cbFilterLodsOnly.setText(QCoreApplication.translate("MultiExporter", u"Only LODs", None))
#if QT_CONFIG(tooltip)
        self.sbFilterLodsNumber.setToolTip(QCoreApplication.translate("MultiExporter", u"Display only LOD number\n"
"(-1 disables setting)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.filterObjects.setToolTip(QCoreApplication.translate("MultiExporter", u"Filter by name", None))
#endif // QT_CONFIG(tooltip)
        self.filterObjects.setPlaceholderText(QCoreApplication.translate("MultiExporter", u"Enter a name to filter and press enter", None))
#if QT_CONFIG(tooltip)
        self.btnExpandAll.setToolTip(QCoreApplication.translate("MultiExporter", u"Expand all in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnExpandAll.setText(QCoreApplication.translate("MultiExporter", u"Expand All", None))
#if QT_CONFIG(tooltip)
        self.btnCollapseAll.setToolTip(QCoreApplication.translate("MultiExporter", u"Collapse all in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnCollapseAll.setText(QCoreApplication.translate("MultiExporter", u"Collapse All", None))
        ___qtreewidgetitem = self.treeLODs.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MultiExporter", u"Path", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MultiExporter", u"LOD Min size", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MultiExporter", u"Hierarchy", None));
#if QT_CONFIG(tooltip)
        ___qtreewidgetitem.setToolTip(1, QCoreApplication.translate("MultiExporter", u"Minimum display size: screen height percentage", None));
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lbLineProperty.setToolTip(QCoreApplication.translate("MultiExporter", u"Edit metadata for selected line(s). Some of this ends up in the associated XML file", None))
#endif // QT_CONFIG(tooltip)
        self.lbLineProperty.setText(QCoreApplication.translate("MultiExporter", u"Edit selected line(s):", None))
#if QT_CONFIG(tooltip)
        self.cbAutoLODs.setToolTip(QCoreApplication.translate("MultiExporter", u"Automatic LODs generation (LOD min size will be automatically set)", None))
#endif // QT_CONFIG(tooltip)
        self.cbAutoLODs.setText(QCoreApplication.translate("MultiExporter", u"Auto LODs", None))
#if QT_CONFIG(tooltip)
        self.lbLodValue.setToolTip(QCoreApplication.translate("MultiExporter", u"LOD minimum display size: expressed in screen height percentage", None))
#endif // QT_CONFIG(tooltip)
        self.lbLodValue.setText(QCoreApplication.translate("MultiExporter", u"LOD min size (%):", None))
#if QT_CONFIG(tooltip)
        self.lodValue.setToolTip(QCoreApplication.translate("MultiExporter", u"Set the final LOD min size value of the model in the XML", None))
#endif // QT_CONFIG(tooltip)
        self.lodValue.setPlaceholderText(QCoreApplication.translate("MultiExporter", u"70.0...", None))
#if QT_CONFIG(tooltip)
        self.btnAdjustLodValue.setToolTip(QCoreApplication.translate("MultiExporter", u"Adjust bad LOD value(s) to minimum safe", None))
#endif // QT_CONFIG(tooltip)
        self.btnAdjustLodValue.setText(QCoreApplication.translate("MultiExporter", u"...", None))
#if QT_CONFIG(tooltip)
        self.lbExportTransforms.setToolTip(QCoreApplication.translate("MultiExporter", u"Keep object's transform in space", None))
#endif // QT_CONFIG(tooltip)
        self.lbExportTransforms.setText(QCoreApplication.translate("MultiExporter", u"Keep transform:", None))
#if QT_CONFIG(tooltip)
        self.btnExportPosition.setToolTip(QCoreApplication.translate("MultiExporter", u"Export world position (keep object's position in space)", None))
#endif // QT_CONFIG(tooltip)
        self.btnExportPosition.setText(QCoreApplication.translate("MultiExporter", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnExportRotation.setToolTip(QCoreApplication.translate("MultiExporter", u"Export world rotation (keep object's rotation in space)", None))
#endif // QT_CONFIG(tooltip)
        self.btnExportRotation.setText(QCoreApplication.translate("MultiExporter", u"...", None))
#if QT_CONFIG(tooltip)
        self.btnExportScale.setToolTip(QCoreApplication.translate("MultiExporter", u"Export world scale (keep object's scale in space)", None))
#endif // QT_CONFIG(tooltip)
        self.btnExportScale.setText(QCoreApplication.translate("MultiExporter", u"...", None))
#if QT_CONFIG(tooltip)
        self.lbObjectOptionPreset.setToolTip(QCoreApplication.translate("MultiExporter", u"Export options applied to selected object(s)", None))
#endif // QT_CONFIG(tooltip)
        self.lbObjectOptionPreset.setText(QCoreApplication.translate("MultiExporter", u"Export options:", None))
        self.cbObjectOptionPreset.setItemText(0, QCoreApplication.translate("MultiExporter", u"default", None))

        self.lbExportPath.setText(QCoreApplication.translate("MultiExporter", u"Export path:", None))
#if QT_CONFIG(tooltip)
        self.btnAddExportPath.setToolTip(QCoreApplication.translate("MultiExporter", u"Add/Edit export path for object(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddExportPath.setText(QCoreApplication.translate("MultiExporter", u"Add/Edit", None))
#if QT_CONFIG(tooltip)
        self.btnRemoveExportPath.setToolTip(QCoreApplication.translate("MultiExporter", u"Remove export path from object(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnRemoveExportPath.setText(QCoreApplication.translate("MultiExporter", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.btnConformLayers.setToolTip(QCoreApplication.translate("MultiExporter", u"This will create a layer for each export model and each LOD and put the corresponding objects in the right layers. Objects not represented in the list will be put in the default layer 0.", None))
#endif // QT_CONFIG(tooltip)
        self.btnConformLayers.setText(QCoreApplication.translate("MultiExporter", u"Conform Layers", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabObjects), QCoreApplication.translate("MultiExporter", u"Scene hierarchy based export", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tabObjects), QCoreApplication.translate("MultiExporter", u"Export based on scene hierarchy", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btnAddPreset.setToolTip(QCoreApplication.translate("MultiExporter", u"Create new gltf (select or create new file)\n"
"(will be added in list or within a group)", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddPreset.setText(QCoreApplication.translate("MultiExporter", u"New", None))
#if QT_CONFIG(tooltip)
        self.btnAddExistingPresets.setToolTip(QCoreApplication.translate("MultiExporter", u"Overwrite existing gltf(s) (select one or more file(s))\n"
"(will be added in list or within a group)", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddExistingPresets.setText(QCoreApplication.translate("MultiExporter", u"Existing", None))
#if QT_CONFIG(tooltip)
        self.btnAddGroup.setToolTip(QCoreApplication.translate("MultiExporter", u"Add a new group (select a folder).\n"
"Export options are applied to groups only.", None))
#endif // QT_CONFIG(tooltip)
        self.btnAddGroup.setText(QCoreApplication.translate("MultiExporter", u"New group", None))
#if QT_CONFIG(tooltip)
        self.btnPresetViewFilter.setToolTip(QCoreApplication.translate("MultiExporter", u"Enable display filters", None))
#endif // QT_CONFIG(tooltip)
        self.btnPresetViewFilter.setText(QCoreApplication.translate("MultiExporter", u"...", None))
#if QT_CONFIG(tooltip)
        self.filterPresets.setToolTip(QCoreApplication.translate("MultiExporter", u"Filter by name", None))
#endif // QT_CONFIG(tooltip)
        self.filterPresets.setText("")
        self.filterPresets.setPlaceholderText(QCoreApplication.translate("MultiExporter", u"Enter a name to filter and press enter", None))
        self.btnPresetExpandAll.setText(QCoreApplication.translate("MultiExporter", u"Expand All", None))
        self.btnPresetCollapseAll.setText(QCoreApplication.translate("MultiExporter", u"Collapse All", None))
        ___qtreewidgetitem1 = self.treePresets.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MultiExporter", u"Path", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MultiExporter", u"Name", None));
        self.lbPresetsLineProperty.setText(QCoreApplication.translate("MultiExporter", u"Edit selected line(s):", None))
#if QT_CONFIG(tooltip)
        self.btnDuplicatePreset.setToolTip(QCoreApplication.translate("MultiExporter", u"Duplicate selected gltf(s) or group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnDuplicatePreset.setText(QCoreApplication.translate("MultiExporter", u"Duplicate", None))
#if QT_CONFIG(tooltip)
        self.btnRemovePreset.setToolTip(QCoreApplication.translate("MultiExporter", u"Remove selected gltf(s) or group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnRemovePreset.setText(QCoreApplication.translate("MultiExporter", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.lbPresetsOptionPreset.setToolTip(QCoreApplication.translate("MultiExporter", u"Export options preset applied to the selected group(s) in the presets view", None))
#endif // QT_CONFIG(tooltip)
        self.lbPresetsOptionPreset.setText(QCoreApplication.translate("MultiExporter", u"Export options:", None))
        self.cbOptionPreset.setItemText(0, QCoreApplication.translate("MultiExporter", u"default", None))

#if QT_CONFIG(tooltip)
        self.cbOptionPreset.setToolTip(QCoreApplication.translate("MultiExporter", u"Option preset applied to the selected group(s) in the presets view", None))
#endif // QT_CONFIG(tooltip)
        self.lbPresetsExportPath.setText(QCoreApplication.translate("MultiExporter", u"Export path:", None))
#if QT_CONFIG(tooltip)
        self.btnEditPresetPath.setToolTip(QCoreApplication.translate("MultiExporter", u"Edit the path of the selected gltf(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnEditPresetPath.setText(QCoreApplication.translate("MultiExporter", u"Edit", None))
#if QT_CONFIG(tooltip)
        self.btnEditGroupPath.setToolTip(QCoreApplication.translate("MultiExporter", u"Edit the path of the selected group(s)", None))
#endif // QT_CONFIG(tooltip)
        self.btnEditGroupPath.setText(QCoreApplication.translate("MultiExporter", u"Edit Group Path", None))
        self.reloadLayersButton.setText(QCoreApplication.translate("MultiExporter", u"Reload Layers", None))
        self.btnLayerExpandAll.setText(QCoreApplication.translate("MultiExporter", u"Expand All", None))
        self.btnLayerCollapseAll.setText(QCoreApplication.translate("MultiExporter", u"Collapse All", None))
        ___qtreewidgetitem2 = self.treeLayer.headerItem()
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MultiExporter", u"         Layers", None));
#if QT_CONFIG(tooltip)
        self.btnApplyPresetLayer.setToolTip(QCoreApplication.translate("MultiExporter", u"Apply ticked layers to preset", None))
#endif // QT_CONFIG(tooltip)
        self.btnApplyPresetLayer.setText(QCoreApplication.translate("MultiExporter", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPresets), QCoreApplication.translate("MultiExporter", u"User defined layer based export", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tabPresets), QCoreApplication.translate("MultiExporter", u"Export based on layer selection", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("MultiExporter", u"Export tools", None))
        self.btnOptions.setText(QCoreApplication.translate("MultiExporter", u"Export options", None))
        self.btnSceneInspector.setText(QCoreApplication.translate("MultiExporter", u"Efficiency", None))
        self.lbTipTitle.setText(QCoreApplication.translate("MultiExporter", u"TIP:", None))
        self.lbTip.setText(QCoreApplication.translate("MultiExporter", u"Auto LODs property will generate lower LODs for you. You may override the last LOD generated by your own by setting its min size to 0.0", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MultiExporter", u"Export models", None))
#if QT_CONFIG(tooltip)
        self.btnExportTicked.setToolTip(QCoreApplication.translate("MultiExporter", u"Export checked object(s) in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnExportTicked.setText(QCoreApplication.translate("MultiExporter", u"Export checked", None))
#if QT_CONFIG(tooltip)
        self.btnExportSelected.setToolTip(QCoreApplication.translate("MultiExporter", u"Export selected object(s) in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnExportSelected.setText(QCoreApplication.translate("MultiExporter", u"Export selected", None))
#if QT_CONFIG(tooltip)
        self.btnExportAll.setToolTip(QCoreApplication.translate("MultiExporter", u"Export all object(s) visible in list", None))
#endif // QT_CONFIG(tooltip)
        self.btnExportAll.setText(QCoreApplication.translate("MultiExporter", u"Export visible in list", None))
#if QT_CONFIG(tooltip)
        self.cbGltfExport.setToolTip(QCoreApplication.translate("MultiExporter", u"Gltf is the file format used to export 3D models into flight simulator", None))
#endif // QT_CONFIG(tooltip)
        self.cbGltfExport.setText(QCoreApplication.translate("MultiExporter", u"Export models as glTF", None))
#if QT_CONFIG(tooltip)
        self.cbXmlExport.setToolTip(QCoreApplication.translate("MultiExporter", u"Micorosft Flight simulator 2024 needs an xml file alongside the gltf model files", None))
#endif // QT_CONFIG(tooltip)
        self.cbXmlExport.setText(QCoreApplication.translate("MultiExporter", u"Generate/Update XML", None))
#if QT_CONFIG(tooltip)
        self.cbTextureLib.setToolTip(QCoreApplication.translate("MultiExporter", u"Generate an XML for the texture Lib when exporting", None))
#endif // QT_CONFIG(tooltip)
        self.cbTextureLib.setText(QCoreApplication.translate("MultiExporter", u"Generate TextureLib", None))
        self.lbProgressBar.setText(QCoreApplication.translate("MultiExporter", u"(Doing nothing):", None))
        self.menuUtils.setTitle(QCoreApplication.translate("MultiExporter", u"Utilities", None))
    # retranslateUi

