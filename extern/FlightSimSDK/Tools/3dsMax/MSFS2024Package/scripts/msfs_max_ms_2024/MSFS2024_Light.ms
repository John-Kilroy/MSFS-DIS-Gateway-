struct MSFS2024LightTools
(
	fn TemperatureToColor T =
	(
		-- Temperature to CIE 1960
		local u = (0.860117757 + 0.000154118254 * T + 0.000000128641212 * T * T) / (1.0 + 0.000842420235 * T + 0.000000708145163 * T * T)
		local v = (0.317398726 + 0.0000422806245 * T + 0.0000000420481691 * T * T) / (1.0 - 0.0000289741816 * T + 0.000000161456053 * T * T)
		
		-- CIE to xyY
		local xx = 3.0 * u / (2.0 * u - 8.0 * v + 4.0)
		local yy = 2.0 * v / (2.0 * u - 8.0 * v + 4.0)
		local Y = 1.0
		
		-- xyY to XYZ
		local X = xx * Y / yy
		local Z = (1.0 - xx - yy) * Y / yy
		
		-- XYZ to RGB (color primaries and white point from sRGB)
		local R =   3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
		local G = - 0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
		local B =   0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z
		
		-- Normalize
		local m = if R > G then if R > B then R else B else if G > B then G else B
		R /= m
		G /= m
		B /= m
		
		if R < 0 do R = 0
		if G < 0 do G = 0
		if B < 0 do B = 0
		
		return (Color R G B) * 255
	),

	fn ConeAngleToSolidAngle A =
	(
		return 2.0 * PI * (1.0 - (cos (A * 0.5)))
	),
	
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
)

