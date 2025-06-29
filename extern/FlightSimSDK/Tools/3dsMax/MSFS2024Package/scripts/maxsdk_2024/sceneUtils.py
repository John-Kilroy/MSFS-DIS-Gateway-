"""Module to interact with a 3dsMax scene.
"""

import math
import re

import pymxs
from pymxs import runtime as rt

import maxsdk_2024.layer as layer
import maxsdk_2024.qtUtils as qtUtils


def getAllObjects():
    """Returns all the objects in the scene
    """
    return rt.objects


def getSelectedObjects():
    """Returns all the selected object in the scene
    """
    return rt.getCurrentSelection()


def getSceneRootNode():
    """Returns the unique Root Node of the scene, this is where we can store scene wide user properties. 
    """
    rootScene = rt.rootScene
    worldSubAnim = rootScene[rt.Name('world')]
    return worldSubAnim.object


def getAllRoots(objects=(getAllObjects())):
    """Returns each root of a collection of object
    """
    allRoots = []
    for o in objects:
        root = getRoot(o)
        if(root not in allRoots):
            allRoots.append(root)
    return allRoots
# returns the root of the object hierarchy.


def getRoot(obj):
    """Recursive function to get the root of an object
    """
    if(obj.parent == rt.undefined):
        return obj
    else:
        return getRoot(obj.parent)


def getChildren(obj):
    """Returns all direct children of an object
    """
    return obj.children

def getDescendants(obj):
    """Returns all the descending hierarchy. Call getRoot() before to get the full hierarchy
    """
    hierarchy = []
    hierarchy.append(obj)
    for m in obj.children:
        hierarchy += getDescendants(m)

    return hierarchy

def getChildrenCount(obj, recursive=True):
    """Returns the number of children (recursive to False to get only direct children)
    Add 1 to get full hierarchy number
    """
    childrenCount = 0
    for child in obj.children:
        childrenCount += 1
        if recursive:
            childrenCount += getChildrenCount(child)
    return childrenCount

def getDescendantsOfMultiple(objects):
    """Returns all the descending hierarchies of a collection of objects.
    """
    objType = type(objects)
    if objType != pymxs.MXSWrapperObjectSet and objType != list:
        return getDescendants(objects)
        
    hierarchies = []
    for o in objects:
        hierarchies += getDescendants(o)

    result = []
    for h in hierarchies:
        if h not in result:
            result.append(h)
    return result

def getSceneNodeUserProp(obj, key):
    if rt.isValidNode(obj) or isRootNode(obj):
        return rt.getUserProp(obj, key)
    return None

def getSceneNodeUserPropBuffer(obj):
    if rt.isValidNode(obj) or isRootNode(obj):
        return rt.getUserPropBuffer(obj)
    return None

def setSceneNodeUserPropBuffer(obj, buffer):
    if rt.isValideNode(obj) or isRootNode(obj):
        rt.setUserPropBuffer(obj, buffer)

def setSceneNodeUserProp(obj, key, value):
    if rt.isValidNode(obj) or isRootNode(obj):
        rt.setUserProp(obj, key, value)

def deleteSceneNodeUserProp(obj, key):
    if rt.isValidNode(obj) or isRootNode(obj):
        rt.deleteUserProp(obj, key)

def getLodSuffixInName(name):
    return re.match(".+_LOD[0-9]+$", name)

def getLodPrefixInName(name):
    return re.match("x[0-9]+_", name)

def getLODLevelFromSceneNodeName(obj):
    """Returns the LOD level of an object as an int, 
    returns None if the object is not a LOD
    """
    w = getLodSuffixInName(obj.name)
    if(w):
        d = re.findall("[0-9]+$", w.string)
        return int(d[0])
    else:
        w = getLodPrefixInName(obj.name)
        if (w):
            d = re.findall("[0-9]+", w.group(0))
            return int(d[0])
        else:
            return None

def getAutoLOD(obj, key="flightsim_lod_autogen"):
    """Returns the value of the auto lod generation property
    """
    try:
        return bool(getSceneNodeUserProp(obj, key))
    except:
        return False

def getSceneNodeBoolProp(obj, key, default=False):
    """Sanitize object property to bool
    """
    value = getSceneNodeUserProp(obj, key)
    if value != None:
        try:
            return bool(value)
        except:
            return default
    return default

