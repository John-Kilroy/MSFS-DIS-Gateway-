plugin Helper MSFS2024SphereBoundingVolumeGizmo
name:"Sphere Gizmo Bounding Volume"
classID:#(0x78ee0ad7, 0x3caa0738)
extends:SphereGizmo
category:"MSFS2024"
replaceUI:false
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