"""Display mesh hierarchy statistics"""

import pymxs
from pymxs import runtime as rt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from maxsdk_2024 import sceneUtils
from maxsdk_2024 import qtUtils
from maxsdk_2024 import uiTheme as uiColors
from maxsdk_2024 import sharedGlobals

from MultiExporter2024 import displayUtils
from MultiExporter2024.ui import meshInspector_ui as meshInspectorUI

from typing import NamedTuple

import random

class VertexInsights(NamedTuple):
    mesh: int
    #normals: int
    #materials: int
    uv0: int
    uv1: int
    vertexColor: int

class MeshStats(NamedTuple):
    sceneObject: pymxs.MXSWrapperBase
    vertexCount: int
    vertexInsights: VertexInsights
    triangleCount: int
    drawCount: int
    children: list

class MeshInspectorWindow():
    def open(sceneObject, windowParent=None):
        if sharedGlobals.G_ME_meshInspectorWindow != None:
            sharedGlobals.G_ME_meshInspectorWindow.close()
        if sceneObject != None and (rt.isValidNode(sceneObject) or sceneUtils.isRootNode(sceneObject)):
            if windowParent == None:
                windowParent = QWidget.find(rt.windows.getMAXHWND())
            sharedGlobals.G_ME_meshInspectorWindow = MeshInspector(parent=windowParent)
            sharedGlobals.G_ME_meshInspectorWindow.setWindowTitle("Mesh Inspector: "+sceneObject.name)
            sharedGlobals.G_ME_meshInspectorWindow.initInspector(sceneObject)
            sharedGlobals.G_ME_meshInspectorWindow.show()
            sharedGlobals.G_ME_meshInspectorWindow.onClosed.connect(lambda: MeshInspectorWindow.close())
            return True
        else:
            return False
        
    def close():
        sharedGlobals.G_ME_meshInspectorWindow = None

