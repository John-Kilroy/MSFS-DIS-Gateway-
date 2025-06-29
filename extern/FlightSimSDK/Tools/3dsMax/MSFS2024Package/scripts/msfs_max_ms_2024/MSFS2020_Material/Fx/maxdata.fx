////////MATERIAL TYPE////////
uniform int p_materialType <
	string UIName = "p_materialType";
> = 0;

#define Material_Standard				1
#define	Material_Decal					2
#define	Material_Windshield				3
#define	Material_PortHole				4
#define	Material_Glass					5
#define	Material_GeoDecalFrosted		6
#define	Material_ClearCoat				7
#define	Material_ParallaxWindow			8
#define	Material_Anisotropic			9
#define	Material_Hair					10
#define	Material_SSS					11
#define	Material_Invisible				12
#define	Material_FakeTerrain			13
#define	Material_FresnelFade			14
#define	Material_EnvironmentOccluder	15
#define	Material_Ghost					16
#define	Material_GeoDecal_Dirt			17
#define	Material_Sail					18
#define	Material_Propeller				19
#define	Material_WindFlex				20
#define	Material_Tree					21
#define	Material_Vegetation				22
#define	Material_Tire					23
//#define Material_PortHoleParallaxInterior 24

////////DEBUG MATERIAL CHECKBOX////////

uniform bool p_windshieldWiperMask < string UIName = "p_windshieldWiperMask"; > = false;
uniform bool p_windshieldInsectsAlbedo < string UIName = "p_windshieldInsectsAlbedo"; > = false;
uniform float p_windshieldInsectsMask < string UIName = "p_windshieldInsectsMask"; > = 1.0f;
uniform bool p_windshieldVertexColorR < string UIName = "p_windshieldVertexColorR"; > = false;
uniform bool p_windshieldVertexColorG < string UIName = "p_windshieldVertexColorG"; > = false;
uniform bool p_windshieldVertexColorB < string UIName = "p_windshieldVertexColorB"; > = false;
uniform bool p_windshieldVertexColorA < string UIName = "p_windshieldVertexColorA"; > = false;

////////MATERIAL PARAMS////////
uniform float4 p_baseColorFactor<
	string UIName = "p_baseColorFactor";
	> = {1,1,1,1};
uniform float4 p_SSSColorFactor<
	string UIName = "p_SSSColorFactor";
	> = {1,1,1,1};
uniform float p_occlusionStrength<
	string UIName = "p_occlusionStrength";
	> = 1;
uniform float p_roughnessFactor<
	string UIName = "p_roughnessFactor";
	> = 1;

uniform float p_EmissiveMultiplierFactor<
	string UIName = "p_EmissiveMultiplierFactor";
	> = 1;

uniform float p_metallicFactor<
	string UIName = "p_metallicFactor";
	> = 1;
uniform float4 p_emissiveFactor<
	string UIName = "p_emissiveFactor";
	> = {0,0,0,0};
uniform float p_normalScale<
	string UIName = "p_normalScale";
	> = 1;
uniform int p_alphaMode<
	string UIName = "p_alphaMode";
	> = 0;
uniform int p_drawOrder<
	string UIName = "p_drawOrder";
	> = 0;
uniform float p_alphaCutoff<
	string UIName = "p_alphaCutoff";
	> = 0.5;
uniform float p_UVOffsetU<
	string UIName = "p_UVOffsetU";
	> = 0.0;
uniform float p_UVOffsetV<
	string UIName = "p_UVOffsetV";
	> = 0.0;	
uniform float p_UVTilingU<
	string UIName = "p_UVTilingU";
	> = 1.0;
uniform float p_UVTilingV<
	string UIName = "p_UVTilingV";
	> = 1.0;
uniform float p_UVRotation<
	string UIName = "p_UVRotation";
	> = 0.0;
uniform float p_wiperAnimState1 <
	string UIName = "p_wiperAnimState1";
	> = 0.0;
uniform float p_tireMudAnimState <
	string UIName = "p_tireMudAnimState";
	> = 0.0;
uniform float p_tireDustAnimState <
	string UIName = "p_tireDustAnimState";
	> = 0.0;
uniform float p_detailUVScale<
	string UIName = "p_detailUVScale";
	> = 2.0;
uniform float p_detailUVOffsetX<
	string UIName = "p_detailUVOffsetX";
	> = 0.0;
uniform float p_detailUVOffsetY<
	string UIName = "p_detailUVOffsetY";
	> = 0.0;