plugin Light MSFS2024FastLight
name:"Street Light"
classID:#(0x204167e8, 0x552ef992)
extends:Free_Light
category:"MSFS2024"
replaceUI:true
autoPromoteDelegateProps:false
version:2
(
	local displayMesh = TriMesh()
	local displayVerts = #([0.0,0.0,0.0])
	local displayDirty = true
	
    parameters main rollout:params
	(
		ColorMode type:#integer animatable:false default:1 ui:ColorMode_UI
		Kelvin type:#float default:6500.0 ui:Kelvin_UI
	    Color type:#color default:white ui:Color_UI animatable:false
		
		UnitMode type:#integer animatable:false default:1 ui:UnitMode_UI
		Intensity type:#float animatable:false default:1000.0 ui:Intensity_UI
		Flux type:#float animatable:false default:1000.0 ui:Flux_UI
		ActivationMode type:#integer animatable:false default:1 ui:ActivationMode_UI
		
	    ConeAngle type:#float animatable:false default:90.0 ui:ConeAngle_UI
		HasSimmetry type:#boolean animatable:false default:false ui:HasSimmetry_UI
		
		FlashFrequency type:#float default:0.0 animatable:false default:false ui:FlashFrequency_UI
		FlashDuration type:#float default:0.2 animatable:false default:false ui:FlashDuration_UI
		FlashPhase type:#float default:0.0 animatable:false default:false ui:FlashPhase_UI
		RotationSpeed type:#float default:0.0 animatable:false default:false ui:RotationSpeed_UI
		RotationPhase type:#float default:0.0 animatable:false default:false ui:RotationPhase_UI
		RandomPhase type:#boolean animatable:false default:true ui:RandomPhase_UI
		
		on ColorMode set val do
		(
			if val == 1 do
				Color = MSFS2024LightTools.TemperatureToColor Kelvin
		)
		
		on Kelvin set val do
		(
			if ColorMode == 1 do
				Color = MSFS2024LightTools.TemperatureToColor val
		)
		
		on Color set val do
		(
			delegate.rgbFilter = val
		)
		
		on Intensity set val do
		(
			delegate.intensity = val
			if UnitMode == 1 do
				Flux = val * (MSFS2024LightTools.ConeAngleToSolidAngle ConeAngle)
			displayDirty = true
		)
		
		on Flux set val do
		(
			if UnitMode == 2 do
				Intensity = val / (MSFS2024LightTools.ConeAngleToSolidAngle ConeAngle)
		)
		
        on ConeAngle set val do
        (
			delegate.distribution = if val >= 360.0 then 0 else 1
			
			delegate.falloff=val
			delegate.hotspot=val
			
			if UnitMode == 1 then
				Flux = Intensity * (MSFS2024LightTools.ConeAngleToSolidAngle val)
			else
				Intensity = Flux / (MSFS2024LightTools.ConeAngleToSolidAngle val)
			
			displayDirty = true
		)
		
		on HasSimmetry set val do
		(
			displayDirty = true
		)
	)
	
	on create do
	(
		delegate.intensityType = 1
		delegate.usekelvin = false
	)
	
	on update do
	(
		if version < 2 do
		(
			print "Update MSFS2024_Material Light"
			this.Intensity *= 200.0
			this.ColorMode = 2
		)
	)
	
	on getDisplayMesh do
	(
		if (displayDirty == true) do
		(
			local arcsegs = 8
			local arcverts = arcsegs+1
			local r = sqrt(this.Intensity/1000.0) / MSFS2024LightTools.GetMetersPerSysUnit()
			
			local vertsCount = arcverts*4*2+1
			local vertEnd = vertsCount
			if this.HasSimmetry == true do vertsCount *= 2
			displayVerts.count = vertsCount
			for i = 1 to arcsegs+1 do
			(
				local a = ((float)(i-1)/arcsegs) * this.ConeAngle * 0.5
				local x = sin a
				local y = cos a
				
				displayVerts[i+0*arcverts] = [ x,0.0,-y] * r
				displayVerts[i+1*arcverts] = [-x,0.0,-y] * r
				displayVerts[i+2*arcverts] = [0.0, x,-y] * r
				displayVerts[i+3*arcverts] = [0.0,-x,-y] * r
				
				a = ((float)(i-1)/arcsegs) * 90.0
				local s = sin(this.ConeAngle * 0.5)
				x = (sin a) * s
				y = (cos a) * s
				z = cos(this.ConeAngle * 0.5)
				displayVerts[i+4*arcverts] = [ x, y,-z] * r
				displayVerts[i+5*arcverts] = [ x,-y,-z] * r
				displayVerts[i+6*arcverts] = [-x, y,-z] * r
				displayVerts[i+7*arcverts] = [-x,-y,-z] * r
			)
			displayVerts[vertEnd] = [0.0,0.0,0.0]
			if this.HasSimmetry == true do
			(
				local halfVerts = vertsCount/2
				for i = 1 to halfVerts do
					displayVerts[i + halfVerts] = displayVerts[i] * [1.0,1.0,-1.0]
			)
			
			local facesCount = arcsegs*4*2+4
			if this.HasSimmetry == true do facesCount *= 2
			if (displayMesh.numfaces != facesCount) then
			(
				local displayFaces = #([0,0,0])
				displayFaces.count = facesCount
				for i = 1 to arcsegs do
				(
					displayFaces[i+0*arcsegs] = [i,i,i+1]+0*arcverts
					displayFaces[i+1*arcsegs] = [i,i,i+1]+1*arcverts
					displayFaces[i+2*arcsegs] = [i,i,i+1]+2*arcverts
					displayFaces[i+3*arcsegs] = [i,i,i+1]+3*arcverts
					
					displayFaces[i+4*arcsegs] = [i,i,i+1]+4*arcverts
					displayFaces[i+5*arcsegs] = [i,i,i+1]+5*arcverts
					displayFaces[i+6*arcsegs] = [i,i,i+1]+6*arcverts
					displayFaces[i+7*arcsegs] = [i,i,i+1]+7*arcverts
				)
				for i = 1 to 4 do
				(
					displayFaces[i+arcsegs*4*2] = [arcverts*i,arcverts*i,vertEnd]
				)
				if this.HasSimmetry == true do
				(
					local halfVerts = vertsCount/2
					local halfFaces = facesCount/2
					for i = 1 to halfFaces do
						displayFaces[i + halfFaces] = displayFaces[i] + halfVerts
				)
				setMesh displayMesh vertices:displayVerts faces:displayFaces
			)
			else
				setMesh displayMesh vertices:displayVerts
			
			displayDirty = false
		)
		displayMesh
	)
	
	rollout params "Parameters"
	(
		group "Color"
		(
			radiobuttons ColorMode_UI "" labels:#("Kelvin","RGB") align:#left columns:1 offsets:#([0,0], [0,8]) 
			spinner Kelvin_UI "" range:[1000, 10000, 3600.0] type:#Float align:#right scale:100 fieldWidth:55 offset:[0,-43]
			colorpicker Color_UI "" modal:false align:#right fieldWidth:65
		)
	    
		group "Power"
		(
			radiobuttons UnitMode_UI "" labels:#("Intensity (cd)","Flux (lm)") align:#left columns:1 offsets:#([0,0], [0,6]) 
			spinner Intensity_UI "" range:[0.0, 1000000.0, 1.0] type:#Float align:#right fieldWidth:55 offset:[0,-41] tooltip:"Intensity in Candelas (lm/sr)"
			spinner Flux_UI "" range:[0.0, 100000.0, 1.0] type:#Float align:#right fieldWidth:55 tooltip:"Power in Lumens (lm)"
			
			radiobuttons ActivationMode_UI "" columns:1 labels:#("Night Only","Always On") align:#left offset:[0,10]
		)
		
		group "Distribution"
		(
			spinner ConeAngle_UI "Cone Angle" range:[0.0, 360, 90.0] type:#Float align:#right
			checkbox HasSimmetry_UI "Symetrical Cone" align:#right tooltip:"Spot will project light in both directions. To use with angles < 180�"
		)
		
		group "Animation"
		(
			spinner FlashFrequency_UI "Frequency (1/min)" range:[0.0, 1000.0, 1.0] align:#right type:#Float width:90 tooltip:"Flashs per minutes"
			spinner FlashDuration_UI "Duration (s)" range:[0.0, 1000.0, 0.2] align:#right type:#float width:90 tooltip:"Flash duration in seconds"
			spinner FlashPhase_UI "Phase (s)" range:[0.0, 1000.0, 0.0] align:#right type:#float width:90 tooltip:"Flash phase in seconds"
			spinner RotationSpeed_UI "Rotation Speed (RPM)" range:[-1000.0, 1000.0, 0.0] align:#right type:#float width:90 tooltip:"Rotations per minute"
			spinner RotationPhase_UI "Rotation Phase" range:[0.0, 1.0, 0.0] align:#right type:#float width:90 tooltip:"Rotation phase. 1.0 mean full rotation."
			checkbox RandomPhase_UI "Random Phase" align:#right tooltip:"Apply a random offset to the phase, per instance of this scene.\nRandom offset will only differ between instances of this scene, not between individual lights in this scene."
		)
		
		on ColorMode_UI changed val do 
		(
			Kelvin_UI.enabled = (val == 1)
			Color_UI.enabled = (val == 2)
		)
		
		on UnitMode_UI changed val do 
		(
			Intensity_UI.enabled = (val == 1)
			Flux_UI.enabled = (val == 2)
		)
		
		on params open do
		(
			Kelvin_UI.enabled = (ColorMode == 1)
			Color_UI.enabled = (ColorMode == 2)
			Intensity_UI.enabled = (UnitMode == 1)
			Flux_UI.enabled = (UnitMode == 2)
		)
	)
)

