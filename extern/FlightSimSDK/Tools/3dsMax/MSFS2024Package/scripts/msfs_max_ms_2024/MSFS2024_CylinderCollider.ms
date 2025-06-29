plugin Helper MSFS2024CylinderGizmo
name:"Cylinder Gizmo"
classID:#(0x53759d0f, 0x661b0fbd)
extends:CylGizmo
category:"MSFS2024"
replaceUI:false
autoPromoteDelegateProps:false
(
	parameters main rollout:params
	(
		IsCollider type:#boolean animatable:false default:true ui:IsCollider_UI
		IsRoad type:#boolean animatable:false default:false ui:IsRoad_UI
	)
	
	rollout params "Cylinder Collider Parameters"
	(
		checkbox IsCollider_UI "Is Collider" type:#boolean
		checkbox IsRoad_UI "Is Road Collider" type:#boolean
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