def getLODValue(obj, key):
    """Returns the value of the LOD ( minSize ), returns None if the user property is not set
    """
    lodProp = getSceneNodeUserProp(obj, key)
    if lodProp != None:
        try:
            return float(lodProp)
        except:
            pass
    return None

def setLODValue(obj, key, lodValue):
    """Set the lod Value of an object.

    \nin:
          obj= pymxs.MXSWrapperBase
          lodValue= int
    """
    log = ""
    if (lodValue == ""):
        rt.deleteUserProp(obj, key)
    else:
        validValue = qtUtils.validateFloatLineEdit(lodValue)
        if validValue is not None:
            setSceneNodeUserProp(obj, key, validValue)
        else:
            log += ("Lod value \"" + lodValue + "\" is not valid.\n")

    return log

defaultLODValues = [70.0, 40.0, 20.0, 10.0] 


def getDefaultLODValue(lodLevel):
    """Given a LOD level as an int, returns the default LOD Value that the object should probably use
    
    \nin:
        lodLevel= int
    
    \out:
        lodValue= float
    """
    defaultCount = len(defaultLODValues)
    if(lodLevel >= defaultCount):
        return defaultLODValues[defaultCount-1]
    if(lodLevel < 0):
        return defaultLODValues[0]
    return defaultLODValues[lodLevel]

def getSharedOptimizeValue(objects):
    """Check every object in the list for the babylon optimize vertice user property we only optimize if all of them do 
    """
    firstState = None
    for obj in objects:
        state = getSceneNodeUserProp(obj, "babylonjs_optimizevertices")
        if state is None:
            state = True
        if firstState is None:
            firstState = state
        if firstState != state:
            return False
    return firstState

def collapseAllAndExpandSelected():
    """Collapse all the Scene Explorer items and expand the selected ones.
    """
    explorer = rt.SceneExplorerManager.GetActiveExplorer()
    if explorer is not None:
        explorer.CollapseAll()
        explorer.ExpandSelected()
        rt.macros.run("Scene Explorer", "SEFindSelected")
        # we run it twice to make sure it focuses on the hierarchy correctly
        rt.macros.run("Scene Explorer", "SEFindSelected")


def sortObjectsByLODLevels(objects):
    """Returns a sorted version of the array in the order LOD0 to LODn
    """
    newList = sorted(objects, key=lambda x: getLODLevelFromSceneNodeName(x), reverse=False)
    return newList


def selectLayers(layers):
    """Select nodes in the layers
    """
    obj = []
    for lay in layers:
        if(rt.classof(lay) == rt.MixinInterface):
            obj += layer.getNodesInLayer(lay)
    rt.select(obj)

######################
####### Gizmo ########
######################
gizmoClasses = [
    "BoxGizmo",
    "SphereGizmo",
    "CylGizmo",
    "LodSphere",
    "MSFS2024SphereFade",
    "CylinderCollider",
    "SphereCollider",
    "BoxCollider",
    "MSFS2024CylinderGizmo",
    "MSFS2024BoxGizmo",
    "MSFS2024SphereGizmo",
    "MSFS2024SphereBoundingVolumeGizmo"
]


def getGizmosInDescendants(roots):
    """Returns all the legal gizmos in the hierachies of all the given roots.

    Legal gizmos are declared by class name in the gizmoClasses list
    """
    gizmos = []
    for o in getDescendantsOfMultiple(roots):
        if (str(rt.classOf(o)) in gizmoClasses):
            gizmos.append(o)
    return gizmos


def convertToBoxCollider(gizmo):
    """Convert a box gizmo to a MSFS2024BoxGizmo
    """
    newGizmo = rt.MSFS2024BoxGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.boxGizmo.width = gizmo.width
    newGizmo.boxGizmo.height = gizmo.height
    newGizmo.boxGizmo.length = gizmo.length
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo


def convertToSphereCollider(gizmo):
    """Convert a sphere gizmo to a MSFS2024SphereGizmo
    """
    newGizmo = rt.MSFS2024SphereGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.sphereGizmo.radius = gizmo.radius
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo

def convertToSphereBoundingVolume(gizmo):
    """Convert a sphere gizmo to a AsoboSphereBoundingVolumeGizmo
    """
    newGizmo = rt.MSFS2024SphereBoundingVolumeGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.sphereGizmo.radius = gizmo.radius
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo


