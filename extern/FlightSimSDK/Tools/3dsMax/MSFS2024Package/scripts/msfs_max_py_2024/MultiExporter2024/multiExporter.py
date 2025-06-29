"""
Provides a UI to export multiple flight sim object type quickly

run() will create the window and connect it to max.
"""
import os
import random
import stat
import logging
import time
import datetime

import json as json

from typing import NamedTuple
from shutil import copyfile, _samefile

import MultiExporter2024.ui.mainwindow_ui as mainWindowUI
import MultiExporter2024.exporter as exporter
import MultiExporter2024.multiExporter as ME
import MultiExporter2024.optionsMenu as optionsMenu
import MultiExporter2024.presetUtils as presetUtils
import MultiExporter2024.constants as const
import MultiExporter2024.BabylonPYMXS2024 as babylonPYMXS2024
import MultiExporter2024.displayUtils as displayUtils

from MultiExporter2024.useTextureLib import exportTextureLibWithGltf
from MultiExporter2024.view import treeViewLods, treeViewLayer, treeViewPreset
from MultiExporter2024.meshInspector import MeshInspectorWindow

from PySide2.QtGui import QIcon, QColor
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (QMainWindow, QWidget, QToolButton, 
                               QAbstractItemView, QApplication, QSizePolicy, 
                               QFileDialog, QMenu
                               )

from TextureTool2024 import textureTool as TT


import maxsdk_2024.uiTheme as uiColors
import maxsdk_2024.userprop as userprop
import maxsdk_2024.sharedGlobals as sharedGlobals
import maxsdk_2024.layer as layer
import maxsdk_2024.node as node
import maxsdk_2024.perforce as perforce
import maxsdk_2024.qtUtils as qtUtils
import maxsdk_2024.sceneUtils as sceneUtils
import maxsdk_2024.utility as utility

from maxsdk_2024.logger import LoggerWidget
from maxsdk_2024.globals import MAXVERSION, MAX2021, RT

from maxsdk_2024.logger import SignalHandler

if MAXVERSION() >= MAX2021:
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser


handler = SignalHandler()
MSFS2024ExportLogger = logging.getLogger("MSFS2024ExportLogger")
MSFS2024ExportLogger.setLevel(level=logging.INFO)
MSFS2024ExportLogger.addHandler(handler)

class ExportTransforms(NamedTuple):
    position: bool
    rotation: bool
    scale: bool