class MeshInspector(QDialog, meshInspectorUI.Ui_meshInspector):
    """
    QWidget to investigate mesh statistics
    \nSignal :
    onClosed : emits when the window is closed
    """
    onClosed = Signal()

    def __init__(self,parent=QWidget.find(rt.windows.getMAXHWND())):
        QDialog.__init__(self,parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove help button from title bar
        self.setAttribute(Qt.WA_DeleteOnClose, True) # Destroy window when closed
        self.setupUi(self)

        self.obj = None # hold reference to node we are currently inspecting
        self._widgetToSceneObjectDict = {}  # holds link between QTreeWidgetItem and 3ds max node
        self.displaySubStatsInList = True #Init sub-stats display in list
        self.displayAccurateStats = False

        ## Tips
        self.tips = (
            "Double click selects object in scene.",
            "Hover vertex count or object name to get detailed per-channel statistics."
        )

        ## Buttons icons
        # see https://help.autodesk.com/view/3DSMAX/2018/ENU/?guid=__developer_icon_guide_icon_guide_html
        # for available sizes
        self.refreshIcon = QIcon(":/Common/RotateCW_20") #available sizes: ['16', '20', '24', '30', '32', '36', '40', '48']
        self.clearDataIcon = QIcon(":/MergeAnimation/ClearSelected_16") #available sizes: ['16', '20', '24', '30', '32', '36', '48']

        self.initUI()

    def initUI(self):
        displayUtils.setLabelColor(self.lbListOptions, uiColors.colorSemiDullWhite)
        self.cbDisplaySubStatsInList.setCheckState(Qt.Checked if self._changeCheckboxDisplaySubStatsInList else Qt.Unchecked)
        self.cbDisplaySubStatsInList.stateChanged.connect(self._changeCheckboxDisplaySubStatsInList)

        ## Display tip
        displayUtils.setLabelColor(self.lbUserHintTitle, uiColors.colorDullWhite)
        displayUtils.setLabelColor(self.lbUserHint, uiColors.colorSemiDullWhite)
        randomTipId = random.randrange(0, len(self.tips))
        self.lbUserHint.setText(self.tips[randomTipId])
        self.lbUserHint.setToolTip(self.tips[randomTipId]) # In case reduced UI size, text is too large to be displayed

        ## Tree
        self.columnIdName = 0
        self.columnIdEfficiency = 1
        self.columnIdDrawCount = 2
        self.columnIdVertexCount = 3
        self.columnIdTriangleCount = 4
        self.columnCount = 5
        self.inspectorTree.setColumnWidth(self.columnIdName, 450)
        self.inspectorTree.setIndentation(self.inspectorTree.indentation() * 0.5)
        #self.inspectorTree.setSortingEnabled(True) # Disabled sorting because would need specific sorting methods (keep summary widget on top, stats/children sub widgets should not be ordered too, and finally values should be sorted using numeric sort instead of alphabetical)
        #self.inspectorTree.sortItems(self.columnIdName, Qt.SortOrder.AscendingOrder) # Also, sorted table is just a mess visually
        self.inspectorTree.setExpandsOnDoubleClick(False)
        self.inspectorTree.itemDoubleClicked.connect(self._doubleClickedItem)

        ## Refresh Button
        self.btnRefreshList.setIconSize(QSize(20, 20))
        self.btnRefreshList.setIcon(self.refreshIcon)
        self.btnRefreshList.setText(" Refresh") #add space around text, no useful padding property for that...
        self.btnRefreshList.pressed.connect(self._clickedRefreshList)

        ## Collapse/Expand buttons
        self.btnCollapseAll.pressed.connect(self._clickedCollapseAll)
        self.btnExpandAll.pressed.connect(self._clickedExpandAll)
    
    """
    Overrides
    """
    def closeEvent(self, event):
        self.onClosed.emit()
        event.accept()
    
    def reject(self) -> None: # Close button in buttonBox is binded with rejectRole
        self.close()
        #return super().reject()
    
    @Slot()
    def _doubleClickedItem(self, item):
        node = self.getWidgetNode(item)
        if node != None: # Dummy Stats and Children rows have no corresponding scene node
            rt.select(node)
    
    """
    Connects
    """
    
    def _clickedCollapseAll(self):
        self.inspectorTree.collapseAll()
    
    def _clickedExpandAll(self):
        self.inspectorTree.expandAll()

    def _clickedRefreshList(self):
        self.refreshList()
    
    def _changeCheckboxDisplaySubStatsInList(self):
        self.displaySubStatsInList = self.cbDisplaySubStatsInList.isChecked()
    
    def _clearChannelData(self, obj, channelName, button):
        hasData = False
        if channelName == "Vertex Color":
            hasData = sceneUtils.hasChannelData_VertexColor(obj)
        elif channelName == "UV0":
            hasData = sceneUtils.hasChannelData_UV0(obj)
        elif channelName == "UV1":
            hasData = sceneUtils.hasChannelData_UV1(obj)
        if hasData:
            # Ask user! About to DELETE a channel
            if qtUtils.popup_Yes_Cancel("You are about to erase data for {0} channel.\nAre you sure?".format(channelName), title="Clear channel?"):
                if channelName == "Vertex Color":
                    sceneUtils.clearChannelData_VertexColor(obj)
                elif channelName == "UV0":
                    sceneUtils.clearChannelData_UV0(obj)
                elif channelName == "UV1":
                    sceneUtils.clearChannelData_UV1(obj)
        else:
            qtUtils.popup("Channel {0} is already empty!\n\nTo see changes in list you need to refresh.".format(channelName), title="No data!")
        
        button.setDown(False) # Reset button to default state if user pressed Cancel somewhere in the process

        #self.refreshList() # Not until it is better please. Instead for now display popup if no data (see just above)
    
    """
    Methods
    """

    """ Main stuff """
    def createList(self):
        if self.obj != None and (rt.isValidNode(self.obj) or sceneUtils.isRootNode(self.obj)):
            self.createRootNodeSummaryWidget(self.obj)
            self.createRootNodeHierarchyWidget(self.obj)
    
    def refreshList(self):
        self.inspectorTree.clearSelection()
        self.inspectorTree.clear()
        self._widgetToSceneObjectDict.clear() # Clear our link dictionnary
        self.createList()

    def initInspector(self, obj):
        self.obj = obj
        self.createList()

    """ Widget to Node distionary """
    def addWidgetNodeLink(self, widget, obj):
        self._widgetToSceneObjectDict[widget] = obj # Create link in dictionary
    
    def addEmptyWidgetNodeLink(self, widget):
        self.addWidgetNodeLink(widget, None) # Fill with blank link in dictionary
    
    def getWidgetNode(self, widget):
        return self._widgetToSceneObjectDict[widget]
    
    """ Display helpers """
    def getVertexCountColor(self, vertexCount, triangleCount):
        efficiencyLevel = sceneUtils.getEfficiencyLevel(sceneUtils.computeMeshEfficiency(vertexCount, triangleCount))
        if efficiencyLevel == 2:
            return uiColors.colorError
        elif efficiencyLevel == 1:
            return uiColors.colorWarning
        return uiColors.colorOK
    
    def getVertexCountBackgroundColor(self, vertexCount, triangleCount):
        efficiencyLevel = sceneUtils.getEfficiencyLevel(sceneUtils.computeMeshEfficiency(vertexCount, triangleCount))
        if efficiencyLevel == 2:
            return uiColors.colorBackgroundError
        elif efficiencyLevel == 1:
            return uiColors.colorBackgroundWarning
        return uiColors.colorBackgroundOK
    
    """ Stats """
    def getHierarchyStats(self, obj):
        drawCount = sceneUtils.getObjectDrawCount(obj)
        
        sceneUtils.cleanupObject(obj)
        vertexCount_Max, vertexCount_Mesh, vertexCount_VertexColor, vertexCount_UV0, vertexCount_UV1 = sceneUtils.getObjectSeparateVertexCount(obj)
        vertexInsights = VertexInsights(vertexCount_Mesh, vertexCount_UV0, vertexCount_UV1, vertexCount_VertexColor)
        vertexCount = vertexCount_Mesh
        vertexCount = max(vertexCount, vertexCount_UV0)
        vertexCount = max(vertexCount, vertexCount_UV1)
        vertexCount = max(vertexCount, vertexCount_VertexColor)
        vertexCount = min(vertexCount_Max, vertexCount)

        triangleCount = sceneUtils.getObjectTriangleCount(obj)

        childrenMeshStats = list()

        objChildren = sceneUtils.getChildren(obj)
        for childObj in objChildren:
            childrenMeshStats.append(self.getHierarchyStats(childObj))

        return MeshStats(obj, vertexCount, vertexInsights, triangleCount, drawCount, childrenMeshStats)

    """ List widgets """
    def createObjectChildWidget(self, parent, name, obj=None):
        newWidget = QTreeWidgetItem()
        self.updateChildWidget(newWidget, name)
        parent.addChild(newWidget)
        self.addWidgetNodeLink(newWidget, obj) # Create link in dictionary of fill with blank link if obj=None
        return newWidget
    
    def createInsightWidget(self, parent, name, vertexCount, triangleCount, obj):
        newWidget = QTreeWidgetItem()
        parent.addChild(newWidget) # Add first for setItemWidget() to work
        self.updateInsightWidget(newWidget, name, vertexCount, triangleCount, obj)
        self.addWidgetNodeLink(newWidget, obj) # Create link in dictionary
        return newWidget

    def createHierarchyWidgets(self, hierarchyStats, parentWidget = None):
        if parentWidget == None:
            parentWidget = QTreeWidgetItem()
            self.inspectorTree.addTopLevelItem(parentWidget) #Need to add as soon as possible for setExpanded() calls to work
        parentWidget.setExpanded(True)
        self.addWidgetNodeLink(parentWidget, hierarchyStats.sceneObject) # Create link in dictionary
        self.updateSceneNodeWidget(parentWidget, hierarchyStats)
        isMesh = sceneUtils.isGeometry(hierarchyStats.sceneObject)
        if self.displaySubStatsInList and isMesh: # Lets hide substats if unecessary (not mesh)
            # create sub tree for insight stats
            widgetChildInsights = self.createObjectChildWidget(parentWidget, "Stats", obj = hierarchyStats.sceneObject)
            self.createInsightWidget(widgetChildInsights, "Mesh", hierarchyStats.vertexInsights.mesh, hierarchyStats.triangleCount, hierarchyStats.sceneObject)
            self.createInsightWidget(widgetChildInsights, "UV0", hierarchyStats.vertexInsights.uv0, hierarchyStats.triangleCount, hierarchyStats.sceneObject)
            self.createInsightWidget(widgetChildInsights, "UV1", hierarchyStats.vertexInsights.uv1, hierarchyStats.triangleCount, hierarchyStats.sceneObject)
            self.createInsightWidget(widgetChildInsights, "Vertex Color", hierarchyStats.vertexInsights.vertexColor, hierarchyStats.triangleCount, hierarchyStats.sceneObject)
            widgetChildInsights.setExpanded(False)
            # create sub tree for object's children
            if len(hierarchyStats.children) > 0:
                widgetChildObjects = self.createObjectChildWidget(parentWidget, "Children")
                widgetChildObjects.setExpanded(True)
                for childStats in hierarchyStats.children:
                    widgetChildObjects_Object = QTreeWidgetItem()
                    widgetChildObjects.addChild(widgetChildObjects_Object) #Need to add as soon as possible for setExpanded() calls to work
                    self.createHierarchyWidgets(childStats, widgetChildObjects_Object)
        else:
            for childStats in hierarchyStats.children:
                widgetChildObjects_Object = QTreeWidgetItem()
                parentWidget.addChild(widgetChildObjects_Object) #Need to add as soon as possible for setExpanded() calls to work
                self.createHierarchyWidgets(childStats, widgetChildObjects_Object)

    def createRootNodeSummaryWidget(self, obj):
        summaryWidget = QTreeWidgetItem()
        self.addWidgetNodeLink(summaryWidget, obj) # Create link in dictionary
        self.updateSceneNodeSummaryWidget(summaryWidget, obj)
        self.inspectorTree.addTopLevelItem(summaryWidget)

    def createRootNodeHierarchyWidget(self, obj):
        hierarchyStats = self.getHierarchyStats(obj)
        self.createHierarchyWidgets(hierarchyStats)

    """ Widget columns """
    def setupColumnDrawCount(self, widget, drawCount, vertexCount):
        drawCountText = "N/A"
        drawCountToolTip = ""
        drawCountColor = uiColors.colorDullWhite
        if vertexCount != 0:
            if sceneUtils.getMaxWrapperClass(rt.GetUsedMtlIDs) != rt.dotNetMethod:
                drawCountText = "?"
                drawCountToolTip = "Error: can't retrieve draw count!"
            else:
                drawCountText = str(drawCount)
                drawCountColor = uiColors.colorWhite
        widget.setText(self.columnIdDrawCount, drawCountText)
        widget.setToolTip(self.columnIdDrawCount, drawCountToolTip)
        widget.setTextColor(self.columnIdDrawCount, drawCountColor)
    
    def setupColumnTriangleCount(self, widget, triangleCount):
        triangleCountText = "N/A"
        triangleCountColor = uiColors.colorDullWhite
        if triangleCount != 0:
            triangleCountText = str(triangleCount)
            triangleCountColor = uiColors.colorWhite
        widget.setText(self.columnIdTriangleCount, triangleCountText)
        widget.setTextColor(self.columnIdTriangleCount, triangleCountColor)

    def setupColumnVertexCountSummary(self, widget, vertexCount, triangleCount):
        vertexCountText = "N/A"
        vertexCountColor = uiColors.colorDullWhite
        vertexCountToolTip = ""
        if vertexCount != 0 and triangleCount != 0:
            vertexCountText = str(vertexCount)
            vertexCountColor = self.getVertexCountColor(vertexCount, triangleCount)
            vertexCountToolTip = "See object below for precise statistics"
        widget.setText(self.columnIdVertexCount, vertexCountText)
        widget.setTextColor(self.columnIdVertexCount, vertexCountColor)
        widget.setToolTip(self.columnIdVertexCount, vertexCountToolTip)

    def missingStats(self, meshStats):
        return meshStats.vertexInsights.uv0 == None or meshStats.vertexInsights.uv1 == None or meshStats.vertexInsights.vertexColor == None

    def setupColumnVertexCount(self, widget, meshStats):
        vertexCountText = "N/A"
        vertexCountColor = uiColors.colorDullWhite
        vertexCountToolTip = ""
        if meshStats.vertexCount != 0 and meshStats.triangleCount != 0:
            vertexCountText = str(meshStats.vertexCount)
            if meshStats.triangleCount == 1:
                vertexCountColor = uiColors.colorOK
            else:
                vertexCountColor = self.getVertexCountColor(meshStats.vertexCount, meshStats.triangleCount)
            vertexCountToolTip = "Mesh:\t{0}\nUV0:\t{1}\nUV1:\t{2}\nVertex Color:\t{3}".format(meshStats.vertexInsights.mesh, meshStats.vertexInsights.uv0, meshStats.vertexInsights.uv1, meshStats.vertexInsights.vertexColor)
            if self.missingStats(meshStats):
                vertexCountText = "{0} ~ {1}".format(vertexCountText, meshStats.triangleCount * 3)
                vertexCountColor = uiColors.colorDullWhite
                vertexCountToolTip = "See object below for precise statistics"
        widget.setText(self.columnIdVertexCount, vertexCountText)
        widget.setTextColor(self.columnIdVertexCount, vertexCountColor)
        widget.setToolTip(self.columnIdVertexCount, vertexCountToolTip)
        return vertexCountToolTip
    
    def setupColumnNameSummary(self, widget, name, nodeCount, toolTip):
        widget.setText(self.columnIdName, "{0} [Total for {1} object{2}]".format(name, nodeCount, "s" if nodeCount > 1 else ""))
        widget.setToolTip(self.columnIdName, toolTip)
    
    def setupColumnName(self, widget, name, classOf, superClassOf, toolTip):
        # show a bit of insight: display what type of object we are dealing with
        objType = f"{superClassOf}"
        # for classes showing inintelligible names, lets replace with our own translation
        if (superClassOf == rt.GeometryClass):
            objType = "mesh"
        if (classOf == rt.Targetobject): # special case for Tape target: another 3dsmax aberration
            objType = "helper"

        widget.setText(self.columnIdName, "{0} ({1})".format(name, objType))
        widget.setToolTip(self.columnIdName, toolTip)

    def setupColumnEfficiencySummary(self, widget, vertexCount, triangleCount):
        backgroundColor = uiColors.colorBackgroundOK

        efficiencyText = "N/A"
        efficiencyToolTip = ""
        efficiencyColor = uiColors.colorDullWhite
        if vertexCount != 0 and triangleCount != 0:
            efficiencyRatio = sceneUtils.computeMeshEfficiency(vertexCount, triangleCount)
            efficiencyLevel = sceneUtils.getEfficiencyLevel(efficiencyRatio)
            efficiencyText = displayUtils.percentText(efficiencyRatio)

            if triangleCount == 1:
                efficiencyColor = uiColors.colorOK
            elif triangleCount * 3 <= vertexCount:
                efficiencyText = displayUtils.errorText(efficiencyText)
                #if not self.displayAccurateStats:
                #    efficiencyToolTip = "Try to get Accurate Stats. "
                efficiencyToolTip += "Check that your mesh and UVs are not exploded into separate triangles. Also check that smoothing groups are properly applied."
                efficiencyColor = uiColors.colorError
                backgroundColor = uiColors.colorBackgroundError
            elif efficiencyLevel == 2:
                efficiencyToolTip = "Some vertices may need welding to improve model efficiency. This includes mesh vertices, normals, UVs  vertices (and channel 2 UVs), vertex colors (try to avoid color seams)"
                efficiencyColor = uiColors.colorError
                backgroundColor = uiColors.colorBackgroundError
            elif efficiencyLevel == 1:
                efficiencyToolTip = "Some vertices may need welding to improve model efficiency. This includes mesh vertices, normals, UVs  vertices (and channel 2 UVs), vertex colors (try to avoid color seams)"
                efficiencyColor = uiColors.colorWarning
                backgroundColor = uiColors.colorBackgroundWarning
            else:
                efficiencyColor = uiColors.colorOK
        widget.setText(self.columnIdEfficiency, efficiencyText)
        widget.setToolTip(self.columnIdEfficiency, efficiencyToolTip)
        widget.setTextColor(self.columnIdEfficiency, efficiencyColor)
        return backgroundColor
    
    def setupColumnEfficiency(self, widget, meshStats):
        missingStats = self.missingStats(meshStats)

        efficiencyText = "N/A"
        efficiencyToolTip = ""
        efficiencyColor = uiColors.colorDullWhite
        if meshStats.vertexCount != 0 and meshStats.triangleCount != 0:
            efficiencyRatio = sceneUtils.computeMeshEfficiency(meshStats.vertexCount, meshStats.triangleCount)
            efficiencyLevel = sceneUtils.getEfficiencyLevel(efficiencyRatio)
            if missingStats:
                efficiencyText = "{0} ~ {1}".format(displayUtils.percentText(0), displayUtils.percentText(efficiencyRatio))
            else:
                efficiencyText = displayUtils.percentText(efficiencyRatio)

            if not missingStats and meshStats.triangleCount == 1:
                efficiencyColor = uiColors.colorOK
            elif missingStats or meshStats.triangleCount * 3 <= meshStats.vertexCount:
                efficiencyText = displayUtils.errorText(efficiencyText)
                #if not self.displayAccurateStats:
                #    efficiencyToolTip = "Try to get Accurate Stats. "
                efficiencyToolTip += "Check that your mesh and UVs are not exploded into separate triangles. Also check that smoothing groups are properly applied."
                efficiencyColor = uiColors.colorError
            elif efficiencyLevel == 2:
                efficiencyToolTip = "Some vertices may need welding to improve model efficiency. This includes mesh vertices, normals, UVs  vertices (and channel 2 UVs), vertex colors (try to avoid color seams)"
                efficiencyColor = uiColors.colorError
            elif efficiencyLevel == 1:
                efficiencyToolTip = "Some vertices may need welding to improve model efficiency. This includes mesh vertices, normals, UVs  vertices (and channel 2 UVs), vertex colors (try to avoid color seams)"
                efficiencyColor = uiColors.colorWarning
            else:
                efficiencyColor = uiColors.colorOK
        widget.setText(self.columnIdEfficiency, efficiencyText)
        widget.setToolTip(self.columnIdEfficiency, efficiencyToolTip)
        widget.setTextColor(self.columnIdEfficiency, efficiencyColor)
    
    """ Widget rows """
    def updateSceneNodeSummaryWidget(self, widget, obj):
        nodeCount = sceneUtils.getObjectHierarchyNodeCount(obj)
        drawCount = sceneUtils.getObjectHierarchyDrawCount(obj)
        vertexCount = sceneUtils.getObjectHierarchyVertexCount(obj)
        triangleCount = sceneUtils.getObjectHierarchyTriangleCount(obj)

        # Exclude max root from node count
        if sceneUtils.isRootNode(obj):
            nodeCount -= 1

        # Column Draw count
        self.setupColumnDrawCount(widget, drawCount, vertexCount)
        # Column Triangle count
        self.setupColumnTriangleCount(widget, triangleCount)
        # Column Vertex count
        vertexCountToolTip = self.setupColumnVertexCountSummary(widget, vertexCount, triangleCount)
        # Column Name
        self.setupColumnNameSummary(widget, obj.name, nodeCount, vertexCountToolTip)
        # Column Efficiency
        backgroundColor = self.setupColumnEfficiencySummary(widget, vertexCount, triangleCount)

        self.setRowBackgroundColor(widget, backgroundColor)

    def updateSceneNodeWidget(self, widget, meshStats):
        # Column Draw count
        self.setupColumnDrawCount(widget, meshStats.drawCount, meshStats.vertexCount)
        # Column Triangle count
        self.setupColumnTriangleCount(widget, meshStats.triangleCount)
        # Column Vertex count
        vertexCountToolTip = self.setupColumnVertexCount(widget, meshStats)
        # Column Name
        self.setupColumnName(widget, meshStats.sceneObject.name, rt.classOf(meshStats.sceneObject), rt.superClassOf(meshStats.sceneObject), vertexCountToolTip)
        # Column Efficiency
        self.setupColumnEfficiency(widget, meshStats)

    def setRowBackgroundColor(self, widget, color):
        for columnId in range(self.columnCount):
            widget.setBackgroundColor(columnId, color)

    def updateChildWidget(self, widget, name):
        widget.setText(self.columnIdName, name)
        widget.setTextColor(self.columnIdName, uiColors.colorDullWhite)
        self.setRowBackgroundColor(widget, uiColors.colorBackgroundLightGrey)
    
    def updateInsightWidget(self, widget, name, vertexCount, triangleCount, obj):
        backgroundColor = uiColors.colorBackgroundLightGrey

        widget.setText(self.columnIdName, name)
        widget.setTextColor(self.columnIdName, uiColors.colorSemiDullWhite)

        objIsGeometry = sceneUtils.isGeometry(obj) # We check to see if proper stats have been retrieved. Else we just display "N/A" in the stats
        vertexCountText = "N/A"
        vertexCountColor = uiColors.colorDullWhite
        if objIsGeometry:
            vertexCountText = str(vertexCount)
            vertexCountColor = uiColors.colorSemiDullWhite
            if vertexCount > 0 and triangleCount != 0:
                if triangleCount == 1:
                    backgroundColor = uiColors.colorBackgroundOK
                else:
                    backgroundColor = self.getVertexCountBackgroundColor(vertexCount, triangleCount)
        widget.setText(self.columnIdVertexCount, vertexCountText)
        widget.setTextColor(self.columnIdVertexCount, vertexCountColor)
        self.setRowBackgroundColor(widget, backgroundColor)

        if name != "Mesh" and objIsGeometry and vertexCount > 0:
            clearChannelWidget, clearChannelLayout = displayUtils.newCellWidget(self.inspectorTree)
            clearChannelLayout.addItem(displayUtils.newHorizontalSpacer())
            #clearChannelButton = QPushButton("X")
            clearChannelButton = QToolButton()
            clearChannelButton.setIconSize(QSize(20, 20))
            clearChannelButton.setIcon(self.clearDataIcon)
            clearChannelButton.setToolTip("Clear channel data")
            clearChannelButton.setFixedSize(20, 20)
            clearChannelButton.pressed.connect(lambda : self._clearChannelData(obj, name, clearChannelButton))
            clearChannelLayout.addWidget(clearChannelButton)
            self.inspectorTree.setItemWidget(widget, self.columnIdVertexCount, clearChannelWidget) # We dont draw background so default cell is visible behind. Perfect