def convertToCylinderCollider(gizmo):
    """Convert a cylinder gizmo to a MSFS2024CylinderGizmo
    """
    newGizmo = rt.MSFS2024CylinderGizmo()
    newGizmo.parent = gizmo.parent
    newGizmo.transform = gizmo.transform
    newGizmo.cylGizmo.radius = gizmo.radius
    newGizmo.cylGizmo.height = gizmo.height
    newGizmo.name = gizmo.name
    gizmo.layer.addnode(newGizmo)
    rt.delete(gizmo)
    return newGizmo


def cleanupBoxCollider(gizmo):
    """Remove negative sizes of a box gizmo
    """
    g = gizmo.boxGizmo
    if(g.width <= 0):
        g.width *= -1
    if(g.length <= 0):
        g.length *= -1
    if(g.height <= 0):
        g.height *= -1
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(gizmo, (rt.EulerAngles(180, 0, 0)))


def cleanupCylinderCollider(gizmo):
    """Remove negative sizes of a Cylinder Gizmos
    """
    g = gizmo.cylGizmo
    if g.radius <= 0:
        g.radius *= -1
    if g.height <= 0:
        g.height *= -1
        rt.toolMode.coordsys(rt.Name("local"))
        rt.rotate(gizmo, (rt.EulerAngles(180, 0, 0)))


def cleanupSphereCollider(gizmo):
    """Make sure the radius of a sphere gizmo is positive
    """
    if gizmo.sphereGizmo.radius <= 0:
        gizmo.sphereGizmo.radius *= -1


# create conversion table by binding the convert function to a dict key
gizmoConversion = {
    "BoxGizmo": convertToBoxCollider,
    "SphereGizmo": convertToSphereCollider,
    "CylGizmo": convertToCylinderCollider
}
gizmoCleanup = {
    "MSFS2024BoxGizmo": cleanupBoxCollider,
    "MSFS2024SphereGizmo": cleanupSphereCollider,
    "MSFS2024SphereBoundingVolumeGizmo": cleanupSphereCollider,
    "MSFS2024CylinderGizmo": cleanupCylinderCollider
}
# finds cleanup function and runs it.


def cleanupGizmosValues(gizmos):
    """Wrapper to cleanup a group of gizmos based on the gizmoCleanup dictionary defined in sceneUtils
    """
    for g in gizmos:
        gClass = str(rt.classOf(g))
        if(gClass in gizmoCleanup.keys()):
            gizmoCleanup[str(rt.classOf(g))](g)
# finds conversion function and runs it.
# Returns new gizmo array


def convertGizmosToAsoboGizmos(gizmos):
    """Wrapper to convert a group of gizmos to their Asobo equivalent based on the gizmoConversion dictionary defined in sceneUtils
    returns a list with the new gizmos converted or not.
    """
    newGizmos = []
    for g in gizmos:
        gRoot = getRoot(g)
        gClass = str(rt.classOf(g))
        if gRoot is g:
            raise Exception('\nERROR : {0} used as top parent'.format(gClass))
        if(gClass in gizmoConversion.keys()):
            g = gizmoConversion[str(rt.classOf(g))](g)
        newGizmos.append(g)
    return newGizmos

######################
####### Filter #######
######################


def filterValidSceneNodes(objects):
    return [o for o in objects if rt.IsValidNode(o)]

def filterLODLevel(objects, lodLevel="[0-9]+"):
    """Only returns objects of the given lodLevel, lodLevel can either be an integer or a regular expression
    """
    newObjects = []
    for o in objects:
        if(re.match(".+_LOD" + str(lodLevel) + "$", o.name)):
            newObjects.append(o)    
        elif (re.match("x" + str(lodLevel) + "_", o.name)):
            newObjects.append(o)
    return newObjects

def filterObjectsWithUserProperty(objects, property):
    """Only returns object USING the property
    """
    newObjects = [o for o in objects if getSceneNodeUserProp(o, property) != None]
    return newObjects

def filterObjectsWithoutUserProperty(objects, property):
    """Only returns object NOT USING the property
    """
    newObjects = [o for o in objects if getSceneNodeUserProp(o, property) == None]
    return newObjects

def filterObjectsVisible(objects):
    """Only returns visible objects
    """
    return [o for o in objects if o.isHidden == False]

def filterObjectsByName(objects, matchingString):
    """Only returns object with matching string in name (case insensitive)
    """
    return [o for o in objects if (str.lower(matchingString) in str.lower(o.name))]