uniform float p_detailNormalScale <
	string UIName = "p_detailNormalScale";
	> = 1.0;
uniform float p_blendThreshold <
	string UIName = "p_blendThreshold";
	> = 0.1;
uniform float p_glassWidth <
	string UIName = "p_glassWidth";
	> = 0.0;
uniform float p_parallaxScale<
	string UIName = "p_parallaxScale";
	> = 0.0;
uniform float p_roomSizeXScale <
	string UIName = "p_roomSizeXScale";
	> = 0.0;
uniform float p_roomSizeYScale <
	string UIName = "p_roomSizeYScale";
	> = 0.0;
uniform float p_roomNumberXY <
	string UIName = "p_roomNumberXY";
	> = 0.0;
uniform float p_fresnelFactor <
	string UIName = "p_fresnelFactor";
	> = 0.0;
uniform float p_fresnelOpacityOffset <
	string UIName = "p_fresnelOpacityOffset";
	> = 0.0;
uniform float p_ghostBiasFactor <
	string UIName = "p_ghostBiasFactor";
	> = 0.0;
uniform float p_ghostPowerFactor <
	string UIName = "p_ghostPowerFactor";
	> = 0.0;
uniform float p_ghostScaleFactor <
	string UIName = "p_ghostScaleFactor";
	> = 0.0;
uniform float p_pearlRange <
	string UIName = "p_pearlRange";
	> = 0.0;
uniform float p_pearlShift <
	string UIName = "p_pearlShift";
	> = 0.0;
uniform float p_pearlBrightness <
	string UIName = "p_pearlBrightness";
	> = 0.0;
uniform float p_iridescentMinThickness <
	string UIName = "p_iridescentMinThickness";
	> = 0.0;
uniform float p_iridescentMaxThickness <
	string UIName = "p_iridescentMaxThickness";
	> = 0.0;
uniform float p_iridescentBrightness <
	string UIName = "p_iridescentBrightness";
	> = 0.0;
uniform float p_sailLightAbsorption <
	string UIName = "p_sailLightAbsorption";
	> = 0.0;
uniform float p_sailLightPropagation <
	string UIName = "p_sailLightPropagation";
	> = 0.0;
uniform float p_dirtUvScale <
	string UIName = "p_dirtUvScale";
	> = 0.0;
uniform float p_dirtAmount <
	string UIName = "p_dirtAmount";
	> = 0.0;
uniform float p_dirtBlendSharpness <
	string UIName = "p_dirtBlendSharpness";
	> = 0.0;

uniform const bool p_baseColorEnabled <
	string UIName = "p_baseColorEnabled";
	> = false;

uniform const bool p_occRoughMetalEnabled <
	string UIName = "p_occRoughMetalEnabled";
	> = false;

uniform bool p_corridorEnabled <
	string UIName = "p_corridorEnabled";
	> = false;

uniform const bool p_decalFrosted<
	string UIName = "p_decalFrosted";
	> = false;
uniform const bool p_blendmaskEnabled <
	string UIName = "p_blendmaskEnabled";
	> = false;
uniform const bool p_foliagemaskEnabled <
	string UIName = "p_foliagemaskEnabled";
	> = false;
uniform const bool p_detailColorEnabled <
	string UIName = "p_detailColorEnabled";
	> = false;
uniform const bool p_detailNormalEnabled <
	string UIName = "p_detailNormalEnabled";
	> = false;
uniform const bool p_detailOccRoughMetalEnabled <
	string UIName = "p_detailOccRoughMetalEnabled";
	> = false;
	
uniform const bool p_pearlescentEnabled <
	string UIName = "p_pearlescentEnabled";
	> = false;
uniform const bool p_iridescentEnabled <
	string UIName = "p_iridescentEnabled";
	> = false;
	
uniform const bool p_occlusionEnabled <
	string UIName = "p_occlusionEnabled";
	> = false;

uniform const bool p_clearcoatColorRoughnessEnabled <
		string UIName = "p_clearcoatColorRoughnessEnabled";
	> = false;
uniform const bool p_clearcoatNormalEnabled <
		string UIName = "p_clearcoatNormalEnabled";
	> = false;

uniform const bool p_windshieldInsectsEnabled <
	string UIName = "p_windshieldInsectsEnabled";
	> = false;
uniform const bool p_windshieldInsectsMaskEnabled <
	string UIName = "p_windshieldInsectsMaskEnabled";
	> = false;
uniform const bool p_tireDetailsEnabled <
	string UIName = "p_tireDetailsEnabled";
	> = false;
