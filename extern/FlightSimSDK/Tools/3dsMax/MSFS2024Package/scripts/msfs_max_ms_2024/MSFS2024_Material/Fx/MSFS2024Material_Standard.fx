#include "core.fx"
float4 PS_STANDARD(vOut IN) : SV_Target
{
	float2 uv = IN.UV.xy;
	float2 uv2 = IN.UV.zw;
	
	float4 albedo = p_baseColorTex.Sample(wrapSampler, uv); //albedo
	float3 occ_rough_metal = p_occlusionRoughnessMetallicTex.Sample(wrapSampler, uv); //occlusion/roughness/metal
	float occlusion = occ_rough_metal.r;
	if (p_occlusionEnabled)
	{
		occlusion *= p_occlusionTex.Sample(wrapSampler, uv2).r; //occlusion sample on uv2
	}
	float roughness = occ_rough_metal.g * p_roughnessFactor;
	float metalness = occ_rough_metal.b *p_metallicFactor;	
	float4 vColor = IN.VertexColor;
	const float emissiveFixFactor = 0.0002; //control emissive output for 3dsmax viewport as it doesn't use HDR
	const float emissiveSubjectiveFixFactor = 1.3; //multiply final value to "burn" a little bit more (feels more like game render)
	float emissiveMultiplier = p_EmissiveMultiplierFactor * emissiveFixFactor;
	emissiveMultiplier = emissiveSubjectiveFixFactor * emissiveMultiplier / (emissiveMultiplier + 1.0);
	float detailMaskKH = 1.0;
	if (p_detailColorEnabled || p_detailNormalEnabled || p_detailOccRoughMetalEnabled)
	{
		detailMaskKH = IN.VertexColor.a * albedo.a;
		vColor.a = 1.0;
	}
	albedo *= p_baseColorFactor;
	//blend part.
	float blend = 1.0;
	if (p_blendmaskEnabled)
	{
		blend = p_blendMaskTex.Sample(wrapSampler, uv).x;
		
		blend = linearstep(saturate(blend - p_blendThreshold), saturate(blend + p_blendThreshold), IN.VertexColor.a);
		float4 blendColor = p_baseColorFactor;
		if (p_detailColorEnabled)
		{
			blendColor = p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY));
			//fake display gamma correct
			//blendColor.xyz = pow(blendColor.xyz, 2.2);
		} 
		albedo = lerp( blendColor, albedo, blend);
	}
	else // detail 
	{ 
		if (p_detailColorEnabled)
		{
			float4 detailColor = p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale * worldMatrix[0][0] + float2(p_detailUVOffsetX, p_detailUVOffsetY));
			detailColor.xyz *= 2.0;
			detailColor.w *= detailMaskKH;
			detailColor.xyz = lerp(float3(1, 1, 1), detailColor.xyz, detailColor.w);
			albedo.xyz = saturate(albedo.xyz * detailColor.xyz);
			//return float4(pow(abs(p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY)).x - 0.5) * 2.0, 0.2) * IN.VertexColor.x, 0, 0, 1.0);
		}
	}
	albedo *= vColor;
	occlusion = lerp(lerp(1.0, occlusion, saturate(p_occlusionStrength)), 0.0, saturate(p_occlusionStrength - 1));
	albedo.rgb = albedo.rgb*occlusion;
	float3 emissiveColor = p_emissiveFactor.xyz * p_emissiveTex.Sample(wrapSampler, uv).xyz * emissiveMultiplier;
	float3 tangentNormal = 2.0 * (p_normalTex.Sample(wrapSampler, uv).xyz - 0.5);
	
	//blend
	if (p_blendmaskEnabled)
	{        
		float3 blendTangentNormal = float3(0,0,1);
		if (p_detailNormalEnabled)
		{            
			blendTangentNormal = 2.0 * (p_detailNormalTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY)).xyz - 0.5) * p_detailNormalScale;
		}		
		
		tangentNormal = lerp(tangentNormal,blendTangentNormal, 1 - blend);   
	
	}

	else // detail
	{		
		float3 detailTangentNormal = float3(0,0,1);
		
		if (p_detailNormalEnabled)
		{
			float3 detailTangentNormal = 2.0 * (p_detailNormalTex.Sample(wrapSampler, uv * p_detailUVScale * worldMatrix[0][0] + float2(p_detailUVOffsetX, p_detailUVOffsetY)).xyz - 0.5) * p_detailNormalScale;
			detailTangentNormal = lerp(float3(0, 0, 1), detailTangentNormal, detailMaskKH);
			tangentNormal += detailTangentNormal;			
		}
	}
	tangentNormal.y = -tangentNormal.y;	
	tangentNormal.xy *= p_normalScale;
	tangentNormal.z = sqrt(saturate(1.f - dot(tangentNormal.xy, tangentNormal.xy)));
    float3x3 TBN = float3x3(normalize(IN.WorldTangent), normalize(IN.WorldBinormal),normalize(IN.WorldNormal)); //transforms world=>tangent space
	TBN = transpose(TBN);	
	
	float3 worldNormal = mul(TBN, normalize(tangentNormal)); //N	

	if(p_pearlescentEnabled)
	{
		float3 Lo = normalize(viewIMatrix[3].xyz - IN.wPos);
		float NdotV = 1.0f - saturate(dot(worldNormal,Lo));
		float pearlShiftRamp = pow(NdotV, p_pearlShift);
		float3 yuvCol = RGBToYUV(albedo.xyz);
		float pearlCos, pearlSin;
		sincos(-pearlShiftRamp * p_pearlRange * 6.2831853f, pearlSin, pearlCos);
		yuvCol.yz = Rotate2D(yuvCol.yz, pearlCos, pearlSin) * 3.1415926f;
		yuvCol.x = saturate(yuvCol.x + saturate(pearlShiftRamp) * p_pearlBrightness);
		albedo.xyz = lerp(albedo.xyz, saturate(YUVToRGB(yuvCol)), metalness);
	}	

    if (p_dirtEnabled)
    {		
        float4 dirtOverlay = p_dirtTex.Sample(wrapSampler, uv * p_dirtUvScale);
        float4 dirtComp = p_dirtOccRoughMetalTex.Sample(wrapSampler, uv * p_dirtUvScale).w;
        float dirtRatio = 1 - p_dirtAmount;
        float dirtThreshold = 1 - p_dirtBlendSharpness;
        float dirtOverlayBlend = linearstep(saturate(dirtRatio - dirtThreshold), saturate(dirtRatio + dirtThreshold), dirtOverlay.w) * p_dirtAmount;
        albedo.xyz = lerp(albedo.xyz, dirtOverlay.xyz, dirtOverlayBlend);
        roughness = lerp(roughness, dirtComp.y, dirtOverlayBlend);
        metalness = lerp(metalness, dirtComp.z, dirtOverlayBlend);
    }
	
	if (p_tireDetailsEnabled) 
	{
		float2 tTireDetails = p_tireDetailsTex.Sample(wrapSampler, uv).rg;

		float dustmask = tTireDetails.y * p_tireDustAnimState;
		float mudMask = step(max(tTireDetails.x, 0.001), p_tireMudAnimState);

		albedo.rgb = lerp(albedo.rgb, float3(0.175f, 0.130f, 0.076f), dustmask);
		albedo.rgb = lerp(albedo.rgb, float3(0.146f, 0.093f, 0.033f), mudMask);
	}

    pbrLighting lighting = PBRModel(IN, worldNormal, albedo, metalness, roughness);
    
	float4 o = float4(lighting.ambientLight + lighting.directLight+ emissiveColor, albedo.a);

	// Debug
	if (p_materialType == Material_Windshield)
	{
		float4 tWindshieldInsects = p_windshieldInsectsTex.Sample(wrapSampler, uv2).rgba;
		float4 tWindshieldInsectsMask = p_windshieldInsectsMaskTex.Sample(wrapSampler, uv2).rgba;
		float4 tWiperMask = p_wiperMaskTex.Sample(wrapSampler, uv).rgba;

		if (p_windshieldWiperMask)
			o.rgb = tWiperMask.rgb;
		else if (p_windshieldInsectsAlbedo)
			o.rgb = lerp(0.0, tWindshieldInsects.rgb, tWindshieldInsects.a * step(tWindshieldInsectsMask.r, p_windshieldInsectsMask));
		else if (p_windshieldVertexColorR)
			o.rgb = IN.VertexColor.r;
		else if (p_windshieldVertexColorG)
			o.rgb = IN.VertexColor.g;
		else if (p_windshieldVertexColorB)
			o.rgb = IN.VertexColor.b;
		else if (p_windshieldVertexColorA)
			o.rgb = IN.VertexColor.a;

		o.a = 1.0;
	}

	o = Alpha(o,IN,p_alphaMode);

	return	o; 
}



////////TECHNIQUES////////
//Group: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476120(v=vs.85).aspx
//Technique: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476122(v=vs.85).aspx
//State Groups: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476121(v=vs.85).aspx
technique11 Tech_Base
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_STANDARD()));
		SetDepthStencilState(DepthOn, 0);
	}
}
technique11 Tech_TwoSide
{
	pass p0
	{
		SetRasterizerState(TwoSide);
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_STANDARD()));
		SetDepthStencilState(DepthOn, 0);
	}
}
technique11 Tech_Legacy
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_LEGACY()));
	}
}

