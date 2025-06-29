(
local script = 
"	
	local hasOldClasses = false
	local oldClasses = #()

	local MSFS2020_IS_PUBLIC_SDK = false
	if (globalVars.isglobal #IS_PUBLIC_SDK and globalVars.get #IS_PUBLIC_SDK != undefined) then
	(
		MSFS2020_IS_PUBLIC_SDK = globalVars.get #IS_PUBLIC_SDK
	)

	if not MSFS2020_IS_PUBLIC_SDK then
	(
		oldClasses = #(MSFS2020_Material, MSFS2020SkyPortal, MSFS2020FastLight, MSFS2020AdvancedLight, MSFS2020BoxGizmo, MSFS2020CylinderGizmo, MSFS2020ProjectedDecal, MSFS2020SphereGizmo, MSFS2020SphereBoundingVolumeGizmo, MSFS2020SphereFade)
	)

	for oldClass in oldClasses do
	(
		if oldClass != undefined then
		(
			oldObjects = getClassInstances oldClass
			if (oldObjects.count > 0) then 
			(
				hasOldClasses = true
				break
			)
		)
	)
	
	if hasOldClasses then
	(
		result = queryBox \"You have elements in your scene that has been saved with MSFS2020 parameters, would you like to upgrade it to MSFS2024 ? (If you don't, you won't be able to use MSFS2024 tools)\"
		if result then
		(
			
			if MSFS2020_IS_PUBLIC_SDK == false then
			(
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020_Material MSFS2024_Material

				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020SkyPortal MSFS2024SkyPortal
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020FastLight MSFS2024FastLight
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020AdvancedLight MSFS2024AdvancedLight
				
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020BoxGizmo MSFS2024BoxGizmo
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020CylinderGizmo MSFS2024CylinderGizmo
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020ProjectedDecal MSFS2024ProjectedDecal
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020SphereGizmo MSFS2024SphereGizmo
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020SphereBoundingVolumeGizmo MSFS2024SphereBoundingVolumeGizmo
				MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object MSFS2020SphereFade MSFS2024SphereFade
			)
		)
	)
"

callbacks.addScript #filePostOpenProcessFinalized script id:#MSFS2024
)
