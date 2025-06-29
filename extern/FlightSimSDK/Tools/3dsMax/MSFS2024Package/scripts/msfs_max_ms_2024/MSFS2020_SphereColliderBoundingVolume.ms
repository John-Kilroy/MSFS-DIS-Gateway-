plugin Helper MSFS2020SphereBoundingVolumeGizmo
name:"Sphere Gizmo Bounding Volume"
classID:#(0x4afc6f92, 0x6580db0e)
extends:SphereGizmo
category:"MSFS2024 (OBSOLETE)"
replaceUI:false
invisible:true
autoPromoteDelegateProps:false
(	
	parameters main rollout:params
	(
		IsSkinBoundingVolume type:#boolean animatable:false default:true ui:IsSkinBoundingVolume_UI
	)
	
	rollout params "Sphere Bounding Volume Parameters"
	(
		 checkbox IsSkinBoundingVolume_UI "Is Skin Bounding Volume" type:#boolean
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