plugin Light MSFS2024AdvancedLight
name:"Advanced Light"
classID:#(0xb0c612d, 0x143591cf)
extends:Free_Light
category:"MSFS2024"
replaceUI:true
autoPromoteDelegateProps:false
version:0
(
	local displayMesh = TriMesh()
	local displayVerts = #([0.0,0.0,0.0])
	local displayDirty = true
	
	fn SetDelegateDistributionShape =
	(
		if (this.ShapeType <= 2) then -- point & sphere
		(
			delegate.distribution = if this.InnerConeAngle < 360.0 then 1 else 0 -- spot else spherical
			delegate.type =  if this.InnerConeAngle < 360.0 then #Free_Disc else #Free_Sphere -- delegate don't support sphere shape for spot
		)
		else if (this.ShapeType == 3) then -- disc
		(
			delegate.distribution = 1 -- spot
			delegate.type = #Free_Disc
		)
	)
	
    parameters main rollout:params
	(
		ColorMode type:#integer animatable:false default:1 ui:ColorMode_UI
		Kelvin type:#float default:6500.0 ui:Kelvin_UI
	    Color type:#color default:white ui:Color_UI animatable:true
		
		UnitMode type:#integer animatable:false default:1 ui:UnitMode_UI
		Intensity type:#float animatable:true default:1000.0 ui:Intensity_UI
		Flux type:#float animatable:false default:1000.0 ui:Flux_UI
		
		-- shape : point / sphere / disc / (rectangle) / (IES profile)
		ShapeType type:#integer animatable:false default:1 ui:ShapeType_UI
		SourceRadius type:#float animatable:false default:10.0 ui:SourceRadius_UI
	    InnerConeAngle type:#float animatable:false default:45.0 ui:InnerConeAngle_UI
	    OuterConeAngle type:#float animatable:false default:90.0 ui:OuterConeAngle_UI
		
		ChannelExterior type:#boolean animatable:false default:true ui:ChannelExterior_UI
		ChannelInterior type:#boolean animatable:false default:true ui:ChannelInterior_UI
		
		on ColorMode set val do
		(
			if val == 1 do Color = MSFS2024LightTools.TemperatureToColor Kelvin
		)
		
		on Kelvin set val do
		(
			if ColorMode == 1 do Color = MSFS2024LightTools.TemperatureToColor val
		)
		
		on Color set val do
		(
			delegate.rgbFilter = val
		)
		
		on Intensity set val do
		(
			delegate.intensity = val
			if UnitMode == 1 do Flux = val * (MSFS2024LightTools.ConeAngleToSolidAngle OuterConeAngle)
			displayDirty = true
		)
		
		on Flux set val do
		(
			if UnitMode == 2 do Intensity = val / (MSFS2024LightTools.ConeAngleToSolidAngle OuterConeAngle)
		)
		
        on ShapeType set val do
        (
			if (ShapeType == 3) do
			(
				if (InnerConeAngle > 180.0) do delegate.hotspot = InnerConeAngle = 180.0
				if (OuterConeAngle > 180.0) do delegate.falloff = OuterConeAngle = 180.0
			)
			SetDelegateDistributionShape()
			displayDirty = true
		)
		
		on SourceRadius set val do
		(
			v = (val / 100.0) / MSFS2024LightTools.GetMetersPerSysUnit()
			delegate.light_Radius = v
			SetDelegateDistributionShape()
			displayDirty = true
		)
		
        on InnerConeAngle set val do
        (
			delegate.hotspot = val
			if (OuterConeAngle < val) do delegate.falloff = OuterConeAngle = val
			displayDirty = true
		)
		
        on OuterConeAngle set val do
        (
			delegate.falloff = val
			if (InnerConeAngle > val) do delegate.hotspot = InnerConeAngle = val
			if UnitMode == 1 then Flux = Intensity * (MSFS2024LightTools.ConeAngleToSolidAngle val)
			else Intensity = Flux / (MSFS2024LightTools.ConeAngleToSolidAngle val)
			displayDirty = true
		)
		
		on ChannelExterior set val do
		(
			if (val == false) do ChannelInterior = true
		)
		
		on ChannelInterior set val do
		(
			if (val == false) do ChannelExterior = true
		)
	)
	
	on create do
	(
		delegate.intensityType = 1
		delegate.usekelvin = false
	)
	
	on update do
	(
		
	)

	on getDisplayMesh do
	(
		if (displayDirty == true) do
		(
			local arcsegs = 8
			local arcverts = arcsegs+1
			local sr = if (this.ShapeType == 1) then 0.0 else (this.SourceRadius/100.0) / MSFS2024LightTools.GetMetersPerSysUnit()
			local r = sqrt(this.Intensity/1000.0) / MSFS2024LightTools.GetMetersPerSysUnit()
			
			local vertsCount = arcverts*4*4+8 -- +8 for inner angle
			displayVerts.count = vertsCount
			if (this.ShapeType <= 2) then
			(
				r += sr
				for i = 1 to arcsegs+1 do
				(
					local a = ((float)(i-1)/arcsegs) * this.OuterConeAngle * 0.5
					local x = sin a
					local y = cos a
					
					-- end arcs
					displayVerts[i+0*arcverts] = [ x,0.0,-y] * r
					displayVerts[i+1*arcverts] = [-x,0.0,-y] * r
					displayVerts[i+2*arcverts] = [0.0, x,-y] * r
					displayVerts[i+3*arcverts] = [0.0,-x,-y] * r
					
					-- start arcs
					displayVerts[i+4*arcverts] = [ x,0.0,-y] * sr
					displayVerts[i+5*arcverts] = [-x,0.0,-y] * sr
					displayVerts[i+6*arcverts] = [0.0, x,-y] * sr
					displayVerts[i+7*arcverts] = [0.0,-x,-y] * sr
					
					a = ((float)(i-1)/arcsegs) * 90.0
					local s = sin(this.OuterConeAngle * 0.5)
					x = (sin a) * s
					y = (cos a) * s
					z = cos(this.OuterConeAngle * 0.5)
					
					-- end circle
					displayVerts[i+8*arcverts] = [ x, y,-z] * r
					displayVerts[i+9*arcverts] = [ x,-y,-z] * r
					displayVerts[i+10*arcverts] = [-x, y,-z] * r
					displayVerts[i+11*arcverts] = [-x,-y,-z] * r
					
					-- start circle
					displayVerts[i+12*arcverts] = [ x, y,-z] * sr
					displayVerts[i+13*arcverts] = [ x,-y,-z] * sr
					displayVerts[i+14*arcverts] = [-x, y,-z] * sr
					displayVerts[i+15*arcverts] = [-x,-y,-z] * sr
				)
				-- inner angle verts
				(
					local a = this.InnerConeAngle * 0.5
					local x = sin a
					local y = cos a
					
					displayVerts[arcverts*4*4+1] = [ x,0.0,-y] * r
					displayVerts[arcverts*4*4+2] = [-x,0.0,-y] * r
					displayVerts[arcverts*4*4+3] = [0.0, x,-y] * r
					displayVerts[arcverts*4*4+4] = [0.0,-x,-y] * r
					
					displayVerts[arcverts*4*4+5] = [ x,0.0,-y] * sr
					displayVerts[arcverts*4*4+6] = [-x,0.0,-y] * sr
					displayVerts[arcverts*4*4+7] = [0.0, x,-y] * sr
					displayVerts[arcverts*4*4+8] = [0.0,-x,-y] * sr
				)
			)
			else if (this.ShapeType == 3) then
			(
				local offset = 1.0 / tan(this.OuterConeAngle * 0.5)
				r += sr + sr * offset
				for i = 1 to arcsegs+1 do
				(
					local a, x, y
					
					-- end arcs
					a = ((float)(i-1)/arcsegs) * this.OuterConeAngle * 0.5
					x = sin a
					y = cos a
					
					displayVerts[i+0*arcverts] = [ x,0.0,-y] * r
					displayVerts[i+1*arcverts] = [-x,0.0,-y] * r
					displayVerts[i+2*arcverts] = [0.0, x,-y] * r
					displayVerts[i+3*arcverts] = [0.0,-x,-y] * r
					
					-- start arcs
					a = (float)(i-1)/arcsegs
					x = a
					
					displayVerts[i+4*arcverts] = [ x,0.0,-offset] * sr
					displayVerts[i+5*arcverts] = [-x,0.0,-offset] * sr
					displayVerts[i+6*arcverts] = [0.0, x,-offset] * sr
					displayVerts[i+7*arcverts] = [0.0,-x,-offset] * sr
					
					-- end circle
					a = ((float)(i-1)/arcsegs) * 90.0
					local s = sin(this.OuterConeAngle * 0.5)
					x = (sin a) * s
					y = (cos a) * s
					local z = cos(this.OuterConeAngle * 0.5)
					
					displayVerts[i+8*arcverts] = [ x, y,-z] * r
					displayVerts[i+9*arcverts] = [ x,-y,-z] * r
					displayVerts[i+10*arcverts] = [-x, y,-z] * r
					displayVerts[i+11*arcverts] = [-x,-y,-z] * r
					
					-- start circle
					a = ((float)(i-1)/arcsegs) * 90.0
					x = sin a
					y = cos a
					
					displayVerts[i+12*arcverts] = [ x, y,-offset] * sr
					displayVerts[i+13*arcverts] = [ x,-y,-offset] * sr
					displayVerts[i+14*arcverts] = [-x, y,-offset] * sr
					displayVerts[i+15*arcverts] = [-x,-y,-offset] * sr
					
				)
				-- inner angle verts
				(
					local a = this.InnerConeAngle * 0.5
					local x = sin a
					local y = cos a
					
					displayVerts[arcverts*4*4+1] = [ x,0.0,-y] * r
					displayVerts[arcverts*4*4+2] = [-x,0.0,-y] * r
					displayVerts[arcverts*4*4+3] = [0.0, x,-y] * r
					displayVerts[arcverts*4*4+4] = [0.0,-x,-y] * r
					
					local a = this.InnerConeAngle * 0.5
					local x = (tan a) * offset
					
					displayVerts[arcverts*4*4+5] = [ x,0.0,-offset] * sr
					displayVerts[arcverts*4*4+6] = [-x,0.0,-offset] * sr
					displayVerts[arcverts*4*4+7] = [0.0, x,-offset] * sr
					displayVerts[arcverts*4*4+8] = [0.0,-x,-offset] * sr
				)
				
				for i = 1 to vertsCount do
					displayVerts[i].z += offset * sr
			)
			
			local facesCount = arcsegs*4*4+4+4
			if (displayMesh.numfaces != facesCount) then
			(
				local displayFaces = #([0,0,0])
				displayFaces.count = facesCount
				for i = 1 to arcsegs do
				(
					for j = 0 to 15 do
						displayFaces[i+j*arcsegs] = [i,i,i+1]+j*arcverts
				)
				for i = 1 to 4 do
				(
					displayFaces[i+arcsegs*4*4] = [arcverts * i, arcverts * i, arcverts * i + arcverts * 4]
				)
				for i = 1 to 4 do
				(
					displayFaces[i+arcsegs*4*4+4] = [arcverts*4*4+i, arcverts*4*4+i, arcverts*4*4+4+i]
				)
				setMesh displayMesh vertices:displayVerts faces:displayFaces
			)
			else
				setMesh displayMesh vertices:displayVerts
			
			displayDirty = false
		)
		displayMesh
	)
	
	rollout params "Parameters"
	(
		group "Color"
		(
			radiobuttons ColorMode_UI "" labels:#("Kelvin","RGB") align:#left columns:1 offsets:#([0,0], [0,8]) 
			spinner Kelvin_UI "" range:[1000, 10000, 3600.0] type:#Float align:#right scale:100 fieldWidth:55 offset:[0,-43]
			colorpicker Color_UI "" modal:false align:#right fieldWidth:65
		)
	    
		group "Power"
		(
			radiobuttons UnitMode_UI "" labels:#("Intensity (cd)","Flux (lm)") align:#left columns:1 offsets:#([0,0], [0,6]) 
			spinner Intensity_UI "" range:[0.0, 1000000.0, 1.0] type:#Float align:#right fieldWidth:55 offset:[0,-41] tooltip:"Intensity in Candelas (lm/sr)"
			spinner Flux_UI "" range:[0.0, 100000.0, 1.0] type:#Float align:#right fieldWidth:55 tooltip:"Power in Lumens (lm)"
		)
		
		group "Shape"
		(
			dropdownlist ShapeType_UI "" items:#("Point","Sphere","Disc") -- "Rectangle","IES profile"
			spinner SourceRadius_UI "Source Radius (cm)" range:[1.0, 1000.0, 10.0] type:#Float align:#right fieldwidth:40
			spinner InnerConeAngle_UI "Inner Angle" range:[0.0, 360.0, 45.0] type:#Float align:#right fieldwidth:40
			spinner OuterConeAngle_UI "Outer Angle" range:[1.0, 360.0, 90.0] type:#Float align:#right fieldwidth:40
		)
		
		group "Channels"
		(
			checkbox  ChannelExterior_UI "Exterior:"
			checkbox  ChannelInterior_UI "Interior:"
		)
		
		on ColorMode_UI changed val do 
		(
			Kelvin_UI.enabled = (val == 1)
			Color_UI.enabled = (val == 2)
		)
		
		on UnitMode_UI changed val do 
		(
			Intensity_UI.enabled = (val == 1)
			Flux_UI.enabled = (val == 2)
		)
		
		on ShapeType_UI selected val do 
		(
			SourceRadius_UI.enabled = (val != 1)
			InnerConeAngle_UI.range.y = if (val == 3) then 180.0 else 360.0
			OuterConeAngle_UI.range.y = if (val == 3) then 180.0 else 360.0
		)
		
		on params open do
		(
			Kelvin_UI.enabled = (ColorMode == 1)
			Color_UI.enabled = (ColorMode == 2)
			Intensity_UI.enabled = (UnitMode == 1)
			Flux_UI.enabled = (UnitMode == 2)
			SourceRadius_UI.enabled = (ShapeType != 1)
			InnerConeAngle_UI.range.y = if (ShapeType == 3) then 180.0 else 360.0
			OuterConeAngle_UI.range.y = if (ShapeType == 3) then 180.0 else 360.0
		)
	)
)