# filters out gizmos
def filterOutGizmos(objects):
    """Only returns non gizmo object
    """
    gizmos = []
    for o in objects:
        if str(rt.classOf(o)) not in gizmoClasses:
            gizmos.append(o)
    return gizmos
# only returns gizmos


def filterGizmos(objects):
    """Only returns the gizmos
    """
    gizmos = []
    for o in objects:
        if str(rt.classOf(o)) in gizmoClasses:
            gizmos.append(o)
    return gizmos
# create a flattened copy of the hierarchy
# Keep the gizmos
# returns root of the newly flattened hierarchy


def conformSceneLayersToTemplate(template):
    """Conform your scene layers and their children nodes to a template dictionary. 
    Keys : baseName 
    Values : list of root node
    A parent layer is created for each baseName
    A child layer is created for each rootNode in the corresponding baseName layer
    The hierarchy of the rootNode is then stored in its layer

    \nin:
    template = dict(key=str, value=list(node))
    """
    layerManager = rt.layerManager
    defaultLayer = layerManager.getLayer(0)
    allObjects = getAllObjects()
    for x in allObjects:
        defaultLayer.addNode(x)
    for baseName in template.keys():
        currentCategory = layerManager.getLayerFromName(baseName)
        if(currentCategory is None):
            currentCategory = layerManager.newLayerFromName(baseName)
        for o in template[baseName]:
            currentLayer = layerManager.getLayerFromName(o.name)
            if(currentLayer is None):
                currentLayer = layerManager.newLayerFromName(o.name)
            hierarchy = getDescendants(o)
            for oo in hierarchy:
                currentLayer.addNode(oo)
            currentLayer.setParent(currentCategory)
    layer.deleteAllEmptyLayerHierarchies()

def flattenMesh(rootNode):
    """Returns a flattened version of the descendants of the given object, keeping gizmos intact
    """
    hierarchy = getDescendants(rootNode)
    objsToFlatten = []
    toKeep = []
    for node in hierarchy:
        cls = rt.classOf(node)
        if cls == rt.Editable_Poly or cls == rt.Editable_Mesh or cls == rt.PolyMeshObject:
            objsToFlatten.append(node)
        else:
            toKeep.append(node)
    flattened = rt.createMesh(
        objsToFlatten, name=rootNode.name, transform=rootNode.transform)
    for node in toKeep:
        snapNode = rt.snapshot(node)
        snapNode.parent = flattened
        snapNode.name = node.name
    flattened.name = rootNode.name
    del objsToFlatten
    del toKeep
    return flattened
# recursive function to copy the hierarchy
# create a copy of a hierarchy and returns the root


def copyHierarchy(rootNode):
    """Recursive function that copy a hierarchy and returns you a reference to the root of the copy
    """
    current = rt.snapshot(rootNode)
    current.name = rootNode.name
    children = getChildren(rootNode)
    for child in children:
        copyChild = copyHierarchy(child)
        copyChild.parent = current
    return current


"""
LOD AND STATS MAX STUFF
"""
def getMaxWrapperSuperClass(maxWrapper):
    return rt.superClassOf(maxWrapper)

def getMaxWrapperClass(maxWrapper):
    return rt.classOf(maxWrapper)

def isMesh(obj):
    return not isRootNode(obj) and getMaxWrapperClass(obj.baseObject) == rt.Editable_mesh and getMaxWrapperClass(obj) == rt.Editable_mesh

def isPoly(obj):
    return not isRootNode(obj) and getMaxWrapperClass(obj) == rt.Editable_Poly

def isGeometry(obj):
    return not isRootNode(obj) and getMaxWrapperSuperClass(obj) == rt.GeometryClass and getMaxWrapperClass(obj) != rt.Targetobject # Seriously 3dsmax fffFffff

def isRootNode(obj):
    return getMaxWrapperClass(obj) == rt.MAXRootNode

def isMultiMaterial(mat):
    return getMaxWrapperClass(mat) == rt.Multimaterial

def getObjectTriangleCount(obj):
    if isGeometry(obj):
        return rt.GetTriMeshFaceCount(obj)[0]
    return 0

def getObjectMaxVertexCount(obj):
    if isGeometry(obj):
        return getObjectTriangleCount(obj) * 3
    return 0

def getObjectVertexCount_Mesh(obj):
    if isGeometry(obj):
        return rt.GetTriMeshFaceCount(obj)[1]
    return 0