uniform const bool p_tireMudNormalEnabled <
	string UIName = "p_tireMudNormalEnabled";
	> = false;
uniform const bool p_dirtEnabled <
	string UIName = "p_dirtEnabled";
	> = false;
	
////////LIGHTS////////
uniform float3 p_lightDir : DIRECTION < 
	string UIName = "p_lightDir";
	string Object = "TargetLight";
	int RefID = 0;
	>;
////////TEXTURES////////
Texture2D <float4> p_baseColorTex : DIFFUSEMAP< 
	string UIName = "p_baseColorTex";
	>;
Texture2D <float4> p_occlusionRoughnessMetallicTex< 
	string UIName = "p_occlusionRoughnessMetallicTex";
	>;
Texture2D <float4> p_normalTex< 
	string UIName = "p_normalTex";
	>;
Texture2D <float4> p_blendMaskTex< 
	string UIName = "p_blendMaskTex";
	>;
Texture2D <float4> p_foliageMaskTex< 
	string UIName = "p_foliageMaskTex";
	>;
Texture2D <float4> p_wetnessAOTex< 
	string UIName = "p_wetnessAOTex";
	>;
Texture2D <float4> p_windshieldDetailNormalTex<
	string UIName = "p_windshieldDetailNormalTex";
	>;
Texture2D <float4> p_scratchesNormalTex <
	string UIName = "p_scratchesNormalTex";
	>;
Texture2D <float4> p_wiperMaskTex <
	string UIName = "p_wiperMaskTex";
	>;
Texture2D <float4> p_windshieldInsectsTex <
	string UIName = "p_windshieldInsectsTex";
	> ;
Texture2D <float4> p_windshieldInsectsMaskTex <
	string UIName = "p_windshieldInsectsMaskTex";
	> ;
Texture2D <float4> p_iridescentThicknessTex <
	string UIName = "p_iridescentThicknessTex";
	> ;
Texture2D <float4> p_anisoDirectionRoughnessTex <
	string UIName = "p_anisoDirectionRoughnessTex";
	> ;
Texture2D <float4> p_dirtTex <
	string UIName = "p_dirtTex";
	> ;
Texture2D <float4> p_dirtOccRoughMetalTex< 
	string UIName = "p_dirtOccRoughMetalTex";
	>;
Texture2D <float4> p_opacityTex <
	string UIName = "p_opacityTex";
	> ;
Texture2D <float4> p_emissiveTex< 
	string UIName = "p_emissiveTex";
	>;
Texture2D <float4> p_detailColorTex<
	string UIName = "p_detailColorTex";
	>;
Texture2D <float4> p_detailOcclusionRoughnessMetallicTex< 
	string UIName = "p_detailOcclusionRoughnessMetallicTex";
	>;
Texture2D <float4> p_detailNormalTex<
	string UIName = "p_detailNormalTex";
	>;
TextureCube <float4> p_irradianceTex<
	string UIName = "p_irradianceTex";
	>;
TextureCube <float4> p_radianceTex<
	string UIName = "p_radianceTex";
	>;
Texture2D <float4> p_specularBRDF_LUT <
	string UIName = "p_specularBRDF_LUT";
	>;
Texture2D <float4> p_occlusionTex <
	string UIName = "p_occlusionTex";
	>;
Texture2D <float4> p_clearcoatColorRoughnessTex <
	string UIName = "p_clearcoatColorRoughnessTex";
	> ;
Texture2D <float4> p_clearcoatNormalTex <
	string UIName = "p_clearcoatNormalTex";
	>;
Texture2D <float4> p_tireDetailsTex <
	string UIName = "p_tireDetailsTex";
	> ;
Texture2D <float4> p_tireMudNormalTex <
	string UIName = "p_tireMudNormalTex";
	> ;
