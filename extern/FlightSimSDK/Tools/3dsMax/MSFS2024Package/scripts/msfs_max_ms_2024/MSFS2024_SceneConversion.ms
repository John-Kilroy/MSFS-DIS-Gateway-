(
    local hasOldClasses = false
	local oldClasses = #(FlightSim, FlightSimLight, AsoboBoxGizmo, AsoboCylinderGizmo, ProjectedDecal, AsoboSphereGizmo, SphereFade)
	
	for oldClass in oldClasses do
	(
		oldObjects = getClassInstances oldClass
		if (oldObjects.count > 0) then 
		(
			hasOldClasses = true
			break
		)
	)

	if hasOldClasses then
	(
        result = queryBox "Your scene has objects and materials using MSFS2020 parameters, would you like to convert it to MSFS2024 ?\n (Be aware that you risk losing data that is not supported in MSFS2024, and once it's lost, there is no way to recover it)"
        if result then
        (
            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object FlightSim MSFS2024_Material

            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object FlightSimLight MSFS2024FastLight
            
            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object AsoboBoxGizmo MSFS2024BoxGizmo
            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object AsoboCylinderGizmo MSFS2024CylinderGizmo
            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object ProjectedDecal MSFS2024ProjectedDecal
            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object AsoboSphereGizmo MSFS2024SphereGizmo
            MSFS2024_Functions.convertMSFS2020ObjectsToMSFS2024Object SphereFade MSFS2024SphereFade
        )
    )
    else
    (
        messageBox "Your scene is already upgraded"
    )
)
