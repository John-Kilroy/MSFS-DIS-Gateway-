plugin Helper MSFS2024SphereFade
name:"Sphere Fade"
classID:#(0x69ac20f9, 0x533132d3)
extends:SphereGizmo
category:"MSFS2024"
replaceUI:false
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