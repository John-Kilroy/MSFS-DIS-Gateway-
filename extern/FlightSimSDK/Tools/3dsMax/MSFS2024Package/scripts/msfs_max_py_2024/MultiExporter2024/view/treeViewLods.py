"""Module to handle PySide2 QTreeWidget in the 3dsMax context. 
"""
from MultiExporter2024.view.treeView import *
from MultiExporter2024 import displayUtils
from MultiExporter2024.meshInspector import MeshInspectorWindow

from pymxs import runtime as rt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk_2024 import utility

from ..constants import *
from ..presetUtils import *

from maxsdk_2024 import uiTheme as uiColors
from enum import Enum

TriState = Enum('TriState', ['FALSE', 'TRUE', 'UNKNOWN'])

class LodObject():
    def __init__(self) -> None:
        self.name = ""
        self.object = None
        self.lodIndex = 0 # ID in list
        self.objNameLodID = None # ID in name
        self.widget = None
        self.isFirstInList = False
        self.isFirstLod = False # First numbered LOD with ID 0, not first in list !
        self.isFirstLodAutoLod = None # Init with None so we can use this as a check to see if property have been set already or not
        self.isLastLod = False
        self.isLastLodOverride = False
        self.isLodIgnored = False
        self.vertexCount = 0
        self.triangleCount = 0
        self.drawCount = 0
        self.numLods = 0
        self.lightDisplay = False

        # we use this to color the name according to severity: 0 is ok, 1 is warning, 2 is wont export, 3 is ignore export
        self.finalErrorState = 0
        #we use this to color the export model name (the one including all LODs) according to severity: 0 is ok, 1 is warning, 2 is wont export, 3 is ignore model
        self.exportModelErrorState = 0
        self.nameToolTip = ""

        self.exportPath = None
        self.lodMinSize = None
        self.autoLOD = None
    
    """
        setup QtWidget
        newWidget arg: when creating widget, we may perform extra steps to ensure all is set properly
    """
    def setupNew(self, sceneNode, widgetParent):
        self.object = sceneNode
        self.widget = QTreeWidgetItem(widgetParent)
        self.widget.setCheckState(0, Qt.CheckState.Unchecked) # when creating widget, its checkstate should be forced to default

    def setupExisting(self, sceneNode, widget):
        self.object = sceneNode
        self.widget = widget

    """
        getRelevantData for stats and feedback
    """
    def getRelevantData(self, lodId, numLods):
        #Get some relevant data
        self.exportPath = userprop.getUserPropString(self.object, PROP_EXPORT_PATH)
        # Fix legacy issues 
        if self.exportPath != None and not os.path.isdir(self.exportPath) :
            self.exportPath = os.path.dirname(self.exportPath) + "\\"
            userprop.setUserProp(self.object, PROP_EXPORT_PATH, self.exportPath)
        
        self.lodMinSize = userprop.getUserPropFloat(self.object, PROP_LOD_VALUE)
        self.autoLOD = userprop.getUserPropBool(self.object, PROP_AUTO_LOD)

        self.lodIndex = lodId
        self.objNameLodID = sceneUtils.getLODLevelFromSceneNodeName(self.object)
        self.isFirstInList = bool(self.lodIndex == 0)
        self.numLods = numLods
        if self.objNameLodID is None and self.numLods == 1: # if we have only 1 LOD in list, consider as LOD0 even if no prefix or suffix
            self.isFirstLod = self.isFirstInList
        else:
            self.isFirstLod = bool(self.lodIndex == 0 and self.objNameLodID == 0)
        if self.lodIndex is not None and self.numLods is not None:
            self.isLastLod = bool((self.lodIndex == self.numLods - 1))

    """
        getStats
    """
    def getStats(self):
        self.drawCount = sceneUtils.getObjectHierarchyDrawCount(self.object)
        self.vertexCount = sceneUtils.getObjectHierarchyVertexCount(self.object)
        self.triangleCount = sceneUtils.getObjectHierarchyTriangleCount(self.object)