plugin Light MSFS2024SkyPortal
name:"Sky Portal"
classID:#(0x3e4d58ee, 0x370452e4)
extends:Free_Light
category:"MSFS2024"
replaceUI:true
autoPromoteDelegateProps:false
version:0
(
	local displayMesh = TriMesh()
	local displayVerts = #([0.0,0.0,0.0])
	local displayDirty = true
	
	fn SetDelegateDistributionShape =
	(
		if (this.ShapeType == 1) then -- disc
		(
			delegate.distribution = 1 -- spot
			delegate.type = #Free_Disc
		)
		else if (this.ShapeType == 2) then -- rect
		(
			delegate.distribution = 1 -- spot
			delegate.type = #Free_Rectangle
		)
	)
	
    parameters main rollout:params
	(
		-- shape : disc / (rectangle)
		ShapeType type:#integer animatable:false default:1 ui:ShapeType_UI
		SourceRadius type:#float animatable:false default:50.0 ui:SourceRadius_UI
	    InnerConeAngle type:#float animatable:false default:160.0 ui:InnerConeAngle_UI
	    OuterConeAngle type:#float animatable:false default:180.0 ui:OuterConeAngle_UI
		
        on ShapeType set val do
        (
			SetDelegateDistributionShape()
			displayDirty = true
		)
		
		on SourceRadius set val do
		(
			v = (val / 100.0) / MSFS2024LightTools.GetMetersPerSysUnit()
			delegate.light_Radius = v
			SetDelegateDistributionShape()
			displayDirty = true
		)
		
        on InnerConeAngle set val do
        (
			delegate.hotspot = val
			if (OuterConeAngle < val) do delegate.falloff = OuterConeAngle = val
			displayDirty = true
		)
		
        on OuterConeAngle set val do
        (
			delegate.falloff = val
			if (InnerConeAngle > val) do delegate.hotspot = InnerConeAngle = val
			displayDirty = true
		)
	)
	
	on create do
	(
		
	)
	
	on update do
	(
		
	)
	
	on getDisplayMesh do
	(
		if (displayDirty == true) do
		(
			local arcsegs = 8
			local arcverts = arcsegs+1
			local sr = (this.SourceRadius/100.0) / MSFS2024LightTools.GetMetersPerSysUnit()
			local r = (this.SourceRadius/100.0)*3.0 / MSFS2024LightTools.GetMetersPerSysUnit()
			
			local vertsCount = arcverts*4*4+8 -- +8 for inner angle
			displayVerts.count = vertsCount
			if (this.ShapeType == 1) then
			(
				local offset = 1.0 / tan(this.OuterConeAngle * 0.5)
				r += sr + sr * offset
				for i = 1 to arcsegs+1 do
				(
					local a, x, y
					
					-- end arcs
					a = ((float)(i-1)/arcsegs) * this.OuterConeAngle * 0.5
					x = sin a
					y = cos a
					
					displayVerts[i+0*arcverts] = [ x,0.0,-y] * r
					displayVerts[i+1*arcverts] = [-x,0.0,-y] * r
					displayVerts[i+2*arcverts] = [0.0, x,-y] * r
					displayVerts[i+3*arcverts] = [0.0,-x,-y] * r
					
					-- start arcs
					a = (float)(i-1)/arcsegs
					x = a
					
					displayVerts[i+4*arcverts] = [ x,0.0,-offset] * sr
					displayVerts[i+5*arcverts] = [-x,0.0,-offset] * sr
					displayVerts[i+6*arcverts] = [0.0, x,-offset] * sr
					displayVerts[i+7*arcverts] = [0.0,-x,-offset] * sr
					
					-- end circle
					a = ((float)(i-1)/arcsegs) * 90.0
					local s = sin(this.OuterConeAngle * 0.5)
					x = (sin a) * s
					y = (cos a) * s
					local z = cos(this.OuterConeAngle * 0.5)
					
					displayVerts[i+8*arcverts] = [ x, y,-z] * r
					displayVerts[i+9*arcverts] = [ x,-y,-z] * r
					displayVerts[i+10*arcverts] = [-x, y,-z] * r
					displayVerts[i+11*arcverts] = [-x,-y,-z] * r
					
					-- start circle
					a = ((float)(i-1)/arcsegs) * 90.0
					x = sin a
					y = cos a
					
					displayVerts[i+12*arcverts] = [ x, y,-offset] * sr
					displayVerts[i+13*arcverts] = [ x,-y,-offset] * sr
					displayVerts[i+14*arcverts] = [-x, y,-offset] * sr
					displayVerts[i+15*arcverts] = [-x,-y,-offset] * sr
					
				)
				-- inner angle verts
				(
					local a = this.InnerConeAngle * 0.5
					local x = sin a
					local y = cos a
					
					displayVerts[arcverts*4*4+1] = [ x,0.0,-y] * r
					displayVerts[arcverts*4*4+2] = [-x,0.0,-y] * r
					displayVerts[arcverts*4*4+3] = [0.0, x,-y] * r
					displayVerts[arcverts*4*4+4] = [0.0,-x,-y] * r
					
					local a = this.InnerConeAngle * 0.5
					local x = (tan a) * offset
					
					displayVerts[arcverts*4*4+5] = [ x,0.0,-offset] * sr
					displayVerts[arcverts*4*4+6] = [-x,0.0,-offset] * sr
					displayVerts[arcverts*4*4+7] = [0.0, x,-offset] * sr
					displayVerts[arcverts*4*4+8] = [0.0,-x,-offset] * sr
				)
				
				for i = 1 to vertsCount do
					displayVerts[i].z += offset * sr
			)
			
			local facesCount = arcsegs*4*4+4+4
			if (displayMesh.numfaces != facesCount) then
			(
				local displayFaces = #([0,0,0])
				displayFaces.count = facesCount
				for i = 1 to arcsegs do
				(
					for j = 0 to 15 do
						displayFaces[i+j*arcsegs] = [i,i,i+1]+j*arcverts
				)
				for i = 1 to 4 do
				(
					displayFaces[i+arcsegs*4*4] = [arcverts * i, arcverts * i, arcverts * i + arcverts * 4]
				)
				for i = 1 to 4 do
				(
					displayFaces[i+arcsegs*4*4+4] = [arcverts*4*4+i, arcverts*4*4+i, arcverts*4*4+4+i]
				)
				setMesh displayMesh vertices:displayVerts faces:displayFaces
			)
			else
				setMesh displayMesh vertices:displayVerts
			
			displayDirty = false
		)
		displayMesh
	)
	
	rollout params "Parameters"
	(
		group "Shape"
		(
			dropdownlist ShapeType_UI "" items:#("Disc") -- "Rectangle"
			spinner SourceRadius_UI "Source Radius (cm)" range:[1.0, 1000.0, 50.0] type:#Float align:#right fieldwidth:40
			spinner InnerConeAngle_UI "Inner Angle" range:[0.0, 180.0, 160.0] type:#Float align:#right fieldwidth:40
			spinner OuterConeAngle_UI "Outer Angle" range:[1.0, 180.0, 180.0] type:#Float align:#right fieldwidth:40
		)
		
		on ShapeType_UI selected val do 
		(
			SourceRadius_UI.enabled = (val == 1)
		)
		
		on params open do
		(
			SourceRadius_UI.enabled = (ShapeType == 1)
		)
	)
)