""" Differentiate poly from mesh """
# Mesh
def getMeshVertexCount_Map(obj, mapID):
    if rt.meshop.getMapSupport(obj, mapID):
        return rt.meshop.getNumMapVerts(obj, mapID)
    else:
        return 0

def getMeshVertexCount_VertexColor(obj):
    vertexColor = getMeshVertexCount_Map(obj, 0) # Vertex Color mapID == 0
    vertexAlpha = getMeshVertexCount_Map(obj, -2) # Vertex Alpha mapID == -2: 3dsmax uses a separate channel for this
    return max(vertexColor, vertexAlpha) # Just take worst case scenario, but would require crossmatch to get real count!

def getMeshVertexCount_UV0(obj):
    return getMeshVertexCount_Map(obj, 1) # UV0 mapID == 1

def getMeshVertexCount_UV1(obj):
    return getMeshVertexCount_Map(obj, 2) # UV1 mapID == 2

# Poly
def getPolyVertexCount_Map(obj, mapID):
    if rt.polyop.getMapSupport(obj, mapID):
        return rt.polyop.getNumMapVerts(obj, mapID)
    else:
        return 0

def getPolyVertexCount_VertexColor(obj):
    vertexColor = getPolyVertexCount_Map(obj, 0) # Vertex Color mapID == 0
    vertexAlpha = getPolyVertexCount_Map(obj, -2) # Vertex Alpha mapID == -2: 3dsmax uses a separate channel for this
    return max(vertexColor, vertexAlpha) # Just take worst case scenario, but would require crossmatch to get real count!

def getPolyVertexCount_UV0(obj):
    return getPolyVertexCount_Map(obj, 1) # UV0 mapID == 1

def getPolyVertexCount_UV1(obj):
    return getPolyVertexCount_Map(obj, 2) # UV1 mapID == 2

"""" All cases covered here """
def getObjectUsedMultiMaterialIDs(obj):
    #Note : since 3dsmax 2023 there's a meshop.getFacesByMatId that would have been useful here...
    materialsCount = obj.material.count
    usedMaterialsCount = materialsCount # fallback to worst case. Completely unrealistic...
    if getMaxWrapperClass(rt.GetUsedMtlIDs) == rt.dotNetMethod:
        usedMaterialsCount = len(rt.GetUsedMtlIDs(obj.inode.handle))
    # Disabled true fallback, as it takes WAAAY too much time
    #else:
    #    mesh = obj.mesh
    #    materialIDs = [0 for i in range(materialsCount)]
    #    for faceID in range(0, rt.meshop.getNumFaces(mesh)):
    #        materialID = rt.getFaceMatID(mesh, faceID)
    #        if materialID > materialsCount:
    #            materialIDs[0] += 1 # Use 0 to store invalid matIDs
    #        else:
    #            materialIDs[materialID] += 1
    #    usedMaterialsCount = 0
    #    for materialID in range(0, materialsCount):
    #        usedMaterialsCount += int(materialIDs[materialID] != 0)
    return usedMaterialsCount

def getObjectDrawCount(obj):
    if isGeometry(obj):
        if obj.material != None and isMultiMaterial(obj.material):
            return getObjectUsedMultiMaterialIDs(obj)
        else:
            return 1
    return 0

def getObjectTotalVertexCount(obj):
    # This is an estimation
    # Would require to crossmatch all datas to get real vertex count
    # Would also require material IDs and Normals too but this should be good enough

    # Note that for example when creating a simple plane, the number of map verts is off... 3dsmax ffFFffFfff...
    # In such cases, get object mesh.
    # Finally just get the worst case scenario but not more than what's possible!

    vertMax = 0
    vertMesh = 0
    vertVC = 0
    vertUV0 = 0
    vertUV1 = 0
    if isGeometry(obj):
        vertMax = getObjectMaxVertexCount(obj)
        vertMesh = getObjectVertexCount_Mesh(obj)
        if isMesh(obj):
            vertVC = getMeshVertexCount_VertexColor(obj)
            vertUV0 = getMeshVertexCount_UV0(obj)
            vertUV1 = getMeshVertexCount_UV1(obj)
        elif isPoly(obj):
            vertVC = getPolyVertexCount_VertexColor(obj)
            vertUV0 = getPolyVertexCount_UV0(obj)
            vertUV1 = getPolyVertexCount_UV1(obj)
        else:
            try:
                objMesh = obj.mesh # This will allocate memory each time it's called, so better to call it once and use allocated var.
                vertVC = getMeshVertexCount_VertexColor(objMesh)
                vertUV0 = getMeshVertexCount_UV0(objMesh)
                vertUV1 = getMeshVertexCount_UV1(objMesh)
            except:
                pass #Particle flow stuff are geometryClass but can have undefined Trimesh!
    vertWorst = max(vertMesh, max(vertVC, max(vertUV0, vertUV1)))
    return min(vertWorst, vertMax)