class TreeViewLods(TreeView):
    """Class to gather scene node, sort them by LOD and put them in a QTreeWidget. Widget are connected to Scene Node using the Dictionary _rootDict
    """

    """
    MAIN TREE STUFF
    """
    def __init__(self, parent):
        TreeView.__init__(self, parent)
        self._showOnlyLodNumber = -1
        # Path elide
        self.pathDelegate = LongPathDelegate()
        self.setItemDelegateForColumn(getEnumId(OBJECTS_COLUMN.PATH), self.pathDelegate)
        
        self._baseNameDict = {}
        self._lods = set()

        self.meshInspector = None

        #self.inspectIcon = QIcon(":/Common/Zoom_16") #available sizes: ['16', '20', '24', '30', '32', '36', '48']
        #self.inspectIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionFlow/OptimizeSelectedTransitions_16") #available sizes: ['16', '20', '24', '32']
        #self.inspectIcon = QIcon(":/CommandPanel/Motion/BipedRollout/MotionFlow/ShowRandomPercentages_16") #available sizes: ['16', '20', '24', '32']
        self.inspectIcon = QIcon(":/BlendedBoxMap/BoundingBox_20") #available sizes: ['20', '24', '30', '40']


    def colorLevels(self):
        return (uiColors.colorOK, uiColors.colorWarning, uiColors.colorError)

    def createTree(self, progressBar = None, lbProgressBar=None):
        if not self.loaded:
            self.clearSelection()
            self._rootDict.clear()
            self._lods.clear()
            self.clear()
            self.createExportModelNameDictionaryFromLODs()
            qtUtils.initProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar, maxRange=len(self._baseNameDict), actionTitle="Loading Objects")
            for exportModelName in self._baseNameDict:  # build the QTree based on this dictionary
                qTreeParent = self.createRootWidget(exportModelName)

                exportModelErrorState = 0
                lastLodObject = None

                modelLods = self._baseNameDict[exportModelName]
                lodRange = range(len(modelLods))

                isFirstLodAutoLod = False
                for i in lodRange:
                    lodObject = LodObject()
                    lodObject.setupNew(sceneNode = modelLods[i], widgetParent = qTreeParent)
                    lodObject.getRelevantData(lodId = i, numLods = len(modelLods))

                    if lodObject.isFirstLod:
                        isFirstLodAutoLod = userprop.getUserPropBool(lodObject.object, PROP_AUTO_LOD)
                    
                    lodObject.isFirstLodAutoLod = isFirstLodAutoLod
                    
                    # Try to remove unused verts from map channels
                    # Try to fix isolated map verts. Useful to get proper stats in list. 
                    # Note that need to check if exported, how... Ingame, each unused vertex is removed in package builder.
                    sceneUtils.cleanupObjectHierarchy(lodObject.object)

                    exportModelErrorState = max(exportModelErrorState, self.updateSceneRootNodeWidget(lodObject=lodObject, lastLodObject=lastLodObject))
                    
                    # add each object to its corresponding widget in the dict
                    self._rootDict[lodObject.widget] = lodObject.object
                    lastLodObject = lodObject

                qTreeParent.setTextColor(0, self.colorLevels()[exportModelErrorState])
                self.addTopLevelItem(qTreeParent)
                self._lods.add(qTreeParent)
                if progressBar is not None:
                    progressBar.setValue(progressBar.value() + 1)
            qtUtils.resetProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar)
            self.expandAll()
            self.loaded = True

    def refreshTree(self, progressBar = None, lbProgressBar=None):
        self.loaded = False
        self.createTree(progressBar=progressBar, lbProgressBar=lbProgressBar)
        # roots = sceneUtils.getAllRoots()
        # qtUtils.initProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar, maxRange=len(roots), actionTitle="Loading Objects")
        # for r in roots:
        #     if (r not in self._rootDict.values()):
        #         qTreeWidget = self.createRootWidget(r)
        #         # add widget to dictionary with object as value
        #         self._rootDict[qTreeWidget] = r
        #         self.addTopLevelItem(qTreeWidget)
        #         if progressBar is not None:
        #             progressBar.setValue(progressBar.value() + 1)
        # qtUtils.resetProgressBar(progressBar=progressBar, labelProgressBar=lbProgressBar)

        # itemsToDelete = []
        # # search for object in the tool list not in the scene anymore
        # for rootItem, root in self._rootDict.items():
        #     if (root not in roots):  # if the object in the list not in the scene anymore get rid of it
        #         self.takeTopLevelItem(self.indexOfTopLevelItem(rootItem))
        #         itemsToDelete.append(rootItem)
        #     else:  # else update the path and content
        #         try:
        #             self.updateSceneRootNodeWidget(root, rootItem)
        #         except:
        #             print("cleaning up old values")
        #             self.takeTopLevelItem(self.indexOfTopLevelItem(rootItem))
        #             itemsToDelete.append(rootItem)

        # for itemToDelete in itemsToDelete:
        #     self._rootDict.pop(itemToDelete)
            
        # TODO here: make a real refresh, check per Parent modif, re-create only concerned ExportModel hierarchy
        # return something if changed somehow
        # - If an object name have been changed
    
    def refreshQtItems(self):
        # here we need to refresh list in the right order to get firstLod and lastLodObject infos
        # TODO: if only changed some properties in list, no need to completely refresh list. Retrieve existing stats as much as possible.
        for exportModelName in self._baseNameDict:
            parentWidget = None

            exportModelErrorState = 0
            lastLodObject = None

            modelLods = self._baseNameDict[exportModelName]
            lodRange = range(len(modelLods))

            isFirstLodAutoLod = False
            for i in lodRange:
                widget = self.getQtWidgetFromSceneRootNode(modelLods[i])
                # If widget is None for some reason then the list is not valid anymore.
                if widget == None:
                    return False
                else:
                    lodObject = LodObject()
                    lodObject.setupExisting(sceneNode = modelLods[i], widget = widget)
                    lodObject.getRelevantData(lodId = i, numLods = len(modelLods))

                    if parentWidget == None:
                        parentWidget = self.getParentItem(lodObject.widget)
                    
                    if lodObject.isFirstLod:
                        isFirstLodAutoLod = userprop.getUserPropBool(lodObject.object, PROP_AUTO_LOD)
                    
                    lodObject.isFirstLodAutoLod = isFirstLodAutoLod
                    
                    exportModelErrorState = max(exportModelErrorState, self.updateSceneRootNodeWidget(lodObject=lodObject, lastLodObject=lastLodObject))
                    lastLodObject = lodObject
                
            if parentWidget != None:
                parentWidget.setTextColor(0, self.colorLevels()[exportModelErrorState])
        return True

    def createRootWidget(self, name=""):
        qTreeWidget = QTreeWidgetItem()
        qTreeWidget.setCheckState(0, Qt.CheckState.Unchecked)
        qTreeWidget.setText(0, name)
        return qTreeWidget

    def updateSceneRootNodeWidget(self, lodObject=LodObject(), lastLodObject=None):
        #Init some useful values
        #lodObject.isFirstLodAutoLod should already been set here!
        maxLodID = 0
        if lodObject.numLods is not None:
            maxLodID = lodObject.numLods - 1
        
        # Last LOD override that is: last LOD in the list having a lodMinSize set of 0
        lodObject.isLastLodOverride = bool((not lodObject.isFirstLod) and lodObject.isFirstLodAutoLod and lodObject.isLastLod and (lodObject.lodIndex != None) and (lodObject.lodMinSize == 0) and lodObject.autoLOD)
        lodObject.isLodIgnored = bool((not lodObject.isFirstLod) and (not lodObject.isLastLodOverride) and lodObject.isFirstLodAutoLod)
        lodObject.lightDisplay |= lodObject.isLodIgnored # ignored LOD: we dont need to retrieve stats, just ignore it. Light display should grey out unretrieved stats by default

        # following stats columns need some data
        if not lodObject.lightDisplay:
            lodObject.getStats()

        # Column EFFICIENCY
        self.setupEfficiencyColumn(lodObject=lodObject)
        # Column DRAW_COUNT
        self.setupDrawCountColumn(lodObject=lodObject)
        # Column VERTEX_COUNT
        self.setupVertexCountColumn(lodObject=lodObject, lastLodObject=lastLodObject)
        # Column LOD_MIN_SIZE
        self.setupLODMinSizeColumn(lodObject=lodObject, lastLodObject=lastLodObject, maxLodID=maxLodID)
        # Column PATH
        self.setupPathColumn(lodObject=lodObject)
        # Column INFO
        self.setupInfoColumn(lodObject=lodObject)
        # Column NAME
        self.setupNameColumn(lodObject=lodObject, maxLodID=maxLodID)       

        return lodObject.exportModelErrorState
    
    def setupEfficiencyColumn(self, lodObject=LodObject()):
        columnIdEfficiency = getEnumId(OBJECTS_COLUMN.EFFICIENCY)

        efficiencyWidget, efficiencyLayout = displayUtils.newCellWidget(self)
        efficiencyLayout.addItem(displayUtils.newHorizontalSpacer())
        inspectButton = QPushButton("")
        #inspectButton.setIconSize(QSize(14, 14)) # magnifier icon setup
        inspectButton.setIconSize(QSize(16, 16))
        inspectButton.setIcon(self.inspectIcon)
        inspectButton.setToolTip("Inspect mesh hierarchy")
        inspectButton.setFixedSize(20, 20)
        inspectButton.pressed.connect(lambda : self._openMeshInspectorWindow(lodObject.object))
        efficiencyLayout.addWidget(inspectButton)
        efficiencyText = "N/A"
        efficiencyToolTip = ""
        efficiencyColor = uiColors.colorDullWhite
        if lodObject.lightDisplay:
            efficiencyText = "..."
        elif lodObject.vertexCount != 0 and lodObject.triangleCount != 0:
            efficiencyRatio = sceneUtils.computeMeshEfficiency(lodObject.vertexCount, lodObject.triangleCount)
            efficiencyLevel = sceneUtils.getEfficiencyLevel(efficiencyRatio)
            efficiencyText = displayUtils.percentText(efficiencyRatio)
            if lodObject.triangleCount == 1:
                efficiencyColor = uiColors.colorOK
            elif lodObject.triangleCount * 3 <= lodObject.vertexCount:
                efficiencyText = displayUtils.errorText(efficiencyText)
                efficiencyToolTip = "Check that your mesh and UVs are not exploded into separate triangles. Also check that smoothing groups are properly applied. If not already done, convert to Poly or Mesh may help"
                efficiencyColor = uiColors.colorError
            elif efficiencyLevel == 2:
                efficiencyToolTip = "Some vertices may need welding to improve model efficiency. This includes mesh vertices, normals, UVs  vertices (and channel 2 UVs), vertex colors (try to avoid color seams)"
                efficiencyColor = uiColors.colorError
            elif efficiencyLevel == 1:
                efficiencyToolTip = "Some vertices may need welding to improve model efficiency. This includes mesh vertices, normals, UVs  vertices (and channel 2 UVs), vertex colors (try to avoid color seams)"
                efficiencyColor = uiColors.colorWarning
            else:
                efficiencyColor = uiColors.colorOK
        if lodObject.widget is not None:
            lodObject.widget.setText(columnIdEfficiency, efficiencyText)
            lodObject.widget.setToolTip(columnIdEfficiency, efficiencyToolTip)
            lodObject.widget.setTextColor(columnIdEfficiency, efficiencyColor)
            # We dont draw background so default cell is visible behind. Perfect
            self.setItemWidget(lodObject.widget, columnIdEfficiency, efficiencyWidget)
        return

    def setupDrawCountColumn(self, lodObject=LodObject()):
        columnIdDrawCount = getEnumId(OBJECTS_COLUMN.DRAW_COUNT)
        drawCountText = "N/A"
        drawCountToolTip = ""
        drawCountColor = uiColors.colorDullWhite

        if lodObject.lightDisplay:
            drawCountText = "..."
        elif lodObject.vertexCount != 0:
            if sceneUtils.getMaxWrapperClass(rt.GetUsedMtlIDs) != rt.dotNetMethod:
                drawCountText = "?"
                drawCountToolTip = "Error: can't retrieve draw count!"
            else:
                drawCountText = str(lodObject.drawCount)
                drawCountToolTip = "Estimated drawcount based on number of materials applied. May be less ingame"

                drawCountColor = uiColors.colorWhite
        lodObject.widget.setText(columnIdDrawCount, drawCountText)
        lodObject.widget.setToolTip(columnIdDrawCount, drawCountToolTip)
        lodObject.widget.setTextColor(columnIdDrawCount, drawCountColor)

    def setupVertexCountColumn(self, lodObject=LodObject(), lastLodObject=None):
        columnIdVertexCount = getEnumId(OBJECTS_COLUMN.VERTEX_COUNT)

        vertexCountText = "N/A"
        vertexCountToolTip = ""
        vertexCountColor = uiColors.colorDullWhite
        if lodObject.lightDisplay:
            vertexCountText = "..."
        elif lodObject.vertexCount != 0:
            vertexCountText = str(lodObject.vertexCount)
            vertexCountColor = uiColors.colorWhite
            if lodObject.isLastLodOverride: #Checking last LOD override against hardcoded limits
                if lodObject.vertexCount >= sceneUtils.getObjectVertexCountLimit_lastLOD():
                    vertexCountColor = uiColors.colorError
                    vertexCountText = displayUtils.errorText(lodObject.vertexCount)
                    vertexCountToolTip = "Vertex count should be less than {0} for last LOD Override: LOD may disappear unexpectedly".format(sceneUtils.getObjectVertexCountLimit_lastLOD())
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = vertexCountToolTip
                    if 1 > lodObject.exportModelErrorState:
                        lodObject.exportModelErrorState = 1
                elif lodObject.vertexCount >= sceneUtils.getObjectVertexCountLimit_lastLOD() * 0.9:
                    vertexCountColor = uiColors.colorWarning
                    vertexCountToolTip = "Vertex count is close to last LOD limit ({0})".format(sceneUtils.getObjectVertexCountLimit_lastLOD())
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = vertexCountToolTip
            else:
                if lodObject.isLastLod and not (lodObject.isFirstLod and lodObject.isFirstLodAutoLod):
                    if lodObject.vertexCount >= sceneUtils.getObjectVertexCountLimit_lastLOD():
                        vertexCountColor = uiColors.colorError
                        vertexCountText = displayUtils.errorText(lodObject.vertexCount)
                        vertexCountToolTip = "Vertex count should be less than {0} for last LOD: LOD may disappear unexpectedly".format(sceneUtils.getObjectVertexCountLimit_lastLOD())
                        if 1 > lodObject.finalErrorState:
                            lodObject.finalErrorState = 1
                            lodObject.nameToolTip = vertexCountToolTip
                        if 1 > lodObject.exportModelErrorState:
                            lodObject.exportModelErrorState = 1
                    elif lodObject.vertexCount >= sceneUtils.getObjectVertexCountLimit_lastLOD() * 0.9:
                        vertexCountColor = uiColors.colorWarning
                        vertexCountToolTip = "Vertex count is close to last LOD limit ({0})".format(sceneUtils.getObjectVertexCountLimit_lastLOD())
                        if 1 > lodObject.finalErrorState:
                            lodObject.finalErrorState = 1
                            lodObject.nameToolTip = vertexCountToolTip
                elif lastLodObject != None:
                    lastObjVertexCount = lastLodObject.vertexCount
                    if lodObject.vertexCount >= lastObjVertexCount:
                        vertexCountColor = uiColors.colorWarning
                        vertexCountText = displayUtils.errorText(lodObject.vertexCount) # used error display even if not an error to emphasize despite being only a warning
                        vertexCountToolTip = "Vertex count should be less than previous LOD"
                        if 1 > lodObject.finalErrorState:
                            lodObject.finalErrorState = 1
                            lodObject.nameToolTip = vertexCountToolTip
                        if 1 > lodObject.exportModelErrorState:
                            lodObject.exportModelErrorState = 1
                    elif lodObject.vertexCount >= lastObjVertexCount * 0.9: # here we check that vertex count is at least 10% lest than previous LOD
                        vertexCountColor = uiColors.colorWarning
                        vertexCountToolTip = "Warning: Vertex count is close to previous LOD vertex count"
                        if 1 > lodObject.finalErrorState:
                            lodObject.finalErrorState = 1
                            lodObject.nameToolTip = vertexCountToolTip
        lodObject.widget.setText(columnIdVertexCount, vertexCountText)
        lodObject.widget.setToolTip(columnIdVertexCount, vertexCountToolTip)
        lodObject.widget.setTextColor(columnIdVertexCount, vertexCountColor)

    def setupLODMinSizeColumn(self, lodObject=LodObject(), lastLodObject=None, maxLodID=0):
        columnIdLodMinSize = getEnumId(OBJECTS_COLUMN.LOD_MIN_SIZE)
        lodText = ""
        lodToolTip = ""
        lodMinSizeColor = uiColors.colorError
        if lodObject.autoLOD: #First we handle if AutoLOD property is set
            if lodObject.isFirstLod or lodObject.isLastLodOverride: #First LOD set to auto will be the only one exported, unless we use the override
                lodMinSizeColor = uiColors.colorOK
            elif lodObject.isFirstInList: #We have first in list not LOD0
                lodMinSizeColor = uiColors.colorWarning
                lodToolTip = "Auto LODs requires object's name: \"[name]_LOD0\", Auto property will be ignored."
                if 1 > lodObject.finalErrorState:
                    lodObject.finalErrorState = 1
                    lodObject.nameToolTip = lodToolTip
            elif not lodObject.isFirstLodAutoLod:
                lodMinSizeColor = uiColors.colorWarning
                lodToolTip = "First LOD is not set to Auto LODs, Auto property will be ignored."
                if 1 > lodObject.finalErrorState:
                    lodObject.finalErrorState = 1
                    lodObject.nameToolTip = lodToolTip
            
            if lodObject.lodMinSize == None:
                lodText = "Auto"
            elif lodObject.isLastLodOverride:
                lodText = "Override ({0})".format(lodObject.lodMinSize)
                lodToolTip = "Last LOD auto generation override"
            elif not lodObject.isFirstLodAutoLod:
                lodText = "{0} (Auto)".format(lodObject.lodMinSize) #Here we inverse the display to reflect Auto property dismiss
            else:
                lodText = "Auto ({0})".format(lodObject.lodMinSize) #Displaying value along with Auto can be useful for last LOD override using Auto LODs
        else:
            #If this LOD doesn't have the AutoLOD property set
            if lodObject.isLastLod:
                lodMinSizeColor = uiColors.colorDullWhite
                lodText = str(lodObject.lodMinSize)
                lodText = displayUtils.ignoredText(lodObject.lodMinSize)
                lodToolTip = "Last LOD min size is ignored"
            elif lodObject.lodMinSize != None: #We have a LOD min size set
                lastObjLodMinSize = None
                lastObjAutoLOD = None
                if lastLodObject != None:
                    lastObjLodMinSize = lastLodObject.lodMinSize
                    lastObjAutoLOD = lastLodObject.autoLOD

                sizeLimit = sceneUtils.getObjectLowestSizePercent(lodObject.object, lodObject.vertexCount)
                if lodObject.lodMinSize < sizeLimit:
                    lodMinSizeColor = uiColors.colorError
                    lodText = displayUtils.errorText(lodObject.lodMinSize)
                    lodToolTip = "LOD may disappear unexpectedly: vertex count is too high for this LOD or min size is too small"
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = lodToolTip
                    if 1 > lodObject.exportModelErrorState and not lodObject.isLodIgnored:
                        lodObject.exportModelErrorState = 1
                elif lastLodObject != None and not lastObjAutoLOD and lastObjLodMinSize != None and lodObject.lodMinSize >= lastObjLodMinSize:
                    lodMinSizeColor = uiColors.colorError
                    lodText = displayUtils.errorText(lodObject.lodMinSize)
                    lodToolTip = "Min size value should be less than previous LOD"
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = lodToolTip
                    if 1 > lodObject.exportModelErrorState and not lodObject.isLodIgnored:
                        lodObject.exportModelErrorState = 1
                elif lodObject.lodMinSize < sizeLimit * (1.0 + sceneUtils.getSafeLodMargin()):
                    lodMinSizeColor = uiColors.colorWarning
                    lodText = str(lodObject.lodMinSize)
                    lodToolTip = "Warning: vertex count is a bit high for this LOD. Maybe try to reduce or increase LOD Value"
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = lodToolTip
                elif lastLodObject != None and not lastObjAutoLOD and lastObjLodMinSize != None and lodObject.lodMinSize >= lastObjLodMinSize * 0.9: # here we check that LOD Value is at least 10% lest than previous LOD
                    lodMinSizeColor = uiColors.colorWarning
                    lodText = str(lodObject.lodMinSize)
                    lodToolTip = "Warning: Min size value is close to previous LOD. Maybe try to add more separation between LODs"
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = lodToolTip
                else:
                    lodMinSizeColor = uiColors.colorOK
                    lodText = str(lodObject.lodMinSize)
            else: #We have nothing setuped for this Lod, display None...
                lodText = str(lodObject.lodMinSize)
                if maxLodID > 0: #...in red in case there are multiple LODs in the list
                    lodMinSizeColor = uiColors.colorWarning
                    lodToolTip = "Min size value should be set for this LOD, else default value will be used"
                    if 1 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 1
                        lodObject.nameToolTip = lodToolTip
                    if 1 > lodObject.exportModelErrorState:
                        lodObject.exportModelErrorState = 1
                else:
                    lodMinSizeColor = uiColors.colorOK
        if lodObject.isLodIgnored: #We may have something properly setuped, but first LOD is set to Auto, meaning each lower LOD will not be exported
            lodMinSizeColor = uiColors.colorDullWhite
            lodToolTip = "First LOD is set to Auto LODs, meaning this LOD will not be exported as it will be auto-generated\nIf you wish to override last LOD by yours, set last LOD AutoLOD property and LOD min size to 0"
            if 3 > lodObject.finalErrorState:
                lodObject.finalErrorState = 3
                lodObject.nameToolTip = lodToolTip
                lodObject.exportModelErrorState = 0
        lodObject.widget.setText(columnIdLodMinSize, lodText)
        lodObject.widget.setToolTip(columnIdLodMinSize, lodToolTip)
        lodObject.widget.setTextColor(columnIdLodMinSize, lodMinSizeColor)
        return lodObject.nameToolTip

    def setupPathColumn(self, lodObject=LodObject()):
        columnIdPath = getEnumId(OBJECTS_COLUMN.PATH)
        
        pathModelPart = lodObject.object.name + ".gltf"
        pathText = "None"
        pathToolTip = ""
        pathColor = uiColors.colorError

        if lodObject.exportPath != None:
            pathText = lodObject.exportPath
            pathToolTip = "path: {0}\nmodel: {1}".format(lodObject.exportPath, pathModelPart)
            pathColor = uiColors.colorWhite
        else:
            pathToolTip = "Add a path to export object"

        if lodObject.isLodIgnored:
            pathColor = uiColors.colorDullWhite

        lodObject.widget.setText(columnIdPath, pathText)
        lodObject.widget.setToolTip(columnIdPath, pathToolTip)
        lodObject.widget.setTextColor(columnIdPath, pathColor)

    def setupInfoColumn(self, lodObject=LodObject()):
        columnIdInfo = getEnumId(OBJECTS_COLUMN.INFO)

        infoText = ""
        infoToolTip = ""

        if lodObject.isFirstInList and lodObject.exportPath != None and lodObject.exportPath != "":
            infoText = "<- XML will use this path"
            infoToolTip = "XML file associated with gltf model files will be exported using the path set on the first object in the list"

        lodObject.widget.setText(columnIdInfo, infoText)
        lodObject.widget.setToolTip(columnIdInfo, infoToolTip)
        lodObject.widget.setTextColor(columnIdInfo, uiColors.colorDullWhite)

    def setupNameColumn(self, lodObject=LodObject(), maxLodID=0):
        columnIdName = getEnumId(OBJECTS_COLUMN.NAME)

        if lodObject.exportPath == None or lodObject.exportPath == "":
            if 2 > lodObject.finalErrorState:
                lodObject.finalErrorState = 2
                lodObject.nameToolTip = "No export path assigned: model will not be exported"
            if 2 > lodObject.exportModelErrorState and not lodObject.isLodIgnored:
                lodObject.exportModelErrorState = 2
        
        # We allow random name if only one object in the list + not Auto LODs property set
        # If Auto LODs property is set, we need _LOD0 as first LOD
        # We need only numbered AND contiguous LODs if we have multiple objects sharing the same name:
        #   Exception for last LOD override, allowing any number > 0
        #   If object without any _LOD[nb] suffix or x[nb]_ prefix in the list -> stop!
        if lodObject.isFirstLod and lodObject.autoLOD:
            if lodObject.objNameLodID == None or (lodObject.objNameLodID != None and lodObject.objNameLodID != 0) and not sceneUtils.getLodSuffixInName(lodObject.object.name):
                if 2 > lodObject.finalErrorState:
                    lodObject.finalErrorState = 2
                    lodObject.nameToolTip = "First LOD using Auto LODs property must be named with a \"_LOD0\" suffix."
                if 2 > lodObject.exportModelErrorState:
                    lodObject.exportModelErrorState = 2
        if lodObject.objNameLodID != None:
            if lodObject.isLastLodOverride and lodObject.objNameLodID <= 0:
                if 2 > lodObject.finalErrorState:
                    lodObject.finalErrorState = 2
                    lodObject.nameToolTip = "Last LOD override can't be named LOD 0."
                if 2 > lodObject.exportModelErrorState:
                    lodObject.exportModelErrorState = 2
            elif not lodObject.isLastLodOverride and lodObject.objNameLodID != lodObject.lodIndex and not lodObject.isFirstLodAutoLod: #and maxLodID > 0: #uncomment to allow single object with any name
                    if 2 > lodObject.finalErrorState:
                        lodObject.finalErrorState = 2
                        lodObject.nameToolTip = "LODs numbers should be contiguous and start at 0."
                    if 2 > lodObject.exportModelErrorState:
                        lodObject.exportModelErrorState = 2
        else:
            if maxLodID > 0:
                if 2 > lodObject.finalErrorState:
                    lodObject.finalErrorState = 2
                    lodObject.nameToolTip = "There should be only numbered LOD names in the list.\nRename object or add LOD number."
                if 2 > lodObject.exportModelErrorState:
                    lodObject.exportModelErrorState = 2
        
        if lodObject.finalErrorState == 3:
            lodObject.widget.setTextColor(columnIdName, uiColors.colorDullWhite)
            lodObject.widget.setText(columnIdName, displayUtils.ignoredText(lodObject.object.name))
        elif lodObject.finalErrorState == 2:
            lodObject.widget.setTextColor(columnIdName, uiColors.colorError)
            lodObject.widget.setText(columnIdName, displayUtils.errorText(lodObject.object.name))
        elif lodObject.finalErrorState == 1:
            lodObject.widget.setTextColor(columnIdName, uiColors.colorWarning)
            lodObject.widget.setText(columnIdName, lodObject.object.name)
        else:
            lodObject.widget.setTextColor(columnIdName, uiColors.colorOK)
            lodObject.widget.setText(columnIdName, lodObject.object.name)
        lodObject.widget.setToolTip(columnIdName, lodObject.nameToolTip)

    def filterTree(self, filterName = "", onlyVisible = False, onlyExportable = False, onlyLods = False, lodId = -1):
        # First, let's see if our filter must filter something.
        # This is done because in case our list is not up to date with our scene some lines may be kept hidden until user click on refresh,
        # in that case we may end up with messed up export: we dont want that
        filterIsActive = filterName != "" or onlyVisible != False or onlyExportable != False or onlyLods != False

        if not filterIsActive:
            self.showAllItems() #show complete list, regardless of sync with scene
        else:
            # retrieve all scene roots in list...
            roots = self._rootDict.values()
            # ...that are STILL VALID in scene
            roots = sceneUtils.filterValidSceneNodes(roots)

            # check which should be displayed
            # ordered filters from ~faster to ~slower to try to make things faster
            if onlyVisible:
                roots = sceneUtils.filterObjectsVisible(roots)
            if onlyExportable:
                roots = sceneUtils.filterObjectsWithUserProperty(roots, PROP_EXPORT_PATH) # only objects ready for export
            if filterName != "":
                roots = sceneUtils.filterObjectsByName(roots, filterName)
            if onlyLods:
                lodLevel = "[0-9]+"
                if lodId >= 0:
                    lodLevel = f"0*{lodId}"
                roots = sceneUtils.filterLODLevel(roots, lodLevel = lodLevel)
            
            # start by hiding everything
            self.hideAllItems()

            # unhide relevant scene roots in list
            for rootItem, root in self._rootDict.items():
                if root in roots:
                    rootItem.setHidden(False)

            # unhide relevant tree parents
            for lodsItem in self._lods:
                hide = self.areAllChildrenHidden(lodsItem)
                lodsItem.setHidden(hide)

    def showAllItems(self):
        for rootItem in self._rootDict.keys():
            rootItem.setHidden(False)
        for lodItem in self._lods:
            lodItem.setHidden(False)
    
    def hideAllItems(self):
        for rootItem in self._rootDict.keys():
            rootItem.setHidden(True)
        for lodItem in self._lods:
            lodItem.setHidden(True)

    def _openMeshInspectorWindow(self, obj):
        if not MeshInspectorWindow.open(obj):#, self):
            qtUtils.popup("Scene node not found!\nIf current scene was updated, you may need to refresh list.", title="Nothing to inspect")

    """
    QT TREE STUFF
    """
    def getParentItem(self, subItem):
        return subItem.parent()
    
    def getItemChildren(self, topItem):
        return self.getSubTreeItems(topItem, nbRecurse = 0)
    
    """ GET TREE """
    # nbRecurse >= 0: set recursive iteration(s), nbRecurse < 0: infinite iterations
    def getSubTreeItems(self, topItem = None, nbRecurse = -1):
        subItems = []
        if topItem == None:
            for i in range(self.topLevelItemCount()):
                topItem = self.topLevelItem(i)
                subItems.extend(self.getSubTreeItems(topItem, nbRecurse))
        else:
            for i in range(topItem.childCount()):
                subTopItem = topItem.child(i)
                subItems.append(subTopItem)
                if (nbRecurse != 0):
                    subItems.extend(self.getSubTreeItems(subTopItem, nbRecurse - 1))
        return subItems

    def getTopTreeItems(self, visibleInList = False):
        topItems = []
        for i in range(self.topLevelItemCount()):
            topItem = self.topLevelItem(i)
            if (not topItem.isHidden() if visibleInList else True):
                topItems.append(topItem)
        return topItems
    
    def getTreeItems(self):
        allItems = []
        for i in range(self.topLevelItemCount()):
            topItem = self.topLevelItem(i)
            allItems.append(topItem)
            allItems.extend(self.getSubTreeItems(topItem))
        return allItems
    
    """ GET SELECTED TREE """
    # nbRecurse >= 0: set recursive iteration(s), nbRecurse < 0: infinite iterations
    def getSelectedSubTreeItems(self, topItem = None, nbRecurse = -1):
        selectedSubItems = []
        if topItem == None:
            #get selected parents, faster to get all children then
            selectedTopItems = self.getSelectedTopTreeItems()
            for selectedTopItem in selectedTopItems:
                selectedSubItems.extend(self.getSubTreeItems(selectedTopItem, nbRecurse)) #If parent is selected, then get all subs
            #get lonely children
            subItems = self.getSubTreeItems(nbRecurse=nbRecurse)
            for subItem in subItems:
                if subItem.isSelected():
                    if not subItem.parent().isSelected(): #If parent is selected, we already added the subItem (+ this is faster than checking in another list)
                        selectedSubItems.append(subItem)
        else:
            if topItem.isSelected(): #ensure parent is not selected
                selectedSubItems.extend(self.getSubTreeItems(topItem, nbRecurse - 1)) #If parent is selected, then get all subs
        return selectedSubItems

    def getSelectedTopTreeItems(self, visibleInList = False):
        selectedTopItems = []
        for i in range(self.topLevelItemCount()):
            topItem = self.topLevelItem(i)
            if topItem.isSelected() and (not topItem.isHidden() if visibleInList else True):
                selectedTopItems.append(topItem)
        return selectedTopItems
    
    def getUnselectedTopTreeItems(self):
        unselectedTopItems = []
        for i in range(self.topLevelItemCount()):
            topItem = self.topLevelItem(i)
            if not topItem.isSelected():
                unselectedTopItems.append(topItem)
        return unselectedTopItems
    
    def getSelectedTreeItems(self):
        allSelectedItems = []
        #get selected parents, faster to get all children then
        selectedTopItems = self.getSelectedTopTreeItems()
        allSelectedItems.extend(selectedTopItems)
        for selectedTopItem in selectedTopItems:
            allSelectedItems.extend(self.getSubTreeItems(selectedTopItem)) #If parent is selected, then get all subs
        #get lonely children
        subItems = self.getSubTreeItems()
        for subItem in subItems:
            if subItem.isSelected():
                if not subItem.parent().isSelected(): #If parent is selected, we already added the subItem (+ this is faster than checking in another list)
                    allSelectedItems.append(subItem)
        return allSelectedItems

    def getSelectedGroups(self):
        selectedGroupItems = []
        #get selected parents, faster to get all children then
        selectedTopItems = self.getSelectedTopTreeItems()
        selectedGroupItems.extend(selectedTopItems)
        for selectedTopItem in selectedTopItems:
            selectedGroupItems.extend(self.getSubTreeItems(selectedTopItem)) #If parent is selected, then get all subs
        return selectedGroupItems
    
    def getSelectedLonelyChildren(self):
        selectedLonelyItems = []
        subItems = self.getSubTreeItems()
        for subItem in subItems:
            if subItem.isSelected():
                if not subItem.parent().isSelected(): #If parent is selected, we already added the subItem (+ this is faster than checking in another list)
                    selectedLonelyItems.append(subItem)
        return selectedLonelyItems

    """ GET CHECKED TREE """
    # nbRecurse >= 0: set recursive iteration(s), nbRecurse < 0: infinite iterations
    def getCheckedSubTreeItems(self, topItem = None, nbRecurse = -1):
        checkedSubItems = []
        if topItem == None:
            #get checked parents, faster to get all children then
            checkedTopItems = self.getSelectedTopTreeItems()
            for checkedTopItem in checkedTopItems:
                checkedSubItems.extend(self.getSubTreeItems(checkedTopItem, nbRecurse)) #If parent is checked, then get all subs
            #get lonely children
            subItems = self.getSubTreeItems(nbRecurse=nbRecurse)
            for subItem in subItems:
                if subItem.checkState(0) == Qt.Checked:
                    if subItem.parent().checkState(0) != Qt.Checked: #If parent is checked, we already added the subItem (+ this is faster than checking in another list)
                        checkedSubItems.append(subItem)
        else:
            if topItem.checkState(0) == Qt.Checked: #ensure parent is not checked
                checkedSubItems.extend(self.getSubTreeItems(topItem, nbRecurse - 1)) #If parent is checked, then get all subs
        return checkedSubItems

    def getCheckedTopTreeItems(self, visibleInList = False):
        checkedTopItems = []
        for i in range(self.topLevelItemCount()):
            topItem = self.topLevelItem(i)
            if topItem.checkState(0) == Qt.Checked and (not topItem.isHidden() if visibleInList else True):
                checkedTopItems.append(topItem)
        return checkedTopItems
    
    def getCheckedTreeItems(self):
        allCheckedItems = []
        #get checked parents, faster to get all children then
        checkedTopItems = self.getSelectedTopTreeItems()
        allCheckedItems.extend(checkedTopItems)
        for checkedTopItem in checkedTopItems:
            allCheckedItems.extend(self.getSubTreeItems(checkedTopItem)) #If parent is checked, then get all subs
        #get lonely children
        subItems = self.getSubTreeItems()
        for subItem in subItems:
            if subItem.checkState(0) == Qt.Checked:
                if subItem.parent().checkState(0) != Qt.Checked: #If parent is checked, we already added the subItem (+ this is faster than checking in another list)
                    allCheckedItems.append(subItem)
        return allCheckedItems

    def getCheckedLonelyChildren(self):
        checkedLonelyItems = []
        subItems = self.getSubTreeItems()
        for subItem in subItems:
            if subItem.checkState(0) == Qt.Checked:
                if not subItem.parent().checkState(0) == Qt.Checked: #If parent is checked, we already added the subItem (+ this is faster than checking in another list)
                    checkedLonelyItems.append(subItem)
        return checkedLonelyItems
    
    """
    TREE VALUES
    """
    def getTreeItemName(self, item):
        return item.text(0)
    
    def getSelectedTopTreeNames(self, visibleInList = False):
        names = []
        for item in self.getSelectedTopTreeItems(visibleInList=visibleInList):
            names.append(self.getTreeItemName(item))
        return names
    
    def getCheckedTopTreeNames(self, visibleInList = False):
        names = []
        for item in self.getCheckedTopTreeItems(visibleInList=visibleInList):
            names.append(self.getTreeItemName(item))
        return names
    
    def getTopTreeNames(self, visibleInList = False):
        if visibleInList:
            names = []
            for item in self.getTopTreeItems(visibleInList=visibleInList):
                names.append(self.getTreeItemName(item))
            return names
        else:
            return self._baseNameDict.keys() #Faster

    """
    UI
    """

    """ SELECTION BEHAVIOR """
    #If a parent is selected, then select children
    def propagateTreeSelection(self, topItem = None):
        if topItem == None:
            selectedTopItems = self.getSelectedTopTreeItems()
            for item in selectedTopItems:
                subItems = self.getSubTreeItems(item)
                for subItem in subItems:
                    subItem.setSelected(True)
        else:
            if topItem.isSelected():
                subItems = self.getSubTreeItems(topItem)
                for subItem in subItems:
                    subItem.setSelected(True)

    """ EXPORT BEHAVIOR FEEDBACK """
    def adjustTreeSelection(self, mode="include"):
        if mode == "exclude":
            #keep parent selected, but only if all children are selected
            selectedTopItems = self.getSelectedTopTreeItems()
            for item in selectedTopItems:
                subItems = self.getSubTreeItems(item)
                for subItem in subItems:
                    if not subItem.isSelected():
                        item.setSelected(False)
                        break
        else:
            #select all children if parent is selected
            selectedTopItems = self.getSelectedTopTreeItems()
            for item in selectedTopItems:
                subItems = self.getSubTreeItems(item)
                for subItem in subItems:
                    if not subItem.isSelected():
                        subItem.setSelected(True)
                        
        #if all children are selected, select parent too
        unselectedTopItems = self.getUnselectedTopTreeItems()
        for item in unselectedTopItems:
            subItems = self.getSubTreeItems(item)
            for subItem in subItems:
                if not subItem.isSelected(): break
            else:
                item.setSelected(True)
    
    # this will include/exclude lonely children, as for XML generation, we only export fully selected lists
    # note: change mode by enum please xD
    def adjustTreeSelection_NoLonelyChild(self, mode="include"):
        self.adjustTreeSelection(mode)
        selectedLonelyItems = self.getSelectedLonelyChildren()
        if mode == "exclude":
            for item in selectedLonelyItems:
                item.setSelected(False)
        else:
            toSelectTopItems = []
            for item in selectedLonelyItems:
                if item.parent() not in toSelectTopItems:
                    toSelectTopItems.append(item.parent())
            for topItem in toSelectTopItems:
                topItem.setSelected(True)
                self.propagateTreeSelection(topItem)
    
    def adjustTreeChecked_NoLonelyChild(self, mode="include"):
        checkedLonelyItems = self.getCheckedLonelyChildren()
        if mode == "exclude":
            for item in checkedLonelyItems:
                item.setCheckState(0, Qt.Unchecked)
        else:
            toCheckTopItems = []
            for item in checkedLonelyItems:
                if item.parent() not in toCheckTopItems:
                    toCheckTopItems.append(item.parent())
            for topItem in toCheckTopItems:
                topItem.setCheckState(0, Qt.Checked)
    
    """ GLOBAL CHECKBOX HELPER """
    #Init custom checkbox
    def setGlobalCheckBox(self, qGlobalCheckBox):
        self._qGlobalCheckBox = qGlobalCheckBox
        self._qGlobalCheckBox.setTristate(False)
        self._qGlobalCheckBox.stateChanged.connect(lambda: self.applyGlobalCheckBoxStateToSelected())
        self._qGlobalCheckBox.setToolTip("Apply this checkbox state to selected")

    def applyGlobalCheckBoxStateToSelected(self):
        #here we need to fix the parent checkbox issue so we need to get lonely children separately
        selectedGroupItems = self.getSelectedGroups()
        selectedLonelyItems = self.getSelectedLonelyChildren()
        #finally, let's apply checkboxes states
        for item in selectedGroupItems:
            item.setCheckState(0, self._qGlobalCheckBox.checkState())
        for item in selectedLonelyItems:
            item.setCheckState(0, self._qGlobalCheckBox.checkState())
            #Here I'm being lazy. Could optim by grouping lonely items per parent
            #and then apply fix for hierarchy only after last child state has been set. If checkbox is too slow then maybe it'd be worth it.
            self.fixTreeCheckBoxes(item)

    """
    BUGFIX BECAUSE 3DS MAX FFfFFffffFFfff
    """
    #Fix subItem's hierarchy
    def fixTreeCheckBoxes(self, subItem):
        if (subItem.parent() != None): #fix for child only: if parent state is changed it is already properly propagated to children
            parent = self.getParentItem(subItem)
            children = self.getItemChildren(parent)
            parentState = TriState.TRUE if subItem.checkState(0) else TriState.FALSE #init state with current subItem checkbox
            states = []
            for o in children:
                if o.checkState(0) != subItem.checkState(0):
                    parentState = TriState.UNKNOWN
                    #break
                states.append(o.checkState(0))
            if parentState == TriState.TRUE:
                parent.setCheckState(0, Qt.Checked)
            elif parentState == TriState.FALSE:
                parent.setCheckState(0, Qt.Unchecked)
            else:
                parent.setCheckState(0, Qt.PartiallyChecked)
                for i in range(len(children)):
                    children[i].setCheckState(0, states[i]) #Here, we fix the issue. Thank you. You're welcome.

    """
    SCENE NODES STUFF
    """
    @Slot()
    def _doubleClickedItem(self, item):
        if(item.childCount() == 0):
            rt.select(self.getSceneNodesFromTreeItem(item, getChildren=self._selectInSceneSelectsChildren))
    
    @Slot()
    def _selectionChanged(self):
        if self._alwaysSelectInScene:
            self.selectSceneNodesFromTreeItems(self.getSelectedSubTreeItems())

    def getSceneNodeFromItem(self, item):
        return self._rootDict[item]

    def getSceneNodesFromTreeItem(self, item, getChildren=True):
        selection = []
        sceneNode = self.getSceneNodeFromItem(item)
        if getChildren:
            sceneNodeChildren = sceneUtils.getDescendants(sceneNode)
            selection.extend(sceneNodeChildren)
        else:
            selection.append(sceneNode) #already done in getDescendants() so no need if getChildren
        return selection

    def selectSceneNodesFromTreeItems(self, items, getChildren=None):
        if getChildren == None:
            getChildren = self._selectInSceneSelectsChildren
        selection = []
        for item in items:
            if(item.childCount() == 0):
                selection.extend(self.getSceneNodesFromTreeItem(item, getChildren=getChildren))
        rt.select(selection)

    """
    EXPORT MODELS NAMES
    """
    def getSceneObjectName(self, obj):
        return obj.name

    def createExportModelNameDictionaryFromLODs(self):
        roots = self.gatherSceneObjects()
        self._baseNameDict.clear()
        for r in roots:  # for each base name excluding LODS
            baseName = utility.removeLODSuffix(r.name)
            if baseName not in self._baseNameDict:
                self._baseNameDict[baseName] = list()
            self._baseNameDict[baseName].append(r)

        # Here we need to sort LODs because we assume ordering is correct when displaying list (so we can check previous LOD values)
        # For now, ordering is solely based on object names, but should use LOD values instead (in case mixing x[nb]_objName with objName_LOD[nb])
        for baseName in self._baseNameDict:
            self._baseNameDict[baseName].sort(key=self.getSceneObjectName)

    def getAllExportModelNames(self):
        return self._baseNameDict.values()
    
    """
    NODES
    """

    #Note: getSelectedSceneRootNodesList is defined in TreeView class.
    #Ultimately, would be better to do a cleanup pass: need to regroup all common funcs and split specific. For now it is messy, added stuff here to avoid breaking Presets view
    def getSelectedSceneRootNodesList(self):
        selectedRoots = []
        for item in self.selectedItems():
            items = self.getQtItemsDescendants(item)
            for i in items:
                if( i in self._rootDict):
                    obj = self._rootDict[i]
                    if(obj not in selectedRoots): #*Is this really needed??
                        selectedRoots.append(obj)
        return selectedRoots

    def gatherSceneObjects(self):
        roots = sceneUtils.getAllRoots()
        return roots

    def getCheckedSceneRootNodesList(self):
        children = []
        for rootItem, root in self._rootDict.items():
            if rootItem.checkState(0) == Qt.Checked:
                children.append(root)
        return children
    
    def getSceneRootNodesList(self):
        allRoots = []
        for root in self._rootDict.values():
            if(root not in allRoots):
                allRoots.append(root)
        return allRoots
    
    def getExportSceneRootNodesList(self, exportOption = EXPORT_OPTION.ALL, exportXML = False, visibleInListOnly = False):
        #return values
        errorLog = list() #If there's any error
        bypassErrorLog = list() # If export Selected or Checked: should warn user that it bypasses the system, but still allow export
        exportObjects = list()

        # here we should have the list in the right order to get firstLod and lodID infos
        #test = self._baseNameDict.values()
        #TODO: check list vs scene
        exportModelItems = self.getTopTreeItems()
        for exportModelItem in exportModelItems:
            # Skip export if hidden when needed
            if visibleInListOnly and exportModelItem.isHidden() and exportOption == EXPORT_OPTION.ALL:
                continue

            exportModelName = self.getTreeItemName(exportModelItem)
            exportModelSubItems = self.getItemChildren(exportModelItem)
            localErrorLog = list()
            localBypassErrorLog = list()
            localExportObjects = list()
            firstLodAutoLod = False
            lodRange = range(len(exportModelSubItems))
            maxLodID = len(lodRange) - 1

            lonelyChildren = False # Lonely children can bypass some checks
            if exportOption == EXPORT_OPTION.SELECTED:
                for item in exportModelSubItems:
                    if not item.isSelected() or (item.isHidden() if visibleInListOnly else False):
                        lonelyChildren = True
                        break
            elif exportOption == EXPORT_OPTION.CHECKED:
                for item in exportModelSubItems:
                    if not item.checkState(0) == Qt.Checked or (item.isHidden() if visibleInListOnly else False):
                        lonelyChildren = True
                        break
            elif exportOption == EXPORT_OPTION.ALL and visibleInListOnly:
                for item in exportModelSubItems:
                    if item.isHidden():
                        lonelyChildren = True
                        break

            for lodID in lodRange:
                # Here we need to perform various checks.
                # If export Selected or Checked, in case it is a lonely child: should warn user that it bypasses the system, but still allow export

                obj = self._baseNameDict[exportModelName][lodID]
                if not rt.isValidNode(obj):
                    localErrorLog.append("Object {0} seems to have been deleted".format(obj.name))
                    continue
                
                isSelected = exportModelSubItems[lodID].isSelected()
                isChecked = exportModelSubItems[lodID].checkState(0) == Qt.Checked
                isVisible = not exportModelSubItems[lodID].isHidden()

                # We need some infos disregarding selected or checked state
                isFirstLod = bool(lodID == 0)
                autoLOD = userprop.getUserPropBool(obj, PROP_AUTO_LOD, False)
                if isFirstLod:
                    firstLodAutoLod = autoLOD
                
                # Process checks on required
                if (exportOption == EXPORT_OPTION.ALL and (isVisible if visibleInListOnly else True) or
                    exportOption == EXPORT_OPTION.SELECTED and isSelected and (isVisible if visibleInListOnly else True) or
                    exportOption == EXPORT_OPTION.CHECKED and isChecked and (isVisible if visibleInListOnly else True)):

                    isLastLod = bool(lodID == maxLodID)
                    lodMinSize = userprop.getUserPropFloat(obj, PROP_LOD_VALUE)
                    objNameLodID = sceneUtils.getLODLevelFromSceneNodeName(obj)
                    
                    isLastLodOverride = bool(not isFirstLod and firstLodAutoLod and isLastLod and lodMinSize != None and lodMinSize == 0) #Last LOD override that is: last LOD in the list having a lodMinSize set of 0
                    
                    if firstLodAutoLod and not isFirstLod and not isLastLodOverride: #In case autoLOD gen, just ignore export when needed
                        continue
                    
                    exportPath = userprop.getUserPropString(obj, PROP_EXPORT_PATH)

                    # Check export path
                    if(exportPath == None or exportPath == ""):
                        localErrorLog.append("No export path for {0}".format(obj.name)) #Note: XML takes the first LOD path, so maybe it would be better to force the same path for all objects... Or at least, put it somewhere.
                    else:
                        exportPath = utility.fixDeprecatedExportPath(exportPath) #automatically fix any remaining deprecated export path... Note: this should NEVER happen, but I dont trust 3dsmax anymore.

                    # We allow random name if only one object in the list + not Auto LODs property set
                    # If Auto LODs property is set, we need _LOD0 as first LOD
                    # We need only numbered AND contiguous LODs if we have multiple objects sharing the same name:
                    #   Exception for last LOD override, allowing any number > 0
                    #   If object without any _LOD[nb] suffix or x[nb]_ prefix in the list -> stop!
                    if isFirstLod and autoLOD:
                        if objNameLodID == None or (objNameLodID != None and objNameLodID != 0) or not sceneUtils.getLodSuffixInName(obj.name):
                            txt = "First LOD using Auto LODs property must be named with a \"_LOD0\" suffix."
                            if lonelyChildren:
                                if txt not in localBypassErrorLog:
                                    localBypassErrorLog.append(txt)
                            else:
                                if txt not in localErrorLog:
                                    localErrorLog.append(txt)
                    if objNameLodID != None:
                        if isLastLodOverride and objNameLodID <= 0:
                            txt = "Last LOD override can't be named LOD 0."
                            if lonelyChildren:
                                localBypassErrorLog.append(txt)
                            else:
                                localErrorLog.append(txt)
                        elif not isLastLodOverride and objNameLodID != lodID and not firstLodAutoLod: #and maxLodID > 0: #uncomment to allow single object with any name
                            txt = "LOD numbers should be contiguous and start at 0."
                            if lonelyChildren:
                                if txt not in localBypassErrorLog:
                                    localBypassErrorLog.append(txt)
                            else:
                                if txt not in localErrorLog:
                                    localErrorLog.append(txt)
                    else:
                        if maxLodID > 0:
                            txt = "Multiple LODs found, but there should be only numbered LOD names in the list."
                            if lonelyChildren and txt not in localBypassErrorLog:
                                localBypassErrorLog.append(txt)
                            elif txt not in localErrorLog:
                                localErrorLog.append(txt)
                    
                    
                    if isFirstLod:
                        localExportObjects.append(obj)
                    elif not firstLodAutoLod or isLastLodOverride:
                        localExportObjects.append(obj)

                    if lonelyChildren and exportXML:
                        txt = "XML export is selected but some LOD(s) will not be exported. Make sure all LODs are exported to match XML definition."
                        localBypassErrorLog.append(txt)

            if len(localErrorLog) > 0:
                errorText = "[EXPORT][ERROR] : {0}:\n".format(exportModelName)
                for txt in localErrorLog:
                    errorText += "\n\t"
                    errorText += txt
                    errorText += "\n"
                errorLog.append(errorText)
            else:
                if len(localBypassErrorLog) > 0:
                    errorText = "[EXPORT][WARNING] : {0}:\n".format(exportModelName)
                    for txt in localBypassErrorLog:
                        errorText += "\n\t"
                        errorText += txt
                        errorText += "\n"
                    bypassErrorLog.append(errorText)
                    
                exportObjects.extend(localExportObjects)
        
        return exportObjects, errorLog, bypassErrorLog
    
    """
    UTILITIES
    """
    def getQtWidgetFromSceneRootNode(self, sceneRootNode):
        keys = [k for k, v in self._rootDict.items() if v == sceneRootNode]
        if len(keys) > 0:
            return keys[0] #Only get 1st result, there should not be more.
        else:
            return None
    
    def getFirstLodWidgetFromSceneRootNode(self, sceneRootNode):
        nodeExportModelName = utility.removeLODSuffix(sceneRootNode.name)
        if len(self._baseNameDict[nodeExportModelName]) > 0:
            return self._baseNameDict[nodeExportModelName][0]
        else:
            return None
    
    def getLastLodWidgetFromSceneRootNode(self, sceneRootNode):
        nodeExportModelName = utility.removeLODSuffix(sceneRootNode.name)
        if len(self._baseNameDict[nodeExportModelName]) > 0:
            return self._baseNameDict[nodeExportModelName][len(self._baseNameDict[nodeExportModelName]) - 1]
        else:
            return None
