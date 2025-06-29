using Autodesk.Max;
using GLTFExport.Entities;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Runtime.Serialization;
using Babylon2GLTF;
using BabylonExport.Entities;
using MSFS2024_Max2Babylon.FlightSimExtension;
using Utilities;

namespace MSFS2024_Max2Babylon.FlightSim
{
	#region Serializable glTF Objects

	[DataContract]
	class GLTFNormalTextureInfo : GLTFTextureInfo
	{
		[DataMember(EmitDefaultValue = false)]
		public float? scale { get; set; }
	}

	[DataContract]
	class GLTFOcclusionTextureInfo : GLTFTextureInfo
	{
		[DataMember(EmitDefaultValue = false)]
		public float? strength { get; set; }

		public static class Defaults
		{
			public static readonly float strength = 1;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboOcclusionStrength : GLTFProperty
	{
		public const string SerializedName = "ASOBO_occlusion_strength";
		[DataMember(EmitDefaultValue = false)] public float? strength { get; set; }

		public static class Defaults
		{
			public static readonly float strength = 1;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboExtraOcclusion : GLTFProperty
	{
		public const string SerializedName = "ASOBO_extra_occlusion";
		[DataMember(EmitDefaultValue = false)] public GLTFOcclusionTextureInfo extraOcclusionTexture { get; set; }
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialGeometryDecal : GLTFProperty // use GLTFChildRootProperty if you want to add a name
	{
		public const string SerializedName = "ASOBO_material_geometry_decal";
		[DataMember(EmitDefaultValue = false)] public string mode { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? baseColorBlendFactor;
		[DataMember(EmitDefaultValue = false)] public float? metallicBlendFactor;
		[DataMember(EmitDefaultValue = false)] public float? roughnessBlendFactor;
		[DataMember(EmitDefaultValue = false)] public float? normalBlendFactor;
		[DataMember(EmitDefaultValue = false)] public float? emissiveBlendFactor;
		[DataMember(EmitDefaultValue = false)] public float? occlusionBlendFactor;
		[DataMember(EmitDefaultValue = true)] public float? blendSharpnessFactor;
		[DataMember(EmitDefaultValue = false)] public float? normalOverrideFactor;
		[DataMember(EmitDefaultValue = false)] public bool? underClearcoat;
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo blendMaskTexture { get; set; }

		public static class Defaults
		{
			public static readonly float normalOverrideFactor = 1.0f;
			public static readonly float blendSharpnessFactor = 1.0f;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialDirt : GLTFProperty // use GLTFChildRootProperty if you want to add a name
	{
		public const string SerializedName = "ASOBO_material_dirt";
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo dirtTexture { get; set; }
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo dirtOcclusionRoughnessMetallicTexture { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? dirtUvScale;
		[DataMember(EmitDefaultValue = false)] public float? dirtBlendSharpness;
		[DataMember(EmitDefaultValue = true)] public float? dirtBlendAmount;

		public static class Defaults
		{
			public static readonly float dirtUvScale = 1.0f;
			public static readonly float dirtBlendSharpness = 0.0f;
			public static readonly float dirtBlendAmount = 0.0f;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialGhostEffect : GLTFProperty // use GLTFChildRootProperty if you want to add a name
	{
		public const string SerializedName = "ASOBO_material_ghost_effect";
		[DataMember(EmitDefaultValue = false)] public float? bias;
		[DataMember(EmitDefaultValue = false)] public float? scale;
		[DataMember(EmitDefaultValue = false)] public float? power;

		public static class Defaults
		{
			public static readonly float bias = 1;
			public static readonly float scale = 1;
			public static readonly float power = 1;
		}
	}


	[DataContract]
	class GLTFExtensionAsoboMaterialDrawOrder : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_draw_order";
		[DataMember(EmitDefaultValue = false)] public int? drawOrderOffset;
		public static class Defaults
		{
			public static readonly int drawOrderOffset = 0;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboDayNightCycle : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_day_night_switch";
	}

	[DataContract]
	class GLTFExtensionAsoboDisableMotionBlur : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_disable_motion_blur";
		[DataMember(EmitDefaultValue = true)] public bool enabled = true;
	}

	[DataContract]
	class GLTFExtensionAsoboFlipBackFace : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_flip_back_face";
	}

	[DataContract]
	class GLTFExtensionAsoboPearlescent : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_pearlescent";
		[DataMember(EmitDefaultValue = false)] public float? pearlShift { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? pearlRange { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? pearlBrightness { get; set; }

		public static class Defaults
		{
			public static readonly float pearlShift = 0.0f;
			public static readonly float pearlRange = 0.0f;
			public static readonly float pearlBrightness = 0.0f;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboIridescent : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_iridescent";
		[DataMember(EmitDefaultValue = false)] public float? iridescentMinThickness { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? iridescentMaxThickness { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? iridescentBrightness { get; set; }
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo iridescentThicknessTexture { get; set; }

		public static class Defaults
		{
			public static readonly float iridescentMinThickness = 10.0f;
			public static readonly float iridescentMaxThickness = 400.0f;
			public static readonly float iridescentBrightness = 1.0f;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboAlphaModeDither : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_alphamode_dither";
		[DataMember(EmitDefaultValue = true)] public bool enabled = true;
		//[DataMember(EmitDefaultValue = false)] public string alphaMode;
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialInvisible : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_invisible";
		[DataMember(EmitDefaultValue = true)] public bool enabled = true;
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialEnvironmentOccluder : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_environment_occluder";
		[DataMember(EmitDefaultValue = true)] public bool enabled = true;
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialUVOptions : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_UV_options";
		[DataMember(EmitDefaultValue = false)] public bool? clampUVX { get; set; }
		[DataMember(EmitDefaultValue = false)] public bool? clampUVY { get; set; }
		[DataMember(EmitDefaultValue = false)] public bool? clampUVZ { get; set; }
		[DataMember(EmitDefaultValue = false)] public float UVOffsetU { get; set; }
		[DataMember(EmitDefaultValue = false)] public float UVOffsetV { get; set; }
		[DataMember(EmitDefaultValue = false)] public float UVTilingU { get; set; }
		[DataMember(EmitDefaultValue = false)] public float UVTilingV { get; set; }
		[DataMember(EmitDefaultValue = false)] public float UVRotation { get; set; }
		public static class Defaults
		{
			public static readonly bool clampUVX = false;
			public static readonly bool clampUVY = false;
			public static readonly bool clampUVZ = false;
			public static readonly float UVOffsetU = 0.0f;
			public static readonly float UVOffsetV = 0.0f;
			public static readonly float UVTilingU = 0.0f;
			public static readonly float UVTilingV = 0.0f;
			public static readonly float UVRotation = 0.0f;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialShadowOptions : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_shadow_options";
		[DataMember(EmitDefaultValue = false)] public bool? noCastShadow { get; set; }
		public static class Defaults
		{
			public static readonly bool noCastShadow = false;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialResponsiveAAOptions : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_antialiasing_options";
		[DataMember(EmitDefaultValue = false)] public bool? responsiveAA { get; set; }
		public static class Defaults
		{
			public static readonly bool responsiveAA = false;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialFakeTerrain : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_fake_terrain";
		[DataMember(EmitDefaultValue = true)] public bool enabled = true;
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialFresnelFade : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_fresnel_fade";
		[DataMember(EmitDefaultValue = false)] public float? fresnelFactor;
		[DataMember(EmitDefaultValue = false)] public float? fresnelOpacityOffset;
		public static class Defaults
		{
			public static readonly float fresnelFactor = 1;
			public static readonly float fresnelOpacityOffset = 1;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboMaterialDetail
	{
		public const string SerializedName = "ASOBO_material_detail_map";

		[DataMember(EmitDefaultValue = false)]
		public float? UVScale { get; set; }
		[DataMember(EmitDefaultValue = false)]
		public float? blendThreshold { get; set; }

		[DataMember(EmitDefaultValue = false)]
		public GLTFTextureInfo detailColorTexture { get; set; }
		[DataMember(EmitDefaultValue = false)]
		public GLTFNormalTextureInfo detailNormalTexture { get; set; }
		[DataMember(EmitDefaultValue = false)]
		public GLTFTextureInfo detailMetalRoughAOTexture { get; set; }
		[DataMember(EmitDefaultValue = false)]
		public GLTFTextureInfo blendMaskTexture { get; set; }

		public static class Defaults
		{
			public static readonly float UVScale = 1;
			public static readonly float blendThreshold = 0.0f;
			public static readonly float NormalScale = 1;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboSSS : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_SSS";
		[DataMember(EmitDefaultValue = false)] public float[] SSSColor;
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo opacityTexture;
		public static class Defaults
		{
			public static readonly float[] SSSColor = new float[] { 1, 1, 1, 1 };
		}
	}

	[DataContract]
	class GLTFExtensionAsoboAnisotropic_v2 : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_anisotropic_v2";
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo anisoDirectionRoughnessTexture;
	}

	[DataContract]
	class GLTFExtensionAsoboWindshield : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_windshield_v3";
		[DataMember(EmitDefaultValue = false)] public float? detail1Rough { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? detail2Rough { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? detail1Opacity { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? detail2Opacity { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? microScratchesTiling { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? microScratchesStrength { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? detailNormalRefractScale { get; set; }
		[DataMember(EmitDefaultValue = false)] public bool? receiveRain { get; set; }
		[DataMember(EmitDefaultValue = false)] public bool? wiperLines { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? wiperLinesTiling { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? wiperLinesStrength { get; set; }

		[DataMember(EmitDefaultValue = false)] public float? rainDropScale { get; set; }
		[DataMember(EmitDefaultValue = true)] public float? wiper1State { get; set; }

		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo wiperMaskTexture;
		[DataMember(EmitDefaultValue = false)] public GLTFNormalTextureInfo windshieldDetailNormalTexture;
		[DataMember(EmitDefaultValue = false)] public GLTFNormalTextureInfo scratchesNormalTexture;

		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo windshieldInsectsTexture;
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo windshieldInsectsMaskTexture;

		public static class Defaults
		{
			public static readonly float detail1Rough = 0;
			public static readonly float detail2Rough = 0;
			public static readonly float detail1Opacity = 0;
			public static readonly float detail2Opacity = 0;
			public static readonly float microScratchesTiling = 1;
			public static readonly float microScratchesStrength = 1;
			public static readonly float detailNormalRefractScale = 1;
			public static readonly bool receiveRain = true;
			public static readonly bool wiperLines = false;
			public static readonly float wiperLinesTiling = 1;
			public static readonly float wiperLinesStrength = 1;
			public static readonly float rainDropScale = 1;
			public static readonly float wiper1State = 0;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboClearCoat_v2 : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_clear_coat_v2";
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo clearcoatColorRoughnessTexture { get; set; }
		[DataMember(EmitDefaultValue = false)] public GLTFNormalTextureInfo clearcoatNormalTexture { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? clearcoatRoughnessFactor;
		[DataMember(EmitDefaultValue = false)] public float? clearcoatNormalFactor;
		[DataMember(EmitDefaultValue = false)] public float? clearcoatColorRoughnessTiling;
		[DataMember(EmitDefaultValue = false)] public float? clearcoatNormalTiling;
		[DataMember(EmitDefaultValue = false)] public bool? clearcoatInverseRoughness;
		[DataMember(EmitDefaultValue = false)] public float? clearcoatBaseRoughness;

		public static class Defaults
		{
			public static readonly float clearcoatRoughnessFactor = 1f;
			public static readonly float clearcoatNormalFactor = 1f;
			public static readonly float clearcoatColorRoughnessTiling = 1f;
			public static readonly float clearcoatNormalTiling = 1f;
			public static readonly bool clearcoatInverseRoughness = false;
			public static readonly float clearcoatBaseRoughness = 0.5f;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboParallaxWindow : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_parallax_window";
		[DataMember(EmitDefaultValue = false)] public float? parallaxScale { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? roomSizeXScale { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? roomSizeYScale { get; set; }
		[DataMember(EmitDefaultValue = false)] public float? roomNumberXY { get; set; }
		[DataMember(EmitDefaultValue = false)] public bool? corridor { get; set; }

		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo behindWindowMapTexture;
		public static class Defaults
		{
			public static readonly float parallaxScale = 0;
			public static readonly float roomSizeXScale = 0.5f;
			public static readonly float roomSizeYScale = 0.5f;
			public static readonly float roomNumberXY = 5;
			public static readonly bool corridor = false;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboFlightSimGlass_v2 : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_glass_v2";
		[DataMember(EmitDefaultValue = false)] public float? glassWidth { get; set; }
		public static class Defaults
		{
			public static readonly float glassWidth = 0;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboFlightSimTree
	{
		public const string SerializedName = "ASOBO_material_foliage_mask";

		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo foliageMaskTexture;
	}

	[DataContract]
	class GLTFExtensionAsoboFlightSimVegetation
	{
		public const string SerializedName = "ASOBO_material_vegetation";
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo foliageMaskTexture;
	}

	[DataContract]
	class GLTFExtensionAsoboFlightSimTire
	{
		public const string SerializedName = "ASOBO_material_tire";
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo tireDetailsTexture;
		[DataMember(EmitDefaultValue = false)] public GLTFTextureInfo tireMudCutoutTexture;
		[DataMember(EmitDefaultValue = false)] public GLTFNormalTextureInfo tireMudNormalTexture;

		[DataMember(EmitDefaultValue = false)] public float? tireMudNormalTiling { get; set; }
		[DataMember(EmitDefaultValue = true)] public float? tireMudAnimState { get; set; }
		[DataMember(EmitDefaultValue = true)] public float? tireDustAnimState { get; set; }

		public static class Defaults
		{
			public static readonly float tireMudNormalTiling = 1;
			public static readonly float tireMudAnimState = 0;
			public static readonly float tireDustAnimState = 0;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboSail : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_sail";
		[DataMember(EmitDefaultValue = false)] public float? sailLightAbsorption { get; set; }
		public static class Defaults
		{
			public static readonly float sailLightAbsorption = 1;
		}
	}

	[DataContract]
	class GLTFExtensionAsoboRainOptions : GLTFProperty
	{
		public const string SerializedName = "ASOBO_material_rain_options";
		[DataMember(EmitDefaultValue = false)] public float? rainDropScale { get; set; }
		[DataMember(EmitDefaultValue = false)] public bool? rainDropSide { get; set; }
		public static class Defaults
		{
			public static readonly float rainDropScale = 1;
			public static readonly bool rainDropSide = false;
		}
	}

	static class GLTFExtensionHelper
	{
		public static string Name_MSFT_texture_dds = "MSFT_texture_dds";
	}

	#endregion

	#region Serializable Extras

	public static class FlightSimGLTFExtras
	{
		public static string Name_ASOBO_material_code = "ASOBO_material_code";

		[DataContract]
		public class MaterialCode
		{
			public enum Code
			{
				Windshield,
				Porthole,
				// todo: rename to GeoDecalProgressive or something like that, rather than tying to in-game usage? e.g. same technique could be used for moss/mud/whatever
				GeoDecalFrosted,
				Propeller,
				Tree,
				Vegetation
			}

			public static MaterialCode AsoboPorthole = new MaterialCode(Code.Porthole);
			//public static MaterialCode AsoboGlass = new MaterialCode(Code.Glass);

			// name is the serialized name, dont change
			[DataMember(EmitDefaultValue = false)]
			string ASOBO_material_code;

			public MaterialCode(Code code)
			{
				ASOBO_material_code = code.ToString();
			}
		}
	}

	#endregion

	public enum MaterialType
	{
		Standard,
		GeoDecal,
		GeoDecalFrosted,
		Windshield,
		Porthole,
		Glass,
		ClearCoat,
		ParallaxWindow,
		Anisotropic,
		Hair,
		SSS,
		Invisible,
		FakeTerrain,
		FresnelFade,
		EnvironmentOccluder,
		Ghost,
		GeoDecal_BlendMasked,
		Sail,
		Propeller,
		NotUsed1,
		Tree,
		Vegetation,
		Tire
	};

	public static class FlightSimMaterialHelper
	{
		public static MaterialType GetMaterialType(int materialValue)
		{
			MaterialType result;
			switch (materialValue)
			{
				case 1:
					result = MaterialType.Standard;
					break;
				case 2:
					result = MaterialType.GeoDecal;
					break;
				case 3:
					result = MaterialType.Windshield;
					break;
				case 4:
					result = MaterialType.Porthole;
					break;
				case 5:
					result = MaterialType.Glass;
					break;
				case 6:
					result = MaterialType.GeoDecalFrosted;
					break;
				case 7:
					result = MaterialType.ClearCoat;
					break;
				case 8:
					result = MaterialType.ParallaxWindow;
					break;
				case 9:
					result = MaterialType.Anisotropic;
					break;
				case 10:
					result = MaterialType.Hair;
					break;
				case 11:
					result = MaterialType.SSS;
					break;
				case 12:
					result = MaterialType.Invisible;
					break;
				case 13:
					result = MaterialType.FakeTerrain;
					break;
				case 14:
					result = MaterialType.FresnelFade;
					break;
				case 15:
					result = MaterialType.EnvironmentOccluder;
					break;
				case 16:
					result = MaterialType.Ghost;
					break;
				case 17:
					result = MaterialType.GeoDecal_BlendMasked;
					break;
				case 18:
					result = MaterialType.Sail;
					break;
				case 19:
					result = MaterialType.Propeller;
					break;
				case 20:
					result = MaterialType.NotUsed1;
					break;
				case 21:
					result = MaterialType.Tree;
					break;
				case 22:
					result = MaterialType.Vegetation;
					break;
				case 23:
					result = MaterialType.Tire;
					break;
				default:
					result = MaterialType.Standard;
					break;
			}

			return result;
		}
	}

	public class FlightSimMaterialExtensionExporter : IBabylonMaterialExtensionExporter
	{
		public MaterialUtilities.ClassIDWrapper MaterialClassID
		{
			get { return FlightSimMaterialUtilities.MSFS2024_classID; }
		}
		public string GetGLTFExtensionName()
		{
			return "ASOBO_flightsim_material";
		}
		public ExtendedTypes GetExtendedType()
		{
			ExtendedTypes extendType = new ExtendedTypes(typeof(BabylonMaterial), typeof(GLTFMaterial));
			return extendType;
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			return false;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			var logger = exporter.logger;
			var babylonMaterial = babylonObject as BabylonMaterial;
			var gltfMaterilal = gltfObject as GLTFMaterial;
			if (FlightSimMaterialUtilities.IsMSFS2024Material(babylonMaterial.maxGameMaterial.MaxMaterial))
			{
				string outputFolder = gltf.OutputFolder;
				gltfMaterilal = ExportGLTFMaterial(
					exporter.exportParameters, 
					gltf, 
					babylonMaterial.maxGameMaterial,
					(string sourcePath, string textureName) => { 
						return TextureUtilities.TryWriteImage(outputFolder, sourcePath, textureName, logger, exporterParameters); 
					},
					(string message, Color color) => {
						logger?.RaiseMessage(message, color, 2); 
					},
					(string message) => { 
						logger?.RaiseWarning(message, 2); 
					},
					(string message) => { 
						logger?.RaiseError(message, 2); 
					}
				);

				gltfMaterilal.index = gltf.MaterialsList.Count;
				gltf.MaterialsList.Add(gltfMaterilal);
				gltfObject = (T2)Convert.ChangeType(gltfMaterilal, typeof(T2));
			}
			else if (FlightSimMaterialUtilities.IsMSFS2020Material(babylonMaterial.maxGameMaterial.MaxMaterial))
			{
				string message = $"[GLTFExporter][ERROR][Animation] Material class of {babylonMaterial.name} has been set up with MSFS2020 tools.";
				throw new System.Exception(message);
			}

			return null;
		}


		public FlightSimMaterialExtensionExporter() { }

		ExportParameters exporterParameters;
		GLTF gltf;
		IIGameMaterial maxGameMaterial;
		Func<string, string, string> tryWriteImageFunc;
		Action<string, Color> raiseMessageAction;
		Action<string> raiseWarningAction;
		Action<string> raiseErrorAction;

		Dictionary<string, GLTFImage> srcTextureExportCache = new Dictionary<string, GLTFImage>();
		Dictionary<string, string> dstTextureExportCache = new Dictionary<string, string>();

		void RaiseMessage(string message) { RaiseMessage(message, Color.CornflowerBlue); }
		void RaiseMessage(string message, Color color) { raiseMessageAction?.Invoke(message, color); }
		void RaiseWarning(string message) { raiseWarningAction?.Invoke(message); }
		void RaiseError(string message) { raiseErrorAction?.Invoke(message); }

		#region Texture Keywords
		// Texture keywords are used to show some warnings if for example an albedo texture has _NORM_ in the name, to help catch issues where textures are used in multiple (incompatible) slots.

		List<string> textureKeywords = new List<string> {
			"_ALBD_",
			"_ALBD.",
			"_ALBEDO_",
			"_ALBEDO.",
			"_COMP_",
			"_COMP.",
			"_NORM_",
			"_NORM.",
			"_NORMAL_",
			"_NORMAL.",
		};

		bool AlbedoTexCheckSuspiciousName(string texturePath)
		{
			string textureName = Path.GetFileName(texturePath).ToUpperInvariant();

			foreach (string textureKeyword in textureKeywords)
			{
				if (textureKeyword.Contains("_ALB"))
					continue;

				if (textureName.Contains(textureKeyword))
				{
					RaiseWarning(string.Format("[GLTFExporter][WARNING][Material] Albedo texture slot uses a texture with keyword '{0}' | {1}", textureKeyword, textureName));
					return true;
				}
			}

			return false;
		}

		bool CompTexCheckSuspiciousName(string texturePath)
		{
			string textureName = Path.GetFileName(texturePath).ToUpperInvariant();

			foreach (string textureKeyword in textureKeywords)
			{
				if (textureKeyword.Contains("_COMP"))
					continue;

				if (textureName.Contains(textureKeyword))
				{
					RaiseWarning(string.Format("[GLTFExporter][WARNING][Material] Occlusion/Roughness/Metallic texture slot uses a texture with keyword '{0}' | {1}", textureKeyword, textureName));
					return true;
				}
			}

			return false;
		}

		bool NormalTexCheckSuspiciousName(string texturePath)
		{
			string textureName = Path.GetFileName(texturePath).ToUpperInvariant();

			foreach (string textureKeyword in textureKeywords)
			{
				if (textureKeyword.Contains("_NORM"))
					continue;

				if (textureName.Contains(textureKeyword))
				{
					RaiseWarning(string.Format("[GLTFExporter][WARNING][Material] Normal texture slot uses a texture with keyword '{0}' | {1}", textureKeyword, textureName));
					return true;
				}
			}

			return false;
		}

		#endregion

		GLTFMaterial ExportGLTFMaterial(ExportParameters exportParameters, GLTF gltf, IIGameMaterial maxGameMaterial,
			Func<string, string, string> tryWriteImageFunc,
			Action<string, Color> raiseMessageAction,
			Action<string> raiseWarningAction,
			Action<string> raiseErrorAction)
		{
			// if the gltf class instance is different, this is a new export
			if (this.gltf != gltf)
			{
				srcTextureExportCache.Clear();
				dstTextureExportCache.Clear();
			}

			// save parameters
			this.exporterParameters = exportParameters;
			this.gltf = gltf;
			this.maxGameMaterial = maxGameMaterial;
			this.tryWriteImageFunc = tryWriteImageFunc;
			this.raiseMessageAction = raiseMessageAction;
			this.raiseWarningAction = raiseWarningAction;
			this.raiseErrorAction = raiseErrorAction;

			GLTFMaterial gltfMaterial = new GLTFMaterial();
			gltfMaterial.name = maxGameMaterial.MaterialName;
			gltfMaterial.id = maxGameMaterial.MaxMaterial.GetGuid().ToString();

			ProcessMaterialProperties(gltfMaterial, maxGameMaterial);

			return gltfMaterial;

			// to get an overview, for debug purposes
			/*
			int numProps = material.IPropertyContainer.NumberOfProperties;
			IIGameProperty[] properties = new IIGameProperty[numProps];
			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = material.IPropertyContainer.GetProperty(i);
				properties[i] = property;
			}

			int numParamBlocks = material.MaxMaterial.NumParamBlocks;
			IIParamBlock2[] paramBlocks = new IIParamBlock2[numParamBlocks];
			for(int i = 0; i < numParamBlocks; ++i)
			{
				IIParamBlock2 paramBlock = material.MaxMaterial.GetParamBlock(i);
				paramBlocks[i] = paramBlock;
			}
			*/
		}



		void ProcessMaterialProperties(GLTFMaterial material, IIGameMaterial maxMaterial)
		{
			#region Helper Variables

			int int_out = 0;
			float float_out = 0.0f;
			string string_out = ""; // passing in a null string causes a null-reference exception, even though strings are immutable anyway
			IPoint4 point4_out = Loader.Global.Point4.Create();
			IPoint3 p3_out = Loader.Global.Point3.Create();

			GLTFImage image;
			GLTFTextureInfo info;

			// Define some variables for the GetPropertyValue parameters.
			// http://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__cpp_ref_class_i_game_property_html
			//
			// The time to retrieve the value, defaulted to the static frame.
			// set to 0 in the exporter with Loader.Global.IGameInterface.SetStaticFrame
			int param_t = 0;
			//
			// The flag indicating if percent fraction value (TYPE_PCNT_FRAC) should be converted (0.1 to 10), default:false 
			bool param_p = false;

			float emisMultiplayer = 1;

			#endregion

			// Iterate over all properties and find what we want by string.
			// This way, it doesn't matter in which param rollout the property is defined.
			// This gives us a little more flexibility in the MaxScript material definition.
			//
			// Some parameters only have to be set if we have a texture:
			// - normal scale
			// - occlusion strength
			// Some parameters only have to be set if we have a specific alphaMode:
			// - alphaCutoff
			//
			// Thus, two for loops!
			// 1. process textures and alphamode
			// 2. the remaining parameters

			int numProps = maxMaterial.IPropertyContainer.NumberOfProperties;

			// cache some extension property values (conditional exports)
			float[] layerColor = new float[] { 1, 1, 1, 1 };
			string layerColorTexPath = null;
			string layerColorMaskPath = null;

			float detailUVScale = GLTFExtensionAsoboMaterialDetail.Defaults.UVScale;
			float blendThreshold = GLTFExtensionAsoboMaterialDetail.Defaults.blendThreshold;
			float detailNormalScale = GLTFExtensionAsoboMaterialDetail.Defaults.NormalScale;
			string detailColorTexPath = null;
			string detailNormalTexPath = null;
			string detailMetalRoughAOTexPath = null;
			string blendMaskTexPath = null;

			float[] SSSColor = null;
			string opacityTexPath = null;

			string foliageMaskTexPath = null;

			string tireDetailsTexPath = null;
			string tireMudNormalTexPath = null;
			float tireMudNormalTiling = GLTFExtensionAsoboFlightSimTire.Defaults.tireMudNormalTiling;
			float tireMudAnimState = GLTFExtensionAsoboFlightSimTire.Defaults.tireMudAnimState;
			float tireDustAnimState = GLTFExtensionAsoboFlightSimTire.Defaults.tireDustAnimState;

			string anisoDirectionRoughnessTexPath = null;

			string clearcoatColorRoughnessPath = null;
			string clearcoatNormalTexPath = null;
			float? clearcoatRoughnessFactor = null;
			float? clearcoatNormalFactor = null;
			float? clearcoatColorRoughnessTiling = null;
			float? clearcoatNormalTiling = null;
			bool? clearcoatInverseRoughness = null;
			float? clearcoatBaseRoughness = null;

			float detail1Rough = GLTFExtensionAsoboWindshield.Defaults.detail1Rough;
			float detail2Rough = GLTFExtensionAsoboWindshield.Defaults.detail2Rough;
			float detail1Opacity = GLTFExtensionAsoboWindshield.Defaults.detail1Opacity;
			float detail2Opacity = GLTFExtensionAsoboWindshield.Defaults.detail2Opacity;
			float microScratchesTiling = GLTFExtensionAsoboWindshield.Defaults.microScratchesTiling;
			float microScratchesStrength = GLTFExtensionAsoboWindshield.Defaults.microScratchesStrength;
			float detailNormalRefractScale = GLTFExtensionAsoboWindshield.Defaults.detailNormalRefractScale;
			bool windshieldReceiveRain = GLTFExtensionAsoboWindshield.Defaults.receiveRain;
			bool wiperLines = GLTFExtensionAsoboWindshield.Defaults.wiperLines;
			float wiperLinesTiling = GLTFExtensionAsoboWindshield.Defaults.wiperLinesTiling;
			float wiperLinesStrength = GLTFExtensionAsoboWindshield.Defaults.wiperLinesStrength;
			float windshieldRainDropScale = GLTFExtensionAsoboWindshield.Defaults.rainDropScale;
			float wiperState1 = GLTFExtensionAsoboWindshield.Defaults.wiper1State;
			string wiperMaskTexPath = null;
			string windshieldDetailNormalTexPath = null;
			string scratchesNormalTexPath = null;
			string windshieldInsectsTexPath = null;
			string windshieldInsectsMaskTexPath = null;

			float parallaxScale = GLTFExtensionAsoboParallaxWindow.Defaults.parallaxScale;
			float roomSizeXScale = GLTFExtensionAsoboParallaxWindow.Defaults.roomSizeXScale;
			float roomSizeYScale = GLTFExtensionAsoboParallaxWindow.Defaults.roomSizeYScale;
			float roomNumberXY = GLTFExtensionAsoboParallaxWindow.Defaults.roomNumberXY;
			bool corridor = GLTFExtensionAsoboParallaxWindow.Defaults.corridor;
			string behindWindowMapTexPath = null;

			float fresnelFactor = GLTFExtensionAsoboMaterialFresnelFade.Defaults.fresnelFactor;
			float fresnelOpacityOffset = GLTFExtensionAsoboMaterialFresnelFade.Defaults.fresnelOpacityOffset;

			float ghostPower = GLTFExtensionAsoboMaterialGhostEffect.Defaults.power;
			float ghostBias = GLTFExtensionAsoboMaterialGhostEffect.Defaults.bias;
			float ghostScale = GLTFExtensionAsoboMaterialGhostEffect.Defaults.scale;

			float glassWidth = GLTFExtensionAsoboFlightSimGlass_v2.Defaults.glassWidth;

			float sailLightAbsorption = GLTFExtensionAsoboSail.Defaults.sailLightAbsorption;

			bool receiveRain = false;
			float rainDropScale = GLTFExtensionAsoboRainOptions.Defaults.rainDropScale;
			bool rainDropSide = GLTFExtensionAsoboRainOptions.Defaults.rainDropSide;

			bool clampUVX = GLTFExtensionAsoboMaterialUVOptions.Defaults.clampUVX;
			bool clampUVY = GLTFExtensionAsoboMaterialUVOptions.Defaults.clampUVY;
			bool clampUVZ = GLTFExtensionAsoboMaterialUVOptions.Defaults.clampUVZ;
			float uvOffsetU = GLTFExtensionAsoboMaterialUVOptions.Defaults.UVOffsetU;
			float uvOffsetV = GLTFExtensionAsoboMaterialUVOptions.Defaults.UVOffsetV;
			float uvTilingU = GLTFExtensionAsoboMaterialUVOptions.Defaults.UVTilingU;
			float uvTilingV = GLTFExtensionAsoboMaterialUVOptions.Defaults.UVTilingV;
			float uvRotation = GLTFExtensionAsoboMaterialUVOptions.Defaults.UVRotation;

			int drawOrderOffset = GLTFExtensionAsoboMaterialDrawOrder.Defaults.drawOrderOffset;
			bool dayNightCycle = false;
			bool disableMotionBlur = true;
			bool flipBackFace = false;
			bool pearlescent = false;
			float pearlShift = GLTFExtensionAsoboPearlescent.Defaults.pearlShift;
			float pearlRange = GLTFExtensionAsoboPearlescent.Defaults.pearlRange;
			float pearlBrightness = GLTFExtensionAsoboPearlescent.Defaults.pearlBrightness;

			bool iridescent = false;
			float iridescentMinThickness = GLTFExtensionAsoboIridescent.Defaults.iridescentMinThickness;
			float iridescentMaxThickness = GLTFExtensionAsoboIridescent.Defaults.iridescentMaxThickness;
			float iridescentBrightness = GLTFExtensionAsoboIridescent.Defaults.iridescentBrightness;
			string iridescentThicknessTexPath = null;

			float occlusionStregth = GLTFExtensionAsoboOcclusionStrength.Defaults.strength;

			bool dirt = false;
			string dirtTexPath = null;
			string dirtOcclusionRoughnessMetallicTexPath = null;
			float dirtUvScale = GLTFExtensionAsoboMaterialDirt.Defaults.dirtUvScale;
			float dirtBlendSharpness = GLTFExtensionAsoboMaterialDirt.Defaults.dirtBlendSharpness;
			float dirtBlendAmount = GLTFExtensionAsoboMaterialDirt.Defaults.dirtBlendAmount;

			#region Material Type (Standard, Decal, Windshield, ...)
			// - Standard
			// - GBuffer Blend
			// - Windshield

			// only create if needed
			GLTFExtensionAsoboMaterialGeometryDecal decalExtensionObject = null;
			GLTFExtensionAsoboMaterialFakeTerrain fakeTerrainExtensionObject = null;
			GLTFExtensionAsoboMaterialInvisible invisibleExtensionObject = null;
			GLTFExtensionAsoboMaterialEnvironmentOccluder environmentOccluderExtensionObject = null;

			GLTFExtensions materialExtensions = new GLTFExtensions();
			GLTFExtensions materialExtras = new GLTFExtensions();

			// material flag is checked for setting specific defaults and other special cases
			// e.g. windshield is always using AlphaMode.BLEND for compatibility with gltf viewers (it's ignored engine side)
			MaterialType materialType = MaterialType.Standard;

			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
				string propertyName = property.Name.ToUpperInvariant();

				switch (propertyName)
				{
					case "MATERIALTYPE":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
								RaiseError("[GLTFExporter][ERROR][Material] Could not retrieve MATERIALTYPE property.");

							materialType = FlightSimMaterialHelper.GetMaterialType(int_out);
							switch (materialType)
							{
								case MaterialType.Standard:
									break;
								case MaterialType.GeoDecal:
									decalExtensionObject = new GLTFExtensionAsoboMaterialGeometryDecal();
									decalExtensionObject.mode = "default";
									break;
								case MaterialType.GeoDecalFrosted:
									decalExtensionObject = new GLTFExtensionAsoboMaterialGeometryDecal();
									decalExtensionObject.mode = "frosted";
									break;
								case MaterialType.Windshield:
									break;
								case MaterialType.Porthole:
									materialExtras.Add(FlightSimGLTFExtras.Name_ASOBO_material_code, FlightSimGLTFExtras.MaterialCode.Code.Porthole.ToString());
									break;
								case MaterialType.Glass:
									break;
								case MaterialType.ClearCoat:
									break;
								case MaterialType.ParallaxWindow:
									break;
								case MaterialType.Ghost:
									break;
								case MaterialType.GeoDecal_BlendMasked:
									decalExtensionObject = new GLTFExtensionAsoboMaterialGeometryDecal();
									decalExtensionObject.mode = "blendMasked";
									break;
								case MaterialType.Anisotropic:
									break;
								case MaterialType.Hair:
									break;
								case MaterialType.SSS:
									break;
								case MaterialType.Invisible:
									invisibleExtensionObject = new GLTFExtensionAsoboMaterialInvisible();
									break;
								case MaterialType.FakeTerrain:
									fakeTerrainExtensionObject = new GLTFExtensionAsoboMaterialFakeTerrain();
									break;
								case MaterialType.FresnelFade:
									break;
								case MaterialType.EnvironmentOccluder:
									environmentOccluderExtensionObject = new GLTFExtensionAsoboMaterialEnvironmentOccluder();
									break;
								case MaterialType.Sail:
									break;
								case MaterialType.Propeller:
									materialExtras.Add(FlightSimGLTFExtras.Name_ASOBO_material_code, FlightSimGLTFExtras.MaterialCode.Code.Propeller.ToString());
									break;
								case MaterialType.Tree:
									materialExtras.Add(FlightSimGLTFExtras.Name_ASOBO_material_code, FlightSimGLTFExtras.MaterialCode.Code.Tree.ToString());
									break;
								case MaterialType.Vegetation:
									materialExtras.Add(FlightSimGLTFExtras.Name_ASOBO_material_code, FlightSimGLTFExtras.MaterialCode.Code.Vegetation.ToString());
									break;
								case MaterialType.Tire:
									break;
								default:
									break;
							}

							RaiseMessage(string.Format("[GLTFExporter][Material] Exporting Material Type: \"{0}\"", materialType.ToString()));
							break;
						}
				}
			}

			#endregion

			#region Decal Extension properties
			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
				string propertyName = property.Name.ToUpperInvariant();
				if (decalExtensionObject != null)
				{
					switch (propertyName)
					{
						case "DECALCOLORFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALCOLORFACTOR property.");
									continue;
								}
								decalExtensionObject.SetBaseColorBlendFactor(float_out);
								break;
							}
						case "DECALROUGHNESSFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALROUGHNESSFACTOR property.");
									continue;
								}
								decalExtensionObject.SetRoughnessBlendFactor(float_out);
								break;
							}
						case "DECALMETALFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALMETALFACTOR property.");
									continue;
								}
								decalExtensionObject.SetMetallicBlendFactor(float_out);
								break;
							}
						case "DECALNORMALFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALNORMALFACTOR property.");
									continue;
								}
								decalExtensionObject.SetNormalBlendFactor(float_out);
								break;
							}
						case "DECALEMISSIVEFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALEMISSIVEFACTOR property.");
									continue;
								}
								decalExtensionObject.SetEmissiveBlendFactor(float_out);
								break;
							}
						case "DECALOCCLUSIONFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALOCCLUSIONFACTOR property.");
									continue;
								}
								decalExtensionObject.SetOcclusionBlendFactor(float_out);
								break;
							}
						case "DECALBLENDSHARPNESSFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALBLENDSHARPNESSFACTOR property.");
									continue;
								}
								decalExtensionObject.SetBlendSharpnessFactor(float_out);
								break;
							}
						case "DECALNORMALOVERRIDEFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALNORMALOVERRIDEFACTOR property.");
									continue;
								}
								decalExtensionObject.SetNormalOverrideFactor(float_out);
								break;
							}
						case "DECALRENDERONCLEARCOAT":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Decal] Could not retrieve DECALRENDERONCLEARCOAT property.");
									continue;
								}
								decalExtensionObject.SetUnderClearcoat(int_out == 0);
								break;
							}
					}
				}
			}

			#endregion

			#region base dirt
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();
					switch (propertyName)
					{
						case "DIRTTEX":
							{
								dirtTexPath = GetImagePath(paramDef, property, param_t, "DIRTTEX");
								if (dirtTexPath != null) dirt = int_out != 0;
								break;
							}
						case "DIRTOCCLUSIONROUGHNESSMETALLICTEX":
							{
								dirtOcclusionRoughnessMetallicTexPath = GetImagePath(paramDef, property, param_t, "DIRTOCCLUSIONROUGHNESSMETALLICTEX");
								if (dirtOcclusionRoughnessMetallicTexPath != null) RaiseError("Dirt overlay requires an Occlusion Roughness Metallic texture.");
								break;
							}
						case "DIRTUVSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("Could not retrieve DIRTUVSCALE property.");
									continue;
								}
								dirtUvScale = float_out;
								break;
							}
						case "DIRTBLENDSHARPNESS":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("Could not retrieve DIRTBLENDSHARPNESS property.");
									continue;
								}
								dirtBlendSharpness = float_out;
								break;
							}
						case "DIRTBLENDAMOUNT":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("Could not retrieve DIRTBLENDAMOUNT property.");
									continue;
								}
								dirtBlendAmount = float_out;
								break;
							}
					}
				}
			}

			#endregion

			#region WindShield
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "WIPERMASKTEX":
							{
								wiperMaskTexPath = GetImagePath(paramDef, property, param_t, "WIPERMASKTEX");
								break;
							}
						case "WINDSHIELDDETAILNORMALTEX":
							{
								windshieldDetailNormalTexPath = GetImagePath(paramDef, property, param_t, "WINDSHIELDDETAILNORMALTEX");
								break;
							}
						case "SCRATCHESNORMALTEX":
							{
								scratchesNormalTexPath = GetImagePath(paramDef, property, param_t, "SCRATCHESNORMALTEX");
								break;
							}
						case "WINDSHIELDINSECTSTEX":
							{
								windshieldInsectsTexPath = GetImagePath(paramDef, property, param_t, "WINDSHIELDINSECTSTEX");
								break;
							}
						case "WINDSHIELDINSECTSMASKTEX":
							{
								windshieldInsectsMaskTexPath = GetImagePath(paramDef, property, param_t, "WINDSHIELDINSECTSMASKTEX");
								break;
							}
						case "DETAIL1ROUGH":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve DETAIL1ROUGH property.");
									continue;
								}
								detail1Rough = float_out;
								break;
							}
						case "DETAIL2ROUGH":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve DETAIL2ROUGH property.");
									continue;
								}
								detail2Rough = float_out;
								break;
							}
						case "DETAIL1OPACITY":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve DETAIL1OPACITY property.");
									continue;
								}
								detail1Opacity = float_out;
								break;
							}
						case "DETAIL2OPACITY":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve DETAIL2OPACITY property.");
									continue;
								}
								detail2Opacity = float_out;
								break;
							}
						case "MICROSCRATCHESTILING":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve MICROSCRATCHESTILING property.");
									continue;
								}
								microScratchesTiling = float_out;
								break;
							}
						case "MICROSCRATCHESSTRENGTH":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve MICROSCRATCHESSTRENGTH property.");
									continue;
								}
								microScratchesStrength = float_out;
								break;
							}
						case "DETAILNORMALREFRACTSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve DETAILNORMALREFRACTSCALE property.");
									continue;
								}
								detailNormalRefractScale = float_out;
								break;
							}
						case "CANRECEIVERAIN":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve CANRECEIVERAIN property.");
									continue;
								}
								windshieldReceiveRain = (int_out != 0);
								break;
							}
						case "WIPERLINES":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve WIPERLINES property.");
									continue;
								}
								wiperLines = (int_out != 0);
								break;
							}
						case "WIPERLINESTILING":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve WIPERLINESTILING property.");
									continue;
								}
								wiperLinesTiling = float_out;
								break;
							}
						case "WIPERLINESSTRENGTH":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve WIPERLINESSTRENGTH property.");
									continue;
								}
								wiperLinesStrength = float_out;
								break;
							}
						case "RAINDROPSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve RAINDROPSCALE property.");
									continue;
								}
								windshieldRainDropScale = float_out;
								break;
							}
						case "WIPERANIMSTATE1":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][WindShield] Could not retrieve WIPERANIMSTATE property.");
									continue;
								}
								wiperState1 = float_out;
								break;
							}
						case "DIRTBLENDAMOUNT":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Standard or CleaCoat] Could not retrieve WIPERANIMSTATE property.");
									continue;
								}
								dirtBlendAmount = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region Tree
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "FOLIAGEMASKTEX":
							{
								foliageMaskTexPath = GetImagePath(paramDef, property, param_t, "FOLIAGEMASKTEX");
								break;
							}
					}
				}
			}
			#endregion

			#region Detail Map Extension Properties

			// allow for all material types, for now
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "DETAILCOLORTEX":
							{
								if (materialType != MaterialType.ParallaxWindow)
								{
									detailColorTexPath = GetImagePath(paramDef, property, param_t, "DETAILCOLORTEX");
								}
								break;
							}
						case "DETAILNORMALTEX":
							{
								detailNormalTexPath = GetImagePath(paramDef, property, param_t, "DETAILNORMALTEX");
								break;
							}
						case "DETAILOCCLUSIONROUGHNESSMETALLICTEX":
							{
								detailMetalRoughAOTexPath = GetImagePath(paramDef, property, param_t, "DETAILOCCLUSIONROUGHNESSMETALLICTEX");
								break;
							}
						case "BLENDMASKTEX":
							{
								blendMaskTexPath = GetImagePath(paramDef, property, param_t, "BLENDMASKTEX");
								break;
							}
						case "DETAILUVSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][DetailMap] Could not retrieve DETAILUVSCALE property.");
									continue;
								}
								detailUVScale = float_out;
								break;
							}
						case "BLENDTHRESHOLD":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][DetailMap] Could not retrieve BLENDTHRESHOLD property.");
									continue;
								}
								blendThreshold = float_out;
								break;
							}
						case "DETAILNORMALSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][DetailMap] Could not retrieve DETAILNORMALSCALE property.");
									continue;
								}
								detailNormalScale = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region SSS Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "SSSCOLOR":
							{
								if (!property.GetPropertyValue(point4_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][SSS] Could not retrieve SSSCOLOR property.");
									continue;
								}
								if (point4_out[0] == GLTFExtensionAsoboSSS.Defaults.SSSColor[0] &&
									point4_out[1] == GLTFExtensionAsoboSSS.Defaults.SSSColor[1] &&
									point4_out[2] == GLTFExtensionAsoboSSS.Defaults.SSSColor[2]
									)
									SSSColor = null;
								else
									SSSColor = new float[] { point4_out[0], point4_out[1], point4_out[2] };
								break;
							}
						case "OPACITYTEX":
							{
								opacityTexPath = GetImagePath(paramDef, property, param_t, "OPACITYTEX");
								break;
							}
					}
				}
			}
			#endregion

			#region Parallax Window Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "PARALLAXSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ParallaxWindow] Could not retrieve PARALLAXSCALE property.");
									continue;
								}
								parallaxScale = float_out;
								break;
							}
						case "ROOMSIZEXSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ParallaxWindow] Could not retrieve ROOMSIZEXSCALE property.");
									continue;
								}
								roomSizeXScale = float_out;
								break;
							}
						case "ROOMSIZEYSCALE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ParallaxWindow] Could not retrieve ROOMSIZEYSCALE property.");
									continue;
								}
								roomSizeYScale = float_out;
								break;
							}
						case "ROOMNUMBERXY":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ParallaxWindow] Could not retrieve ROOMNUMBERXY property.");
									continue;
								}
								roomNumberXY = float_out;
								break;
							}
						case "CORRIDOR":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ParallaxWindow] Could not retrieve CORRIDOR property.");
									continue;
								}
								corridor = (int_out != 0);
								break;
							}
						case "DETAILCOLORTEX": //because we reuse the slot from the detailmap
							{
								behindWindowMapTexPath = GetImagePath(paramDef, property, param_t, "DETAILCOLORTEX");
								break;
							}
					}
				}
			}
			#endregion

			#region Anisotropic Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "ANISODIRECTIONROUGHNESSTEX":
							{
								anisoDirectionRoughnessTexPath = GetImagePath(paramDef, property, param_t, "ANISODIRECTIONROUGHNESSTEX");
								break;
							}
					}
				}
			}
			#endregion

			#region Glass Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "GLASSWIDTH":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Glass] Could not retrieve GLASSWIDTH property.");
									continue;
								}
								glassWidth = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region FresnelFade Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "FRESNELFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][FresnelFade] Could not retrieve FRESNELFACTOR property.");
									continue;
								}
								fresnelFactor = float_out;
								break;
							}
						case "FRESNELOPACITYOFFSET":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][FresnelFade] Could not retrieve FRESNELOPACITYOFFSET property.");
									continue;
								}
								fresnelOpacityOffset = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region GhostEffect Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "GHOSTBIASFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][GhostEffect] Could not retrieve GHOSTBIASFACTOR property.");
									continue;
								}
								ghostBias = float_out;
								break;
							}
						case "GHOSTSCALEFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][GhostEffect] Could not retrieve GHOSTSCALEFACTOR property.");
									continue;
								}
								ghostScale = float_out;
								break;
							}
						case "GHOSTPOWERFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][GhostEffect] Could not retrieve GHOSTPOWERFACTOR property.");
									continue;
								}
								ghostPower = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region ClearCoat_v2 Extension Properties
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "CLEARCOATCOLORROUGHNESSTEX":
							{
								clearcoatColorRoughnessPath = GetImagePath(paramDef, property, param_t, "CLEARCOATCOLORROUGHNESSTEX");
								break;
							}
						case "CLEARCOATNORMALTEX":
							{
								clearcoatNormalTexPath = GetImagePath(paramDef, property, param_t, "CLEARCOATNORMALTEX");
								break;
							}
						case "CLEARCOATROUGHNESSFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ClearCoat_v2] Could not retrieve CLEARCOATROUGHNESSFACTOR property.");
									continue;
								}
								if (float_out != GLTFExtensionAsoboClearCoat_v2.Defaults.clearcoatRoughnessFactor)
									clearcoatRoughnessFactor = float_out;
								break;
							}
						case "CLEARCOATNORMALFACTOR":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ClearCoat_v2] Could not retrieve CLEARCOATNORMALFACTOR property.");
									continue;
								}
								if (float_out != GLTFExtensionAsoboClearCoat_v2.Defaults.clearcoatNormalFactor)
									clearcoatNormalFactor = float_out;
								break;
							}
						case "CLEARCOATCOLORROUGHNESSTILING":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ClearCoat_v2] Could not retrieve CLEARCOATCOLORROUGHNESSTILING property.");
									continue;
								}
								if (float_out != GLTFExtensionAsoboClearCoat_v2.Defaults.clearcoatColorRoughnessTiling)
									clearcoatColorRoughnessTiling = float_out;
								break;
							}
						case "CLEARCOATNORMALTILING":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ClearCoat_v2] Could not retrieve CLEARCOATNORMALTILING property.");
									continue;
								}
								if (float_out != GLTFExtensionAsoboClearCoat_v2.Defaults.clearcoatNormalTiling)
									clearcoatNormalTiling = float_out;
								break;
							}
						case "CLEARCOATINVERSEROUGHNESS":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ClearCoat_v2] Could not retrieve CLEARCOATINVERSEROUGHNESS property.");
									continue;
								}
								if ((int_out != 0) != GLTFExtensionAsoboClearCoat_v2.Defaults.clearcoatInverseRoughness)
									clearcoatInverseRoughness = (int_out != 0);
								break;
							}
						case "CLEARCOATBASEROUGHNESS":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ClearCoat_v2] Could not retrieve CLEARCOATBASEROUGHNESS property.");
									continue;
								}
								if (float_out != GLTFExtensionAsoboClearCoat_v2.Defaults.clearcoatBaseRoughness)
									clearcoatBaseRoughness = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region OcclusionStrength
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "OCCLUSIONSTRENGTH":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][OcclusionStrength] Could not retrieve OCCLUSIONSTRENGTH property.");
									continue;
								}
								occlusionStregth = float_out;
								if (occlusionStregth != GLTFExtensionAsoboOcclusionStrength.Defaults.strength)
								{
									GLTFExtensionAsoboOcclusionStrength occlusionStrengthObject = new GLTFExtensionAsoboOcclusionStrength();
									occlusionStrengthObject.strength = occlusionStregth;
									materialExtensions.Add(GLTFExtensionAsoboOcclusionStrength.SerializedName, occlusionStrengthObject);
								}
								break;
							}
					}
				}
			}
			#endregion

			#region Draw Order
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "DRAWORDER":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][DrawOrder] Could not retrieve DRAWORDER property.");
									continue;
								}
								int drawOrder = int_out;
								if (drawOrder != 0)
								{
									GLTFExtensionAsoboMaterialDrawOrder drawOrderExtensionObject = new GLTFExtensionAsoboMaterialDrawOrder();
									drawOrderExtensionObject.drawOrderOffset = drawOrder;
									materialExtensions.Add(GLTFExtensionAsoboMaterialDrawOrder.SerializedName, drawOrderExtensionObject);
								}
								break;
							}
					}
				}
			}
			#endregion

			#region UV Options
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "CLAMPUVX":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve CLAMPUVX property.");
									continue;
								}
								clampUVX = (int_out != 0);
								break;
							}
						case "CLAMPUVY":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve CLAMPUVY property.");
									continue;
								}
								clampUVY = (int_out != 0);
								break;
							}
						case "CLAMPUVZ":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve CLAMPUVZ property.");
									continue;
								}
								clampUVZ = (int_out != 0);
								break;
							}
						case "UVOFFSETU":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve UVOFFSETU property.");
									continue;
								}
								uvOffsetU = float_out;
								break;
							}
						case "UVOFFSETV":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve UVOFFSETV property.");
									continue;
								}
								uvOffsetV = float_out;
								break;
							}
						case "UVTILINGU":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve UVTILINGU property.");
									continue;
								}
								uvTilingU = float_out;
								break;
							}
						case "UVTILINGV":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve UVTILINGV property.");
									continue;
								}
								uvTilingV = float_out;
								break;
							}
						case "UVROTATION":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][UVOptions] Could not retrieve UVROTATION property.");
									continue;
								}
								uvRotation = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region Collision&Road
			{
				GLTFExtensionAsoboTags asoboTagsExtensionObject = new GLTFExtensionAsoboTags();
				asoboTagsExtensionObject.tags = new List<string>();
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();


					switch (propertyName)
					{

						case "COLLISIONMATERIAL":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Collision&Road] Could not retrieve COLLISIONMATERIAL property.");
									continue;
								}
								bool collisionMaterial = (int_out != 0);
								if (collisionMaterial)
								{
									if (!asoboTagsExtensionObject.tags.Contains(AsoboTag.Collision.ToString()))
									{
										asoboTagsExtensionObject.tags.Add(AsoboTag.Collision.ToString());
									}
								}
								break;
							}
						case "ROADMATERIAL":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Collision&Road] Could not retrieve ROADMATERIAL property.");
									continue;
								}
								bool roadMaterial = (int_out != 0);
								if (roadMaterial)
								{
									if (!asoboTagsExtensionObject.tags.Contains(AsoboTag.Road.ToString()))
									{
										asoboTagsExtensionObject.tags.Add(AsoboTag.Road.ToString());
									}
								}
								break;
							}
					}
				}
				if (asoboTagsExtensionObject.tags.Count > 0)
				{
					if (!materialExtensions.ContainsKey(GLTFExtensionAsoboTags.SerializedName))
					{
						materialExtensions.Add(GLTFExtensionAsoboTags.SerializedName, asoboTagsExtensionObject);
					}
				}
			}
			#endregion

			#region ResponsiveAA Options
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "RESPONSIVEAA":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ResponsiveAA] Could not retrieve RESPONSIVEAA property.");
									continue;
								}
								bool responsiveAA = (int_out != 0);
								if (responsiveAA)
								{
									GLTFExtensionAsoboMaterialResponsiveAAOptions responsiveAaOptionMaterialExtensionObject = new GLTFExtensionAsoboMaterialResponsiveAAOptions();
									responsiveAaOptionMaterialExtensionObject.responsiveAA = responsiveAA;
									materialExtensions.Add(GLTFExtensionAsoboMaterialResponsiveAAOptions.SerializedName, responsiveAaOptionMaterialExtensionObject);
								}
								break;
							}
					}
				}
			}
			#endregion

			#region Shadow Options
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "NOCASTSHADOW":
							{
								if (!property.GetPropertyValue(ref int_out, param_t))
								{
									RaiseError("[GLTFExporter][ERROR][Material][ShadowOptions] Could not retrieve NOCASTSHADOW property.");
									continue;
								}
								bool noCastShadow = (int_out != 0);
								if (noCastShadow)
								{
									GLTFExtensionAsoboMaterialShadowOptions shadowOptionMaterialExtensionObject = new GLTFExtensionAsoboMaterialShadowOptions();
									shadowOptionMaterialExtensionObject.noCastShadow = noCastShadow;
									materialExtensions.Add(GLTFExtensionAsoboMaterialShadowOptions.SerializedName, shadowOptionMaterialExtensionObject);
								}
								break;
							}
					}
				}
			}
			#endregion

			#region Textures & AlphaMode

			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
				string propertyName = property.Name.ToUpperInvariant();

				switch (propertyName)
				{
					case "ALPHAMODE":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][AlphaMode] Could not retrieve ALPHAMODE property.");
								continue;
							}

							// overrides for specific material types
							if (materialType == MaterialType.GeoDecal || materialType == MaterialType.Windshield || materialType == MaterialType.Glass || materialType == MaterialType.GeoDecalFrosted || materialType == MaterialType.GeoDecal_BlendMasked)
								material.SetAlphaMode(GLTFMaterial.AlphaMode.BLEND.ToString());
							else if (materialType == MaterialType.Porthole)
								material.SetAlphaMode(GLTFMaterial.AlphaMode.OPAQUE.ToString());
							else if (materialType == MaterialType.Propeller)
								material.SetAlphaMode(GLTFMaterial.AlphaMode.OPAQUE.ToString());
							else
							{
								int alphaMode = int_out - 1;
								if (alphaMode == 3)
								{
									alphaMode = (int)GLTFMaterial.AlphaMode.BLEND;
									GLTFExtensionAsoboAlphaModeDither ditherExtensionObject = new GLTFExtensionAsoboAlphaModeDither();
									materialExtensions.Add(GLTFExtensionAsoboAlphaModeDither.SerializedName, ditherExtensionObject);
								}
								else if (alphaMode > 3 || alphaMode < 0)
								{
									alphaMode = (int)GLTFMaterial.AlphaMode.OPAQUE;
									RaiseWarning("[GLTFExporter][WARNING][Material][AlphaMode] Unknown alpha mode: exporting OPAQUE");
								}
								else material.SetAlphaMode(((GLTFMaterial.AlphaMode)(alphaMode)).ToString());
							}
							break;
						}
					case "BASECOLORTEX":
						{
							string_out = GetImagePath(paramDef, property, param_t, "BASECOLORTEX");
							image = ExportImage(string_out);
							if (image == null)
								continue;

							AlbedoTexCheckSuspiciousName(string_out);
							info = CreateTextureInfo(image);
							material.SetBaseColorTexture(info);

							break;
						}
					case "LAYERCOLORTEX":
						{
							layerColorTexPath = GetImagePath(paramDef, property, param_t, "LAYERCOLORTEX");
							break;
						}
					case "LAYERMASKTEX":
						{
							layerColorMaskPath = GetImagePath(paramDef, property, param_t, "LAYERMASKTEX");
							break;
						}
					case "OCCLUSIONROUGHNESSMETALLICTEX":
						{
							string_out = GetImagePath(paramDef, property, param_t, "OCCLUSIONROUGHNESSMETALLICTEX");
							image = ExportImage(string_out);
							if (image == null)
								continue;

							CompTexCheckSuspiciousName(string_out);
							info = CreateTextureInfo(image);
							material.SetMetallicRoughnessTexture(info);
							material.SetOcclusionTexture(info);

							break;
						}
					case "OCCLUSIONTEX":
						{
							string_out = GetImagePath(paramDef, property, param_t, "OCCLUSIONTEX");
							image = ExportImage(string_out);
							if (image == null)
								continue;

							if (IsPropertyImageExist(maxMaterial, "OCCLUSIONROUGHNESSMETALLICTEX", param_t))
							{
								// Occlusion UV1 already set in ORM, set Occlusion UV2 in extraOcclusionTexture
								GLTFOcclusionTextureInfo extraOccInfo = CreateTextureInfo<GLTFOcclusionTextureInfo>(image);
								extraOccInfo.texCoord = 1;

								GLTFExtensionAsoboExtraOcclusion extraOcc = new GLTFExtensionAsoboExtraOcclusion();
								extraOcc.extraOcclusionTexture = extraOccInfo;

								materialExtensions.Add(GLTFExtensionAsoboExtraOcclusion.SerializedName, extraOcc);
							}
							else
							{
								// Occlusion UV1 not set in ORM, set Occlusion UV2 in OcclusionTexture
								info = CreateTextureInfo<GLTFOcclusionTextureInfo>(image);
								info.texCoord = 1;
								material.SetOcclusionTexture(info);
							}

							break;
						}
					case "NORMALTEX":
						{
							string_out = GetImagePath(paramDef, property, param_t, "NORMALTEX");
							image = ExportImage(string_out);
							if (image == null)
								continue;

							NormalTexCheckSuspiciousName(string_out);
							info = CreateTextureInfo<GLTFNormalTextureInfo>(image);
							material.SetNormalTexture(info);

							break;
						}
					case "EMISSIVETEX":
						{
							string_out = GetImagePath(paramDef, property, param_t, "EMISSIVETEX");
							image = ExportImage(string_out);
							if (image == null)
								continue;

							info = CreateTextureInfo(image);
							material.SetEmissiveTexture(info);

							break;
						}
				}
			}

			#endregion

			#region Pearlescent

			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
				string propertyName = property.Name.ToUpperInvariant();
				switch (propertyName)
				{
					case "PEARLESCENT":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve PEARLESCENT property.");
								continue;
							}
							pearlescent = int_out != 0;
							break;
						}
					case "PEARLSHIFT":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve PEARLSHIFT property.");
								continue;
							}
							pearlShift = float_out;
							break;
						}
					case "PEARLRANGE":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve PEARLRANGE property.");
								continue;
							}
							pearlRange = float_out;
							break;
						}
					case "PEARLBRIGHTNESS":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve PEARLBRIGHTNESS property.");
								continue;
							}
							pearlBrightness = float_out;
							break;
						}
				}
			}

			#endregion

			#region Iridescent

			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
				string propertyName = property.Name.ToUpperInvariant();
				switch (propertyName)
				{
					case "IRIDESCENT":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve IRIDESCENT property.");
								continue;
							}
							iridescent = int_out != 0;
							break;
						}
					case "IRIDESCENTMINTHICKNESS":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve IRIDESCENTMINTHICKNESS property.");
								continue;
							}
							iridescentMinThickness = float_out;
							break;
						}
					case "IRIDESCENTMAXTHICKNESS":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve IRIDESCENTMAXTHICKNESS property.");
								continue;
							}
							iridescentMaxThickness = float_out;
							break;
						}
					case "IRIDESCENTBRIGHTNESS":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Pearlescent] Could not retrieve IRIDESCENTBRIGHTNESS property.");
								continue;
							}
							iridescentBrightness = float_out;
							break;
						}
					case "IRIDESCENTTHICKNESSTEX":
						{
							iridescentThicknessTexPath = GetImagePath(paramDef, property, param_t, "IRIDESCENTTHICKNESSTEX");
							break;
						}
				}
			}

			#endregion

			#region Sail

			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				string propertyName = property.Name.ToUpperInvariant();
				switch (propertyName)
				{
					case "SAILLIGHTABSORPTION":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Sail] Could not retrieve SAILLIGHTABSORPTION property.");
								continue;
							}
							sailLightAbsorption = float_out;
							break;
						}
				}
			}

			#endregion

			#region Rain

			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;

				string propertyName = property.Name.ToUpperInvariant();
				switch (propertyName)
				{
					case "CANRECEIVERAIN":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Rain] Could not retrieve CANRECEIVERAIN property.");
								continue;
							}
							receiveRain = (int_out != 0);
							break;
						}
					case "RAINDROPSCALE":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Rain] Could not retrieve RAINDROPSCALE property.");
								continue;
							}
							rainDropScale = float_out;
							break;
						}
					case "RAINDROPSIDE":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Rain] Could not retrieve RAINDROPSIDE property.");
								continue;
							}
							rainDropSide = (int_out != 0);
							break;
						}
				}
			}

			#endregion

			#region Vegetation
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "FOLIAGEMASKTEX":
							{
								foliageMaskTexPath = GetImagePath(paramDef, property, param_t, "FOLIAGEMASKTEX");
								break;
							}
					}
				}
			}
			#endregion

			#region Tire
			{
				for (int i = 0; i < numProps; ++i)
				{
					IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

					if (property == null)
						continue;

					IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
					string propertyName = property.Name.ToUpperInvariant();

					switch (propertyName)
					{
						case "TIREDETAILSTEX":
							{
								tireDetailsTexPath = GetImagePath(paramDef, property, param_t, "TIREDETAILSTEX");
								break;
							}
						case "TIREMUDNORMALTEX":
							{
								tireMudNormalTexPath = GetImagePath(paramDef, property, param_t, "TIREMUDNORMALTEX");
								break;
							}
						case "TIREMUDNORMALTILING":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Tire] Could not retrieve TIREMUDNORMALTILING property.");
									continue;
								}
								tireMudNormalTiling = float_out;
								break;
							}
						case "TIREMUDANIMSTATE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Tire] Could not retrieve TIREMUDANIMSTATE property.");
									continue;
								}
								tireMudAnimState = float_out;
								break;
							}
						case "TIREDUSTANIMSTATE":
							{
								if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								{
									RaiseError("[GLTFExporter][ERROR][Material][Tire] Could not retrieve TIREDUSTANIMSTATE property.");
									continue;
								}
								tireDustAnimState = float_out;
								break;
							}
					}
				}
			}
			#endregion

			#region The Other Parameters



			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;
				string propertyName = property.Name.ToUpperInvariant();


				switch (propertyName)
				{
					case "BASECOLOR":
						{
							if (!property.GetPropertyValue(point4_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve BASECOLOR property.");
								continue;
							}
							material.SetBaseColorFactor(point4_out.X, point4_out.Y, point4_out.Z);

							if (invisibleExtensionObject != null)
								material.SetBaseColorFactorAlpha(0.7f);
							else
								material.SetBaseColorFactorAlpha(point4_out.W);

							break;
						}
					case "LAYERCOLOR":
						{
							if (!property.GetPropertyValue(point4_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve LAYERCOLOR property.");
								continue;
							}
							for (int c = 0; c < 4; ++c)
								layerColor[c] = point4_out[c];

							break;
						}
					case "EMISSIVEMUL":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve emissiveMul property.");
								continue;
							}
							emisMultiplayer = float_out;
							break;
						}
					case "ROUGHNESS":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve ROUGHNESS property.");
								continue;
							}
							material.SetRoughnessFactor(float_out);
							break;
						}
					case "METALLIC":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve METALLIC property.");
								continue;
							}
							material.SetMetallicFactor(float_out);
							break;
						}
					case "NORMALSCALE":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve NORMALSCALE property.");
								continue;
							}

							// only set if normal texture is defined
							GLTFNormalTextureInfo normalTexture = material.normalTexture as GLTFNormalTextureInfo;
							if (normalTexture == null)
								continue;

							material.SetNormalScale(float_out);
							break;
						}
					case "AO":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve AO property.");

							// only set if occlusion texture is defined
							GLTFOcclusionTextureInfo occlusionTexture = material.occlusionTexture as GLTFOcclusionTextureInfo;
							if (occlusionTexture == null)
								continue;

							material.SetOcclusionStrength(float_out);
							break;
						}
					case "ALPHACUTOFF":
						{
							if (!property.GetPropertyValue(ref float_out, param_t, param_p))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve ALPHACUTOFF property.");
								continue;
							}

							// only set if alphamode == mask
							if (material.alphaMode == GLTFMaterial.AlphaMode.MASK.ToString())
							{
								material.SetAlphaCutoff(float_out);
							}
							break;
						}
					case "DOUBLESIDED":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve DOUBLESIDED property.");
								continue;
							}

							material.SetDoubleSided(int_out != 0);
							break;
						}
					case "DAYNIGHTCYCLE":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve DAYNIGHTCYCLE property.");
								continue;
							}
							dayNightCycle = int_out != 0;
							break;
						}
					case "DISABLEMOTIONBLUR":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve DISABLEMOTIONBLUR property.");
								continue;
							}
							disableMotionBlur = int_out != 0;
							break;
						}
					case "FLIPBACKFACE":
						{
							if (!property.GetPropertyValue(ref int_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Others] Could not retrieve FLIPBACKFACE property.");
								continue;
							}
							flipBackFace = int_out != 0;
							break;
						}
				}
			}

			#region ComputeEmissive
			for (int i = 0; i < numProps; ++i)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);

				if (property == null)
					continue;
				string propertyName = property.Name.ToUpperInvariant();


				switch (propertyName)
				{
					case "EMISSIVE":
						{
							if (!property.GetPropertyValue(point4_out, param_t))
							{
								RaiseError("[GLTFExporter][ERROR][Material][Emissive] Could not retrieve EMISSIVE property.");
								continue;
							}
							material.SetEmissiveFactor(point4_out.X * emisMultiplayer, point4_out.Y * emisMultiplayer, point4_out.Z * emisMultiplayer);

							break;
						}
				}
			}
			#endregion
			#endregion


			#region Process Extension Objects

			GLTFExtensionAsoboRainOptions rainOptionsExtensionObject = null;
			if (materialType == MaterialType.ClearCoat)
			{
				if (receiveRain)
				{
					rainOptionsExtensionObject = new GLTFExtensionAsoboRainOptions();

					if (rainDropScale != GLTFExtensionAsoboRainOptions.Defaults.rainDropScale)
						rainOptionsExtensionObject.rainDropScale = rainDropScale;
				}
			}

			if (materialType == MaterialType.Windshield)
			{
				if (receiveRain)
				{
					rainOptionsExtensionObject = new GLTFExtensionAsoboRainOptions();

					if (rainDropScale != GLTFExtensionAsoboRainOptions.Defaults.rainDropScale)
						rainOptionsExtensionObject.rainDropScale = rainDropScale;
					if (rainDropSide != GLTFExtensionAsoboRainOptions.Defaults.rainDropSide)
						rainOptionsExtensionObject.rainDropSide = rainDropSide;
				}
			}

			GLTFExtensionAsoboPearlescent pearlescentOptionsExtensionObject = null;
			if (materialType == MaterialType.Standard)
			{
				if (pearlescent)
				{
					pearlescentOptionsExtensionObject = new GLTFExtensionAsoboPearlescent();

					pearlescentOptionsExtensionObject.pearlShift = pearlShift;
					pearlescentOptionsExtensionObject.pearlRange = pearlRange;
					pearlescentOptionsExtensionObject.pearlBrightness = pearlBrightness;
				}
			}

			GLTFExtensionAsoboIridescent iridescentExtensionObject = null;
			if (materialType == MaterialType.Windshield)
			{
				if (iridescent)
				{
					iridescentExtensionObject = new GLTFExtensionAsoboIridescent();

					if (iridescentMinThickness != GLTFExtensionAsoboIridescent.Defaults.iridescentMinThickness)
						iridescentExtensionObject.iridescentMinThickness = iridescentMinThickness;
					if (iridescentMaxThickness != GLTFExtensionAsoboIridescent.Defaults.iridescentMaxThickness)
						iridescentExtensionObject.iridescentMaxThickness = iridescentMaxThickness;
					if (iridescentBrightness != GLTFExtensionAsoboIridescent.Defaults.iridescentBrightness)
						iridescentExtensionObject.iridescentBrightness = iridescentBrightness;

					if (!string.IsNullOrWhiteSpace(iridescentThicknessTexPath))
					{
						image = ExportImage(iridescentThicknessTexPath, true);
						if (image != null)
						{
							info = CreateTextureInfo(image);
							iridescentExtensionObject.iridescentThicknessTexture = info;
						}
					}
				}
			}

			GLTFExtensionAsoboDayNightCycle dayNightOptionsExtensionObject = null;
			GLTFExtensionAsoboMaterialDirt dirtOptionsExtensionObject = null;
			if ((materialType == MaterialType.Standard || materialType == MaterialType.ClearCoat))
			{
				if (dirt)
				{
					dirtOptionsExtensionObject = new GLTFExtensionAsoboMaterialDirt();
					if (!string.IsNullOrWhiteSpace(dirtTexPath))
					{
						image = ExportImage(dirtTexPath, true);
						if (image != null)
						{
							info = CreateTextureInfo(image);
							dirtOptionsExtensionObject.dirtTexture = info;
						}
					}
					if (!string.IsNullOrWhiteSpace(dirtOcclusionRoughnessMetallicTexPath))
					{
						image = ExportImage(dirtOcclusionRoughnessMetallicTexPath, true);
						if (image != null)
						{
							info = CreateTextureInfo(image);
							dirtOptionsExtensionObject.dirtOcclusionRoughnessMetallicTexture = info;
						}
					}
					if (dirtUvScale != 1.0) dirtOptionsExtensionObject.dirtUvScale = dirtUvScale;
					if (dirtBlendSharpness != 0.0) dirtOptionsExtensionObject.dirtBlendSharpness = dirtBlendSharpness;
					dirtOptionsExtensionObject.dirtBlendAmount = dirtBlendAmount;
				}
				if (dayNightCycle)
				{
					dayNightOptionsExtensionObject = new GLTFExtensionAsoboDayNightCycle();
				}
			}

			GLTFExtensionAsoboDisableMotionBlur disableMotionBlurExtensionObject = null;
			if (disableMotionBlur)
			{
				disableMotionBlurExtensionObject = new GLTFExtensionAsoboDisableMotionBlur();
			}

			GLTFExtensionAsoboFlipBackFace flipBackFaceExtensionObject = null;
			if (flipBackFace && materialType != MaterialType.Sail && materialType != MaterialType.EnvironmentOccluder && material.doubleSided)
			{
				flipBackFaceExtensionObject = new GLTFExtensionAsoboFlipBackFace();
			}

			GLTFExtensionAsoboAnisotropic_v2 anisotropicExtensionObject = null;
			if (!string.IsNullOrWhiteSpace(anisoDirectionRoughnessTexPath) && (materialType == MaterialType.Anisotropic || materialType == MaterialType.Hair))
			{
				anisotropicExtensionObject = new GLTFExtensionAsoboAnisotropic_v2();

				image = ExportImage(anisoDirectionRoughnessTexPath, true);
				if (image != null)
				{
					info = CreateTextureInfo(image);
					anisotropicExtensionObject.anisoDirectionRoughnessTexture = info;
				}
			}

			// Tree extension only if there is Foliage Mask Texture Applied
			GLTFExtensionAsoboFlightSimTree treeExtensionObject = null;
			if (materialType == MaterialType.Tree)
			{
				// Tree extension
				if (!string.IsNullOrWhiteSpace(foliageMaskTexPath))
				{
					treeExtensionObject = new GLTFExtensionAsoboFlightSimTree();
					image = ExportImage(foliageMaskTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						treeExtensionObject.foliageMaskTexture = info;
					}
				}

			}

			// Vegetation extension only if there is Foliage Mask Texture Applied and Vegetation material type
			GLTFExtensionAsoboFlightSimVegetation vegetationExtensionObject = null;
			if (materialType == MaterialType.Vegetation)
			{
				vegetationExtensionObject = new GLTFExtensionAsoboFlightSimVegetation();
				if (!string.IsNullOrWhiteSpace(foliageMaskTexPath))
				{
					image = ExportImage(foliageMaskTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						vegetationExtensionObject.foliageMaskTexture = info;
					}
				}
			}

			// Tire extension only if materialType is tire
			GLTFExtensionAsoboFlightSimTire tireExtensionObject = null;
			if (materialType == MaterialType.Tire)
			{
				tireExtensionObject = new GLTFExtensionAsoboFlightSimTire();
				if (!string.IsNullOrWhiteSpace(tireDetailsTexPath))
				{
					image = ExportImage(tireDetailsTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						tireExtensionObject.tireDetailsTexture = info;
					}
				}

				// tireDetails is required to export tireMudNormal
				if (!string.IsNullOrWhiteSpace(tireMudNormalTexPath) && tireExtensionObject.tireDetailsTexture != null)
				{
					image = ExportImage(tireMudNormalTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo<GLTFNormalTextureInfo>(image);
						tireExtensionObject.tireMudNormalTexture = (GLTFNormalTextureInfo)info;
					}
				}

				tireExtensionObject.tireMudNormalTiling = tireMudNormalTiling;
				tireExtensionObject.tireMudAnimState = tireMudAnimState;
				tireExtensionObject.tireDustAnimState = tireDustAnimState;
			}

			// Windshield extension, only if it's a WINDSHIELD material
			GLTFExtensionAsoboWindshield windshieldExtensionObject = null;
			if (materialType == MaterialType.Windshield)
			{
				windshieldExtensionObject = new GLTFExtensionAsoboWindshield();

				if (windshieldReceiveRain != GLTFExtensionAsoboWindshield.Defaults.receiveRain)
					windshieldExtensionObject.receiveRain = windshieldReceiveRain;
				// if receiveRain is true 
				if (windshieldExtensionObject.receiveRain == null)
				{
					if (windshieldRainDropScale != GLTFExtensionAsoboWindshield.Defaults.rainDropScale)
						windshieldExtensionObject.rainDropScale = windshieldRainDropScale;
				}
				if (wiperLines != GLTFExtensionAsoboWindshield.Defaults.wiperLines)
					windshieldExtensionObject.wiperLines = wiperLines;
				// if wiperLines is true and they're is a wiperMask texture
				if (windshieldExtensionObject.wiperLines == true && wiperMaskTexPath != null)
				{
					if (wiperLinesTiling != GLTFExtensionAsoboWindshield.Defaults.wiperLinesTiling)
						windshieldExtensionObject.wiperLinesTiling = wiperLinesTiling;
					if (wiperLinesStrength != GLTFExtensionAsoboWindshield.Defaults.wiperLinesStrength)
						windshieldExtensionObject.wiperLinesStrength = wiperLinesStrength;
				}
				if (detail1Rough != GLTFExtensionAsoboWindshield.Defaults.detail1Rough)
					windshieldExtensionObject.detail1Rough = detail1Rough;
				if (detail2Rough != GLTFExtensionAsoboWindshield.Defaults.detail2Rough)
					windshieldExtensionObject.detail2Rough = detail2Rough;
				if (detail1Opacity != GLTFExtensionAsoboWindshield.Defaults.detail1Opacity)
					windshieldExtensionObject.detail1Opacity = detail1Opacity;
				if (detail2Opacity != GLTFExtensionAsoboWindshield.Defaults.detail2Opacity)
					windshieldExtensionObject.detail2Opacity = detail2Opacity;
				if (microScratchesTiling != GLTFExtensionAsoboWindshield.Defaults.microScratchesTiling)
					windshieldExtensionObject.microScratchesTiling = microScratchesTiling;
				if (microScratchesStrength != GLTFExtensionAsoboWindshield.Defaults.microScratchesStrength)
					windshieldExtensionObject.microScratchesStrength = microScratchesStrength;
				if (detailNormalRefractScale != GLTFExtensionAsoboWindshield.Defaults.detailNormalRefractScale)
					windshieldExtensionObject.detailNormalRefractScale = detailNormalRefractScale;
				windshieldExtensionObject.wiper1State = wiperState1;


				if (!string.IsNullOrWhiteSpace(wiperMaskTexPath))
				{
					image = ExportImage(wiperMaskTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						windshieldExtensionObject.wiperMaskTexture = info;
					}
				}

				if (!string.IsNullOrWhiteSpace(windshieldDetailNormalTexPath))
				{
					image = ExportImage(windshieldDetailNormalTexPath);
					if (image != null)
					{
						NormalTexCheckSuspiciousName(windshieldDetailNormalTexPath);
						info = CreateTextureInfo<GLTFNormalTextureInfo>(image);
						windshieldExtensionObject.windshieldDetailNormalTexture = (GLTFNormalTextureInfo)info;

						if (detailNormalScale != GLTFExtensionAsoboMaterialDetail.Defaults.NormalScale)
							windshieldExtensionObject.windshieldDetailNormalTexture.scale = detailNormalScale;
					}
				}

				if (!string.IsNullOrWhiteSpace(scratchesNormalTexPath))
				{
					image = ExportImage(scratchesNormalTexPath);
					if (image != null)
					{
						NormalTexCheckSuspiciousName(scratchesNormalTexPath);
						info = CreateTextureInfo<GLTFNormalTextureInfo>(image);
						windshieldExtensionObject.scratchesNormalTexture = (GLTFNormalTextureInfo)info;
					}
				}

				if (!string.IsNullOrWhiteSpace(windshieldInsectsTexPath))
				{
					image = ExportImage(windshieldInsectsTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						windshieldExtensionObject.windshieldInsectsTexture = info;

						// Only export WindShieldInsectsMask if WindShieldInsects exist
						if (!string.IsNullOrWhiteSpace(windshieldInsectsMaskTexPath))
						{
							image = ExportImage(windshieldInsectsMaskTexPath, true);
							if (image != null)
							{
								info = CreateTextureInfo(image);
								windshieldExtensionObject.windshieldInsectsMaskTexture = info;
							}
						}
					}
				}
			}

			// SSS extension, no Opacity map (sampler name in engine) assigned, just need the SSS material or the Hair Material
			GLTFExtensionAsoboSSS SSSExtensionObject = null;
			if (materialType == MaterialType.SSS || materialType == MaterialType.Hair)
			{
				SSSExtensionObject = new GLTFExtensionAsoboSSS
				{
					SSSColor = SSSColor
				};

				if (!string.IsNullOrWhiteSpace(opacityTexPath))
				{
					image = ExportImage(opacityTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						SSSExtensionObject.opacityTexture = info;
					}
				}
			}

			// Parallax Window extension, no HeightMap (sampler name in engine) assigned, just need the parallax window material
			GLTFExtensionAsoboParallaxWindow parallaxWindowExtensionObject = null;
			if (materialType == MaterialType.ParallaxWindow)
			{
				parallaxWindowExtensionObject = new GLTFExtensionAsoboParallaxWindow
				{
					parallaxScale = parallaxScale,
					roomSizeXScale = roomSizeXScale,
					roomSizeYScale = roomSizeYScale,
					roomNumberXY = roomNumberXY,
					corridor = corridor
				};

				if (!string.IsNullOrWhiteSpace(behindWindowMapTexPath))
				{
					image = ExportImage(behindWindowMapTexPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						parallaxWindowExtensionObject.behindWindowMapTexture = info;
					}
				}
			}

			// UV Option extension
			GLTFExtensionAsoboMaterialUVOptions UVOptionsExtensionObject = null;
			if (clampUVX || clampUVY || clampUVZ || (uvOffsetU != 0 || uvOffsetV != 0) || (uvTilingU != 1 || uvTilingV != 1) || uvRotation != 0)
			{
				UVOptionsExtensionObject = new GLTFExtensionAsoboMaterialUVOptions
				{
					clampUVX = clampUVX,
					clampUVY = clampUVY,
					clampUVZ = clampUVZ,
					UVOffsetU = uvOffsetU,
					UVOffsetV = uvOffsetV,
					UVTilingU = uvTilingU,
					UVTilingV = uvTilingV,
					UVRotation = uvRotation
				};
			}

			// fresnel extension
			GLTFExtensionAsoboMaterialFresnelFade fresnelFadeExtensionObject = null;
			if (materialType == MaterialType.FresnelFade)
			{
				fresnelFadeExtensionObject = new GLTFExtensionAsoboMaterialFresnelFade
				{
					fresnelFactor = fresnelFactor,
					fresnelOpacityOffset = fresnelOpacityOffset
				};
			}

			// ghost extension
			GLTFExtensionAsoboMaterialGhostEffect ghostExtensionObject = null;
			if (materialType == MaterialType.Ghost)
			{
				ghostExtensionObject = new GLTFExtensionAsoboMaterialGhostEffect
				{
					bias = ghostBias,
					power = ghostPower,
					scale = ghostScale
				};
			}

			// FlightSim extension, replacing glass extra, set by FlightSimGlass OR glass material
			GLTFExtensionAsoboFlightSimGlass_v2 flightSimGlassExtensionObject = null;
			if (materialType == MaterialType.Glass)
			{
				flightSimGlassExtensionObject = new GLTFExtensionAsoboFlightSimGlass_v2
				{
					glassWidth = glassWidth
				};
			}

			// Sail Extension, require Sail material
			GLTFExtensionAsoboSail sailExtensionObject = null;
			if (materialType == MaterialType.Sail)
			{
				sailExtensionObject = new GLTFExtensionAsoboSail();
				if (sailLightAbsorption != GLTFExtensionAsoboSail.Defaults.sailLightAbsorption)
					sailExtensionObject.sailLightAbsorption = sailLightAbsorption;
			}

			//Clear Coat 2 extension, require a Clear Coat material
			GLTFExtensionAsoboClearCoat_v2 clearCoat_v2ExtensionObject = null;
			if (materialType == MaterialType.ClearCoat)
			{
				clearCoat_v2ExtensionObject = new GLTFExtensionAsoboClearCoat_v2();

				if (clearcoatInverseRoughness == false || clearcoatInverseRoughness == null)
				{
					image = ExportImage(clearcoatColorRoughnessPath, true);
					if (image != null)
					{
						info = CreateTextureInfo(image);
						clearCoat_v2ExtensionObject.clearcoatColorRoughnessTexture = info;
					}
				}

				image = ExportImage(clearcoatNormalTexPath, true);
				if (image != null)
				{
					info = CreateTextureInfo<GLTFNormalTextureInfo>(image);
					clearCoat_v2ExtensionObject.clearcoatNormalTexture = (GLTFNormalTextureInfo)info;
				}

				if (clearcoatRoughnessFactor != null)
					clearCoat_v2ExtensionObject.clearcoatRoughnessFactor = clearcoatRoughnessFactor;
				if (clearcoatNormalFactor != null)
					clearCoat_v2ExtensionObject.clearcoatNormalFactor = clearcoatNormalFactor;
				if (clearcoatColorRoughnessTiling != null)
					clearCoat_v2ExtensionObject.clearcoatColorRoughnessTiling = clearcoatColorRoughnessTiling;
				if (clearcoatNormalTiling != null)
					clearCoat_v2ExtensionObject.clearcoatNormalTiling = clearcoatNormalTiling;
				if (clearcoatInverseRoughness != null)
					clearCoat_v2ExtensionObject.clearcoatInverseRoughness = clearcoatInverseRoughness;
				if (clearcoatBaseRoughness != null && clearcoatInverseRoughness == true)
					clearCoat_v2ExtensionObject.clearcoatBaseRoughness = clearcoatBaseRoughness;
			}

			// detail map extension, only if we have a detail color and/or detail normal map AND there is no a parallaxWindow extension
			GLTFExtensionAsoboMaterialDetail detailExtensionObject = null;
			if (materialType != MaterialType.ParallaxWindow)
			{
				if (!string.IsNullOrWhiteSpace(detailColorTexPath) || !string.IsNullOrWhiteSpace(detailNormalTexPath) || !string.IsNullOrWhiteSpace(detailMetalRoughAOTexPath) || !string.IsNullOrWhiteSpace(blendMaskTexPath))
				{
					detailExtensionObject = new GLTFExtensionAsoboMaterialDetail();
					if (!string.IsNullOrWhiteSpace(detailColorTexPath))
					{
						image = ExportImage(detailColorTexPath);
						if (image != null)
						{
							AlbedoTexCheckSuspiciousName(detailColorTexPath);
							info = CreateTextureInfo(image);
							detailExtensionObject.detailColorTexture = info;
						}
					}
					if (!string.IsNullOrWhiteSpace(detailNormalTexPath))
					{
						image = ExportImage(detailNormalTexPath);
						if (image != null)
						{
							NormalTexCheckSuspiciousName(detailNormalTexPath);
							info = CreateTextureInfo<GLTFNormalTextureInfo>(image);
							detailExtensionObject.detailNormalTexture = (GLTFNormalTextureInfo)info;

							if (detailNormalScale != GLTFExtensionAsoboMaterialDetail.Defaults.NormalScale)
								detailExtensionObject.detailNormalTexture.scale = detailNormalScale;
						}
					}
					if (!string.IsNullOrWhiteSpace(detailMetalRoughAOTexPath))
					{
						image = ExportImage(detailMetalRoughAOTexPath);
						if (image != null)
						{
							CompTexCheckSuspiciousName(detailMetalRoughAOTexPath);
							info = CreateTextureInfo(image);
							detailExtensionObject.detailMetalRoughAOTexture = info;
						}
					}
					if (!string.IsNullOrWhiteSpace(blendMaskTexPath) 
						&& materialType != MaterialType.GeoDecal_BlendMasked
						&& materialType != MaterialType.Tire) // blendmasked use as TireMudCutout in material Tire
					{
						image = ExportImage(blendMaskTexPath);
						if (image != null)
						{
							info = CreateTextureInfo(image);
							detailExtensionObject.blendMaskTexture = info;
						}
					}

					if (detailUVScale != GLTFExtensionAsoboMaterialDetail.Defaults.UVScale)
						detailExtensionObject.UVScale = detailUVScale;

					if (blendThreshold != GLTFExtensionAsoboMaterialDetail.Defaults.blendThreshold)
						detailExtensionObject.blendThreshold = blendThreshold;

				}
			}

			// GeoDecal Blend Masked map extension, only if we have a blend mask assigned and material type is GeoDecal_BlendMasked
			if (!string.IsNullOrWhiteSpace(blendMaskTexPath) && (materialType == MaterialType.GeoDecal_BlendMasked))
			{
				image = ExportImage(blendMaskTexPath, true);
				if (image != null)
				{
					info = CreateTextureInfo(image);
					decalExtensionObject.blendMaskTexture = info;
				}
			}

			// Tire Mud Cutout map extension, only if we have a blend mask assigned and material type is Tire
			if (!string.IsNullOrWhiteSpace(blendMaskTexPath) && (materialType == MaterialType.Tire))
			{
				image = ExportImage(blendMaskTexPath, true);
				if (image != null)
				{
					info = CreateTextureInfo(image);
					tireExtensionObject.tireMudCutoutTexture = info;
				}
			}

			#endregion

			#region Post-processing

			// add used extensions to dictionaries
			if (dayNightOptionsExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboDayNightCycle.SerializedName, dayNightOptionsExtensionObject);

			if (disableMotionBlurExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboDisableMotionBlur.SerializedName, disableMotionBlurExtensionObject);

			if (flipBackFaceExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboFlipBackFace.SerializedName, flipBackFaceExtensionObject);

			if (rainOptionsExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboRainOptions.SerializedName, rainOptionsExtensionObject);

			if (pearlescentOptionsExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboPearlescent.SerializedName, pearlescentOptionsExtensionObject);

			if (iridescentExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboIridescent.SerializedName, iridescentExtensionObject);

			if (decalExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialGeometryDecal.SerializedName, decalExtensionObject);

			if (dirtOptionsExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialDirt.SerializedName, dirtOptionsExtensionObject);

			if (detailExtensionObject != null && parallaxWindowExtensionObject == null) //we add an detail extension object only if there is no parallaxWindowExtension
				materialExtensions.Add(GLTFExtensionAsoboMaterialDetail.SerializedName, detailExtensionObject);

			if (SSSExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboSSS.SerializedName, SSSExtensionObject);

			if (anisotropicExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboAnisotropic_v2.SerializedName, anisotropicExtensionObject);

			if (windshieldExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboWindshield.SerializedName, windshieldExtensionObject);

			if (vegetationExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboFlightSimVegetation.SerializedName, vegetationExtensionObject);

			if (treeExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboFlightSimTree.SerializedName, treeExtensionObject);

			if (tireExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboFlightSimTire.SerializedName, tireExtensionObject);

			if (clearCoat_v2ExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboClearCoat_v2.SerializedName, clearCoat_v2ExtensionObject);

			if (parallaxWindowExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboParallaxWindow.SerializedName, parallaxWindowExtensionObject);

			if (flightSimGlassExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboFlightSimGlass_v2.SerializedName, flightSimGlassExtensionObject);

			if (ghostExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialGhostEffect.SerializedName, ghostExtensionObject);

			if (invisibleExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialInvisible.SerializedName, invisibleExtensionObject);

			if (fakeTerrainExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialFakeTerrain.SerializedName, fakeTerrainExtensionObject);

			if (fresnelFadeExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialFresnelFade.SerializedName, fresnelFadeExtensionObject);

			if (UVOptionsExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialUVOptions.SerializedName, UVOptionsExtensionObject);

			if (environmentOccluderExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboMaterialEnvironmentOccluder.SerializedName, environmentOccluderExtensionObject);

			if (sailExtensionObject != null)
				materialExtensions.Add(GLTFExtensionAsoboSail.SerializedName, sailExtensionObject);

			if (materialExtensions.Count > 0)
			{
				material.extensions = materialExtensions;

				// set all extensions as used but not required
				foreach (var pair in material.extensions)
				{
					if (!gltf.extensionsUsed.Contains(pair.Key))
						gltf.extensionsUsed.Add(pair.Key);
				}
			}

			if (materialExtras.Count > 0)
			{
				material.extras = materialExtras;
			}

			#endregion
		}

		bool IsPropertyImageExist(IIGameMaterial maxMaterial, string compareString, int param_t)
		{
			int numProps = maxMaterial.IPropertyContainer.NumberOfProperties;
			for (int i = 0; i < numProps; i++)
			{
				IIGameProperty property = maxMaterial.IPropertyContainer.GetProperty(i);
				if (property == null)
					continue;

				IParamDef paramDef = property.MaxParamBlock2?.GetParamDef(property.ParamID);
				string propertyName = property.Name.ToUpperInvariant();

				if (propertyName == compareString)
				{
					string string_out = GetImagePath(paramDef, property, param_t, compareString);
					if (string_out != null)
						return true;
				}
			}
			return false;
		}

		string GetImagePath(IParamDef paramDef, IIGameProperty property, int param_t, string debugName)
		{
			if (paramDef.Type != ParamType2.Filename)
				RaiseError($"[GLTFExporter][ERROR][Material][Texture] {debugName} is not a Filename property.");
			if (paramDef.AssetTypeId != Autodesk.Max.MaxSDK.AssetManagement.AssetType.BitmapAsset)
				RaiseError($"[GLTFExporter][ERROR][Material][Texture] {debugName} AssetTypeId is not of type BitmapAsset.");

			string string_out = property.MaxParamBlock2?.GetStr(property.ParamID, param_t, 0);
			if (string.IsNullOrWhiteSpace(string_out))
				return null;

			var path = Loader.Global.MaxSDK.Util.Path.Create();
			path.SetPath(string_out);
			string_out = path.ConvertToAbsolute.String;

			if (string.IsNullOrWhiteSpace(string_out))
				return null;

			return string_out;
		}

		GLTFImage ExportImage(string sourceTexturePath, bool allowDDS = false)
		{
			if (string.IsNullOrWhiteSpace(sourceTexturePath))
				return null;

			if (srcTextureExportCache.TryGetValue(sourceTexturePath, out GLTFImage info))
			{
				return info;
			}

			string textureName = Path.GetFileName(sourceTexturePath);
			string validExtension = Path.GetExtension(sourceTexturePath);

			if (validExtension == null || string.IsNullOrEmpty(validExtension))
			{
				RaiseWarning($"[GLTFExporter][WARNING][Material] Texture has an invalid extension: {sourceTexturePath}");
				return null;
			}

			if (dstTextureExportCache.TryGetValue(textureName, out string otherTexturePath))
			{
				RaiseWarning("[GLTFExporter][WARNING][Material] Texture with the exported name already exists and will be re-used or overwritten!");
				RaiseWarning("-> You have referenced a texture with the same name in different folders.");
				RaiseWarning("-- -> Texture: " + textureName);
				RaiseWarning("-- -> Material: " + maxGameMaterial.MaterialName);
				RaiseWarning("-- -> This texture path: " + sourceTexturePath);
				RaiseWarning("-- -> Other texture path: " + otherTexturePath);
			}
			else dstTextureExportCache.Add(textureName, sourceTexturePath);

			info = gltf.AddImage();
			info.uri = PathUtilities.GetRelativePath(exporterParameters.outputPath, sourceTexturePath);
			info.FileExtension = validExtension;

			srcTextureExportCache.Add(sourceTexturePath, info);

			return info;
		}

		GLTFTextureInfo CreateTextureInfo(GLTFImage image, GLTFSampler sampler = null)
		{
			return CreateTextureInfo<GLTFTextureInfo>(image, sampler);
		}
		T CreateTextureInfo<T>(GLTFImage image, GLTFSampler sampler = null) where T : GLTFTextureInfo, new()
		{
			GLTFTexture texture;
			if (image.FileExtension.ToUpperInvariant() == "DDS")
			{
				// texture object without image
				texture = gltf.AddTexture(null, sampler);

				// texture object for dds extension image reference
				GLTFTexture ddsTexture = new GLTFTexture();
				ddsTexture.sampler = sampler?.index;
				ddsTexture.source = image?.index;


				texture.extensions = new GLTFExtensions
				{
					{ GLTFExtensionHelper.Name_MSFT_texture_dds, ddsTexture }
				};

				if (!gltf.extensionsUsed.Contains(GLTFExtensionHelper.Name_MSFT_texture_dds))
					gltf.extensionsUsed.Add(GLTFExtensionHelper.Name_MSFT_texture_dds);
			}
			else
			{
				texture = gltf.AddTexture(image, sampler);
			}

			string imageName = Path.GetFileNameWithoutExtension(image.uri);
			texture.name = imageName;
			return CreateTextureInfo<T>(texture);
		}
		T CreateTextureInfo<T>(int textureIndex) where T : GLTFTextureInfo, new()
		{
			return CreateTextureInfo<T>(gltf.TexturesList[textureIndex]);
		}
		T CreateTextureInfo<T>(GLTFTexture texture) where T : GLTFTextureInfo, new()
		{
			return new T { index = texture.index };
		}
	}

	static class FlightSimClassExtensions
	{
		public static class Defaults
		{
			public static readonly float[] BaseColorFactor = new float[] { 1, 1, 1, 1 };
			public static readonly float[] EmissiveFactor = new float[] { 0, 0, 0 };
			public const float MetallicFactor = 1.0f;
			public const float RoughnessFactor = 1.0f;

			public const float NormalScale = 1.0f;
			public const float OcclusionStrength = 1.0f;

			public const GLTFMaterial.AlphaMode AlphaMode = GLTFMaterial.AlphaMode.OPAQUE;
			public const float AlphaCutoff = 0.5f;
			public const bool DoubleSided = false;

			public const float BaseColorBlendFactor = 1.0f;
			public const float MetallicBlendFactor = 1.0f;
			public const float RoughnessBlendFactor = 1.0f;
			public const float NormalBlendFactor = 1.0f;
			public const float EmissiveBlendFactor = 1.0f;
			public const float OcclusionBlendFactor = 1.0f;

			public const bool UnderClearcoat = true;
		}

		#region GLTFMaterial helper functions
		// Pretty much all material parameters are optional, which means a lot of variables (nested) are null or have null parents before we set them.
		// These functions exist to make this a bit easier to read and use the gltf spec defaults when variables have to be initialized.
		// In addition, we try to minimize what we export by setting variables to null when they're defaults.

		#region Textures

		public static void SetBaseColorTexture(this GLTFMaterial material, GLTFTextureInfo info)
		{
			// it's not so easy to undo the output writing, so don't allow this
			if (material.pbrMetallicRoughness != null && material.pbrMetallicRoughness.baseColorTexture != null)
				throw new InvalidOperationException("Base color texture already set.");

			if (material.pbrMetallicRoughness == null)
				material.pbrMetallicRoughness = new GLTFPBRMetallicRoughness();

			material.pbrMetallicRoughness.baseColorTexture = info;
		}
		public static void SetMetallicRoughnessTexture(this GLTFMaterial material, GLTFTextureInfo info)
		{
			// it's not so easy to undo the output writing, so don't allow this
			if (material.pbrMetallicRoughness != null && material.pbrMetallicRoughness.metallicRoughnessTexture != null)
				throw new InvalidOperationException("occlusion/metallic/roughness texture already set.");

			if (material.pbrMetallicRoughness == null)
				material.pbrMetallicRoughness = new GLTFPBRMetallicRoughness();

			material.pbrMetallicRoughness.metallicRoughnessTexture = info;
		}
		public static void SetEmissiveTexture(this GLTFMaterial material, GLTFTextureInfo info)
		{
			// it's not so easy to undo the output writing, so don't allow this
			if (material.emissiveTexture != null)
				throw new InvalidOperationException("Emissive texture already set.");

			material.emissiveTexture = info ?? throw new ArgumentNullException(nameof(info));
		}
		public static void SetOcclusionTexture(this GLTFMaterial material, GLTFTextureInfo info)
		{
			// it's not so easy to undo the output writing, so don't allow this
			if (material.occlusionTexture != null)
				throw new InvalidOperationException("Occlusion texture already set.");

			material.occlusionTexture = info ?? throw new ArgumentNullException(nameof(info));
		}
		public static void SetNormalTexture(this GLTFMaterial material, GLTFTextureInfo info)
		{
			// it's not so easy to undo the output writing, so don't allow this
			if (material.normalTexture != null)
				throw new InvalidOperationException("Normal texture already set.");

			material.normalTexture = info ?? throw new ArgumentNullException(nameof(info));
		}

		#endregion

		#region Factors

		public static void SetBaseColorFactorAlpha(this GLTFMaterial gltfMaterial, float alpha)
		{
			if (alpha == Defaults.BaseColorFactor[3])
			{
				if (gltfMaterial.pbrMetallicRoughness == null || gltfMaterial.pbrMetallicRoughness.baseColorFactor == null)
					return;

				if (gltfMaterial.pbrMetallicRoughness.baseColorFactor[0] == Defaults.BaseColorFactor[0]
					&& gltfMaterial.pbrMetallicRoughness.baseColorFactor[1] == Defaults.BaseColorFactor[1]
					&& gltfMaterial.pbrMetallicRoughness.baseColorFactor[2] == Defaults.BaseColorFactor[2])
				{
					gltfMaterial.pbrMetallicRoughness.baseColorFactor = null;
					return;
				}
			}

			if (gltfMaterial.pbrMetallicRoughness == null)
				gltfMaterial.pbrMetallicRoughness = new GLTFPBRMetallicRoughness();

			if (gltfMaterial.pbrMetallicRoughness.baseColorFactor == null)
				gltfMaterial.pbrMetallicRoughness.baseColorFactor = new float[] {
					Defaults.BaseColorFactor[0], Defaults.BaseColorFactor[1], Defaults.BaseColorFactor[2], alpha };
			else
				gltfMaterial.pbrMetallicRoughness.baseColorFactor[3] = alpha;
		}
		public static void SetBaseColorFactor(this GLTFMaterial gltfMaterial, float r, float g, float b)
		{
			if (r == Defaults.BaseColorFactor[0] && g == Defaults.BaseColorFactor[1] && b == Defaults.BaseColorFactor[2])
			{
				if (gltfMaterial.pbrMetallicRoughness == null || gltfMaterial.pbrMetallicRoughness.baseColorFactor == null)
					return;

				if (gltfMaterial.pbrMetallicRoughness.baseColorFactor[3] == 1.0f)
				{
					gltfMaterial.pbrMetallicRoughness.baseColorFactor = null;
					return;
				}
			}

			if (gltfMaterial.pbrMetallicRoughness == null)
				gltfMaterial.pbrMetallicRoughness = new GLTFPBRMetallicRoughness();

			if (gltfMaterial.pbrMetallicRoughness.baseColorFactor == null)
				gltfMaterial.pbrMetallicRoughness.baseColorFactor = new float[] { r, g, b, Defaults.BaseColorFactor[3] };
			else
			{
				gltfMaterial.pbrMetallicRoughness.baseColorFactor[0] = r;
				gltfMaterial.pbrMetallicRoughness.baseColorFactor[1] = g;
				gltfMaterial.pbrMetallicRoughness.baseColorFactor[2] = b;
			}
		}
		public static void SetEmissiveFactor(this GLTFMaterial gltfMaterial, float r, float g, float b)
		{
			if (r == Defaults.EmissiveFactor[0] && g == Defaults.EmissiveFactor[1] && b == Defaults.EmissiveFactor[2])
			{
				gltfMaterial.emissiveFactor = null;
				return;
			}

			if (gltfMaterial.emissiveFactor == null)
			{
				gltfMaterial.emissiveFactor = new float[] { r, g, b };
			}
			else
			{
				gltfMaterial.emissiveFactor[0] = r;
				gltfMaterial.emissiveFactor[1] = g;
				gltfMaterial.emissiveFactor[2] = b;
			}
		}
		public static void SetRoughnessFactor(this GLTFMaterial gltfMaterial, float roughness)
		{
			if (roughness == Defaults.RoughnessFactor)
			{
				if (gltfMaterial.pbrMetallicRoughness == null)
					return;

				gltfMaterial.pbrMetallicRoughness.roughnessFactor = null;
				return;
			}

			if (gltfMaterial.pbrMetallicRoughness == null)
				gltfMaterial.pbrMetallicRoughness = new GLTFPBRMetallicRoughness();

			gltfMaterial.pbrMetallicRoughness.roughnessFactor = roughness;
		}
		public static void SetMetallicFactor(this GLTFMaterial gltfMaterial, float metallic)
		{
			if (metallic == Defaults.MetallicFactor)
			{
				if (gltfMaterial.pbrMetallicRoughness == null)
					return;

				gltfMaterial.pbrMetallicRoughness.metallicFactor = null;
				return;
			}

			if (gltfMaterial.pbrMetallicRoughness == null)
				gltfMaterial.pbrMetallicRoughness = new GLTFPBRMetallicRoughness();

			gltfMaterial.pbrMetallicRoughness.metallicFactor = metallic;
		}

		#endregion

		public static void SetNormalScale(this GLTFMaterial gltfMaterial, float normalScale)
		{
			GLTFNormalTextureInfo normalTexture = (GLTFNormalTextureInfo)gltfMaterial.normalTexture;
			normalTexture.scale = normalScale == Defaults.NormalScale ? null : (float?)normalScale;
		}
		public static void SetOcclusionStrength(this GLTFMaterial gltfMaterial, float occlusionStrength)
		{
			GLTFOcclusionTextureInfo occlusionTexture = (GLTFOcclusionTextureInfo)gltfMaterial.occlusionTexture;
			occlusionTexture.strength = occlusionStrength == Defaults.OcclusionStrength ? null : (float?)occlusionStrength;
		}

		public static void SetAlphaCutoff(this GLTFMaterial gltfMaterial, float alphaCutoff)
		{
			gltfMaterial.alphaCutoff = alphaCutoff == Defaults.AlphaCutoff ? null : (float?)alphaCutoff;
		}
		public static void SetAlphaMode(this GLTFMaterial gltfMaterial, string alphaMode)
		{
			gltfMaterial.alphaMode = alphaMode == Defaults.AlphaMode.ToString() ? null : alphaMode;
		}
		public static void SetDoubleSided(this GLTFMaterial gltfMaterial, bool doubleSided)
		{
			gltfMaterial.doubleSided = doubleSided;
		}

		#endregion

		#region Decal Extension helper functions

		public static void SetBaseColorBlendFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == Defaults.BaseColorBlendFactor)
				decalMaterial.baseColorBlendFactor = null;
			else decalMaterial.baseColorBlendFactor = factor;
		}
		public static void SetRoughnessBlendFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == Defaults.RoughnessBlendFactor)
				decalMaterial.roughnessBlendFactor = null;
			else decalMaterial.roughnessBlendFactor = factor;
		}
		public static void SetMetallicBlendFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == Defaults.MetallicBlendFactor)
				decalMaterial.metallicBlendFactor = null;
			else decalMaterial.metallicBlendFactor = factor;
		}
		public static void SetNormalBlendFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == Defaults.NormalBlendFactor)
				decalMaterial.normalBlendFactor = null;
			else decalMaterial.normalBlendFactor = factor;
		}
		public static void SetEmissiveBlendFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == Defaults.EmissiveBlendFactor)
				decalMaterial.emissiveBlendFactor = null;
			else decalMaterial.emissiveBlendFactor = factor;
		}
		public static void SetOcclusionBlendFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == Defaults.OcclusionBlendFactor)
				decalMaterial.occlusionBlendFactor = null;
			else decalMaterial.occlusionBlendFactor = factor;
		}
		public static void SetBlendSharpnessFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == GLTFExtensionAsoboMaterialGeometryDecal.Defaults.blendSharpnessFactor)
				decalMaterial.blendSharpnessFactor = GLTFExtensionAsoboMaterialGeometryDecal.Defaults.blendSharpnessFactor;
			else decalMaterial.blendSharpnessFactor = factor;
		}
		public static void SetNormalOverrideFactor(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, float factor)
		{
			if (factor == GLTFExtensionAsoboMaterialGeometryDecal.Defaults.normalOverrideFactor)
				decalMaterial.normalOverrideFactor = null;
			else decalMaterial.normalOverrideFactor = factor;
		}
		public static void SetUnderClearcoat(this GLTFExtensionAsoboMaterialGeometryDecal decalMaterial, bool underClearcoat)
		{
			if (underClearcoat == Defaults.UnderClearcoat)
				decalMaterial.underClearcoat = null;
			else
				decalMaterial.underClearcoat = underClearcoat;
		}
		#endregion
	}
}