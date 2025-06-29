struct MSFS2024_BlobMeshizeStruct
(
	fn output text =
	(
		format "Warning (Generate blob mesh): %\n" text
	),
	
	-- entries in HLSL shader
	public shaderSlots = struct shaderSlots
	(
		/* PARAMS */
		public float4_baseColorFactor = 			"p_baseColorFactor",
		public float4_SSSColorFactor = 				"p_SSSColorFactor",
		public float_occlusionStrength = 			"p_occlusionStrength",
		public float_roughnessFactor = 				"p_roughnessFactor",
		public float_EmissiveMultiplierFactor = 	"p_EmissiveMultiplierFactor",
		public float_metallicFactor = 				"p_metallicFactor",
		public float4_emissiveFactor = 				"p_emissiveFactor",
		public float_normalScale = 					"p_normalScale",
		public int_alphaMode = 						"p_alphaMode",
		public int_drawOrder = 						"p_drawOrder",
		public float_alphaCutoff = 					"p_alphaCutoff",
		public float_UVOffsetU = 					"p_UVOffsetU",
		public float_UVOffsetV = 					"p_UVOffsetV",
		public float_UVTilingU = 					"p_UVTilingU",
		public float_UVTilingV = 					"p_UVTilingV",
		public float_UVRotation = 					"p_UVRotation",
		public float_wiperAnimState1 = 				"p_wiperAnimState1",
		public float_tireMudAnimState = 			"p_tireMudAnimState",
		public float_tireDustAnimState = 			"p_tireDustAnimState",
		public float_detailUVScale = 				"p_detailUVScale",
		public float_detailUVOffsetX = 				"p_detailUVOffsetX",
		public float_detailUVOffsetY = 				"p_detailUVOffsetY",
		public float_detailNormalScale = 			"p_detailNormalScale",
		public float_blendThreshold = 				"p_blendThreshold",
		public float_glassWidth = 					"p_glassWidth",
		public float_parallaxScale = 				"p_parallaxScale",
		public float_roomSizeXScale = 				"p_roomSizeXScale",
		public float_roomSizeYScale = 				"p_roomSizeYScale",
		public float_roomNumberXY = 				"p_roomNumberXY",
		public float_fresnelFactor = 				"p_fresnelFactor",
		public float_fresnelOpacityOffset = 		"p_fresnelOpacityOffset",
		public float_ghostBiasFactor = 				"p_ghostBiasFactor",
		public float_ghostPowerFactor = 			"p_ghostPowerFactor",
		public float_ghostScaleFactor = 			"p_ghostScaleFactor",
		public float_pearlRange = 					"p_pearlRange",
		public float_pearlShift = 					"p_pearlShift",
		public float_pearlBrightness = 				"p_pearlBrightness",
		public float_iridescentMinThickness = 		"p_iridescentMinThickness",
		public float_iridescentMaxThickness = 		"p_iridescentMaxThickness",
		public float_iridescentBrightness = 		"p_iridescentBrightness",
		public float_sailLightAbsorption = 			"p_sailLightAbsorption",
		public float_sailLightPropagation = 		"p_sailLightPropagation",
		public float_dirtUvScale = 					"p_dirtUvScale",
		public float_dirtAmount = 					"p_dirtAmount",
		public float_dirtBlendSharpness = 			"p_dirtBlendSharpness",
		public bool_baseColorEnabled = 				"p_baseColorEnabled",
		public bool_occRoughMetalEnabled = 			"p_occRoughMetalEnabled",
		public bool_corridorEnabled = 				"p_corridorEnabled",
		public bool_decalFrosted = 					"p_decalFrosted",
		public bool_blendmaskEnabled = 				"p_blendmaskEnabled",
		public bool_foliagemaskEnabled = 			"p_foliagemaskEnabled",
		public bool_detailColorEnabled = 			"p_detailColorEnabled",
		public bool_detailNormalEnabled = 			"p_detailNormalEnabled",
		public bool_detailOccRoughMetalEnabled = 	"p_detailOccRoughMetalEnabled",
		public bool_pearlescentEnabled = 			"p_pearlescentEnabled",
		public bool_iridescentEnabled = 			"p_iridescentEnabled",
		public bool_occlusionEnabled = 				"p_occlusionEnabled",
		public bool_clearcoatColorRoughnessEnabled = "p_clearcoatColorRoughnessEnabled",
		public bool_clearcoatNormalEnabled = 		"p_clearcoatNormalEnabled",
		public bool_windshieldInsectsEnabled = 		"p_windshieldInsectsEnabled",
		public bool_windshieldInsectsMaskEnabled = 	"p_windshieldInsectsMaskEnabled",
		public bool_tireDetailsEnabled = 			"p_tireDetailsEnabled",
		public bool_tireMudNormalEnabled = 			"p_tireMudNormalEnabled",
		public bool_tireWear1Enabled = 				"p_tireWear1Enabled",
		public bool_tireWear2Enabled = 				"p_tireWear2Enabled",
		public bool_tireWear3Enabled = 				"p_tireWear3Enabled",
		public bool_tireWear4Enabled = 				"p_tireWear4Enabled",
		public bool_dirtEnabled = 					"p_dirtEnabled",
		public float3_lightDir = 					"p_lightDir",
		
		/* TEXTURES (all float4) */
		public tex2D_baseColorTex = 						"p_baseColorTex",
		public tex2D_occlusionRoughnessMetallicTex = 		"p_occlusionRoughnessMetallicTex",
		public tex2D_normalTex = 							"p_normalTex",
		public tex2D_blendMaskTex = 						"p_blendMaskTex",
		public tex2D_foliageMaskTex = 						"p_foliageMaskTex",
		public tex2D_wetnessAOTex = 						"p_wetnessAOTex",
		public tex2D_windshieldDetailNormalTex = 			"p_windshieldDetailNormalTex",
		public tex2D_scratchesNormalTex = 					"p_scratchesNormalTex",
		public tex2D_wiperMaskTex = 						"p_wiperMaskTex",
		public tex2D_windshieldInsectsTex = 				"p_windshieldInsectsTex",
		public tex2D_windshieldInsectsMaskTex = 			"p_windshieldInsectsMaskTex",
		public tex2D_iridescentThicknessTex = 				"p_iridescentThicknessTex",
		public tex2D_anisoDirectionRoughnessTex = 			"p_anisoDirectionRoughnessTex",
		public tex2D_dirtTex = 								"p_dirtTex",
		public tex2D_dirtOccRoughMetalTex = 				"p_dirtOccRoughMetalTex",
		public tex2D_opacityTex = 							"p_opacityTex",
		public tex2D_emissiveTex = 							"p_emissiveTex",
		public tex2D_detailColorTex = 						"p_detailColorTex",
		public tex2D_detailOcclusionRoughnessMetallicTex = 	"p_detailOcclusionRoughnessMetallicTex",
		public tex2D_detailNormalTex = 						"p_detailNormalTex",
		public texCube_irradianceTex = 						"p_irradianceTex",
		public texCube_radianceTex = 						"p_radianceTex",
		public tex2D_specularBRDF_LUT = 					"p_specularBRDF_LUT",
		public tex2D_occlusionTex = 						"p_occlusionTex",
		public tex2D_clearcoatColorRoughnessTex = 			"p_clearcoatColorRoughnessTex",
		public tex2D_clearcoatNormalTex = 					"p_clearcoatNormalTex",
		public tex2D_tireDetailsTex = 						"p_tireDetailsTex",
		public tex2D_tireMudNormalTex = 					"p_tireMudNormalTex",
		public tex2D_tireWear1Tex = 						"p_tireWear1Tex",
		public tex2D_tireWear2Tex = 						"p_tireWear2Tex",
		public tex2D_tireWear3Tex = 						"p_tireWear3Tex",
		public tex2D_tireWear4Tex = 						"p_tireWear4Tex"
		
-- 		public texStandardMatDebug_diffuse =				"Diffuse" -- DEBUG using standard mat
	);,

	fn getMaterialTexFromShaderSlot &shaderSlots &shaderSlot =
	(
		case shaderSlot of
		(
			(shaderSlots.tex2D_baseColorTex):							"BaseColorTex"
			(shaderSlots.tex2D_occlusionRoughnessMetallicTex):			"OcclusionRoughnessMetallicTex"
			(shaderSlots.tex2D_normalTex):								"NormalTex"
			(shaderSlots.tex2D_wetnessAOTex):							"WetnessAOTex"
			(shaderSlots.tex2D_windshieldDetailNormalTex):				"WindshieldDetailNormalTex"
			(shaderSlots.tex2D_anisoDirectionRoughnessTex):				"AnisoDirectionRoughnessTex"
			(shaderSlots.tex2D_opacityTex):								"OpacityTex"
			(shaderSlots.tex2D_dirtTex):								"DirtTex"
			(shaderSlots.tex2D_dirtOccRoughMetalTex):					"DirtOcclusionRoughnessMetallicTex"
			(shaderSlots.tex2D_emissiveTex):							"EmissiveTex"
			(shaderSlots.tex2D_detailColorTex):							"DetailColorTex"
			(shaderSlots.tex2D_detailOcclusionRoughnessMetallicTex):	"DetailOcclusionRoughnessMetallicTex"
			(shaderSlots.tex2D_detailNormalTex):						"DetailNormalTex"
			(shaderSlots.tex2D_blendMaskTex):							"BlendMaskTex"
			(shaderSlots.tex2D_foliageMaskTex):							"FoliageMaskTex"
			(shaderSlots.tex2D_occlusionTex):							"OcclusionTex"
			(shaderSlots.tex2D_clearcoatColorRoughnessTex):				"ClearcoatColorRoughnessTex"
			(shaderSlots.tex2D_clearcoatNormalTex):						"ClearcoatNormalTex"
			(shaderSlots.tex2D_scratchesNormalTex):						"ScratchesNormalTex"
			(shaderSlots.tex2D_wiperMaskTex):							"WiperMaskTex"
			(shaderSlots.tex2D_iridescentThicknessTex):					"IridescentThicknessTex"
			(shaderSlots.tex2D_windshieldInsectsTex):					"WindshieldInsectsTex"
			(shaderSlots.tex2D_windshieldInsectsMaskTex):				"WindshieldInsectsMaskTex"
			(shaderSlots.tex2D_tireDetailsTex):							"TireDetailsTex"
			(shaderSlots.tex2D_tireMudNormalTex):						"TireMudNormalTex"
-- 			(shaderSlots.texStandardMatDebug_diffuse):					"diffuseMap" -- DEBUG using standard mat
			default:
			(
				MSFS2024_BlobMeshizeStruct.output ("Unsupported shader slot: " + shaderSlot)
				undefined
			)
		)
	),
	
	fn getShaderSlotFromTexName &shaderSlots &texName =
	(
		case texName of
		(
			"BaseColorTex":							shaderSlots.tex2D_baseColorTex
			"OcclusionRoughnessMetallicTex":		shaderSlots.tex2D_occlusionRoughnessMetallicTex
			"NormalTex":							shaderSlots.tex2D_normalTex
			"WetnessAOTex":							shaderSlots.tex2D_wetnessAOTex
			"WindshieldDetailNormalTex":			shaderSlots.tex2D_windshieldDetailNormalTex
			"AnisoDirectionRoughnessTex":			shaderSlots.tex2D_anisoDirectionRoughnessTex
			"OpacityTex":							shaderSlots.tex2D_opacityTex
			"DirtTex":								shaderSlots.tex2D_dirtTex
			"DirtOcclusionRoughnessMetallicTex":	shaderSlots.tex2D_dirtOccRoughMetalTex
			"EmissiveTex":							shaderSlots.tex2D_emissiveTex
			"DetailColorTex":						shaderSlots.tex2D_detailColorTex
			"DetailOcclusionRoughnessMetallicTex":	shaderSlots.tex2D_detailOcclusionRoughnessMetallicTex
			"DetailNormalTex":						shaderSlots.tex2D_detailNormalTex
			"BlendMaskTex":							shaderSlots.tex2D_blendMaskTex
			"FoliageMaskTex":						shaderSlots.tex2D_foliageMaskTex
			"OcclusionTex":							shaderSlots.tex2D_occlusionTex
			"ClearcoatColorRoughnessTex":			shaderSlots.tex2D_clearcoatColorRoughnessTex
			"ClearcoatNormalTex":					shaderSlots.tex2D_clearcoatNormalTex
			"ScratchesNormalTex":					shaderSlots.tex2D_scratchesNormalTex
			"WiperMaskTex":							shaderSlots.tex2D_wiperMaskTex
			"IridescentThicknessTex":				shaderSlots.tex2D_iridescentThicknessTex
			"WindshieldInsectsTex":					shaderSlots.tex2D_windshieldInsectsTex
			"WindshieldInsectsMaskTex":				shaderSlots.tex2D_windshieldInsectsMaskTex
			"TireDetailsTex":						shaderSlots.tex2D_tireDetailsTex
			"TireMudNormalTex":						shaderSlots.tex2D_tireMudNormalTex
			default:
			(
				MSFS2024_BlobMeshizeStruct.output ("Unsupported texture name: " + texName)
				undefined
			)
		)
	),
	
	fn getMaterialTexPathFromShaderSlot mat &shaderSlots &matUsedSlots &tempTexturePaths &shaderSlot =
	(
		local texMatName = MSFS2024_BlobMeshizeStruct.getMaterialTexFromShaderSlot &shaderSlots &shaderSlot
		if texMatName != undefined then
		(
			local texPath = copy (getProperty mat texMatName)
-- 			texPath = texPath.fileName -- DEBUG using standard mat
-- 			format "material %:\ttexPath: %\n" mat.name texPath
			if texPath != "" then
			(
				append matUsedSlots shaderSlot
				if pathConfig.isAbsolutePath texPath then
				(
					texPath
				)
				else
				(
					-- TEMP: should not alter scene mats...
					local tempTexturePath = #(texMatName, texPath) -- using key - value array
					append tempTexturePaths tempTexturePath
					setProperty mat texMatName (pathConfig.convertPathToAbsolute texPath)
					
					pathConfig.convertPathToAbsolute texPath
				)
			)
			else undefined
		)
		else undefined
	),
	
	fn setMaterialTexPathFromShaderSlot mat &shaderSlots &shaderSlot &texPath =
	(
		local texMatName = MSFS2024_BlobMeshizeStruct.getMaterialTexFromShaderSlot &shaderSlots &shaderSlot
		if texMatName != undefined then
		(
			local relativeTexPath = copy texPath
			relativeTexPath = pathConfig.convertPathToRelativeTo relativeTexPath (pathConfig.getCurrentProjectFolder())
			relativeTexPath = pathConfig.normalizePath relativeTexPath
			
			-- check if we are effectively inside of project path
			-- else, keep absolute path
			local correctTexPath
			local folders = filterString relativeTexPath "\\"
			if folders[1] != ".." then correctTexPath = relativeTexPath
			else correctTexPath = texPath
			
			setProperty mat texMatName correctTexPath
		)
	),
	
	fn chooseSavePath =
	(
		local f = getSavePath caption:"Choose textures output folder" initialDir:maxFilePath
		f
	),
	
	fn isFSMaterial mat =
	(
		classOf mat == MSFS2024_Material
-- 		classOf mat == Standardmaterial -- DEBUG using standard mat
	),

	fn getFSMaterials =
	(
		local fsMats = #()
		for obj in selection do
		(
			local mat = obj.material
			if MSFS2024_BlobMeshizeStruct.isFSMaterial mat then
			(
				appendIfUnique fsMats mat
			)
			else if classOf mat == Multimaterial then
			(
				local subMatCount = getNumSubMtls mat
				for i = 1  to subMatCount do
				(
					local subMat = getSubMtl mat i
					if MSFS2024_BlobMeshizeStruct.isFSMaterial subMat then
					(
						appendIfUnique fsMats subMat
					)
				)
			)
		)
		fsMats
	),
	
	fn setPipelineSetting pipeline setting value =
	(
		local bSuccess = sgsdk_SetSetting pipeline setting value
		if not bSuccess then
		(
			MSFS2024_BlobMeshizeStruct.output ("Failed to set setting: " + setting)
		)
		bSuccess
	),
	
	/*
	* Setup casters
	*
	* outputPixelFormat: #RGBA8 #RGB8 #R8 #RGBA16 #RGB16 #R16 #RGBA32F
	*/
	fn setMaterialCaster pipeline caster &shaderSlots &shaderSlot &matUsedSlots &casterId outputTextureFormat tangentSpaceNormals: outputPixelFormat:#RGB16 =
	(
		local bSuccess = true
		if (findItem matUsedSlots shaderSlot) != 0 then -- dont add caster if material slot has no texture
		(
			try
			(
				sgsdk_AddMaterialCaster pipeline caster
			)
			catch
			(
				MSFS2024_BlobMeshizeStruct.output ("Failed to set material caster: " + caster)
				bSuccess = false
			)
			
			if bSuccess then
			(
				local casterBaseString = "MaterialCaster/" + casterId as string + "/" + caster -- TODO here: how to assign caster base property ?
				local casterSettingBaseString = casterBaseString + "Settings/"
				
				-- Add proper material channel to cast
				local materialChannelSetting = casterSettingBaseString + "MaterialChannel"
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline materialChannelSetting shaderSlot
				
				-- Bleed and Fill
				local dilationSetting = casterSettingBaseString + "Dilation"
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline dilationSetting 10 -- default 10
				local fillModeSetting = casterSettingBaseString + "FillMode"
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline fillModeSetting 1 -- 0:no dithering, 1:Floyd-Steinberg, 2:Jarvis Judice Ninke, 3:Sierra-3 (three row)
				
				-- Dithering
				local ditherTypeSetting = casterSettingBaseString + "DitherType"
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline ditherTypeSetting true
				
				-- Output channels
-- 				local outChannelNb = case outputPixelFormat of
-- 				(
-- 					#RGBA8:		4
-- 					#RGB8:		3
-- 					#R8:		1
-- 					#RGBA16:	4
-- 					#RGB16:		3
-- 					#R16:		1
-- 					#RGBA32F:	4
-- 					default:
-- 					(
-- 						MSFS2024_BlobMeshizeStruct.output ("Unsupported output pixel format: " + outputPixelFormat)
-- 						3
-- 					)
-- 				)
-- 				local outputChannelsSetting = casterSettingBaseString + "OutputChannels"
-- 				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputChannelsSetting outChannelNb
				
				-- Bit depth
-- 				local bitDepth = case outputPixelFormat of
-- 				(
-- 					#RGBA8:		8
-- 					#RGB8:		8
-- 					#R8:		8
-- 					#RGBA16:	16
-- 					#RGB16:		16
-- 					#R16:		16
-- 					#RGBA32F:	32
-- 					default:
-- 					(
-- 						MSFS2024_BlobMeshizeStruct.output ("Unsupported output pixel format: " + outputPixelFormat)
-- 						8
-- 					)
-- 				)
-- 				local outputChannelBitDepthSetting = casterSettingBaseString + "OutputChannelBitDepth"
-- 				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputChannelBitDepthSetting bitDepth
				
				-- Set texture format
				local outputImageFileFormatSetting = casterSettingBaseString + "OutputImageFileFormat"
				case outputTextureFormat of
				(
					#BMP:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 0
					#DDS:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 1
					#JPEG:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 2
					#PNG:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 3
					#TGA:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 4
					#TIFF:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 5
					#EXR:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputImageFileFormatSetting 8
					default:	MSFS2024_BlobMeshizeStruct.output ("Unsupported output texture file format: " + outputTextureFormat)
				)
				
				-- Set pixel format
				local outputPixelFormatSetting = casterSettingBaseString + "OutputPixelFormat"
				case outputPixelFormat of
				(
					#RGBA8:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 0
					#RGB8:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 1
					#R8:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 2
					#RGBA16:	MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 3
					#RGB16:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 4
					#R16:		MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 5
					#RGBA32F:	MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline outputPixelFormatSetting 6
					default:	MSFS2024_BlobMeshizeStruct.output ("Unsupported output pixel format: " + outputPixelFormat)
				)
				
				-- Specific options
				case caster of
				(
					"ColorCaster":
					(
						-- Just in case...
						local skipCastingIfNoInputChannelSetting = casterSettingBaseString + "SkipCastingIfNoInputChannel"
						MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline skipCastingIfNoInputChannelSetting true
						
						-- Total baked layers opacity
						local bakeOpacityInAlphaSetting = casterSettingBaseString + "BakeOpacityInAlpha"
						MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline bakeOpacityInAlphaSetting true
					)
					"NormalCaster":
					(
						if tangentSpaceNormals != unsupplied and tangentSpaceNormals then
						(
							-- set the correct tangent space type
							local tangentSpaceSetting = casterSettingBaseString + "GenerateTangentSpaceNormals"
							MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline tangentSpaceSetting true
						)
					)
				)
				local setSRGB = case shaderSlot of
				(
					(shaderSlots.tex2D_baseColorTex):	true
					(shaderSlots.tex2D_emissiveTex):	true
					default:							false
				)
				if setSRGB then
				(
					-- adjust sRGB output
					local sRGBSetting = casterSettingBaseString + "OutputSRGB"
					MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline sRGBSetting true
				)
				
				casterId += 1
			)
		)
		bSuccess
	),
	
	fn setupShadingNetworkMaterialTex mat shadingNetworkMaterial &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlot sRGB:false =
	(
		if (findItem disableShaderSlots shaderSlot) == 0 then -- discard if slot casting is disabled
		(
			local texPath = MSFS2024_BlobMeshizeStruct.getMaterialTexPathFromShaderSlot mat &shaderSlots &matUsedSlots &tempTexturePaths &shaderSlot -- For now, used to alter paths from relative to absolute
			if texPath != "" and texPath != undefined then
			(
	-- 			sgsdk_MaterialTexture mat.name shaderSlot texPath sRGB -- Didnt work
			)
			case shaderSlot of
			(
				(shaderSlots.tex2D_occlusionTex):
				(
					sgsdk_MaterialTextureMapChannel mat.name shaderSlot 2 -- UV2
				)
			)
			
			local tex = sgsdk_CreateShadingTextureNode shaderSlot
			sgsdk_ConnectNodeToChannel tex shadingNetworkMaterial shaderSlot
			sgsdk_SetSRGB tex sRGB
		)
	),
	
	fn setupMaterials &shaderSlots &matUsedSlots &disableShaderSlots &tempMatTexturePaths type:#Hair =
	(
		local mats = MSFS2024_BlobMeshizeStruct.getFSMaterials()
		for mat in mats do
		(
			local matName = mat.name
-- 			format "Setting up shading network for: %\n" matName

			-- material
			local shadingNetworkMat
			try
			(
				shadingNetworkMat = sgsdk_CreateMaterialMetadata matName
			)
			catch
			(
				MSFS2024_BlobMeshizeStruct.output ("Failed to create shading network for material: " + matName + "\n\tIn case unexpected results: relaunch 3dsmax.")
			)
			
			if shadingNetworkMat != undefined then
			(
				local tempTexturePaths = #()
				
-- 				MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat shaderSlots shaderSlots.texStandardMatDebug_diffuse sRGB:true -- DEBUG using standard material
				
				-- get material type
				local matType = mat.matList[mat.materialType]
				case matType of
				(
					#Hair:
					(
						MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlots.tex2D_baseColorTex sRGB:true
						MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlots.tex2D_occlusionRoughnessMetallicTex
						MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlots.tex2D_normalTex
						MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlots.tex2D_emissiveTex sRGB:true
						MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlots.tex2D_occlusionTex
						MSFS2024_BlobMeshizeStruct.setupShadingNetworkMaterialTex mat shadingNetworkMat &shaderSlots &matUsedSlots &disableShaderSlots &tempTexturePaths &shaderSlots.tex2D_anisoDirectionRoughnessTex
					)
					default:
					(
						MSFS2024_BlobMeshizeStruct.output ("Unsupported material type for shading network: " + matType)
					)
				)
				
				local matTexturePaths = #(mat, tempTexturePaths) -- using key, value array
				append tempMatTexturePaths matTexturePaths
			)
		)
	),
	
	fn resetRelativeTexturePaths &tempMatTexturePaths =
	(
		for matEntry in tempMatTexturePaths do
		(
			local mat = matEntry[1]
			local texPaths = matEntry[2]
			for texPathEntry in texPaths do
			(
				local texMatName = texPathEntry[1]
				local texPath = texPathEntry[2]
				setProperty mat texMatName texPath
			)
		)
		free tempMatTexturePaths
	),
	
	fn cleanupOnExit =
	(
		sgsdk_ClearPipelines()
	),
	
	/*
	* MAIN FUNCTION
	*
	* outputTextureFormat : #BMP #DDS #JPEG #PNG #TGA #TIFF #EXR
	* disableShaderSlots must be an array of strings matching shaderSlots's texture names
	*/
	fn createBlobMesh obj onScreenPixelSize:70 bakeMaterialFrom: bakeMaterialTo: outputTextureSize:[512, 512] outputTextureFormat:#PNG disableShaderSlots:#() =
	(
		if obj != undefined and superClassOf obj == GeometryClass then
		(
			-- params
			local bakeMaterialFrom, texOutputDir, bakingMaterialName
			local bakeMaterial = bakeMaterialFrom != unsupplied and bakeMaterialFrom != undefined
			if bakeMaterial then
			(
				if bakeMaterialTo == unsupplied or bakeMaterialTo == undefined then bakeMaterialTo = bakeMaterialFrom
				
				local texOutputDir = MSFS2024_BlobMeshizeStruct.chooseSavePath()
				if texOutputDir == undefined then
				(
					return()
					texOutputDir = ".\\"
				)
				
				local bakingMaterialName = "bakingMaterial"
			)
			
			-- clear sg in case something went wrong last time
			sgsdk_Reset()
			--sgsdk_ClearPipelines()
			--sgsdk_ClearGlobalMapping()
			
			select obj
			local tempMatTexturePaths = #() -- Used to restore relative texture paths for simplygon process to work.
			
			local pipeline = sgsdk_CreatePipeline "RemeshingPipeline"
			
			MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "GlobalSettings/DefaultTangentCalculatorType" 1
			MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/RemeshingSettings/OnScreenSize" onScreenPixelSize
			
			local shaderSlots
			if bakeMaterial then
			(
				local bmStruct = MSFS2024_BlobMeshizeStruct()
				shaderSlots = bmStruct.shaderSlots()
				
				sgsdk_UseShadingNetwork true
				local matUsedSlots = #()
				MSFS2024_BlobMeshizeStruct.setupMaterials &shaderSlots &matUsedSlots &disableShaderSlots &tempMatTexturePaths type:bakeMaterialFrom
				sgsdk_SetTextureOutputDirectory texOutputDir
				--sgsdk_SetGenerateMaterial true
				
				-- enable material baking
				-- mapping image is required for material baking
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/MappingImageSettings/GenerateMappingImage" true
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/MappingImageSettings/GenerateTangents" true

				-- in this case we want to generate texture coordinates (UVs)
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/MappingImageSettings/GenerateTexCoords" true

				-- the name of the resulting texture coordinate field
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/MappingImageSettings/TexCoordName" bakingMaterialName
				
				-- width/height of the baked textures
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/MappingImageSettings/Output0/TextureWidth" outputTextureSize.x
				MSFS2024_BlobMeshizeStruct.setPipelineSetting pipeline "RemeshingProcessor/MappingImageSettings/Output0/TextureHeight" outputTextureSize.y
				
				-- add material casters
				local casterId = 0
				case bakeMaterialFrom of
				(
					#Hair:
					(
						-- Here we remove alpha from albedo by letting default output setting to RGB only
						MSFS2024_BlobMeshizeStruct.setMaterialCaster pipeline "ColorCaster"	&shaderSlots &shaderSlots.tex2D_baseColorTex					&matUsedSlots &casterId outputTextureFormat
						MSFS2024_BlobMeshizeStruct.setMaterialCaster pipeline "ColorCaster"	&shaderSlots &shaderSlots.tex2D_occlusionRoughnessMetallicTex	&matUsedSlots &casterId outputTextureFormat
						MSFS2024_BlobMeshizeStruct.setMaterialCaster pipeline "NormalCaster"	&shaderSlots &shaderSlots.tex2D_normalTex						&matUsedSlots &casterId outputTextureFormat tangentSpaceNormals:true
						MSFS2024_BlobMeshizeStruct.setMaterialCaster pipeline "ColorCaster"	&shaderSlots &shaderSlots.tex2D_emissiveTex						&matUsedSlots &casterId outputTextureFormat
						MSFS2024_BlobMeshizeStruct.setMaterialCaster pipeline "ColorCaster"	&shaderSlots &shaderSlots.tex2D_occlusionTex					&matUsedSlots &casterId outputTextureFormat
						MSFS2024_BlobMeshizeStruct.setMaterialCaster pipeline "ColorCaster"	&shaderSlots &shaderSlots.tex2D_anisoDirectionRoughnessTex		&matUsedSlots &casterId outputTextureFormat
					)
					default:
					(
						MSFS2024_BlobMeshizeStruct.output ("Unsupported casting type: " + bakeMaterialFrom)
					)
				)
			)
			
			-- Run process
			local success = true
			try
			(
				local bSimplygonResult = sgsdk_RunPipelineOnSelection pipeline
			)
			catch
			(
				MSFS2024_BlobMeshizeStruct.output "Simplygon processing failed"
				success = false
			)
			
			-- Reset 3dsmax scene
			MSFS2024_BlobMeshizeStruct.resetRelativeTexturePaths tempMatTexturePaths -- reset paths and free memory
			
			-- Post processing for 3dsmax scene organization
			if success then
			(
				processedMeshes = sgsdk_GetProcessedMeshes()
				
-- 				lastMats = sgsdk_GetMaterials()
-- 				format "lastMats: %\n" lastMats
				
				for meshName in processedMeshes do
				(
-- 					format "Setup new mesh: %\n" meshName
					
					-- hopefully we only have unique names here
					local newNode = getNodeByName meshName
					if newNode != undefined then
					(
						-- Properly rename new blob mesh
						local newNodeName = obj.name + "_blobMesh"
						newNode.name = uniqueName newNodeName
						
						-- Put new node in proper layer
						local currentLayer = obj.layer
						currentLayer.addNode newNode
						
						-- Assign new materials
						if bakeMaterial then
						(
							local newMat = MSFS2024_Material()
							local newMatTypeId = findItem newMat.matList bakeMaterialTo
							if newMatTypeId != 0 then
							(
								newMat.materialType = newMatTypeId
								newMat.name = meshName + "_material"
								
								local sgMat = sgsdk_GetMaterialForMesh meshName
								local channels = sgsdk_GetChannelsForMaterial sgMat
								for chan in channels do
								(
									local texPath = sgsdk_GetTexturePathForChannel sgMat chan
									MSFS2024_BlobMeshizeStruct.setMaterialTexPathFromShaderSlot newMat &shaderSlots &chan &texPath
								)
								newNode.material = newMat
							)
							else
							(
								MSFS2024_BlobMeshizeStruct.output ("Cannot set unsupported material type: " + bakeMaterialTo)
							)
						)
					)
				)
			)
			sgsdk_ClearPipelines()
			true
		)
		else
		(
			MSFS2024_BlobMeshizeStruct.output "Failed to create blob mesh for following:\n"
			print obj
			false
		)
	),
	
	/*
	* Process each selected object separately and create a blob mesh for each one
	*/
	fn createMultipleBlobMeshesFromSelected onScreenPixelSize:70 bakeMaterialFrom: bakeMaterialTo: outputTextureSize:[512, 512] outputTextureFormat:#PNG disableShaderSlots:#() =
	(
		-- loop for all objects
		local sel = getCurrentSelection()
		if sel.count > 0 then
		(
			for obj in sel do
			(
				MSFS2024_BlobMeshizeStruct.createBlobMesh obj onScreenPixelSize:onScreenPixelSize bakeMaterialFrom:bakeMaterialFrom bakeMaterialTo:bakeMaterialTo \
					outputTextureSize:outputTextureSize outputTextureFormat:outputTextureFormat disableShaderSlots:disableShaderSlots
			)
			select sel -- reset selection
		)
		else messageBox "Nothing selected!"
	),
	
	/*
	* Merge selected objects into one and create only one blob mesh
	*/
	fn createSingleBlobMeshFromSelected onScreenPixelSize:70 bakeMaterialFrom: bakeMaterialTo: outputTextureSize:[512, 512] outputTextureFormat:#PNG disableShaderSlots:#() =
	(
		local sel = getCurrentSelection()
		if sel.count > 0 then
		(
			local objToProcess
			local tempObj
			if sel.count == 1 then objToProcess = sel[1]
			else
			(
				with redraw off
				(
					-- create new clean edit_poly and attach all to it
					local referenceObj = sel[1] -- use first in selection for name
					tempObj = Editable_mesh vertices:#() faces:#() name:referenceObj.name
					convertToPoly tempObj
					-- Put new obj in proper layer
					local currentLayer = sel[1].layer -- using layer of first object in selection
					currentLayer.addNode tempObj
					for obj in sel do
					(
						if superClassOf obj == GeometryClass then
						(
							local copyObj = copy obj
							-- when copying with skin and transform not properly reset to identity, weird stuff happens.
							-- we need to disable skin before to reset proper transform
							for m in copyObj.modifiers do
							(
								if classOf m == Skin then m.enabled = false
							)
							convertToPoly copyObj
							--resetxform copyObj
							--collapsestack copyObj
							polyop.attach tempObj copyObj
						)
					)
					objToProcess = tempObj
				)
			)
			MSFS2024_BlobMeshizeStruct.createBlobMesh objToProcess onScreenPixelSize:onScreenPixelSize bakeMaterialFrom:bakeMaterialFrom bakeMaterialTo:bakeMaterialTo \
				outputTextureSize:outputTextureSize outputTextureFormat:outputTextureFormat disableShaderSlots:disableShaderSlots
			if tempObj != undefined then delete tempObj
			select sel -- reset selection
		)
		else messageBox "Nothing selected!"
	),
	
	/*
	* Run using #single or #multiple to create a single merged blob mesh or one blob mesh per object
	* See flight sim material for material types
	*/
	fn blobMeshize mode:#single onScreenPixelSize:70 bakeMaterialFrom:#Hair bakeMaterialTo: outputTextureSize:[512, 512] outputTextureFormat:#PNG disableShaderSlots:#() =
	(
		if sgsdk_RunPipelineOnSelection != undefined then
		(
			case mode of
			(
				#single:	MSFS2024_BlobMeshizeStruct.createSingleBlobMeshFromSelected		onScreenPixelSize:onScreenPixelSize bakeMaterialFrom:bakeMaterialFrom bakeMaterialTo:bakeMaterialTo outputTextureSize:outputTextureSize outputTextureFormat:outputTextureFormat disableShaderSlots:disableShaderSlots
				#multiple:	MSFS2024_BlobMeshizeStruct.createMultipleBlobMeshesFromSelected	onScreenPixelSize:onScreenPixelSize bakeMaterialFrom:bakeMaterialFrom bakeMaterialTo:bakeMaterialTo outputTextureSize:outputTextureSize outputTextureFormat:outputTextureFormat disableShaderSlots:disableShaderSlots
				default:	MSFS2024_BlobMeshizeStruct.output ("Blob mesh generation: unrecognized mode: " + (mode as string))
			)
		)
		else
		(
			messageBox "Please install simplygon to run this script."
		)
	)
)

