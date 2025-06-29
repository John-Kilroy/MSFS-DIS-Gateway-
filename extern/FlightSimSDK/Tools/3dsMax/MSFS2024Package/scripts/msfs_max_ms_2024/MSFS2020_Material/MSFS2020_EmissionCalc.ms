global AsoboEmissionCalcPos
if AsoboEmissionCalc != undefined then destroydialog AsoboEmissionCalc

rollout AsoboEmissionCalc "Emissive Calculator" width:250
(
	group ""
	(
		spinner width "Rect dimensions:" range:[0,10000,40] fieldWidth:55 type:#worldunits scale:0.01 offset:[44,0] across:2
		spinner height "x" range:[0,10000,25] fieldWidth:55 type:#worldunits scale:0.01 align:#right
		spinner diameter "Disc diameter:" range:[0,10000,35] fieldWidth:55 type:#worldunits scale:0.01 align:#right
		spinner area "Area (m²):" range:[0,10000,1000] fieldWidth:55 type:#float scale:0.001 align:#right
		spinner nits "Luminance (cd/m²):" range:[0,10000000,1000] fieldWidth:55 type:#float scale:1.0 align:#right
		spinner candelas "Luminous intensity (cd):" range:[0,1000000,100] fieldWidth:55 type:#float scale:1.0 align:#right
		radioButtons lock "" labels:#("Lock Luminance","Lock Intensity") align:#right
	)
	
	fn GetMetersPerSysUnit =
	(
		metersPerUnit = case units.systemType of
		(
			#Inches: 0.0254
			#Feet: 0.3048
			#Miles: 1609.0
			#Millimeters: 0.001
			#Centimeters: 0.01
			#Meters: 1.0
			#Kilometers: 1000.0
		)
		return metersPerUnit * units.SystemScale
	)
	
	fn Sqr v = (return v*v)
	
	fn computeDisc = (diameter.value = sqrt(area.value / pi) * 2.0 / GetMetersPerSysUnit())
	fn computeRect = (width.value = height.value = (sqrt area.value) / GetMetersPerSysUnit())
	
	fn computeCandelas = (candelas.value = nits.value * area.value)
	fn computeNits = (nits.value = candelas.value / area.value)
	fn computeCandelasOrNits = (if lock.state == 1 then computeCandelas() else computeNits())
	
	on width changed val do
	(
		area.value = width.value * height.value * Sqr(GetMetersPerSysUnit())
		computeDisc()
		computeCandelasOrNits()
	)
	on height changed val do
	(
		area.value = width.value * height.value * Sqr(GetMetersPerSysUnit())
		computeDisc()
		computeCandelasOrNits()
	)
	on diameter changed val do
	(
		area.value = pi * (diameter.value*diameter.value*0.25) * Sqr(GetMetersPerSysUnit())
		computeRect()
		computeCandelasOrNits()
	)
	on area changed val do
	(
		computeRect()
		computeDisc()
		computeCandelasOrNits()
	)
	
	on nits changed val do (computeCandelas())
	on candelas changed val do (computeNits())
		
	on AsoboEmissionCalc open do
	(
		area.value = 1.0 / GetMetersPerSysUnit()
		computeRect()
		computeDisc()
		computeCandelasOrNits()
	)
	on AsoboEmissionCalc close do (AsoboEmissionCalcPos = GetDialogPos AsoboEmissionCalc)
)

if AsoboEmissionCalcPos != undefined then
	createDialog AsoboEmissionCalc pos:AsoboEmissionCalcPos
else
	createDialog AsoboEmissionCalc