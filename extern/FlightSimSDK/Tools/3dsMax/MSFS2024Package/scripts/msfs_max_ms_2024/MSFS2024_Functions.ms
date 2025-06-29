struct MSFS2024_Functions (
	
	/* GENERIC */
	fn xor b1 b2 = 
	(
		(not (b1 and b2)) and (b1 or b2)
	),
	
	
	
	/* PROGRESS BAR */
	fn createProgressBar title:"" =
	(
		rollout progress title width:600 height:60
		(
			label lbProgress "Initialisation..."
			progressbar progBar height:24 color:(color 126 171 106)
		)
		createDialog progress
		progress.progBar.value = 0
		progress
	),
	fn updateProgressBar progressDialog barValue text: pauseOnUpdate:false =
	(
		progressDialog.progBar.value = barValue * 100.0
		if text != unsupplied then progressDialog.lbProgress.text = text
		if pauseOnUpdate then sleep 0.3
	),
	fn deleteProgressBar progressDialog =
	(
		destroyDialog progressDialog
	),
	
	
	/* FILTERS */
	fn isViewportMirrored node = -- retourne true si l'objet est mirrored dans la viewport
	(
		local obj=#((node.scale).x<0,(node.scale).y<0,(node.scale).z<0)
		MSFS2024_Functions.xor obj[1] (MSFS2024_Functions.xor obj[2] obj[3])
	),
	
	fn geomTrueFilter obj = 
	(
		(superclassof obj == Geometryclass) or (superclassof obj == shape and obj.Baseobject.render_displayRenderMesh)
	),
	fn isFsCollisionGizmo obj =
	(
		case classOf obj of
		(
			MSFS2024CylinderGizmo: true
			MSFS2024SphereGizmo: true
			MSFS2024BoxGizmo: true
			default: false
		)
	),
	fn isFsLight obj =
	(
		case classOf obj of
		(
			MSFS2024ProjectedDecal: true
			MSFS2024AdvancedLight: true
			MSFS2024FastLight: true
			MSFS2024SkyPortal: true
			default: false
		)
	),
	
	
	/* SCENE UTILS */
	fn initGetUsedMtlIDs =
	(
		if classof GetUsedMtlIDs != dotNetMethod do (
			local source = 
			"
				using Autodesk.Max;
				using System;
				using System.Collections;
				using System.Collections.Generic;
			
				class MeshMaterialIDs
				{
				static private IGlobal global = GlobalInterface.Instance;
			
				static private IMesh GetMeshFromNode( IINode node )
				{            
					IObject obj = node.EvalWorldState( 0, true ).Obj;
					IClass_ID triClass = global.Class_ID.Create( 9, 0 );
					IClass_ID polyClass = global.Class_ID.Create( 1562457754, 0 );
					IClass_ID patchClass = global.Class_ID.Create( 4144, 0 );
			
					if ( obj.IsSubClassOf( triClass ) )
					{
						return ((ITriObject)obj).Mesh;
					}
					else if ( obj.IsSubClassOf( polyClass ) )
					{                
						ITriObject mesh = (ITriObject)((IPolyObject)obj).ConvertToType( 0, triClass );
						return mesh.Mesh;
					}
					else if ( obj.IsSubClassOf( patchClass ) )
					{
						return ((IPatchObject)obj).GetMesh( 0 );
					}
					else if ( obj.CanConvertToType( triClass ) == 1 )
					{
						ITriObject tri = (ITriObject)obj.ConvertToType( 0, triClass );
						return tri.Mesh_;
					}
					else
					{
						return null;
					}
				}
			
				static public int[] GetUsedMtlIDs( uint handle )
				{
					IINode node = global.COREInterface.GetINodeByHandle( handle );
					IMesh mesh = GetMeshFromNode( node );
			
					if ( mesh == null ) return null;
			
					BitArray used_ids = new BitArray( ushort.MaxValue );
					List<int> material_ids = new List<int>( ushort.MaxValue );
			
					foreach ( IFace face in mesh.Faces )
					{
						if ( used_ids.Get( face.MatID ) == false )
						{
							material_ids.Add( face.MatID + 1 );
							used_ids.Set( face.MatID, true );
						}
			
					}
			
					return material_ids.ToArray();
			
				}
			
				}
			"
		 
			csharpProvider = dotnetobject "Microsoft.CSharp.CSharpCodeProvider"
			compilerParams = dotnetobject "System.CodeDom.Compiler.CompilerParameters"
			compilerParams.ReferencedAssemblies.Add("System.dll");		
			compilerParams.ReferencedAssemblies.Add((getdir #maxroot) + "Autodesk.Max.dll");			
			compilerParams.GenerateInMemory = on
			compilerResults = csharpProvider.CompileAssemblyFromSource compilerParams #(source)
		 
		 
			if (compilerResults.Errors.Count > 0 ) then
			(
				local errs = stringstream ""
				for i = 0 to (compilerResults.Errors.Count-1) do
				(
					local err = compilerResults.Errors.Item[i]
					format "Error:% Line:% Column:% %\n" err.ErrorNumber err.Line err.Column err.ErrorText to:errs
				)
				format "%\n" errs
				undefined
			)
			else
			(
				local assembly = compilerResults.CompiledAssembly.CreateInstance "MeshMaterialIDs"	
			
				global GetUsedMtlIDs = assembly.GetUsedMtlIDs
			)
		 
		)
	),
	
	fn getRoot_recursive obj =
	(
		if obj.parent == undefined
		then return object
		else return (getRoot_recursive obj.parent)
	),
	fn getChildrens parent childrenArray inList:#() onlyLast:false = 
	(
		if inList.count == 0 then
		(
			if onlyLast and parent.children.count == 0 then
			(
				append childrenArray parent
			)
			for child in parent.children do (
				if not onlyLast then append childrenArray child
				MSFS2024_Functions.getChildrens child childrenArray onlylast:onlyLast
			) 
		)
		else
		(
			for child in parent.children do
			(
				if (findItem inList child) != 0 then
				(
					append childrenArray child
					MSFS2024_Functions.getChildrens child childrenArray inList:inList
				)
			) 
		)
	),
	fn getHierarchies selection inSelection:false onlyRoot:false =
	(
		local rootOfSelection = #()
		local ObjectsAlreadyParsed = #()
		if inSelection then
		(
			for obj in selection do (
				local itmFound = findItem ObjectAlreadyParsed obj
				if itmFound == 0 then
				(
					append ObjectAlreadyParsed obj
					if obj.parent == undefined then --si obj est un root de la scene
					(
						local rootAndChildrenArray = #(obj)
						MSFS2024_Functions.getChildrens obj rootAndChildrenArray inList:selection --on recup les enfants deja selectionne
						for objectAlreadyParsed in rootAndChildrenArray do appendifunique objectsAlreadyParsed objectAlreadyParsed --on les stocke dans objectsAlreadyParsed
						if onlyRoot then append rootOfSelection obj
						else append rootOfSelection (rootAndChildrenArray)
					)
					else
					(
						local parentInSelectionFound = false
						for i=selection.count to 1 by -1 where selection[i] != obj and obj.parent == selection[i] do --on cherche si le parent de obj se trouve dans la selection
						(
							parentInSelectionFound = true
							exit
						)

						if parentInSelectionFound then appendIfUnique objectsAlreadyParsed obj
						else --si le parent de o ne se trouve pas dans la selection alors c'est un root de la selection
						(
							local rootAndChildrenArray = #(obj)
							MSFS2024_Functions.getChildrens obj rootAndChildrenArray inList:selection
							for objectAlreadyParsed in rootAndChildrenArray do appendIfUnique objectsAlreadyParsed objectAlreadyParsed
							
							if onlyRoot then append rootOfSelection obj
							else rootOfSelection (rootAndChildrenArray)
						)
					)
				)
			)
		)
		else
		(
			for obj in selection do
			(
				local itemFound = findItem ObjectsAlreadyParsed obj --si l'objet n'est pas deja traite
				if itemFound == 0 then
				(
					if obj.parent == undefined then --si o est un root de la scene
					(
						local rootAndChildrenArray = #(obj)
						MSFS2024_Functions.getChildrens obj rootAndChildrenArray --on recup les enfants deja selectionne
						for objectAlreadyParsed in rootAndChildrenArray do appendIfUnique ObjectsAlreadyParsed objectAlreadyParsed --on les stocke dans ObjectsAlreadyParsed
						if onlyRoot then append rootOfSelection (MSFS2024_Functions.getRoot_recursive obj)
						else append rootOfSelection (rootAndChildrenArray)
					)
					else
					(
						local parentInSelectionFound = false
						local objCopy = obj
						local originalRootInSelection = obj
						do
						(
							parentFound = findItem selection (obj.parent)
							if parentFound != 0 then originalRootInSelection = (obj.parent)
							obj = obj.parent
						) while obj.parent != undefined

						local rootAndChildrenArray = #(originalRootInSelection)
						MSFS2024_Functions.getChildrens originalRootInSelection rootAndChildrenArray --on recup les enfants deja selectionne
						for objectAlreadyParsed in rootAndChildrenArray do appendIfUnique objectsAlreadyParsed objectAlreadyParsed --on les stocke dans objectsAlreadyParsed
						if onlyRoot then appen rootOfSelection (MSFS2024_Functions.getRoot_recursive originalRootInSelection)
						else append rootOfSelection (rootAndChildrenArray)
					)
				)
			)
		)
		
		return rootOfSelection
	),
	
	
	fn createMeshManual children objCreated =
	(
		local newMultiMat = #() --contient le tableau des nouveaux materiaux a appliquer sur le mesh generated
		local existingMultiMat = #()
		if objCreated.material != undefined then --permet de sauvegarder le multimat/mat final
		(
			if ClassOf objCreated.material == Multimaterial then
			(
				for subMat in objCreated.material do 
				(
					append existingMultiMat subMat
				)
			)
			else append existingMultiMat objCreated.material
		)

		for obj in children do --boucle qui fait un snapshot de chaque objet et qui prepare proprement la multimat de l'objet final
		(
			objTemp = snapshot obj
			objTemp.parent = undefined
			ResetXForm objTemp
			convertToMesh objTemp
			local saveMat = objTemp.material --hack pour pas perdre l'history du undo quand attach (probleme avec les multi mat)
			if ClassOf saveMat == Multimaterial then
			(
				IDTrueUsed = #{}
				FacesIDTable = #()
				for f = 1 to objTemp.numfaces do --pour toutes les faces de l'objet
				(
					local faceMatID = (getFaceMatID objTemp f)
					if not(IDTrueUsed[faceMatID]) then --si c'est un nouvel ID pas encore traité
					(
						FacesIDTable[faceMatID] = #{f}
						IDTrueUsed[(getFaceMatID objTemp f)] = true
					)
					else
					(
						append (FacesIDTable[faceMatID]) f
					)
				)

				for indexMat in IDTrueUsed do -- pour chaque mat vraiment applique au mesh
				(
					matCurrent = saveMat[indexMat]
					matID = findItem newMultiMat matCurrent
					if matID == 0 then --materiaux pas encore dans le multi final
					(
						append newMultiMat matCurrent
						newID = newMultiMat.count
						for f in (FacesIDTable[indexMat]) do setFaceMatID objTemp f newID --on applique le nouvel Id aux faces
					)
					else for f in (FacesIDTable[indexMat]) do setFaceMatID objTemp f matID --on applique le bon ID existant aux faces
				)
			)
			else
			(
				matCurrent = saveMat
				if matCurrent != undefined then
				(
					matID = findItem newMultiMat matCurrent
					if matID == 0 then
					(
						append newMultiMat matCurrent
						newID = newMultiMat.count
						for f = 1 to objTemp.numfaces do setFaceMatID objTemp f newID
					)
					else for f = 1 to objTemp.numfaces do setFaceMatID objTemp f matID
				)
			)
			objTemp.material = undefined
			local flip = MSFS2024_Functions.isViewportMirrored objTemp
			polyop.attach objCreated objTemp
		)

		local finalMat
		if newMultiMat.count != 0 then
		(
			finalMat = multimaterial numsubs:(newMultiMat.count) --creation du material final appliqué sur l'objet generated
			finalMat.name = objCreated.name + "_mat"
			for i = 1 to (newMultiMat.count) do
			(
				if newMultiMat[i] == undefined then
				(
					finalMat[i] = MSFS2024_Material()
					finalMat[i].name = "NewMSFS2024Material%" + (i as string)
				)
				else finalMat[i] = newMultiMat[i]
			)
			objCreated.material = finalMat
		)
		return objCreated
	),
	
	
	/* LAYERS */
	
	/*
	* Create new layer from name
	* return created layer
	*/
	fn createLayer name:"Debug layer" current:false visible:true =
	(
		local layer = LayerManager.newLayerFromName name
		layer.on = visible
		layer.ishidden = not visible
		layer.lock = false
		if current then layer.current = true -- cant set to false here
		layer
	),
	
	/*
	* Delete layer from name
	* Only delete if empty
	* return true on success, false if failed
	*/
	fn deleteLayer name:"Debug layer" =
	(
		LayerManager.deleteLayerByName name
	),
	
	fn addHierarchyNodesToLayer obj layer =
	(
		for child in obj.children do MSFS2024_Functions.addHierarchyNodesToLayer child
		layer.addNode obj
	),
	
	/* FLATTEN HIERARCHY */
	
	/*
	* Remove hierarchy completely
	* Initially done because C# functions are failing miserably
	*/
	fn deleteHierarchyNodes obj =
	(
		for child in obj.children do MSFS2024_Functions.deleteHierarchyNodes child
		delete obj
	),
	/*
	* Create new clean mesh
	* ready to merge other meshes to
	* return newly created mesh
	* if position is supplied, it will override transform position values. This is useful to create a new mesh with clean transform (no scale, no rotation)
	*/
	fn createMergeMesh transform:(matrix3 1) position: name: =
	(
		if position != unsupplied then transform.position = position
		local mergeMesh = Editable_mesh vertices:#() faces:#() transform:transform name:name
		convertToPoly mergeMesh
		mergeMesh
	),
	/*
	* Merge mesh into ready to merge one
	*/
	fn mergeMeshTo obj mergeMesh =
	(
		local objTemp = snapshot obj
		objTemp.parent = undefined
		convertToPoly objTemp -- If original object is editable poly with sub-object mode active (tested with face sub-object mode), ResetXForm will simply crash. LOL. Pre-converting seems to solve the issue.
		ResetXForm objTemp
		convertToPoly objTemp
		polyop.attach mergeMesh objTemp
	),
	/*
	* Flatten nodes hierarchy and merge meshes sharing the same flatten group together (use flightsim_flatten_group user property to define groups)
	* Note that groupNames defined below are reserved and should not be set by user, else it may lead to unexpected results
	* If 2 meshes are separated by a gizmo in hierarchy, we dont care: final hierarchy will have only one mesh with gizmo as child
	* Keep optional parent arg undefined when calling this fn
	* Init groupNames, groupNodes, newNodes as empty arrays
	*/
	fn recursivelyFlattenMesh obj &groupNames &groupNodes &newNodes parent:undefined =
	(
		-- filter objects per groups and types
		local isMesh = false
		local groupName
		if MSFS2024_Functions.geomTrueFilter obj then
		(
			groupName = getUserPropVal obj "flightsim_flatten_group" asString:true
			if groupName == undefined or groupName == emptyVal then groupName = "defaultFlattenGroup"
			isMesh = true
		)
		else if MSFS2024_Functions.isFsLight obj then				groupName = "lightFlattenGroup"
		else if MSFS2024_Functions.isFsCollisionGizmo obj then		groupName = "collisionGizmoFlattenGroup"
		
		local newNode
		-- if object is not in a group: we dont support it in flatten process
		if groupName != undefined then
		(
			-- pre-fill groups
			local groupId = findItem groupNames groupName
			if groupId == 0 then
			(
				append groupNames groupName
				append groupNodes #()
				groupId = groupNames.count
			)
			
			if isMesh then
			(
				-- create merge mesh if non existing already
				if groupNodes[groupId].count == 0 then
				(
					newNode = MSFS2024_Functions.createMergeMesh position:obj.position name:obj.name
					append groupNodes[groupId] newNode
				)
				MSFS2024_Functions.mergeMeshTo obj groupNodes[groupId][1] 
			)
			else
			(
				newNode = copy obj
				append groupNodes[groupId] newNode
			)
			
			if newNode != undefined then
			(
				append newNodes newNode
				if parent == undefined then parent = newNode
			)
		)
		
		local children = obj.children
		for child in children do
		(
			parent = MSFS2024_Functions.recursivelyFlattenMesh child &groupNames &groupNodes &newNodes parent:parent
		)
		
		parent --return parent
	),
	fn flattenMeshes obj &groupNames &groupNodes =
	(
		local hierarchyNodes = #()
		local parent = MSFS2024_Functions.recursivelyFlattenMesh obj &groupNames &groupNodes &hierarchyNodes
		if parent != undefined then
		(
			-- only parent afterwards so we are sure we have found our parent
			for n in hierarchyNodes where n != parent do
			(
				n.parent = parent
			)
			parent.parent = undefined
			parent.pivot = obj.position
		)
		parent --return parent
	),
	/*
	* Flatten hierarchy from parent node
	* In case parent must be a mesh (for example when dealing with collision gizmos, exported as mesh extension in gltf):
	*	set needMeshParent to true
	*	if no mesh is found in hierarchy, will return undefined
	* layerName can be left empty. If supplied, will put flattened hierarchy in new visible layer
	*/
	fn flattenHierarchy obj flattenedParentNodeName:"newFlattenedHierarchyParent" needMeshParent:false keepUserProps:true layerName: = 
	(
		if obj == undefined then
		(
			undefined -- early return if nothing to process
		)
		else
		(
			with redraw off
			(
				local cmdPanelBackup = getCommandPanelTaskMode()
				setCommandPanelTaskMode #create --optim: avoid modifier panel refresh
				
				local groupNames = #()
				local groupNodes = #()
				local flattenedHierarchyParent = MSFS2024_Functions.flattenMeshes obj &groupNames &groupNodes
				free groupNames
				free groupNodes
				if flattenedHierarchyParent != undefined then
				(
					if needMeshParent and superclassof flattenedHierarchyParent != Geometryclass then
					(
						-- search for first mesh object
						local meshFound
						for child in flattenedHierarchyParent.children while meshFound == undefined do
						(
							if superclassof child == Geometryclass then
							(
								meshFound = child
							)
						)
						-- transfer parenthood to found mesh
						if meshFound != undefined then
						(
							meshFound.parent = undefined
							meshFound.pivot = flattenedHierarchyParent.pivot
							for child in flattenedHierarchyParent.children do child.parent = meshFound
							flattenedHierarchyParent.parent = meshFound
							flattenedHierarchyParent = meshFound
						)
						else
						(
							-- if need mesh parent but no mesh can be found, return undefined
							MSFS2024_Functions.deleteHierarchyNodes flattenedHierarchyParent
							return undefined
						)
					)
					flattenedHierarchyParent.name = flattenedParentNodeName
					if keepUserProps then
					(
						setUserPropBuffer flattenedHierarchyParent (getUserPropBuffer obj)
					)
					
					-- put in layer if needed
					if layerName != unsupplied then
					(
						local tempLayer = MSFS2024_Functions.createLayer name:layerName
						MSFS2024_Functions.addHierarchyNodesToLayer flattenedHierarchyParent tempLayer
					)
				)
				
				setCommandPanelTaskMode cmdPanelBackup --reset commandpanel state
				flattenedHierarchyParent
			)
		)
	),
	
	
	/* UPGRADE TO 2024 */
	fn convertMSFS2020ObjectsToMSFS2024Object old_className new_className =
	(
		oldObjects = (getClassInstances old_className)
		if oldObjects.count <= 0 then return undefined
			
		pbar = MSFS2024_Functions.createProgressBar title:"Scene conversion MSFS2024"
		exceptionPropList= #(#Free_Disc, #SphereGizmo, #BoxGizmo, #CylGizmo, #Directionallight, #Free_Light)
		hasOldObjects = false
		i = 0.0
		for oldObject in oldObjects do
		(
			if (isProperty oldObject #name and oldObject.name != undefined) then 
			(
				newObject = new_className name:oldObject.name
				MSFS2024_Functions.updateProgressBar pbar (i/oldObjects.count) text:("Converting " + oldObject.name) 
			)
			else
			(
				newObject = new_className()
				MSFS2024_Functions.updateProgressBar pbar (i/oldObjects.count) text:("Converting " + (old_className as string) + " objects to " + (new_className as string) + " objects") 
			)
			
			propertyNames = getPropNames oldObject
			for property in propertyNames do
			(
				isExceptionProp = false
				for exceptionProp in exceptionPropList do (
					if property == exceptionProp then
					(
						isExceptionProp = true
						break
					)
				)

				if isExceptionProp then
				(
					propertyExtendedNames = getPropNames (getProperty oldObject property)
					for propertyExtended in propertyExtendedNames do
					(
						if (isProperty (getProperty newObject property) propertyExtended) and (getProperty (getProperty oldObject property) propertyExtended) != undefined then
						(
							setProperty (getProperty newObject property) propertyExtended (getProperty (getProperty oldObject property) propertyExtended)
						)
					)
				)

				if (isProperty newObject property) and (getProperty oldObject property) != undefined and not isExceptionProp then
				(
					setProperty newObject property (getProperty oldObject property)
				)
			)
			replaceInstances oldObject newObject
			if superClassOf newObject != material then
				delete newObject

			hasOldObjects = true
			i += 1.0
		)
		MSFS2024_Functions.deleteProgressBar pbar
	)
)