macroScript MSFS2024_BlobMeshize
category:"MSFS2024"
buttonText:"Generate blob mesh"
--icon:#("Standard_Modifiers",19)
toolTip:"Generate blob mesh for hairs"
(
	local uiWidth = 420
	local matList = #(#Unknown)
	local matListDisplayNames = #("Error retrieving material types")
	local matTexList = #("Error retrieving material texture names")
	local defaultCastTo = 1
	local defaultActiveTexSlotsIds = #{}
	local outTextureFormats = #(#BMP, #DDS, #JPEG, #PNG, #TGA, #TIFF, #EXR)
	local shaderSlots
	
	local widthMargin = 5
	local widthMargins = widthMargin * 2
	local halfWidthWithMargins = (uiWidth - widthMargins) / 2.0
	
	rollout MSFS2024_BlobMeshizeUI "Generate blob mesh"
	(
		label lbInfo "This tool will generate a blob mesh from selection and bake textures." align:#center offset:[0,5]
		
		local grpOptionsHeight = 60
		groupbox grpOptions "Options" width:(halfWidthWithMargins-widthMargin) height:grpOptionsHeight align:#center offset:[-halfWidthWithMargins / 2.0,10]
		spinner spOnScreenSize "On screen size (%):" tooltip:"Desired screen size for object display\nHigher values: longer process time" \
			range:[0,10000, 6.5] scale:0.1 fieldwidth:50 align:#right offset:[-halfWidthWithMargins, 15-grpOptionsHeight]
		
		checkbox chkCastMaterial "Cast materials" tooltip:"Enable material casting" checked:true offset:[0,0]
		
		local grpCastMaterialOptionsHeight = 560
		groupbox grpCastMaterialOptions "Cast materials options" width:(halfWidthWithMargins-widthMargin) height:grpCastMaterialOptionsHeight align:#center offset:[halfWidthWithMargins / 2.0,-grpOptionsHeight]
		
		label lbTextureSize "Texture size (px):" offset:[halfWidthWithMargins,15-grpCastMaterialOptionsHeight] align:#left
		spinner textureSizeX "Width:" tooltip:"Texture width in pixels" range:[4,16384, 512] type:#integer fieldwidth:45 across:2 align:#left offset:[halfWidthWithMargins,0]
		spinner textureSizeY "Height:" tooltip:"Texture height in pixels" range:[4,16384, 512] type:#integer fieldwidth:45 align:#right offset:[0, 0]
		
		dropdownlist ddlTextureFormat "Texture format:" tooltip:"Set texture format" items:outTextureFormats selection:4 height:(outTextureFormats.count + 1) width:150 offset:[halfWidthWithMargins,0]
		
		checkbox chkForceOutMaterialType "Cast to specific material" tooltip:"Force casting to specific material" checked:true offset:[halfWidthWithMargins,5]
		dropdownlist ddlToMaterialType "" tooltip:"Material type to cast" items:matListDisplayNames selection:defaultCastTo height:(matListDisplayNames.count + 1) width:150 offset:[halfWidthWithMargins+20,0]
		
		multiListBox mlbOutTextures "(ctrl+click) Active texture slots:" tooltip:"Enable casting for selected textures only" items:matTexList selection:defaultActiveTexSlotsIds \
			width:(halfWidthWithMargins-widthMargin*3) align:#center offset:[halfWidthWithMargins / 2.0,5] height:28
		
		radiobuttons rbtnsMode "Generate:" labels:#("One per object", "Merge all objects into one") tooltip:"Generate one blob mesh per selected object, or a single merged from selection\n(if merged from multiple objects, you will need to re-skin/wrap afterward)" \
			columns:1 default:2 align:#left offset:[0,-90]
		button btnGenerateBlobMesh "Generate blob mesh" tooltip:"Generate blob mesh for selected object(s)" align:#center width:160 height:40 offset:[-halfWidthWithMargins / 2.0,0]
		
		label lbInfo2 "Note : you need simplygon properly installed and activated" align:#center offset:[0,10]
		
		label lbBottomMargin "" offset:[0,-10]
		
		on chkCastMaterial changed state do
		(
			grpCastMaterialOptions.enabled = state
			chkForceOutMaterialType.enabled = state
			ddlToMaterialType.enabled = if state then chkForceOutMaterialType.checked else false
			mlbOutTextures.enabled = state
			lbTextureSize.enabled = state
			textureSizeX.enabled = state
			textureSizeY.enabled = state
			ddlTextureFormat.enabled = state
		)
		on chkForceOutMaterialType changed state do ddlToMaterialType.enabled = state
		
		on btnGenerateBlobMesh pressed do
		(
			local modes = #(#multiple, #single)
			local disabledShaderSlots = #()
			for i = 1 to matTexList.count do
			(
				if not mlbOutTextures.selection[i] then
				(
					local texName = matTexList[i] + "Tex"
					local shaderSlot = MSFS2024_BlobMeshizeStruct.getShaderSlotFromTexName &shaderSlots &texName
					append disabledShaderSlots shaderSlot
				)
			)
			local bakeMaterialFrom = if chkCastMaterial.checked then #Hair else undefined
			local bakeMaterialTo = if chkForceOutMaterialType.checked then matList[ddlToMaterialType.selection] else undefined
			local onScreenPixelSize = spOnScreenSize.value * 0.01 * 1080.0 -- mimic MFSF2024 simplygon setup
			MSFS2024_BlobMeshizeStruct.blobMeshize mode:(modes[rbtnsMode.state]) onScreenPixelSize:onScreenPixelSize bakeMaterialFrom:bakeMaterialFrom bakeMaterialTo:bakeMaterialTo \
				outputTextureSize:[textureSizeX.value, textureSizeY.value] outputTextureFormat:(outTextureFormats[ddlTextureFormat.selection]) disableShaderSlots:disabledShaderSlots
		)
	)
	
	on execute do
	(
		-- close dialog if already open
		try
		(
			destroyDialog MSFS2024_BlobMeshizeUI
		)
		catch()
		
		-- populate material fields
		local tempMat = MSFS2024_Material()
		matList = copy tempMat.matList #nomap
		matListDisplayNames = copy tempMat.matListDisplayNames #nomap
		matTexList = copy tempMat.TexList #nomap
		
		local castToId = findItem matList #Standard
		if castToId != 0 then defaultCastTo = castToId
		
		local defaultActiveTexSlots = #(
			"BaseColor",
			"OcclusionRoughnessMetallic",
			"Normal"
			)
		for slot in defaultActiveTexSlots do
		(
			local slotId = findItem matTexList slot
			if slotId != 0 then append defaultActiveTexSlotsIds slotId
		)
		
		local bmStruct = MSFS2024_BlobMeshizeStruct()
		shaderSlots = bmStruct.shaderSlots()
		
		-- create dialog
		createDialog MSFS2024_BlobMeshizeUI width:uiWidth
	)
	--on closeDialogs do destroyDialog MSFS2024_BlobMeshizeUI
)