class MainWindow(QMainWindow, mainWindowUI.Ui_MultiExporter):

    #region Initialisation
    def __init__(self, parent = None):
        self.initCustomScripts()

        """
            CustomPrivateMembers
        """
        ## Set Option Menu Attribute
        self.optionsMenuWindow = None
        ## Set The Last Edited Preset Attribute
        self.lastEditedPreset = None
        ## Mesh inspector window
        sharedGlobals.G_ME_meshInspectorWindow = None
        ## Set the Config Parser
        self.config = ConfigParser()
        ## Set the scene root
        self.sceneRoot = sceneUtils.getSceneRootNode()
        ## Last opened panel
        saveLastOpenedPanel = sceneUtils.getSceneNodeUserProp(self.sceneRoot, const.PROP_LAST_OPENED_PANEL)
        self.lastOpenedPanel = const.TAB.OBJECTS.name if saveLastOpenedPanel is None else saveLastOpenedPanel

        parent = QWidget.find(RT.windows.getMAXHWND())
        QMainWindow.__init__(self, parent)
        ## Buttons icons
        # see https://help.autodesk.com/view/3DSMAX/2018/ENU/?guid=__developer_icon_guide_icon_guide_html
        # for available sizes
        ## Note: use QPixmap instead of QIcon to use as simple icon (not button) + use setPixmap on a label
        self.refreshIcon = QIcon(":/Common/RotateCW_20") #available sizes: ['16', '20', '24', '30', '32', '36', '40', '48']
        self.folderIcon = QIcon(":/Common/Folder_20") #available sizes: ['16', '20', '24', '32']
        self.addFolderIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionFlow/AppendFile_20") #available sizes: ['16', '20', '24', '32']
        self.adjustLodValueIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionMixer/TrimClips_20") #available sizes: ['16', '20', '24', '32']

        self.moveIcon = QIcon(":/MainUI/Move_24") #available sizes: ['24', '30', '36', '48']
        self.rotateIcon = QIcon(":/Common/RotateCW_24") #available sizes: ['16', '20', '24', '30', '32', '36', '40', '48']
        self.scaleIcon = QIcon(":/MainUI/UniformScale_24") #available sizes: ['24', '30', '36', '48']

        self.listAddIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionFlow/CreateMultipleClips_20") #available sizes: ['16', '20', '24', '32']
        self.viewFilterLabelIcon = QIcon(":/TrackView/DopeSheet/FilterSelectedTracksToggle_24") #available sizes: ['24', '30', '36', '48']
        #self.inspectIcon = QIcon(":/Common/Zoom_20") #available sizes: ['16', '20', '24', '30', '32', '36', '48']
        #self.inspectIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionMixer/ZoomExtents_20") #available sizes: ['16', '20', '24', '32']
        #self.inspectIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionFlow/ShowRandomPercentages_20") #available sizes: ['16', '20', '24', '32']
        self.inspectIcon = QIcon(":/BlendedBoxMap/BoundingBox_20") #available sizes: ['20', '24', '30', '40']
        #self.inspectIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionFlow/OptimizeSelectedTransitions_20") #available sizes: ['16', '20', '24', '32']
        self.optionsIcon = QIcon(":/Common/Settings_20") #available sizes: ['12', '15', '16', '18', '20', '24', '32']

        ## Nothing to see here. Look away.
        self.quackQuackIcons = [
            QIcon(":/CommandPanel/Motion/BipedRollout/FootstepsCreation/Walk_24"), 
            QIcon(":/CommandPanel/Motion/BipedRollout/LegStates_24"), 
            QIcon(":/CommandPanel/Motion/BipedRollout/FootstepsCreation/Run_24"), 
            QIcon(":/CommandPanel/Motion/BipedRollout/FootstepsCreation/Jump_24"), 
            QIcon(":/MainUI/PivotDoor_24")
        ]
        self.coinCoinIcons = [
            QIcon(":/MainUI/Snow_24"), 
            QIcon(":/MainUI/Spray_24"), 
            QIcon(":/MainUI/RingWave_24"), 
            QIcon(":/MainUI/Simulate_24"), 
            QIcon(":/StateSets/VertexChannelDisplay_24"), 
            QIcon(":/StateSets/Environment_24")
        ]
        ## You have seen nothing.

        ## Tips
        # Object panel
        self.objectsTabTips = (
            "If you want to export only one LOD (Gltf), you need to uncheck XML export.",
            "XML export will select all model LODs.",
            "Auto LODs property will generate lower LODs for you. You may override the last LOD generated with your own by setting its min size to 0.0.",
            "Click \"Collapse All\" to get a quick look of what's wrong in the list.",
            "If LOD name is not green, hover to get more infos. Check the other columns to see what's wrong.",
            "Hover anything that is not white or green in the list to get more infos.",
            "Anything that is not white or green in the list may be adressed.",
            "Any warning or error found will be displayed in yellow or red.",
            "If an error is found and the LOD cant be exported, its name will turn red.",
            "LOD min size (%) is the LOD minimum display size: expressed in screen height percentage.",
            "Double click the object name will select it in the scene. Use the \"Always select in scene\" option for single click action.",
            "Open export folder will open a new explorer window in the Export path directory of selected object(s).",
            "The XML file reference all LODs of a model and should be exported along all LODs (Gltfs) to be kept up to date.",
            "If you wish to export only one LOD, be sure the XML is up to date and matching the LODs description.",
            "If you wish to export only XML, be sure all the referenced Gltfs are exported as well.",
            "Right click on an item in the list allow for quick actions.",
            "LOD Efficiency have nothing to do with polycount. Small meshes can be inefficient too!",
            "LOD Efficiency will increase if you can reduce vertex count.",
            "Efficiency, Draw count and Vertex count are only rough estimations. Accurate statistics can only be checked ingame.",
            "A \"~\" in column's title means it shows only rough estimations. Accurate statistics can only be checked ingame.",
            "Click on the magnifier in the efficiency column to get detailed LOD infos."
        )

        ## Tips
        # Preset panel
        self.presetsTabTips = (
            ""
        )

    def run(self):
        ME.run()

    def show(self):
        # Initialize Container and Babylon Exporter to prepare the export(s)
        initialize()
        # Init the MultiExporter View
        self.setupUi(self)
        self.initUI()
        # Create trees and initialize Data
        self.initTrees()
        # Show window
        super().show()

    def initUI(self):

        #region  Coin coin
        ## Nothing to see here. Look away.
        self.coinCoin = 0
        self.quackQuack = 0
        self.coin.setIconSize(QSize(24, 24))
        self.coin.pressed.connect(self._quackQuack)
        ## You have seen nothing.
        #endregion

        #region Shared views UI
        ## Refresh Button
        self.btnRefresh.setIconSize(QSize(20, 20))
        self.btnRefresh.setIcon(self.refreshIcon)
        self.btnRefresh.setText(" Refresh") #add space around text, no useful padding property for that...
        self.btnRefresh.pressed.connect(self._clickedRefreshList)
        ## Change Tab Event
        self.tabWidget.currentChanged.connect(self._changedTab)
        ## Export Buttons
        self.btnExportSelected.pressed.connect(lambda : self._clickedExport(exportOption=const.EXPORT_OPTION.SELECTED))
        self.btnExportTicked.pressed.connect(lambda : self._clickedExport(exportOption=const.EXPORT_OPTION.CHECKED))
        self.btnExportAll.pressed.connect(lambda : self._clickedExport(exportOption=const.EXPORT_OPTION.ALL))
        ## Export options
        #init values
        self._exportGltf = self.cbGltfExport.isChecked()
        self._exportXml = self.cbGltfExport.isChecked()
        self._exportTextureLib = self.cbTextureLib.isChecked()
        #link events
        self.cbGltfExport.stateChanged.connect(self._changeCheckboxGltfExport)
        self.cbXmlExport.stateChanged.connect(self._changeCheckboxXmlExport)
        self.cbTextureLib.stateChanged.connect(self._changeCheckboxTextureLib)
        ## Open export folder Button
        self.btnOpenExportFolder.setIconSize(QSize(20, 20))
        self.btnOpenExportFolder.setIcon(self.folderIcon)
        self.btnOpenExportFolder.setText(" Open export folder") #add space around text, no useful padding property for that...
        self.btnOpenExportFolder.pressed.connect(self._clickedOpenExportFolder)
        ## Export tools
        self.btnOptions.setIconSize(QSize(20, 20))
        self.btnOptions.setIcon(self.optionsIcon)
        self.btnOptions.setText(" Export options") #add space around text, no useful padding property for that...
        self.btnOptions.setToolTip("Open export options setup window")
        self.btnOptions.pressed.connect(self._openOptionsMenu)
        self.btnSceneInspector.setIconSize(QSize(20, 20))
        self.btnSceneInspector.setIcon(self.inspectIcon)
        self.btnSceneInspector.setText(" Check scene efficiency") #add space around text, no useful padding property for that...
        self.btnSceneInspector.setToolTip("Inspect scene hierarchy")
        self.btnSceneInspector.pressed.connect(self._openMeshInspectorWindow)
        ## Button Open Texture Tool
        self.openTextureToolAction.triggered.connect(self._openTextureTool)
        ## Run Resolve Unique ID
        self.runResolveUniqueIDsAction.triggered.connect(self._clickedResolveUniqueID)
        ## Quick options space
        displayUtils.setLabelColor(self.lbQuickOptions, uiColors.colorSemiDullWhite)
        self.cbAlwaysSelectInScene.stateChanged.connect(self._changeCheckboxAlwaysSelectInScene)
        self.cbSelectInSceneSelectsChildren.stateChanged.connect(self._changeCheckboxSelectChildrenInScene)
        ## Display tip of the not day :)
        self.showRelevantTip()
        displayUtils.setLabelColor(self.lbTipTitle, uiColors.colorDullWhite)
        displayUtils.setLabelColor(self.lbTip, uiColors.colorSemiDullWhite)
        self.lbTipTitle.setToolTip("Displays a random tip each time you launch the Exporter")
        #endregion
        
        #region Objects view UI
        ## Collapse/Expand tree
        self.btnCollapseAll.pressed.connect(self.treeLODs.collapseAll)
        self.btnExpandAll.pressed.connect(self.treeLODs.expandAll)
        self.btnCollapseAll.setEnabled(False)
        self.btnExpandAll.setEnabled(False)
        ## Add/Remove export path Buttons
        self.btnAddExportPath.pressed.connect(self._clickedAddExportPath)
        self.btnRemoveExportPath.pressed.connect(self._clickedRemoveExportPath)
        ## Conform Layers Button
        self.btnConformLayers.pressed.connect(self._clickedConformLayers)
        ## Auto LODs CheckBox
        self.cbAutoLODs.stateChanged.connect(self._changeCheckboxAutoLODs)
        ## LODs values field
        self.lodValue.returnPressed.connect(self._clickedSetLODValues)
        self.lodValue.focusInEvent = lambda _ : self._focusInLODValues()
        self.lodValue.focusOutEvent = lambda _ : self._focusOutLODValues()
        ## Adjust LOD Value Button
        self.btnAdjustLodValue.setIconSize(QSize(20, 20))
        self.btnAdjustLodValue.setIcon(self.adjustLodValueIcon)
        self.btnAdjustLodValue.setText("")
        self.btnAdjustLodValue.pressed.connect(self._clickedAdjustLodValue)
        ## Export transform Buttons
        self.btnExportPosition.setIconSize(QSize(20, 20))
        self.btnExportPosition.setIcon(self.moveIcon)
        self.btnExportPosition.setText("")
        self.btnExportPosition.clicked.connect(self._clickedSetExportPosition)
        self.btnExportRotation.setIconSize(QSize(20, 20))
        self.btnExportRotation.setIcon(self.rotateIcon)
        self.btnExportRotation.setText("")
        self.btnExportRotation.clicked.connect(self._clickedSetExportRotation)
        self.btnExportScale.setIconSize(QSize(20, 20))
        self.btnExportScale.setIcon(self.scaleIcon)
        self.btnExportScale.setText("")
        self.btnExportScale.clicked.connect(self._clickedSetExportScale)
        ## Option Preset Combo Box Options Applied to Object(s)
        self.horizontalLayout_6.removeWidget(self.cbObjectOptionPreset)
        self.cbObjectOptionPreset.deleteLater()
        self.cbObjectOptionPreset = optionsMenu.ComboBoxOptionPreset(None, self.tabObjects)
        self.cbObjectOptionPreset.setObjectName("cbObjectOptionPreset")
        self.cbObjectOptionPreset.setToolTip("Export options applied to selected object(s)")
        self.cbObjectOptionPreset.setEditable(False)
        self.cbObjectOptionPreset.setMaximumWidth(130)
        self.cbObjectOptionPreset.setMinimumWidth(130)
        self.horizontalLayout_6.insertWidget(15,self.cbObjectOptionPreset) #Caution! Here adjust item offset in layout if adding new items
        ## Filter Object(s)
        self.btnHierarchyViewFilter.setIconSize(QSize(20, 20))
        self.btnHierarchyViewFilter.setIcon(self.viewFilterLabelIcon)
        self.btnHierarchyViewFilter.setText("")
        self.btnHierarchyViewFilter.clicked.connect(self._clickedHierarchyViewFilter)
        self.filterObjects.returnPressed.connect(self._clickedFilterItemObjects)
        btnClearFilterObjects = self.filterObjects.findChild(QToolButton)
        btnClearFilterObjects.clicked.connect(self._clickedFilterItemObjects) # ClearButton event
        self.cbFilterExportableOnly.stateChanged.connect(self._changeCheckboxExportableOnly)
        self.cbFilterVisibleOnly.stateChanged.connect(self._changeCheckboxVisibleOnly)
        self.cbFilterLodsOnly.stateChanged.connect(self._changeCheckboxLodsOnly)
        self.sbFilterLodsNumber.valueChanged.connect(self._changeSpinboxLodsOnlyNumber)
        #endregion

        #region Objects Tab
        ## LOD(s) View Tree Set Up
        columnIdName = const.getEnumId(const.OBJECTS_COLUMN.NAME)
        columnIdEfficiency = const.getEnumId(const.OBJECTS_COLUMN.EFFICIENCY)
        columnIdDrawCount = const.getEnumId(const.OBJECTS_COLUMN.DRAW_COUNT)
        columnIdVertexCount = const.getEnumId(const.OBJECTS_COLUMN.VERTEX_COUNT)
        columnIdLodMinSize = const.getEnumId(const.OBJECTS_COLUMN.LOD_MIN_SIZE)
        columnIdPath = const.getEnumId(const.OBJECTS_COLUMN.PATH)
        columnIdInfo = const.getEnumId(const.OBJECTS_COLUMN.INFO)
        self.verticalLayout_4.removeWidget(self.treeLODs)
        self.treeLODs.deleteLater()
        self.treeLODs = treeViewLods.TreeViewLods(self.tabObjects)
        self.treeLODs.setAlternatingRowColors(True)
        self.treeLODs.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeLODs.setIndentation(20)
        self.treeLODs.setObjectName("treeLODs")
        self.treeLODs.setSortingEnabled(True)
        self.treeLODs.sortItems(columnIdName, Qt.SortOrder.AscendingOrder)
        self.treeLODs.header().setDefaultSectionSize(100)
        self.treeLODs.headerItem().setText(columnIdName, QApplication.translate("MultiExporter", "         Hierarchy", None, -1))
        self.treeLODs.setColumnWidth(columnIdName, 450)
        self.treeLODs.headerItem().setText(columnIdEfficiency, QApplication.translate("MultiExporter", "~Efficiency", None, -1))
        self.treeLODs.headerItem().setToolTip(columnIdEfficiency, "(Quick estimation: not fully accurate)\nMesh efficiency: the higher the better.\nThis checks current LOD vertex count against optimal vertex count\n(optimal means all vertices welded together: it will almost NEVER be the case)")
        self.treeLODs.setColumnWidth(columnIdEfficiency, 80)
        self.treeLODs.headerItem().setText(columnIdDrawCount, QApplication.translate("MultiExporter", "~Draw count", None, -1))
        self.treeLODs.headerItem().setToolTip(columnIdDrawCount, "(Quick estimation: not fully accurate)\nDraw count. May differ from actual ingame count")
        self.treeLODs.headerItem().setText(columnIdVertexCount, QApplication.translate("MultiExporter", "~Vertex count", None, -1))
        self.treeLODs.headerItem().setToolTip(columnIdVertexCount, "(Quick estimation: not fully accurate)\nVertex count. May differ from actual ingame count")
        self.treeLODs.headerItem().setText(columnIdLodMinSize, QApplication.translate("MultiExporter", "LOD Min size %", None, -1))
        self.treeLODs.headerItem().setToolTip(columnIdLodMinSize, "LOD minimum display size: expressed in screen height percentage")
        self.treeLODs.headerItem().setText(columnIdPath, QApplication.translate("MultiExporter", "Path", None, -1))
        self.treeLODs.setColumnWidth(columnIdPath, 450)
        self.treeLODs.headerItem().setText(columnIdInfo, QApplication.translate("MultiExporter", "", None, -1)) # As this is just extra info, remove header text
        self.verticalLayout_4.insertWidget(1, self.treeLODs)
        self.checkBoxLODModifier = qtUtils.createCheckBox(qtWidget=self.treeLODs)
        self.treeLODs.setGlobalCheckBox(self.checkBoxLODModifier)
        self.treeLODs.itemClicked.connect(lambda item, column : (self._clickedLOD(item, column)))
        self.treeLODs.itemSelectionChanged.connect(self._selectionChangedLOD)

        ## Disable UI for Objects tab as nothing is selected by default
        self.setEnabledState_ObjectViewProperties(False)
        #endregion

        #region Presets View UI

        ## Add New Preset Button
        self.btnAddPreset.pressed.connect(self._clickedAddPreset)
        ## Add Existing Preset(s) Button
        self.btnAddExistingPresets.setIconSize(QSize(20, 20))
        self.btnAddExistingPresets.setIcon(self.listAddIcon)
        self.btnAddExistingPresets.setText(" Existing") #add space around text, no useful padding property for that...
        self.btnAddExistingPresets.pressed.connect(self._clickedAddExistingPresets)
        ## Remove Preset(s) Button
        self.btnRemovePreset.pressed.connect(self._clickedRemovePreset)
        ## Duplicate Preset(s) Button
        self.btnDuplicatePreset.pressed.connect(self._clickedDuplicatePreset)
        ## Edit Preset(s) Path(s)
        self.btnEditPresetPath.pressed.connect(self._clickedEditPresetPath)
        ## Edit Group Path(s)
        self.btnEditGroupPath.pressed.connect(self._clickedEditGroupPath)
        ## Add New Group By Giving a Path
        self.btnAddGroup.setIconSize(QSize(20, 20))
        self.btnAddGroup.setIcon(self.addFolderIcon)
        self.btnAddGroup.setText(" Group") #add space around text, no useful padding property for that...
        self.btnAddGroup.pressed.connect(self._clickedAddPresetGroupWithPath)
        ## Save Preset Configuration
        self.saveglTFConfigurationAction.triggered.connect(self._clickedSavePresetsConfiguration)
        ## Import Preset Configuration
        self.importglTFConfigurationAction.triggered.connect(self._clickedImportPresets)
        ## Option Preset Combo Box Options Applied to Group(s) of Preset(s)
        self.horizontalLayout_9.removeWidget(self.cbOptionPreset)
        self.cbOptionPreset.deleteLater()
        self.cbOptionPreset = optionsMenu.ComboBoxOptionPreset(None,self.verticalLayoutWidget_2)
        self.cbOptionPreset.setObjectName("cbOptionPreset")
        self.cbOptionPreset.setToolTip("Option preset applied to the selected group(s) or object(s) in the presets view")
        self.cbOptionPreset.setEditable(False)
        self.cbOptionPreset.setMaximumWidth(130)
        self.cbOptionPreset.setMinimumWidth(130)
        self.horizontalLayout_9.insertWidget(6, self.cbOptionPreset)
        self.cbOptionPreset.activated.connect(self._clickedApplyOptionPresetToGroup)
        ## Filter Preset(s) Bar
        self.btnPresetViewFilter.setIconSize(QSize(20, 20))
        self.btnPresetViewFilter.setIcon(self.viewFilterLabelIcon)
        self.btnPresetViewFilter.setText("")
        self.btnPresetViewFilter.clicked.connect(self._clickedPresetViewFilter)
        self.filterPresets.returnPressed.connect(self._clickedFilterItemPresets)
        btnClearFilterPresets = self.filterPresets.findChild(QToolButton)
        btnClearFilterPresets.clicked.connect(self._clickedFilterItemPresets) # ClearButton event
        # Set initial splitter pos to let layers have more space
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 3)
        #endregion

        #region Presets Tab
        ## Preset(s) View Tree Set Up
        columnIdName = const.getEnumId(const.PRESETS_COLUMN.NAME)
        columnIdPath = const.getEnumId(const.PRESETS_COLUMN.PATH)
        self.verticalLayout_9.removeWidget(self.treePresets)
        self.treePresets.deleteLater()
        self.treePresets = treeViewPreset.TreeViewPreset(self.tabPresets)
        self.treePresets.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treePresets.sizePolicy().hasHeightForWidth())
        self.treePresets.setSizePolicy(sizePolicy)
        self.treePresets.setDragEnabled(True)
        self.treePresets.setDragDropMode(QAbstractItemView.DragDrop)
        self.treePresets.setDefaultDropAction(Qt.MoveAction)
        self.treePresets.setAlternatingRowColors(True)
        self.treePresets.setSortingEnabled(True)
        self.treePresets.sortItems(columnIdName, Qt.SortOrder.AscendingOrder)
        self.treePresets.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treePresets.setObjectName("treePresets")
        self.treePresets.headerItem().setText(columnIdName, QApplication.translate("MultiExporter", "         Name", None, -1))
        self.treePresets.setColumnWidth(columnIdName, 450)
        self.treePresets.headerItem().setText(columnIdPath, QApplication.translate("MultiExporter", "Path", None, -1))
        self.treePresets.setColumnWidth(columnIdPath, 450)
        self.verticalLayout_9.insertWidget(2, self.treePresets)
        self.treePresets.itemSelectionChanged.connect(self._selectionChangedPreset)
        self.checkBoxPresetModifier = qtUtils.createCheckBox(qtWidget=self.treePresets)
        self.treePresets.setGlobalCheckBox(self.checkBoxPresetModifier)

        header = self.treePresets.header()
        header.setDefaultSectionSize(250)
        
        ## Expand All Preset(s)
        self.btnPresetExpandAll.pressed.connect(self.treePresets.expandAll)
        ## Collapse All Preset(s)
        self.btnPresetCollapseAll.pressed.connect(self.treePresets.collapseAll)

        ## Disable UI for Presets tab as nothing is selected by default
        self.setEnabledState_PresetsViewProperties(False)
        #endregion
        
        #region Layers Tab
        ## Apply Layer(s) to Preset(s)
        self.btnApplyPresetLayer.pressed.connect(self._clickedApplyLayerSelection)

        # Layer(s) View Tab Set Up
        self.verticalLayout_11.removeWidget(self.treeLayer)
        self.treeLayer.deleteLater()
        self.treeLayer = treeViewLayer.TreeViewLayer(self.tabPresets)
        self.treeLayer.setAlternatingRowColors(True)
        self.treeLayer.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeLayer.setSortingEnabled(True)
        self.treeLayer.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.treeLayer.setObjectName("treeLayer")
        self.treeLayer.headerItem().setText(0, QApplication.translate("MultiExporter", "         Layers", None, -1))
        self.verticalLayout_11.insertWidget(1, self.treeLayer)
        self.checkBoxLayerModifier = qtUtils.createCheckBox(qtWidget=self.treeLayer)
        self.checkBoxLayerModifier.setTristate(True)
        self.treeLayer.setGlobalCheckBox(self.checkBoxLayerModifier)
        self.treeLayer.itemChanged.connect(self._changedLayerItem)

        ## Expand All Layer(s) Button
        self.btnLayerExpandAll.pressed.connect(self.treeLayer.expandAll)
        ## Collapse All Layer(s) Button
        self.btnLayerCollapseAll.pressed.connect(self.treeLayer.collapseAll)
        ## Reload Layers from scene
        self.reloadLayersButton.pressed.connect(lambda : self.treeLayer.refreshTree(progressBar=self.progressBar, lbProgressBar=self.lbProgressBar))

        self.setFocus()
        self.installEventFilter(self)
        # Init disabled
        self.treeLayer.setEnabled(False)
        #endregion
        
        #region Tab Widget
        if self.lastOpenedPanel == const.TAB.OBJECTS.name:
            self.tabWidget.setCurrentWidget(self.tabObjects)
        else:
            self.tabWidget.setCurrentWidget(self.tabPresets)
        #endregion

        #region Logger
        self.loggerWidget = LoggerWidget()
        self.loggerAreaVLayout.addWidget(self.loggerWidget)
        self.loggerWidget.adjustLoggerLineHeight()
        handler.emitter.logRecord.connect(self.loggerWidget.appendLogRecord)
        #endregion

        #region Common stuff
        ## Disable common UI for Objects and Presets tab as nothing is selected by default
        self.setEnabledState_CommonViewProperties(False)
        qtUtils.resetProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar)
        #endregion

        return

    def initTrees(self):
        """ Init Object(s) and Preset(s) Trees"""
        if self.lastOpenedPanel == const.TAB.OBJECTS.name:
            self.treeLODs.createTree()
            self.setupObjectsTab()
            self.adjustLodListRelatedUI() #Objects tab: adjust needed UI
        else:
            self.treePresets.createTree()
            self.treeLayer.createTree()
            self.setupPresetsTab()
        self.showRelevantTip()

    def initCustomScripts(self):
        # Following is used to retrieve used material IDs faster than a maxscript function
        # Thanks to https://www.scriptspot.com/forums/3ds-max/general-scripting/get-used-material-id-list-from-editablepoly-without-face-check
        RT.execute(" MSFS2024_Functions.initGetUsedMtlIDs()") ## You can find this script in MSFS2024_Functions.ms

    #endregion

    #region Overloading Events
    def closeEvent(self, event):
        if(self.optionsMenuWindow != None):
            self.optionsMenuWindow.close()
            self.optionsMenuWindow = None
        if sharedGlobals.G_ME_meshInspectorWindow != None:
            sharedGlobals.G_ME_meshInspectorWindow.close()
            sharedGlobals.G_ME_meshInspectorWindow = None

        sceneUtils.setSceneNodeUserProp(self.sceneRoot, const.PROP_LAST_OPENED_PANEL, self.lastOpenedPanel)
        global window
        window = None

    def contextMenuEvent(self, event):
        rect = self.tabWidget.geometry()
        if(rect.contains(event.pos())): # This is shitty: should have been the actual tree widget geometry, but for some reason it introduces an offset...
            menu = QMenu(self)
            isLodView = self.currentTabIs(const.TAB.OBJECTS)
            isPresetView = self.currentTabIs(const.TAB.PRESETS)
            if(isLodView):
                selectInScene = menu.addAction("Select in scene")
                openFolder = menu.addAction("Open export folder")
                menu.addSeparator()
                exportAll = menu.addAction("Export")
                exportGltf = menu.addAction("Export Gltf only")
                generateXML = menu.addAction("Export XML only")
            if (isPresetView):
                rename = menu.addAction("Rename selected")
                remove = menu.addAction("Remove selected")
                duplicate = menu.addAction("Duplicate selected")
                menu.addSeparator()
                addPreset = menu.addAction("Add new preset")
                addGroup = menu.addAction("Add new group")
                menu.addSeparator()
                openFolder = menu.addAction("Open export folder")
                menu.addSeparator()
                exportAction = menu.addAction("Export")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if (isLodView):
                if action == exportAll:
                    self._clickedExport(exportOption=const.EXPORT_OPTION.SELECTED, overrideGltfXmlOptions = (True, True))
                if action == exportGltf:
                    self._clickedExport(exportOption=const.EXPORT_OPTION.SELECTED, overrideGltfXmlOptions = (True, False))
                if action == generateXML:
                    self._clickedExport(exportOption=const.EXPORT_OPTION.SELECTED, overrideGltfXmlOptions = (False, True))
                if action == selectInScene:
                    tree = self.getCurrentTree()
                    tree.selectSceneNodesFromTreeItems(tree.getSelectedSubTreeItems())
            if (isPresetView):
                if action == rename:
                    self._clickedRenamePreset()
                if action == addPreset:
                    self._clickedAddPreset()
                if action == addGroup:
                    self._clickedAddPresetGroupWithPath()
                if action == remove:
                    self._clickedRemovePreset()
                if action == duplicate:
                    self._clickedDuplicatePreset()
                if action == exportAction:
                    self._clickedExport(exportOption=const.EXPORT_OPTION.SELECTED)
            if action == openFolder:
                self._clickedOpenExportFolder()
    
    #endregion

    #region Events Handlers
    def _clickedFilterItemObjects(self):
        self.filterSceneHierarchyList()
    
    def _clickedHierarchyViewFilter(self):
        self.adjustSceneHierarchyFilterUI()
        self.filterSceneHierarchyList()

    def _clickedFilterItemPresets(self):
        self.filterPresetsList()
    
    def _clickedPresetViewFilter(self):
        self.adjustPresetsFilterUI()
        self.filterPresetsList()

    def _refreshOptionPreset(self):
        self.refreshOptionPreset()

    def _openOptionsMenu(self):
        if (self.optionsMenuWindow == None):
            self.optionsMenuWindow = optionsMenu.OptionsMenu(parent=self)
            self.optionsMenuWindow.currentTab = self.getCurrentTab()
            self.optionsMenuWindow.show()
            self.optionsMenuWindow.onClosed.connect(lambda: self._closeOptionsMenu())
            self.optionsMenuWindow.onModifiedData.connect(lambda : self._refreshOptionPreset())
            self.optionsMenuWindow._initUIPanelSpecifics()
        else:
            # Changed default behavior to Modal so should not need this.
            # Left it in case we want old behavior in the near future
            self.optionsMenuWindow.activateWindow()
        self.btnOptions.setDown(False) # because we're dealing with a modal window now, button will get stuck pressed

    def _closeOptionsMenu(self):
        self.optionsMenuWindow = None
    
    def _openMeshInspectorWindow(self):
        if not MeshInspectorWindow.open(sceneUtils.getSceneRootNode()):#, self):
            qtUtils.popup("Nothing to inspect", title="Nothing to inspect")

    def _openTextureTool(self):
        TT.run()

    def _clickedResolveUniqueID(self):
        babylonPYMXS2024.runResolveID()

    def _clickedConformLayers(self, prompt=True):
        self.conformSceneLayersToLODView(prompt=prompt)

    def _clickedAddPresetGroupWithPath(self):
        initDir = ""
        presets = self.treePresets.getSelectedPresets()
        if len(presets) > 0:
            initDir = presets[0].path

        filePath = presetUtils.askForNewDirectoryPath(title="Create New Group", initDir=initDir)
        groupName = "NewGroup"
        groupPath = ".\\"
        if filePath is not None and filePath != "":
            groupName = os.path.basename(filePath)
            filePath = utility.convertAbsolutePathToRelative(filePath, RT.pathConfig.getCurrentProjectFolder())
            newGroup = presetUtils.createNewGroup(groupName=groupName, optionPreset=None, filePath=filePath)
            groupItem = self.treePresets.createRootWidget(obj=newGroup)

            if len(presets) > 0:
                for preset in presets:
                    groupPath = newGroup.path + '\\' + preset.name + '.gltf'
                    preset.edit(group=newGroup.identifier, path=groupPath)
                    self.treePresets._updateParentingPreset(preset, groupItem)
                    
        self.btnAddGroup.setDown(False)

    def _clickedAddPreset(self):
        groups = self.treePresets.getSelectedGroups()
        groupID = None
        defaultFilePath = ""

        if (len(groups) > 0):
            groupID = groups[0].identifier
            defaultFilePath = groups[0].path

        filePath = presetUtils.askForCustomSavePath("Create or select gltf file", defaultFilePath, fileMode=QFileDialog.FileMode.AnyFile, relative=True)
        if filePath is not None:
            presetName = os.path.split(filePath)[1]
            presetName = os.path.splitext(presetName)[0]
            preset = presetUtils.createNewPreset(presetName, group=groupID, filePath=filePath)

            self.treePresets.createRootWidget(obj = preset)

        self.btnAddPreset.setDown(False)

    def _clickedAddExistingPresets(self):
        groups = self.treePresets.getSelectedGroups()
        groupID = None
        defaultFilePath = ""

        if (len(groups) > 0):
            groupID = groups[0].identifier
            defaultFilePath = groups[0].path

        filePaths = presetUtils.askForCustomSavePath("Select one or more gltf file(s)", defaultFilePath, fileMode=QFileDialog.FileMode.ExistingFiles, relative=True)
        if filePaths is None:
            self.btnAddExistingPresets.setDown(False)
            return
        
        for path in filePaths: ## for all presets paths
            presetName = os.path.split(path)[1]
            presetName = os.path.splitext(presetName)[0]
            preset = presetUtils.createNewPreset(presetName, group=groupID, filePath=path)

            self.treePresets.createRootWidget(obj = preset)

        self.btnAddExistingPresets.setDown(False)

    def _clickedRenamePreset(self):
        self.treePresets.startEditingSelectedItem()

    def _clickedSavePresetsConfiguration(self):
        currentTree = self.getCurrentTree()
        if (currentTree != self.treePresets):
            return

        presets = self.treePresets.getAllPresetsList()
        if len(presets) == 0:
            RT.messageBox("There is no presets to save")
            return
        
        filePath = qtUtils.openSaveFileNameDialog(caption="Export presets configuration location",  _filter= "MEP(*.mep)", _dir="", forcedExtension=".mep")
        if (filePath is None):
            RT.messageBox("File coult not be opened/created")
            return

        self.resetPresetCFG()
        for preset in presets:
            PrsObjDic = {}
            for POK in dir(preset):
                ExculeList = ["_load","_write","create","delete","edit","get"]
                if POK in ExculeList:
                    continue

                if  "__" in POK:
                    continue

                if isinstance(getattr(preset, POK), str):
                    PrsObjDic[POK] = getattr(preset, POK)
                    if POK == "group":
                        groupQtItem = self.treePresets.getQtGroupItemFromIdentifier(PrsObjDic[POK])
                        PrsObjDic[POK] += ",{0}".format(groupQtItem.text(0) if groupQtItem is not None else "")

                elif isinstance(getattr(preset, POK), list):
                    ListinStr = ""
                    lst = getattr(preset,POK)
                    for j in range(len(lst)):
                        if j == 0:
                            ListinStr = "{0}".format(lst[j])
                        else:
                            ListinStr = "{0},{1}".format(ListinStr,lst[j])
                    PrsObjDic[POK] = ListinStr

            #Debug What will be serialized
            for objs in PrsObjDic:
                print("{0} = {1}".format(objs,PrsObjDic[objs]))

            self.writeExportPresetsCFG(presetName = preset.identifier, _PrsObjDic = PrsObjDic, filepath = filePath)

    def _clickedImportPresets(self):
        filePath = qtUtils.openSaveFileNameDialog(caption="Import presets configuration",  _filter= "MEP(*.mep)", _dir="", forcedExtension=".mep")
        presetList = self.getPresetsCFG(filepath = filePath)
        for preset in presetList:
            name = ""
            LayerNames = []
            path = ""
            missingLayers = []
            groupID = None

            #Prepare Data For Preset Creation
            for param in preset:
                if param == "name":
                    name = preset[param]
                if param == "layernames":
                    LayerNames = preset[param].split(",")
                if param == "path":
                    path = preset[param]
                if param == "group":
                    groupParam = preset[param].split(",")
                    groupID = groupParam[0] if len(groupParam) > 0 else None
                    groupName = groupParam[1] if len(groupParam) > 1 else None

            #CheckforSceneIncompatibility
            for strLay in LayerNames:
                lay = layer.get_layer(strLay)
                if lay == None:
                    missingLayers.append(strLay)

            if len(missingLayers) > 0:
                misLayString = ""
                for i in range(len(missingLayers)):
                    if i == 0:
                        misLayString = missingLayers[i]
                    else:
                        misLayString = "{0}, {1}".format(misLayString, missingLayers[i])
                qtUtils.popup("Your scene configuration does not match with the preset you are trying to import (Layers: {0} are missing)".format(misLayString), title="Preset Import Error")
                return

            #CreatenewPreset
            newPreset = presetUtils.createNewPreset(labelName = name, group = groupID, filePath=path)
            newPreset.edit(layerNames=LayerNames)
            self.treePresets.createRootWidget(obj = newPreset)
            if groupID is None:
                continue

            groupQtItem = self.treePresets.getQtGroupItemFromIdentifier(groupID)
            if groupQtItem is None:
                groupPath = os.path.dirname(path) 
                groupName = os.path.basename(groupPath) if groupName is None else groupName
                newGroup = presetUtils.createNewGroup(groupName=groupName, optionPreset=None, filePath=groupPath, identifier=groupID)
                groupQtItem = self.treePresets.createRootWidget(obj = newGroup)

            if groupQtItem is not None:
                self.treePresets._updateParentingPreset(newPreset, groupQtItem)

    def _clickedRemovePreset(self):
        groups = self.treePresets.getSelectedGroups()
        presets = self.treePresets.getSelectedPresets()

        for group in groups:
            childs = self.treePresets.getPresetsFromGroup(group)
            for child in childs:
                found = next((True for preset in presets if preset.identifier == child.identifier), False)
                if found:
                    continue
                presets.append(child)

        self.treePresets.removeItems(presets=presets, groups=groups)

    def _clickedDuplicatePreset(self):
        groups = self.treePresets.getSelectedGroups()
        presets = self.treePresets.getSelectedPresets()
        groupTransfer = dict()
        for group in groups:
            oldId = group.identifier
            newGroup = presetUtils.createNewGroup(groupName=group.name, optionPreset=group.optionPreset, filePath=group.path)
            self.treePresets.createRootWidget(obj=newGroup)
            newId = newGroup.identifier
            groupTransfer[oldId] = newId
            childs = self.treePresets.getPresetsFromGroup(group)
            for child in childs:
                presets.append(child)

        for preset in presets:
            targetGroup = preset.group
            if targetGroup in groupTransfer:
                targetGroup = groupTransfer[targetGroup]
            filepath = preset.path
            newPreset = presetUtils.createNewPreset(labelName=preset.name, group=targetGroup, filePath=filepath, layerNames=preset.layerNames)
            self.treePresets.createRootWidget(obj=newPreset)

    def _changedTab(self):
        self.showRelevantTip()
        #Add a switch case to handle each tab
        if self.currentTabIs(const.TAB.OBJECTS):
            self.setupObjectsTab()
            self.treeLODs.createTree()
            self.lastOpenedPanel = const.TAB.OBJECTS.name

        elif self.currentTabIs(const.TAB.PRESETS):
            self.setupPresetsTab()
            self.treePresets.createTree(progressBar=self.progressBar, lbProgressBar=self.lbProgressBar)
            self.treeLayer.createTree(progressBar=self.progressBar, lbProgressBar=self.lbProgressBar)
            self.lastOpenedPanel = const.TAB.PRESETS.name

    ## Nothing to see here. Look away.
    def _quackQuack(self):
        fullWinValue = 30 # If you reached this number, I'd say you win.
        if (self.quackQuack < len(self.quackQuackIcons)):
            self.coin.setIcon(self.quackQuackIcons[self.quackQuack])
            self.quackQuack += 1
        else:
            if (self.coinCoin == 0 or self.quackQuack != (0 + len(self.quackQuackIcons))):
                self.quackQuack = random.randrange(0, len(self.coinCoinIcons))
                self.coin.setIcon(self.coinCoinIcons[self.quackQuack])
                self.quackQuack += len(self.quackQuackIcons)
                self.coin.setToolTip("Dont click on the snowflake!")
                self.lbCoin.setText(">")
                self.lbCoin.setToolTip("Try your luck!")
                successColor = QColor.fromHsl(min(120, self.coinCoin * 120 / fullWinValue), 255, 160, 60)
                p = self.coin.palette()
                p.setColor(self.coin.backgroundRole(), successColor)
                self.coin.setPalette(p)
                self.coinCoin += 1
            else:
                self.coinCoin -= 1
                self.coin.setToolTip("")
                self.coin.setEnabled(False)
                self.lbCoin.setToolTip("You succeeded {0} times".format(self.coinCoin))
                self.lbCoin.setText(str(self.coinCoin))
                successColor = QColor.fromHsl(min(120, self.coinCoin * 120 / fullWinValue), 255, 160)
                displayUtils.setLabelColor(self.lbCoin, successColor)
    ## You have seen nothing. Especially not these droids.

    def _clickedOpenExportFolder(self):
        exportPath = None

        if self.currentTabIs(const.TAB.OBJECTS):
            selected = self.treeLODs.getSelectedSceneRootNodesList()
            if len(selected) < 1:
                return
            exportPath = exporter.getAbsoluteExportPath(selected[0])

        elif self.currentTabIs(const.TAB.PRESETS):
            selectedGroups = self.treePresets.getSelectedGroups()
            if len(selectedGroups) < 1:
                selected = self.treePresets.getSelectedPresets()
                if len(selected) < 1:
                    return
                exportPath = presetUtils.getAbsoluteExportPath(selected[0])
            else:
                exportPath = presetUtils.getAbsoluteExportPath(selectedGroups[0])

        if exportPath is None:
            if self.currentTabIs(const.TAB.OBJECTS):
                qtUtils.popup(text="There is no export path, please add one or select another object in list")
            elif self.currentTabIs(const.TAB.PRESETS):
                qtUtils.popup(text="There is no export path, please add one or select a preset or group with a valid path")
            return

        if os.path.isfile(exportPath):
            exportPath = os.path.dirname(exportPath)

        try:
            os.startfile(exportPath)
        except WindowsError:
            qtUtils.popup(title="WindowsError", text="The given path does not exist")

        self.btnOpenExportFolder.setDown(False) # in case we display a popup, button will get stuck pressed

    def _changeCheckboxExportableOnly(self):
        self.filterSceneHierarchyList()

    def _changeCheckboxLodsOnly(self):
        self.sbFilterLodsNumber.setEnabled(bool(self.cbFilterLodsOnly.checkState() == Qt.Checked))
        self.filterSceneHierarchyList()

    def _changeSpinboxLodsOnlyNumber(self):
        self.filterSceneHierarchyList()

    def _changeCheckboxVisibleOnly(self):
        self.filterSceneHierarchyList()

    def _changeCheckboxSelectChildrenInScene(self):
        state = self.cbSelectInSceneSelectsChildren.checkState() == Qt.Checked
        self.treeLODs._selectInSceneSelectsChildren = state
        self.treeLayer._selectInSceneSelectsChildren = state

    def _changeCheckboxAlwaysSelectInScene(self):
        state = self.cbAlwaysSelectInScene.checkState() == Qt.Checked
        self.treeLODs._alwaysSelectInScene = state
        self.treeLayer._alwaysSelectInScene = state

    def _clickedEditPresetPath(self):
        selectedPresets = self.treePresets.getSelectedPresets()
        presetUtils.changeExportPathForPresets(selectedPresets)

        for selectedPreset in selectedPresets:
            self.treePresets.resfreshQtPresetItemFromID(id = selectedPreset.identifier, obj = selectedPreset)

    def _clickedEditGroupPath(self):
        groups = self.treePresets.getSelectedGroups()

        if (len(groups) == 0):
            RT.messageBox("Please select a group")
            return

        presetUtils.addExportPathToGroups(groups)
        for group in groups:
            if group.path == '.':
                continue

            presets = self.treePresets.getPresetsFromGroup(group)
            for preset in presets:
                newPath = group.path + '\\' + preset.name + '.gltf'
                preset.edit(path=newPath)
                self.treePresets.resfreshQtPresetItemFromID(id = preset.identifier, obj = preset)

            self.treePresets.resfreshQtGroupItemFromID(id = group.identifier, obj = group)

    def _changedLayerItem(self):
        selected = self.treePresets.getSelectedPresets()
        if len(selected) != 1:
            return
        self.lastEditedPreset = selected[0]
        self.treeLayer.isEdited = True
        self.btnApplyPresetLayer.setText("Apply*")

    def _selectionChangedPreset(self):
        if (self.treeLayer.isEdited and self.lastEditedPreset):
            layerSelection = self.treeLayer.getCheckedLayerNames()
            self.applyLayerSelectionToPreset(self.lastEditedPreset, layerSelection)
                
        selectedGroups = self.treePresets.getSelectedGroups()
        if len(selectedGroups) == 1:
            self.treeLayer.uncheckAllLayers()
            self.treeLayer.setEnabled(False)

            optionPresetId = self.cbOptionPreset.getOptionPresetIndexByIdentifier(selectedGroups[0].optionPreset)
            if optionPresetId is not None:
                self.cbOptionPreset.setCurrentIndex(optionPresetId)
            else:
                self.cbOptionPreset.setCurrentIndex(0)
        else:
            selectedPresets = self.treePresets.getSelectedPresets()
            if len(selectedPresets) == 1:
                self.treeLayer.setEnabled(True)
                preset = selectedPresets[0]

                layerNames = preset.layerNames
                self.treeLayer.intializeCheckLayers(layerNames)

                if len(self.treeLayer.getPartCheckedLayerNames()) == 0:
                    checkedItems = self.treeLayer.getCheckedLayers()
                    for ci in checkedItems:
                        self.treeLayer._changedWidgetItem(widget=ci, col=0)
                self.btnApplyPresetLayer.setText("Apply")

                optionPreset = self.treePresets.joinOptionsToPresets([preset])[0][1] # returns a list of Tuple(preset, optionPreset)
                optionPresetId = self.cbOptionPreset.getOptionPresetIndexByIdentifier(optionPreset.identifier)
                if optionPresetId is not None:
                    self.cbOptionPreset.setCurrentIndex(optionPresetId)
                else:
                    self.cbOptionPreset.setCurrentIndex(0)
            else:
                self.treeLayer.uncheckAllLayers()
                self.treeLayer.setEnabled(False)

        ## UI adjust
        selectedState = (len(selectedGroups) > 0 or len(selectedPresets) > 0)
        self.setEnabledState_CommonViewProperties(selectedState)
        self.setEnabledState_PresetsViewProperties(selectedState)

    def _clickedApplyOptionPresetToGroup(self):
        selectedPresets = self.treePresets.getSelectedPresets()
        if len(selectedPresets) > 0:
            RT.messageBox("Option presets are applied to groups, please select a group.")
            return

        groups = self.treePresets.getSelectedGroups()
        if len(groups) < 1:
            return
            
        optionIndex = self.cbOptionPreset.currentIndex()
        if optionIndex < 0:
            return

        optionPreset = self.cbOptionPreset.itemData(optionIndex)
        for group in groups:
            group.edit(optionPreset=optionPreset.identifier)
            
        self.treeLayer.setEnabled(False)
        self.cbObjectOptionPreset._changedIndex(optionIndex)

    def _clickedApplyLayerSelection(self):
        presets = self.treePresets.getSelectedPresets()
        checkedLayers = self.treeLayer.getCheckedLayerNames()
        for preset in presets:
            self.applyLayerSelectionToPreset(preset, checkedLayers)

    def _clickedLOD(self, item, column):
        if (column == 0): # We want to update checkbox status, wich is located in column 0, so only check for changes if click occured in checkbox's column
            # JUST to fix broken behavior of parent tristate checkboxes. FfffFFFfffFffff....
            self.treeLODs.fixTreeCheckBoxes(item) 

        if (item.parent() == None):
            # Try to illustrate that selecting only parent is the SAME as selecting all children too by propagating selection
            self.treeLODs.propagateTreeSelection(item) #Try to illustrate that selecting only parent is the SAME as selecting all children too by propagating selection

    def _selectionChangedLOD(self):
        # Here want to adjust selection, but this is not possible because itemSelectionChanged event is fired before itemClicked event. See _clickedLOD() above
        selected = self.treeLODs.getSelectedSceneRootNodesList()
        if len(selected) > 0:
            self.setEnabledState_ObjectViewProperties(True)
            self.setEnabledState_CommonViewProperties(True)

            self.autoSetupTransformExportForObjectsPanel(selected) #Fix any un-specified transform

            self.checkBoxStateFromSelection(self.cbAutoLODs, selected, const.PROP_AUTO_LOD)
            self.textFieldStateFromSelection(self.lodValue, selected, const.PROP_LOD_VALUE)
            self.transformButtonStateFromSelection(selected)
            return
        
        self.setEnabledState_ObjectViewProperties(False)
        self.setEnabledState_CommonViewProperties(False)

    def _changeCheckboxAutoLODs(self):
        lods = self.treeLODs.getSelectedSceneRootNodesList()
        for lod in lods:
            autoGenState = self.cbAutoLODs.checkState()
            if autoGenState == Qt.PartiallyChecked:
                continue
            autoGen = True if autoGenState == Qt.Checked else False
            userprop.setUserProp(lod, const.PROP_AUTO_LOD, autoGen)

        self.checkBoxStateFromSelection(self.cbAutoLODs, lods, const.PROP_AUTO_LOD)
        self.refreshObjectListItems()

    def _clickedAdjustLodValue(self):
        lods = self.treeLODs.getSelectedSceneRootNodesList()
        errorLog = ""
        for lod in lods:
            minimumLodValue = sceneUtils.getObjectLowestSizePercent(lod)
            safeLodValue = minimumLodValue * (1.0 + sceneUtils.getSafeLodMargin())
            safeLodValue = utility.roundToUpper(safeLodValue, 2)
            currentLodValue = sceneUtils.getLODValue(lod, const.PROP_LOD_VALUE)
            if currentLodValue is not None and currentLodValue >= minimumLodValue:
                continue
            # we only change truly bad setup. If a value is within the tolerance margin, then it's up to the user
            errorLog += sceneUtils.setLODValue(lod, const.PROP_LOD_VALUE, safeLodValue)

        self.textFieldStateFromSelection(self.lodValue, self.treeLODs.getSelectedSceneRootNodesList(), const.PROP_LOD_VALUE) #update LOD value text field
        self.refreshObjectListItems()
        if errorLog == "":
            MSFS2024ExportLogger.error(errorLog)

    def _clickedSetExportPosition(self, checked):
        trs = ExportTransforms(checked, self.btnExportRotation.isChecked(), self.btnExportScale.isChecked())
        self.setLODsExportTransform(trs)
        qtUtils.setButtonTristateWithColors(self.btnExportPosition, False)
    
    def _clickedSetExportRotation(self, checked):
        trs = ExportTransforms(self.btnExportPosition.isChecked(), checked, self.btnExportScale.isChecked())
        self.setLODsExportTransform(trs)
        qtUtils.setButtonTristateWithColors(self.btnExportRotation, False)
    
    def _clickedSetExportScale(self, checked):
        trs = ExportTransforms(self.btnExportPosition.isChecked(), self.btnExportRotation.isChecked(), checked)
        self.setLODsExportTransform(trs)
        qtUtils.setButtonTristateWithColors(self.btnExportScale, False)

    def _focusInLODValues(self):
        self.lodValue.setPlaceholderText("")

    def _focusOutLODValues(self):
        self.applyLODValues()
        self.lodValue.setPlaceholderText("70.0...")

    def _clickedSetLODValues(self):
        self.applyLODValues()
        self.lodValue.clearFocus()

    def _changeCheckboxGltfExport(self):
        self._exportGltf = self.cbGltfExport.isChecked()
        if not self._exportGltf and not self._exportXml:
            self.cbXmlExport.setCheckState(Qt.Checked)

    def _changeCheckboxXmlExport(self):
        self._exportXml = self.cbXmlExport.isChecked()
        if not self._exportXml and not self._exportGltf:
            self.cbGltfExport.setCheckState(Qt.Checked)

    def _changeCheckboxTextureLib(self):
        self._exportTextureLib = self.cbTextureLib.isChecked()

    def _clickedAddExportPath(self):
        selectedLods = self.treeLODs.getSelectedSceneRootNodesList()
        forcedPath = exporter.getAbsoluteExportPath(selectedLods[0])
        exporter.addExportPathToObjects(selectedLods, forcedPath=forcedPath)
        self.refreshObjectListItems()

    def _clickedRemoveExportPath(self, prompt=True):
        selectedLods = self.treeLODs.getSelectedSceneRootNodesList()
        exporter.removeExportPathToObjects(selectedLods,prompt=prompt)
        self.refreshObjectListItems()            

    def _clickedRefreshList(self):
        self.refreshObjectListItems()
    
    def _clickedExport(self, exportOption=const.EXPORT_OPTION.NONE, overrideGltfXmlOptions=None):
        if overrideGltfXmlOptions is not None:
            self._exportGltf, self._exportXml = overrideGltfXmlOptions

        self.export(exportOption)
    #endregion

    #region Methods
    def getExportModelNamesForXmlExport(self, exportOption, visibleInListOnly):
        exportModelNamesForXmlExport = []
        if exportOption == const.EXPORT_OPTION.SELECTED:
            self.treeLODs.adjustTreeSelection_NoLonelyChild()
            exportModelNamesForXmlExport = self.treeLODs.getSelectedTopTreeNames(visibleInList=visibleInListOnly)
        elif exportOption == const.EXPORT_OPTION.CHECKED:
            self.treeLODs.adjustTreeChecked_NoLonelyChild()
            exportModelNamesForXmlExport = self.treeLODs.getCheckedTopTreeNames(visibleInList=visibleInListOnly)
        else: # exportOption == const.EXPORT_OPTION.ALL
            exportModelNamesForXmlExport = self.treeLODs.getTopTreeNames(visibleInList=visibleInListOnly)
        return exportModelNamesForXmlExport

    def exportLODsGltf(self, sceneRootNodes):
        if len(sceneRootNodes) < 1:
            return []
        MSFS2024ExportLogger.info("== GLTF EXPORT ======================================================================================================================")
        exportedGltfs = self.sendLODsToExporter(sceneRootNodes)
        return exportedGltfs

    def generateLODsXMLs(self, modelNames):
        if len(modelNames) < 1:
            return False
        MSFS2024ExportLogger.info("== XML EXPORT ======================================================================================================================")
        self.generateXmlFromListNames(modelNames)
        return True

    def exportLODs(self, exportOption):
        # For now only allow with export all...
        visibleInListOnly = self.btnHierarchyViewFilter.isChecked() and exportOption == const.EXPORT_OPTION.ALL
        
        # TODO: retrieve same errors for XML and Gltf, and adjust export accordingly: if wish to proceed anyway, should NOT attempt to export faulty XML models

        #region XML
        exportModelNamesForXmlExport = []
        if self._exportXml:
            exportModelNamesForXmlExport = self.getExportModelNamesForXmlExport(exportOption, visibleInListOnly)
        #endregion
        
        #region Prepare assets for exports
        sceneRootNodesForGltfExport = []
        errorLog = []
        bypassErrorLog = []

        if self._exportGltf and not (self._exportXml and len(exportModelNamesForXmlExport) == 0):
            # If export selected, make sure selection tree is fine. Since it is already done for XML export, avoid useless operation
            if exportOption == const.EXPORT_OPTION.SELECTED and not self._exportXml:
                self.treeLODs.adjustTreeSelection()

            if exportOption != const.EXPORT_OPTION.NONE:
                sceneRootNodesForGltfExport, errorLog, bypassErrorLog = self.treeLODs.getExportSceneRootNodesList(exportOption, exportXML=self._exportXml, visibleInListOnly=visibleInListOnly)

            self.autoSetupTransformExportForObjectsPanel(sceneRootNodesForGltfExport) #Fix any un-specified transform
        #endregion

        #region User Feedbacks
        # Errors
        if len(errorLog) > 0:
            for txt in errorLog:
                MSFS2024ExportLogger.error(txt)
            if not qtUtils.popup_Yes_No(
                title="Errors found", 
                text="Errors were found, please check Log for more infos.\n\n \
                      Proceed anyway?\n\n \
                      YES: skip errors and problematic models\n \
                      NO: cancel export"):
                return []

        # Nothing to export
        elif (self._exportXml and len(exportModelNamesForXmlExport) == 0) or (self._exportGltf and len(sceneRootNodesForGltfExport) == 0):
            msgBox = qtUtils.getNewMessageBox("You need at least one object to export.", title="Nothing to export!")
            msgBox.setStyleSheet("QLabel{min-width: 300px;}") #Message box width is driven by text but if it's too short, title gets cropped. Lets force a min-width so title is fully visible
            msgBox.exec_()
            return []
        #endregion

        #region Lonely children issues
        if len(bypassErrorLog) > 0:
            for txt in bypassErrorLog:
                MSFS2024ExportLogger.warning(txt)

            if not qtUtils.popup_Yes_No(
                title="Lonely children", 
                text="Some objects will be exported and may cause issues in the associated XML (check Log for more infos).\n \
                      If you're unsure, please fix issues before export.\n\n \
                      Proceed anyway?\n\n \
                      YES: skip errors BUT export faulty models anyway!\n \
                      NO: cancel export"
                    ):
                return []
        #endregion

        #region Export (start with GLTF as it may require scene save. If user doesn't want to: dont export anything!)
        exportedGltfs = self.exportLODsGltf(sceneRootNodesForGltfExport)

        if self.checkCancelExport():
            return exportedGltfs

        self.generateLODsXMLs(exportModelNamesForXmlExport)
        
        if self.checkCancelExport():
            return exportedGltfs

        MSFS2024ExportLogger.info("== END OF EXPORT PROCESS ============================================================================================================")
        #endregion
        return exportedGltfs

    def checkCancelExport(self):
        if sharedGlobals.G_ME_cancelExport:
            MSFS2024ExportLogger.info("== EXPORT PROCESS CANCELED ============================================================================================================")
            return True
        return False

    def updateLoggerForExport(self):
        self.loggerWidget.enableCancelExportBtn()
        if self.loggerWidget.autoClearOnExport:
            self.loggerWidget.clearLog()
    
    def exportPresets(self, exportOption):
        # For now only allow with export all...
        visibleInListOnly = self.btnHierarchyViewFilter.isChecked() and exportOption == const.EXPORT_OPTION.ALL
        exportedGltfs = []
        presetsAndOptions = self.treePresets.getPresetsWithOptions(exportOption, visibleInListOnly)
        if len(presetsAndOptions) > 0:
            exportedGltfs = self.sendPresetsWithOptionsToExporter(presetsAndOptions)
            qtUtils.resetProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar)
            return exportedGltfs
        
        msgBox = qtUtils.getNewMessageBox("You need at least one object to export.", title="Nothing to export!")
        msgBox.setStyleSheet("QLabel{min-width: 300px;}") #Message box width is driven by text but if it's too short, title gets cropped. Lets force a min-width so title is fully visible
        msgBox.exec_()
        return []

    def export(self, exportOption=const.EXPORT_OPTION.NONE):
        beforeExportSceneNodeSelection = RT.selection

        # We use a var defined outside to be able to retrieve it from multiple places... Yes this is ugly and should be done differently
        sharedGlobals.G_ME_cancelExport = False
        # self.updateLoggerForExport()

        #region export glTF and XML model
        exportedGltfs = []
        if self.currentTabIs(const.TAB.OBJECTS): #Objects TAB
            exportedGltfs = self.exportLODs(exportOption)
        elif self.currentTabIs(const.TAB.PRESETS): #Presets TAB
            exportedGltfs = self.exportPresets(exportOption)
        #endregion

        #region Textures
        shouldExportTextures = any(exportedGltf.exportParameters.writeTextures for exportedGltf in exportedGltfs)
        if shouldExportTextures:
            self.exportTextures(exportedGltfs)
        #endregion

        #region Texture XMLs
        if self._exportTextureLib:
            exportedGltfParameters = [exportedGltf.exportParameters for exportedGltf in exportedGltfs]
            self.exportTextureLib(exportedGltfParameters)
        #endregion

        RT.clearSelection() #in case nothing was selected, following statement will not work
        RT.select(beforeExportSceneNodeSelection)

        # self.loggerWidget.disableCancelExportBtn()
        if sharedGlobals.G_ME_cancelExport:
            qtUtils.popup("Export canceled!\n\nPlease check log to see what has already been exported.", "Canceled!")

    def setEnabledState_PresetsViewProperties(self, state):
        self.lbPresetsLineProperty.setEnabled(state)
        self.btnDuplicatePreset.setEnabled(state)
        self.btnRemovePreset.setEnabled(state)
        self.lbPresetsOptionPreset.setEnabled(state)
        self.cbOptionPreset.setEnabled(state)
        self.lbPresetsExportPath.setEnabled(state)
        self.btnEditPresetPath.setEnabled(state)
        self.btnEditGroupPath.setEnabled(state)

    def setEnabledState_ObjectViewProperties(self, state):
        self.lbLineProperty.setEnabled(state)
        self.cbAutoLODs.setEnabled(state)
        self.lbLodValue.setEnabled(state)
        self.lodValue.setEnabled(state)
        self.btnAdjustLodValue.setEnabled(state)
        self.cbObjectOptionPreset.setEnabled(state)
        self.lbObjectOptionPreset.setEnabled(state)
        self.lbExportPath.setEnabled(state)
        self.btnAddExportPath.setEnabled(state)
        self.btnRemoveExportPath.setEnabled(state)
        self.lbExportTransforms.setEnabled(state)
        self.btnExportPosition.setEnabled(state)
        self.btnExportRotation.setEnabled(state)
        self.btnExportScale.setEnabled(state)
        if not state:
            qtUtils.setButtonTristateWithColors(self.btnExportPosition, False)
            qtUtils.setButtonTristateWithColors(self.btnExportRotation, False)
            qtUtils.setButtonTristateWithColors(self.btnExportScale, False)
            self.btnExportPosition.setChecked(False)
            self.btnExportRotation.setChecked(False)
            self.btnExportScale.setChecked(False)

    def setEnabledState_CommonViewProperties(self, state):
        self.btnOpenExportFolder.setEnabled(state)

    def generateXmlFromListNames(self, exportModelNames):
        count = len(exportModelNames)
        maxProgress = count * 2 # We multiply by 2 to get 50% progress before AND after process
        if count < 1:
            return
            
        qtUtils.initProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar, maxRange=maxProgress, actionTitle="XML export")
        for exportModelName in exportModelNames:
            if sharedGlobals.G_ME_cancelExport:
                break
            self.progressBar.setValue(self.progressBar.value() + 1)
            objects = self.treeLODs._baseNameDict[exportModelName]
            metadataPath = exporter.getMetadataPath(objects[0]) #XML Path is set using the first LOD path
            if (metadataPath is None or metadataPath == ".xml"):
                MSFS2024ExportLogger.error("[XML][ERROR] {0}: No export path. Skipping XML file for {1}.".format(objects[0].name, exportModelName))
            else:
                exporter.createLODMetadata(metadataPath, objects)
            self.progressBar.setValue(self.progressBar.value() + 1)
        qtUtils.resetProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar)

    def isSameValueSelection(self, selected, objProperty):
        # returns True if all objects have the same property set, False otherwise
        if len(selected) < 1:
            return False

        value = userprop.getUserProp(selected[0], objProperty, defaultValue=False)
        for i in range(1, len(selected)):
            if userprop.getUserProp(selected[i], objProperty, defaultValue=False) != value:
                return False
        return True

    def checkBoxStateFromSelection(self, checkBox, selected, objProperty, invertState=False, disableTriState=False):
        # disableTriState if you dont need to keep track of a None value. Else, None defaults to False
        identical = self.isSameValueSelection(selected, objProperty)
        if (identical):
            checkBox.setTristate(False)
            state = userprop.getUserProp(selected[0], objProperty, defaultValue=False)
            if invertState:
                state = not state
            checkBox.setCheckState(Qt.Checked if state else Qt.Unchecked)
        elif not disableTriState:
            checkBox.setTristate(True)
            checkBox.setCheckState(Qt.PartiallyChecked)
        else:
            checkBox.setTristate(False)
            checkBox.setCheckState(Qt.Unchecked)

    def textFieldStateFromSelection(self, textField, selected, objProperty):
        identical = self.isSameValueSelection(selected, objProperty)
        if not identical:
            textField.setText("")
            return

        value = userprop.getUserProp(selected[0], objProperty)
        if(value is not None):
            textField.setText(str(value))
        else:
            textField.setText("")

    def transformButtonStateFromSelection(self, selected):
        transforms = []
        for i in range(0, len(selected)):
            transforms.append(self.getExportTransforms(selected[i]))
        identicalPos = True
        identicalRot = True
        identicalScl = True
        pos = False
        rot = False
        scl = False
        if (len(transforms) > 0):
            pos = transforms[0].position
            rot = transforms[0].rotation
            scl = transforms[0].scale
            if (len(transforms) > 1):
                for i in range(1, len(transforms)):
                    if (transforms[i].position != pos):
                        identicalPos = False
                    if (transforms[i].rotation != rot):
                        identicalRot = False
                    if (transforms[i].scale != scl):
                        identicalScl = False
                    if not identicalPos and not identicalRot and not identicalScl:
                        break
        if identicalPos:
            qtUtils.setButtonTristateWithColors(self.btnExportPosition, False)
            self.btnExportPosition.setChecked(pos)
        else:
            qtUtils.setButtonTristateWithColors(self.btnExportPosition, True)
        if identicalRot:
            qtUtils.setButtonTristateWithColors(self.btnExportRotation, False)
            self.btnExportRotation.setChecked(rot)
        else:
            qtUtils.setButtonTristateWithColors(self.btnExportRotation, True)
        if identicalScl:
            qtUtils.setButtonTristateWithColors(self.btnExportScale, False)
            self.btnExportScale.setChecked(scl)
        else:
            qtUtils.setButtonTristateWithColors(self.btnExportScale, True)

    def exportGltfTextures(self, gltfPath, textureDir):
        if not os.path.exists(gltfPath):
            return
        
        if not os.path.exists(textureDir):
            os.makedirs(textureDir)

        jsonFileObject = None
        try:
            with open(gltfPath, 'r') as file:
                jsonFileObject = json.load(file)
        except IOError:
            MSFS2024ExportLogger.error(f"[TEXTURE] File '{gltfPath}' could not be opened. File access denied")
            MSFS2024ExportLogger.error(f"[TEXTURE] Textures will not be written")
            return
        
        if jsonFileObject is None:
            return
        
        images = jsonFileObject.get("images")
        if images is None:
            return
        
        gltfDirPath = os.path.dirname(gltfPath)
        for image in images:
            imagePath = image.get("uri")
            if imagePath is None:
                continue
            imageName = os.path.basename(imagePath)
            imagePath = os.path.join(gltfDirPath, imagePath)
            if not os.path.exists(imagePath):
                continue

            newImagePath = os.path.join(textureDir, imageName)

            # Change texture path in gltf
            if len(os.path.commonprefix([newImagePath, gltfPath])) != 0:
                image['uri'] = os.path.relpath(path=newImagePath, start=gltfDirPath)
            
            # Copy image if the image not already exists in the folder
            if _samefile(imagePath, newImagePath):
                continue

            copyfile(imagePath, newImagePath)
            MSFS2024ExportLogger.info(f"[TEXTURE][{imageName}] Texture copied from '{imagePath}' to '{newImagePath}'")

        # Serializing json
        json_object = json.dumps(jsonFileObject, indent=4)

        # Write in file
        try:
            file = open(gltfPath, 'w+')
            if file:
                file.write(json_object)
            file.close()
        except IOError:
            MSFS2024ExportLogger.error(f"[TEXTURE] File '{gltfPath}' could not be written. File access denied")
            return

        return

    def exportTextures(self, exportedGltfs):
        qtUtils.initProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar, actionTitle="Textures export")
        timeStart = time.time()
        MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")
        MSFS2024ExportLogger.info(f"[TEXTURE] Export Texture(s) started  at : {str(datetime.datetime.now())}")
        self.progressBar.setMaximum(len(exportedGltfs))
        for exportedGltf in exportedGltfs:
            self.progressBar.setValue(self.progressBar.value() + 1)
            exportParameters = exportedGltf.exportParameters
            if not exportParameters.writeTextures:
                continue
            self.exportGltfTextures(exportParameters.outputPath, exportParameters.textureFolder)

        qtUtils.resetProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar)
        delta = round(time.time() - timeStart,3)
        MSFS2024ExportLogger.info(f"[TEXTURE] Operation completed in {delta}")
        MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")

        return

    def showRelevantTip(self):
        # Tips are not the sames depending of tab displayed
        #Temp check to disable tips in presets panel
        tipsActive = self.currentTabIs(const.TAB.OBJECTS)
        if tipsActive:
            tipList = self.objectsTabTips #if self.currentTabIs(const.TAB.OBJECTS) else self.presetsTabTips
            randomTipId = random.randrange(0, len(tipList))
            self.lbTip.setText(tipList[randomTipId])
            self.lbTip.setToolTip(tipList[randomTipId]) # In case reduced UI size, text is too large to be displayed
        self.lbTip.setVisible(tipsActive)
        self.lbTipTitle.setVisible(tipsActive)

    def setupObjectsTab(self):
        # Each time we switch to this tab
        selectedObjects = self.treeLODs.getSelectedSceneRootNodesList()
        self.setEnabledState_CommonViewProperties(len(selectedObjects) > 0)

        self.btnOpenExportFolder.setToolTip("Open export path of selected object")
        self.adjustLodListRelatedUI()

        self.lbQuickOptions.setVisible(True)
        self.cbAlwaysSelectInScene.setVisible(True)
        self.cbSelectInSceneSelectsChildren.setVisible(True)

        self.btnExportTicked.setToolTip("Export checked object(s)")
        self.btnExportSelected.setToolTip("Export selected object(s)")
        self.btnExportAll.setToolTip("Export all object(s) visible in list")
        self.btnExportAll.setText("Export visible in list")
        self.cbXmlExport.setVisible(True)
        self.cbGltfExport.setVisible(True)
        self.btnRefresh.setVisible(True)

        self.saveglTFConfigurationAction.setVisible(False)
        self.importglTFConfigurationAction.setVisible(False)

        if not self._exportGltf and not self._exportXml:
            self.cbGltfExport.setCheckState(Qt.Checked) #should not be useful but anyway...

    def setupPresetsTab(self):
        # Each time we switch to this tab
        selectedGroups = self.treePresets.getSelectedGroups()
        selectedPresets = self.treePresets.getSelectedPresets()
        self.setEnabledState_CommonViewProperties(len(selectedGroups) > 0 or len(selectedPresets) > 0)

        self.btnOpenExportFolder.setToolTip("Open export path of selected group or preset")

        self.lbQuickOptions.setVisible(False)
        self.cbAlwaysSelectInScene.setVisible(False)
        self.cbSelectInSceneSelectsChildren.setVisible(False)

        self.btnExportTicked.setToolTip("Export checked group(s) / preset(s)")
        self.btnExportSelected.setToolTip("Export selected group(s) / preset(s)")
        self.btnExportAll.setToolTip("Export all preset(s)")
        self.btnExportAll.setText("Export all")
        self.cbXmlExport.setVisible(False)
        self.cbGltfExport.setVisible(False)
        self.btnRefresh.setVisible(False)

        self.saveglTFConfigurationAction.setVisible(True)
        self.importglTFConfigurationAction.setVisible(True)

    def getExportTransforms(self, obj):
        exportTransform = sceneUtils.getSceneNodeBoolProp(obj, const.PROP_EXPORT_TRANSFORM, True)
        exportPosition = sceneUtils.getSceneNodeBoolProp(obj, const.PROP_EXPORT_POSITION, exportTransform)
        exportRotation = sceneUtils.getSceneNodeBoolProp(obj, const.PROP_EXPORT_ROTATION, exportTransform)
        exportScale = sceneUtils.getSceneNodeBoolProp(obj, const.PROP_EXPORT_SCALE, exportTransform)
        return ExportTransforms(exportPosition, exportRotation, exportScale)

    def cleanupExportTransformsProps(self, obj):
        sceneUtils.deleteSceneNodeUserProp(obj, const.PROP_EXPORT_TRANSFORM)
        sceneUtils.deleteSceneNodeUserProp(obj, const.PROP_EXPORT_POSITION)
        sceneUtils.deleteSceneNodeUserProp(obj, const.PROP_EXPORT_ROTATION)
        sceneUtils.deleteSceneNodeUserProp(obj, const.PROP_EXPORT_SCALE)

    def setLODExportTransforms(self, obj, exportTransforms):
        #Just fancy stuff to compact user properties and to show it's possible.
        #As a reminder, default value if not set is TRUE with const.PROP_EXPORT_TRANSFORM as main prop, and each transform as override

        self.cleanupExportTransformsProps(obj)

        propSetCount = 0
        if exportTransforms.position: propSetCount += 1
        if exportTransforms.rotation: propSetCount += 1
        if exportTransforms.scale: propSetCount += 1
        if propSetCount == 3:
            sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_TRANSFORM, True) #Even if this is the same as nothing set, we know this is now the desired behavior and wont override it
        elif propSetCount < 2:
            #Here we use const.PROP_EXPORT_TRANSFORM with override if needed
            sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_TRANSFORM, False)
            if exportTransforms.position: sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_POSITION, True)
            if exportTransforms.rotation: sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_ROTATION, True)
            if exportTransforms.scale: sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_SCALE, True)
        else:
            #Else let's display needed transforms separately
            if not exportTransforms.position: sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_POSITION, exportTransforms.position)
            if not exportTransforms.rotation: sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_ROTATION, exportTransforms.rotation)
            if not exportTransforms.scale: sceneUtils.setSceneNodeUserProp(obj, const.PROP_EXPORT_SCALE, exportTransforms.scale)

    def setLODsExportTransform(self, trs):
        lods = self.treeLODs.getSelectedSceneRootNodesList()
        for lod in lods:
            self.setLODExportTransforms(lod, trs)
        self.refreshObjectListItems()

    def autoSetupTransformExportForObjectsPanel(self, objects):
        for i in range(0, len(objects)):
            exportTransform = sceneUtils.getSceneNodeUserProp(objects[i], const.PROP_EXPORT_TRANSFORM)
            exportPosition = sceneUtils.getSceneNodeUserProp(objects[i], const.PROP_EXPORT_POSITION)
            exportRotation = sceneUtils.getSceneNodeUserProp(objects[i], const.PROP_EXPORT_ROTATION)
            exportScale = sceneUtils.getSceneNodeUserProp(objects[i], const.PROP_EXPORT_SCALE)
            if exportTransform == None and exportPosition == None and exportRotation == None and exportScale == None:
                self.setLODExportTransforms(objects[i], ExportTransforms(False, True, True)) #By default, should keep rotation and scale but NOT position for historical reasons

    def applyLODValues(self):
        selectedLods = self.treeLODs.getSelectedSceneRootNodesList()
        errorLog = ""
        for selectedLod in selectedLods:
            lodValueChoice = self.lodValue.text()
            errorLog += sceneUtils.setLODValue(selectedLod, const.PROP_LOD_VALUE, lodValueChoice)
        if errorLog != "":
            MSFS2024ExportLogger.error(errorLog)
        self.textFieldStateFromSelection(self.lodValue, selectedLods, const.PROP_LOD_VALUE)
        self.refreshObjectListItems()

    def getCurrentTab(self):
        return list(const.TAB)[self.tabWidget.currentIndex()]

    def currentTabIs(self, Tab=const.TAB.UNKNOWN):
        return self.tabWidget.currentIndex() == const.getEnumId(Tab)

    def resetPresetCFG(self):
        for configs in self.config.sections():
            self.config.remove_section(configs)

    def writeExportPresetsCFG(self, presetName="PresetConfig", _PrsObjDic=[], filepath=os.path.join(RT.pathConfig.getCurrentProjectFolder(), "MultiExporter.mep")):
        if len(_PrsObjDic) < 1:
            return

        if MAXVERSION() >= MAX2021:
            self.config[presetName] = {}
            PresetConfig = self.config[presetName]
            for Pobjs in _PrsObjDic:
                PresetConfig[Pobjs] = _PrsObjDic[Pobjs]
        else:
            if self.config.has_section(presetName):
                self.config.remove_section(presetName)
            self.config.add_section(presetName)
            for Pobjs in _PrsObjDic:
                self.config.set(presetName, Pobjs, _PrsObjDic[Pobjs])

        #UpdateFile
        if os.path.isfile(filepath):
            os.chmod(filepath, stat.S_IWRITE)

        with open(filepath, 'w') as configFile:
            self.config.write(configFile)

    def getPresetsCFG(self, filepath=os.path.join(RT.pathConfig.getCurrentProjectFolder(), "MultiExporter.mep")): #
        OutPresList = []
        for configs in self.config.sections():
            self.config.remove_section(configs)
        self.config.read(filepath)
        for sec in self.config.sections():
            OutPresetDic = {}
            for (key, val) in self.config.items(sec):
                OutPresetDic[key] = val
            OutPresList.append(OutPresetDic)

        return OutPresList

    def applyLayerSelectionToPreset(self, preset, layerNames):
        if layerNames != preset.layerNames:
            preset.edit(layerNames=layerNames)
            RT.setSaveRequired(True)

        self.btnApplyPresetLayer.setText("Apply")
        self.treeLayer.isEdited = False

    def adjustLodListRelatedUI(self):
        if self.currentTabIs(const.TAB.OBJECTS):
            listNotEmpty = len(self.treeLODs._baseNameDict) > 0
            self.btnCollapseAll.setEnabled(listNotEmpty)
            self.btnExpandAll.setEnabled(listNotEmpty)

    def refreshOptionPreset(self):
        self.cbOptionPreset.refresh()
        self.cbObjectOptionPreset.refresh()
        return

    def refreshObjectListItems(self):
        #TODO here: retain selection & checkboxes
        if not self.currentTabIs(const.TAB.OBJECTS): ## Object Tab
            return
            
        tree = self.getCurrentTree()
        if not tree.refreshQtItems():
            tree.refreshTree(progressBar=self.progressBar, lbProgressBar=self.lbProgressBar)

        ## refresh Option Presets Combo Box
        self.refreshOptionPreset()

        ## refresh filters
        self.filterSceneHierarchyList()
        self.filterPresetsList()

        self.adjustLodListRelatedUI() #Objects tab: adjust needed UI

    def getCurrentTree(self):
        if self.currentTabIs(const.TAB.OBJECTS):
            return self.treeLODs
        if self.currentTabIs(const.TAB.PRESETS):
            return self.treePresets
    
    def filterSceneHierarchyList(self):
        if not self.btnHierarchyViewFilter.isChecked(): #deactivate filters if btn not checked
            self.treeLODs.filterTree()
        else:
            filterName = self.filterObjects.text()
            onlyVisible = bool(self.cbFilterVisibleOnly.checkState() == Qt.Checked)
            onlyExportable = bool(self.cbFilterExportableOnly.checkState() == Qt.Checked)
            onlyLods = bool(self.cbFilterLodsOnly.checkState() == Qt.Checked)
            lodId = self.sbFilterLodsNumber.value()
            self.treeLODs.filterTree(filterName = filterName, onlyVisible = onlyVisible, onlyExportable = onlyExportable, onlyLods = onlyLods, lodId = lodId)
    
    def adjustSceneHierarchyFilterUI(self):
        state = self.btnHierarchyViewFilter.isChecked()
        self.cbFilterExportableOnly.setEnabled(state)
        self.cbFilterVisibleOnly.setEnabled(state)
        self.cbFilterLodsOnly.setEnabled(state)
        self.sbFilterLodsNumber.setEnabled(bool(self.cbFilterLodsOnly.checkState() == Qt.Checked and state))
        self.filterObjects.setEnabled(state)

    def filterPresetsList(self):
        if not self.btnPresetViewFilter.isChecked(): #deactivate filters if btn not checked
            self.treePresets.filterTree()
        else:
            filterName = self.filterPresets.text()
            self.treePresets.filterTree(filterName = filterName)
        
    def adjustPresetsFilterUI(self):
        state = self.btnPresetViewFilter.isChecked()
        self.filterPresets.setEnabled(state)

    def conformSceneLayersToLODView(self, prompt=True):
        if(self.getCurrentTree() != self.treeLODs):
            return
        if(prompt==True):
            if(not qtUtils.popup_Yes_No(
                title="Conform",
                text="""Conforming the scene layers to the LOD View will destroy all your layers and create a hierarchy of layers reflecting the LOD View object list. It will put all the other objects in the default layer. This is optional.\n
                Are you really sure you want to do this ?""")):
                return
        sceneUtils.conformSceneLayersToTemplate(self.treeLODs._baseNameDict)

    def sendLODsToExporter(self, objects, prompt=True):
        count = len(objects)
        if count < 1:
            return []

        exportedGltfs = []
        optionPreset = self.cbObjectOptionPreset.itemData(self.cbObjectOptionPreset.currentIndex())

        qtUtils.initProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar, actionTitle="GLTF export")
        exportedGltfs = exporter.exportObjects(objects, optionPreset, prompt=prompt, textureLib=self._exportTextureLib, progressBar=self.progressBar)
        qtUtils.resetProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar)
            
        return exportedGltfs

    def exportTextureLib(self, exportedGltfParameters):
        qtUtils.initProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar, actionTitle="TextureLib export")
        timeStart = time.time()
        try :
            MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")
            MSFS2024ExportLogger.info("[TEXTURELIB] Generating XML(s) for Texture(s) started  at : " + str(datetime.datetime.now()) + "")
            exportTextureLibWithGltf(exportedGltfParameters, progressBar=self.progressBar)
        except BaseException as e :
            qtUtils.popup_scroll(title="ERROR TextureLib", text=str(e))

        qtUtils.resetProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar)
        delta = round(time.time() - timeStart,3)
        MSFS2024ExportLogger.info("[TEXTURELIB] Operation completed in {0}".format(delta))
        MSFS2024ExportLogger.info("--------------------------------------------------------------------------------------------------------------------------------------------------------")

    def checkoutGLTF(self, gltfPath):
        pathLessExtension = os.path.splitext(gltfPath)[0]
        perforce.P4edit(pathLessExtension + ".bin")
        perforce.P4edit(pathLessExtension + ".gltf")

    def sendPresetsWithOptionsToExporter(self, presetsAndOptions):
        '''
        in : presetsAndOptions = list(tuple(PresetObject,OptionPresetObject))
        out: exportedGltfs list(Tuple:ExportGltf)
        '''
        exportParametersWithNoSceneModifications = []
        exportParametersWithSceneModifications = []
        applyPreexportToScene = True
        
        #region Prepare Presets for export
        for preset, optionPreset in presetsAndOptions:
            if sharedGlobals.G_ME_cancelExport:
                return []

            gltfFilePath = preset.path
            if not os.path.isabs(preset.path):
                gltfFilePath = utility.convertRelativePathToAbsolute(preset.path, RT.pathConfig.getCurrentProjectFolder())

            if not os.path.exists(os.path.dirname(gltfFilePath)):
                gltfFilePath = utility.convertRelativePathToAbsolute(preset.path, RT.maxFilePath)
            
            if not os.path.exists((os.path.dirname(gltfFilePath))):
                MSFS2024ExportLogger.error(f"[MultiExporter][ERROR] Preset {preset.name} : Export path {gltfFilePath} does not exists.")
                return []

            if optionPreset == None:
                MSFS2024ExportLogger.error("[MultiExporter][ERROR] There is no option preset applied to this group/preset, please select one.")
                return []

            babylonParameter = babylonPYMXS2024.BabylonParameters(gltfFilePath, "gltf")
            babylonParameter = babylonPYMXS2024.applyOptionPresetToBabylonParam(optionPreset, babylonParameter)
            babylonParameter.exportLayers = preset.layerNames

            #region Write Textures
            if babylonParameter.writeTextures:
                textureFolder = babylonParameter.textureFolder if (babylonParameter.textureFolder != "") else os.path.dirname(gltfFilePath)
                babylonParameter.textureFolder = utility.convertRelativePathToAbsolute(textureFolder, RT.pathConfig.getCurrentProjectFolder())
                if not os.path.exists(babylonParameter.textureFolder):
                    MSFS2024ExportLogger.error(f"[MultiExporter][ERROR] Texture Folder {babylonParameter.textureFolder} does not exists.")
                    return []
            #endregion

            if babylonParameter.usePreExportProcess:
                exportParametersWithSceneModifications.append(babylonParameter)
            else:
                exportParametersWithNoSceneModifications.append(babylonParameter)
            
            applyPreexportToScene = applyPreexportToScene and babylonParameter.applyPreprocessToScene
        #endregion

        if sharedGlobals.G_ME_cancelExport:
            return []

        maximum = (len(exportParametersWithSceneModifications) + len(exportParametersWithNoSceneModifications))
        qtUtils.initProgressBar(progressBar=self.progressBar, labelProgressBar=self.lbProgressBar, maxRange=maximum, actionTitle="Export progress")

        #region Save scene
        hasPreExportProcess = len(exportParametersWithSceneModifications) > 0
        if hasPreExportProcess: 
            if qtUtils.popup_Yes_No(title="Your Max File needs to be saved.",
                                    text="Your max file needs to be saved before exporting to set the pre-export process.") :
                RT.saveMaxFile(os.path.join(RT.maxFilePath, RT.maxFileName))
            else:
                qtUtils.popup(title="Export has been canceled", text="The export has been canceled.")
                return []
        #endregion

        exportedGltfs = []
        #region Export without pre-process
        for exportParameterWithNoSceneModifications in exportParametersWithNoSceneModifications: ## Do not have pre-process
            if sharedGlobals.G_ME_cancelExport:
                return exportedGltfs

            # We need to checkout files before export
            self.checkoutGLTF(exportParameterWithNoSceneModifications.outputPath)
            if babylonPYMXS2024.runBabylonExporter(exportParameterWithNoSceneModifications):
                exportedGltfs.append(
                    exporter.ExportGltf(
                        exportPath = exportParameterWithNoSceneModifications.outputPath,
                        sceneNode = None,
                        exportParameters = exportParameterWithNoSceneModifications
                    )
                )
            self.progressBar.setValue(self.progressBar.value() + 1)
        #endregion

        #region Export with pre-process
        if hasPreExportProcess:
            RT.holdMaxFile()
            success = babylonPYMXS2024.runPreExportProcess()
            if not success:
                RT.fetchMaxFile(quiet = True)
                return exportedGltfs

            for exportParameterWithSceneModifications in exportParametersWithSceneModifications:
                if sharedGlobals.G_ME_cancelExport:
                    return exportedGltfs

                # We need to checkout files before export
                self.checkoutGLTF(exportParameterWithSceneModifications.outputPath)
                if babylonPYMXS2024.runBabylonExporter(exportParameterWithSceneModifications):
                    exportedGltfs.append(
                        exporter.ExportGltf(
                            exportPath = exportParameterWithSceneModifications.outputPath,
                            sceneNode = None,
                            exportParameters = exportParameterWithSceneModifications
                        )
                )
                self.progressBar.setValue(self.progressBar.value() + 1)

            if not applyPreexportToScene:
                RT.fetchMaxFile(quiet = True)
        #endregion

        return exportedGltfs

    #endregion
    
    def endClass():
        return