//Porthole parallax interior
/*Texture2D <float4> p_phpiInteriorHallwayAlbedoTex< 
	string UIName = "p_phpiInteriorHallwayAlbedoTex";
	>;
Texture2D <float4> p_phpiInteriorHallwayNormalAoTex< 
	string UIName = "p_phpiInteriorHallwayNormalAoTex";
	>;
Texture2D <float4> p_phpiInteriorHallwayEmissiveTex< 
	string UIName = "p_phpiInteriorHallwayEmissiveTex";
	>;
Texture2D <float4> p_phpiInteriorLeftWallAlbedoTex< 
	string UIName = "p_phpiInteriorLeftWallAlbedoTex";
	>;
Texture2D <float4> p_phpiInteriorLeftWallNormalAoTex< 
	string UIName = "p_phpiInteriorLeftWallNormalAoTex";
	>;
Texture2D <float4> p_phpiInteriorLeftWallEmissiveTex< 
	string UIName = "p_phpiInteriorLeftWallEmissiveTex";
	>;
Texture2D <float4> p_phpiInteriorRightWallAlbedoTex< 
	string UIName = "p_phpiInteriorRightWallAlbedoTex";
	>;
Texture2D <float4> p_phpiInteriorRightWallNormalAoTex< 
	string UIName = "p_phpiInteriorRightWallNormalAoTex";
	>;
Texture2D <float4> p_phpiInteriorRightWallEmissiveTex< 
	string UIName = "p_phpiInteriorRightWallEmissiveTex";
	>;
Texture2D <float4> p_phpiSideProjectionAlbedoHeightTex< 
	string UIName = "p_phpiSideProjectionAlbedoHeightTex";
	>;
Texture2D <float4> p_phpiSideProjectionNormalAoTex< 
	string UIName = "p_phpiSideProjectionNormalAoTex";
	>;
Texture2D <float4> p_phpiSideProjectionEmissiveTex< 
	string UIName = "p_phpiSideProjectionEmissiveTex";
	>;
Texture2D <float4> p_phpiFrontProjectionAlbedoHeightTex< 
	string UIName = "p_phpiFrontProjectionAlbedoHeightTex";
	>;
Texture2D <float4> p_phpiFrontProjectionNormalAoTex< 
	string UIName = "p_phpiFrontProjectionNormalAoTex";
	>;
Texture2D <float4> p_phpiFrontProjectionEmissiveTex< 
	string UIName = "p_phpiFrontProjectionEmissiveTex";
	>;
Texture2D <float4> p_phpiBackProjectionAlbedoHeightTex< 
	string UIName = "p_phpiBackProjectionAlbedoHeightTex";
	>;
Texture2D <float4> p_phpiBackProjectionNormalAoTex< 
	string UIName = "p_phpiBackProjectionNormalAoTex";
	>;
Texture2D <float4> p_phpiBackProjectionEmissiveTex< 
	string UIName = "p_phpiBackProjectionEmissiveTex";
	>;
Texture2D <float4> p_phpiTopProjectionAlbedoHeightTex< 
	string UIName = "p_phpiTopProjectionAlbedoHeightTex";
	>;
Texture2D <float4> p_phpiTopProjectionNormalAoTex< 
	string UIName = "p_phpiTopProjectionNormalAoTex";
	>;
Texture2D <float4> p_phpiTopProjectionEmissiveTex< 
	string UIName = "p_phpiTopProjectionEmissiveTex";
	>;	*/

////////CONSTANTES////////
cbuffer UpdatePerFrame : register(b0)
{
float4x4 worldMatrix 			: World;
float4x4 viewMatrix				: View;
float4x4 projMatrix 			: Projection;
float4x4 worldViewProjMatrix 	: WorldViewProj;
float4x4 worldIMatrix 			: WorldI;
float4x4 WorldITXf				: WorldInverseTranspose;
float4x4 viewIMatrix 			: ViewI;
float4x4 viewInverseMatrix		: ViewInverse;
}
//float time 						: TIME;
float2 viewportSize				: VIEWPORTPIXELSIZE;
////////APP->VERTEX////////
int texcoord0 : Texcoord
<
	int Texcoord = 0;
	int MapChannel = 1; //UV1
>;
int texcoord1 : Texcoord
<
	int Texcoord = 1;
	int MapChannel = 2; //UV2
>;
int texcoord2 : Texcoord
<
	int Texcoord = 2;
	int MapChannel = 0; //COLOR
>;
int texcoord3 : Texcoord
<
	int Texcoord = 3;
	int MapChannel = -2; //ALPHA
>;

////////////SAMPLER///////////
SamplerState wrapSampler
{
	FILTER = ANISOTROPIC;
	MaxAnisotropy = 8;
	AddressU = WRAP;
	AddressV = WRAP;
};
SamplerState clampSampler
{
	FILTER = ANISOTROPIC;
	MaxAnisotropy = 8;
	AddressU = CLAMP;
	AddressV = CLAMP;
};
SamplerState BRDFSampler
{
	FILTER = ANISOTROPIC;
	MaxAnisotropy = 8;
	AddressU = CLAMP;
	AddressV = CLAMP;
};