plugin Helper MSFS2020SphereFade
name:"Sphere Fade"
classID:#(0x794b56ca, 0x172623ba)
extends:SphereGizmo
category:"MSFS2024 (OBSOLETE)"
replaceUI:false
invisible:true
autoPromoteDelegateProps:false
(	
	parameters main rollout:params
	(
		
	)
	
	rollout params "Sphere Fade Parameters"
	(
		
	)

	fn setAsDoNotExport nodeVar =
	(
		setUserProp nodeVar "babylonjs_noexport" True
	)

	on attachedToNode n do
	(
		setAsDoNotExport(n)
	)
)