def getObjectSeparateVertexCount(obj):
    vertMax = 0
    vertMesh = 0
    vertVC = 0
    vertUV0 = 0
    vertUV1 = 0
    if isGeometry(obj):
        vertMax = getObjectMaxVertexCount(obj)
        vertMesh = getObjectVertexCount_Mesh(obj)
        if isMesh(obj):
            vertVC = getMeshVertexCount_VertexColor(obj)
            vertUV0 = getMeshVertexCount_UV0(obj)
            vertUV1 = getMeshVertexCount_UV1(obj)
        elif isPoly(obj):
            vertVC = getPolyVertexCount_VertexColor(obj)
            vertUV0 = getPolyVertexCount_UV0(obj)
            vertUV1 = getPolyVertexCount_UV1(obj)
        else:
            try:
                objMesh = obj.mesh # This will allocate memory each time it's called, so better to call it once and use allocated var.
                vertVC = getMeshVertexCount_VertexColor(objMesh)
                vertUV0 = getMeshVertexCount_UV0(objMesh)
                vertUV1 = getMeshVertexCount_UV1(objMesh)
            except:
                pass #Particle flow stuff are geometryClass but can have undefined Trimesh!
    return vertMax, vertMesh, vertVC, vertUV0, vertUV1

def cleanupObject(obj):
    # This will marginaly fix issues. It expects only edit_poly or edit_mesh base objects with no modifier to work properly... Too bad.
    if isMesh(obj):
        rt.meshop.deleteIsoMapVertsAll(obj)
    elif isPoly(obj):
        obj.DeleteIsoMapVerts() # This only works on Edit_Poly objects, thus a plane having an edit_poly modifier on top will not be affected
    elif isGeometry(obj):
        # Lets go for the ugly part. This will not affect many objects and may not worth the try/excepts...
        try:
            rt.meshop.deleteIsoMapVertsAll(obj) # This may catch editable mesh having an edit_poly modifier on top
        except:
            try:
                obj.DeleteIsoMapVerts() # This may catch editable poly having modifier that does not affect too much the mesh type (mirror, etc...)
            except:
                pass

def cleanupObjectHierarchy(obj):
    cleanupObject(obj)
    children = obj.Children
    for child in children:
        cleanupObjectHierarchy(child)

def clearChannelData(obj, mapID):
    if isMesh(obj):
        rt.meshop.setMapSupport(obj, mapID, False)
    elif isPoly(obj):
        rt.polyop.setMapSupport(obj, mapID, False)
    elif isGeometry(obj):
        if qtUtils.popup_Yes_Cancel("Object {0} needs to be converted to an Editable Poly first.\nProceed?".format(obj.name), title="Convert to Edit Poly?"):
            rt.convertToPoly(obj)
            rt.polyop.setMapSupport(obj, mapID, False)

def clearChannelData_UV0(obj):
    with pymxs.undo(True, "Clear UV0 channel"):
        clearChannelData(obj, 1)

def clearChannelData_UV1(obj):
    with pymxs.undo(True, "Clear UV1 channel"):
        clearChannelData(obj, 2)

def clearChannelData_VertexColor(obj):
    with pymxs.undo(True, "Clear Vertex Color channel"):
        clearChannelData(obj, 0) # Vertex color
        clearChannelData(obj, -2) # Vertex alpha

def hasChannelData(obj, mapID):
    if isMesh(obj):
        return rt.meshop.getMapSupport(obj, mapID)
    elif isPoly(obj):
        return rt.polyop.getMapSupport(obj, mapID)
    elif isGeometry(obj):
        return rt.meshop.getMapSupport(obj.mesh, mapID)

def hasChannelData_UV0(obj):
    return hasChannelData(obj, 1)

def hasChannelData_UV1(obj):
    return hasChannelData(obj, 2)