#region ROOT DEBUG FUNCTION

def _printRootNodeProperties():
    rootNode = sceneUtils.getSceneRootNode()
    print(userprop.getUserPropBuffer(rootNode))

def _cleanupProp(prop):
    rootNode = sceneUtils.getSceneRootNode()
    userprop.removeUserProp(rootNode, prop)

def _cleanupRootNodeProperties():
    rootNode = sceneUtils.getSceneRootNode()
    userprop.setUserPropBuffer(rootNode, "")  # CLEANUP ROOT NODE PROPERTIES
    print("Root node user properties wiped")
#endregion

#region OPENING PROCEDURES

def writeDefaultBabylonParametersInRootNode():
    sceneRoot = sceneUtils.getSceneRootNode()
    for prop in babylonPYMXS2024.propertyToDefault.keys():
        value = userprop.getUserProp(sceneRoot, prop, babylonPYMXS2024.propertyToDefault[prop])
        userprop.setUserProp(sceneRoot, prop, value)

def checkIfContainerUnloaded():
    cont = node.get_all_containers()
    for c in cont:
        if c.unloaded == True:
            r = RT.queryBox("You have unloaded containers in your scene, you must load them all to export correctly, load them automatically ?")
            if r :
                node.load_all_containers()
            break

def initialize():
        writeDefaultBabylonParametersInRootNode()
        checkIfContainerUnloaded()
        babylonPYMXS2024.initializeBabylonExport()
#endregion

#region Window
window = None

def run():
    global window
    if(window == None):
        window = MainWindow()
        window.show()
        return

    if window.windowState() != Qt.WindowActive:
        window.showNormal()     # if minimized: put back to windowed mode
        window.activateWindow() # if hidden behind some other window: bring to front
#endregion