def hasChannelData_VertexColor(obj):
    vcData = hasChannelData(obj, 0) # Vertex color
    vaData = hasChannelData(obj, -2) # Vertex alpha
    return vcData or vaData

"""
LOD AND STATS CALC
"""
def getSafeLodMargin():
    return 0.1 #consider 10% margin to be a bit too close to limit

def getObjectHeight(obj):
    # approximate game: retrieve bounding sphere radius
    objBB = rt.nodeLocalBoundingBox(obj)
    return rt.distance(objBB[0], objBB[1])

def getObjectViewportHeight(obj, distance, fov = 45.0):
    fovMod = math.tan(fov * 0.5) * distance
    return getObjectHeight(obj) / fovMod

def getObjectHierarchyNodeCount(obj):
    return getChildrenCount(obj) + 1

def getObjectHierarchyDrawCount(obj, alreadyCheckedMats=list()):
    # getDrawCount: ~matsPerMesh * meshes(need to check Keep Instances)
    # if not Keep Instances, meshes are merged together resulting in only one mesh
    drawCount = getObjectDrawCount(obj)
    if not isRootNode(obj) and obj.material not in alreadyCheckedMats: # Here if obj.material == None we want to add it to the alreadyCheckedMats list as meshes will end up sharing the same shader
        alreadyCheckedMats.append(obj.material)
    children = obj.Children
    for child in children:
        drawCount += getObjectHierarchyDrawCount(child)#, alreadyCheckedMats)
    return drawCount

def getObjectHierarchyTriangleCount(obj):
    triangleCount = getObjectTriangleCount(obj)
    children = obj.Children
    for child in children:
        triangleCount += getObjectHierarchyTriangleCount(child)
    return triangleCount

def getObjectHierarchyVertexCount(obj):
    vertexCount = getObjectTotalVertexCount(obj)
    children = obj.Children
    for child in children:
        vertexCount += getObjectHierarchyVertexCount(child)
    return vertexCount

def getObjectVertexCountLimit_lastLOD():
    return 150

def getObjectVertexCountLimit_previousLastLOD():
    return 300

def getObjectLowestSizeFromVertexCount(vertexCount):
    screenHeightVertexLimit = 250000 #this is the limit for 100% screen height, but it can go beyond if object height > screen height
    lodCurvePower = 2
    lod1VertexLimit = getObjectVertexCountLimit_previousLastLOD()
    baseCurve = (vertexCount - lod1VertexLimit) / (screenHeightVertexLimit - lod1VertexLimit)
    return math.pow(baseCurve, 1 / lodCurvePower) * 0.99 + 0.01

def getObjectLowestSize(obj, vertexCount = None):
    vertexCount = vertexCount if vertexCount != None else getObjectHierarchyVertexCount(obj) #avoid potentially costly retrieval if already done
    if vertexCount < getObjectVertexCountLimit_lastLOD():
        return 0.0
    elif vertexCount < getObjectVertexCountLimit_previousLastLOD():
        return 0.005
    else:
        return getObjectLowestSizeFromVertexCount(vertexCount)

def getObjectLowestSizePercent(obj, vertexCount = None):
    return getObjectLowestSize(obj, vertexCount) * 100.0

def remapToUnitRange(value, min, max):
    return (value - min) / (max - min)

def adjustedEfficiency(value, factor=0.1):
    # adjust curve in [0~1] interval
    # Factor tend to 0: curve tend to y=ceil(x)
    # factor tend to +inf: curve tend to y=x
    return (factor * value + value) / (factor + value)

def computeMeshEfficiency(vertexCount, triangleCount):
    efficiencyRatio = vertexCount / triangleCount # 3.0 to 0.5
    efficiencyRatio = 1 - remapToUnitRange(efficiencyRatio, 0.5, 3.0) # 0.0 to 1.0
    #efficiencyRatio = triangleCount / (2 * vertexCount) # 0.16666... to 1.0
    #efficiencyRatio = self.adjustedEfficiency(efficiencyRatio) # Gives the illusion that meshes are more efficient than they really are. We only want really "bad" ones to pop out
    efficiencyRatio = int(round(efficiencyRatio * 100, 0)) # display as %
    return efficiencyRatio

def getEfficiencyLevel(efficiency):
    if efficiency < 40:
        return 2
    elif efficiency < 70:
        return 1
    return 0

"""
LOD AND STATS END
"""
