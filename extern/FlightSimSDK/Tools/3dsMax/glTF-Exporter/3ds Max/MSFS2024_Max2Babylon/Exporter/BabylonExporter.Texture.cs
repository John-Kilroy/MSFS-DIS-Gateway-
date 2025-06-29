using System;
using System.Collections.Generic;
using System.IO;
using Autodesk.Max;
using BabylonExport.Entities;
using Utilities;
using System.Drawing;
using System.Drawing.Imaging;

namespace MSFS2024_Max2Babylon
{
	public partial class BabylonExporter
	{
		private static readonly List<string> validFormats = new List<string>(new string[] { "png", "jpg", "jpeg", "tga", "bmp", "gif" });
		private static readonly List<string> invalidFormats = new List<string>(new string[] { "dds", "tif", "tiff" });
		private readonly Dictionary<string, BabylonTexture> textureMap = new Dictionary<string, BabylonTexture>();

		public ITexmap GetSubTexmap(IStdMat2 stdMat, int index)
		{
			if (!stdMat.MapEnabled(index))
			{
				return null;
			}

			return stdMat.GetSubTexmap(index);
		}

		// -------------------------------
		// --- "public" export methods ---
		// -------------------------------

		private BabylonTexture ExportTexture(IStdMat2 stdMat, int index, out BabylonFresnelParameters fresnelParameters, BabylonScene babylonScene, bool allowCube = false, bool forceAlpha = false)
		{
			fresnelParameters = null;

			if (!stdMat.MapEnabled(index))
			{
				return null;
			}

			ITexmap texMap = stdMat.GetSubTexmap(index);
			if (texMap == null)
			{
				logger?.RaiseWarning("[BABYLON][WARNING][Material][Texture] Texture channel " + index + " activated but no texture found.", 2);
				return null;
			}

			texMap = ExportFresnelParameters(texMap, out fresnelParameters);
			float amount = stdMat.GetTexmapAmt(index, 0);

			return ExportTexture(texMap, babylonScene, amount, allowCube, forceAlpha);
		}
		private BabylonTexture ExportSpecularTexture(IIGameMaterial materialNode, float[] specularColor, BabylonScene babylonScene)
		{
			ITexmap specularColorTexMap = GetTexMap(materialNode, 2);
			ITexmap specularLevelTexMap = GetTexMap(materialNode, 3);

			// --- Babylon texture ---

			IBitmapTex specularColorTexture = GetBitmapTex(specularColorTexMap);
			IBitmapTex specularLevelTexture = GetBitmapTex(specularLevelTexMap);

			if (specularLevelTexture == null)
			{
				// Copy specular color image
				// Assume specular color texture is already pre-multiplied by a global specular level value
				// So do not use global specular level
				return ExportTexture(specularColorTexture, babylonScene);
			}

			// Use one as a reference for UVs parameters
			IBitmapTex texture = specularColorTexture ?? specularLevelTexture;
			if (texture == null)
			{
				return null;
			}

		   logger?.RaiseMessage("Multiply specular color and level textures", 2);

			string nameText = (specularColorTexture != null ? Path.GetFileNameWithoutExtension(specularColorTexture.Map.FullFilePath) : TextureUtilities.ColorToStringName(specularColor)) 
							   + Path.GetFileNameWithoutExtension(specularLevelTexture.Map.FullFilePath) + "_specularColor";

			string textureID = texture.GetGuid().ToString();
			if (textureMap.ContainsKey(textureID))
			{
				return textureMap[textureID];
			}
			else
			{ 
				var babylonTexture = new BabylonTexture(textureID)
				{
					name = nameText + ".jpg" // TODO - unsafe name, may conflict with another texture name
				};

				// Level
				babylonTexture.level = 1.0f;

				// UVs
				var uvGen = ExportUV(texture.UVGen, babylonTexture);

				// Is cube
				ExportIsCube(texture.Map.FullFilePath, babylonTexture, false);


				// --- Multiply specular color and level maps ---

				// Alpha
				babylonTexture.hasAlpha = false;
				babylonTexture.getAlphaFromRGB = false;

				textureMap.Add(babylonTexture.Id, babylonTexture);
				return babylonTexture;
			}
		}
		private BabylonTexture ExportPBRTexture(IIGameMaterial materialNode, int index, BabylonScene babylonScene, float amount = 1.0f, bool allowCube = false)
		{
			var texMap = GetTexMap(materialNode, index);
			if (texMap != null)
			{
				return ExportTexture(texMap, babylonScene, amount, allowCube);
			}
			return null;
		}
		private BabylonTexture ExportClearCoatTexture(ITexmap intensityTexMap, ITexmap roughnessTexMap, float coatWeight, float coatRoughness, BabylonScene babylonScene, string materialName, bool invertRoughness)
		{
			// --- Babylon texture ---
			var intensityTexture = GetBitmapTex(intensityTexMap);
			var roughnessTexture = GetBitmapTex(roughnessTexMap);

			var texture = intensityTexture ?? roughnessTexture;
			if (texture == null)
			{
				return null;
			}

			// Use one as a reference for UVs parameters

		   logger?.RaiseMessage("Export Clear Coat weight+roughness texture", 2);

			string nameText = Path.GetFileNameWithoutExtension(texture.Map.FullFilePath);

			var textureID = texture.GetGuid().ToString();
			if (textureMap.ContainsKey(textureID))
			{
				return textureMap[textureID];
			}
			else
			{
				var babylonTexture = new BabylonTexture(textureID)
				{
					name = nameText, // TODO - unsafe name, may conflict with another texture name
									 // Level
					level = 1.0f
				};

				// UVs
				_ = ExportUV(texture.UVGen, babylonTexture);

				// Is cube
				ExportIsCube(texture.Map.FullFilePath, babylonTexture, false);

				// --- Merge maps ---
				var hasIntensity = IsTextureOk(intensityTexture);
				var hasRoughness = IsTextureOk(roughnessTexture);
				if (!hasIntensity && !hasRoughness)
				{
					return null;
				}

				// Set image format
				babylonTexture.name += ".jpg";
				return babylonTexture;
			}
		}
		private BabylonTexture ExportBaseColorAlphaTexture(ITexmap baseColorTexMap, ITexmap alphaTexMap, float[] baseColor, float alpha, BabylonScene babylonScene, string materialName, bool isOpacity = false)
		{
			// --- Babylon texture ---

			var baseColorTexture = GetBitmapTex(baseColorTexMap);
			var alphaTexture = GetBitmapTex(alphaTexMap);

			var texture = baseColorTexture != null ? baseColorTexture : alphaTexture;
			if (texture == null)
			{
				return null;
			}

			var baseColorTextureMapExtension = Path.GetExtension(baseColorTexture.Map.FullFilePath).ToLower();

			if (alphaTexture == null && baseColorTexture != null && alpha == 1)
			{
				if (baseColorTexture.AlphaSource == 0 &&
						(baseColorTextureMapExtension == ".tif" || baseColorTextureMapExtension == ".tiff"))
					{
						logger?.RaiseWarning($"[BABYLON][WARNING][Material][Texture] Diffuse texture named {baseColorTexture.Map.FullFilePath} is a .tif file and its Alpha Source is 'Image Alpha' by default.", 3);
						logger?.RaiseWarning($"[BABYLON][WARNING][Material][Texture] If you don't want material to be in BLEND mode, set diffuse texture Alpha Source to 'None (Opaque)'", 3);
					}


				if (baseColorTexture.AlphaSource == 3 && // 'None (Opaque)'
					baseColorTextureMapExtension == ".jpg" || baseColorTextureMapExtension == ".jpeg" || baseColorTextureMapExtension == ".bmp" || baseColorTextureMapExtension == ".png" )
					{
						// Copy base color image
						return ExportTexture(baseColorTexture, babylonScene);
					}
				}

			// Use one as a reference for UVs parameters


		   logger?.RaiseMessage("Export baseColor+Alpha texture", 2);

			string nameText = null;

			nameText = (baseColorTexture != null ? Path.GetFileNameWithoutExtension(baseColorTexture.Map.FullFilePath) : TextureUtilities.ColorToStringName(baseColor));

			var textureID = texture.GetGuid().ToString();
			if (textureMap.ContainsKey(textureID))
			{
				return textureMap[textureID];
			}
			else
			{ 
				var babylonTexture = new BabylonTexture(textureID)
				{
					name = nameText // TODO - unsafe name, may conflict with another texture name
				};

				// Level
				babylonTexture.level = 1.0f;

				// UVs
				_ = ExportUV(texture.UVGen, babylonTexture);

				// Is cube
				ExportIsCube(texture.Map.FullFilePath, babylonTexture, false);


				// --- Merge baseColor and alpha maps ---
				bool hasBaseColor = IsTextureOk(baseColorTexMap);
				bool hasAlpha = IsTextureOk(alphaTexMap);

				// Alpha
				// If the texture file format does not traditionally support an alpha channel, export the base texture as opaque
				if (baseColorTextureMapExtension == ".jpg" || baseColorTextureMapExtension == ".jpeg" || baseColorTextureMapExtension == ".bmp")
				{
					babylonTexture.hasAlpha = false;
				}
				else
				{
					babylonTexture.hasAlpha = IsTextureOk(alphaTexMap) || (IsTextureOk(baseColorTexMap) && baseColorTexture.AlphaSource == 0) || alpha < 1.0f;
				}

				babylonTexture.getAlphaFromRGB = false;
				if ((!IsTextureOk(alphaTexMap) && alpha == 1.0f && (IsTextureOk(baseColorTexMap) && baseColorTexture.AlphaSource == 0)) &&
					(baseColorTextureMapExtension == ".tif" || baseColorTextureMapExtension == ".tiff"))
				{
					logger?.RaiseWarning($"[BABYLON][WARNING][Material][Texture] Diffuse texture named {baseColorTexture.Map.FullFilePath} is a .tif file and its Alpha Source is 'Image Alpha' by default.", 3);
					logger?.RaiseWarning($"[BABYLON][WARNING][Material][Texture] If you don't want material to be in BLEND mode, set diffuse texture Alpha Source to 'None (Opaque)'", 3);
				}

				if (!hasBaseColor && !hasAlpha)
				{
					return null;
				}

				// Set image format
				ImageFormat imageFormat = babylonTexture.hasAlpha ? ImageFormat.Png : ImageFormat.Jpeg;
				babylonTexture.name += imageFormat == ImageFormat.Png ? ".png" : ".jpg";

				return babylonTexture;
			}
		}
		private BabylonTexture ExportORMTexture(ITexmap ambientOcclusionTexMap, ITexmap roughnessTexMap, ITexmap metallicTexMap, float metallic, float roughness, BabylonScene babylonScene, bool invertRoughness)
		{
			// --- Babylon texture ---
			IBitmapTex metallicTexture = GetBitmapTex(metallicTexMap);
			IBitmapTex roughnessTexture = GetBitmapTex(roughnessTexMap);
			IBitmapTex ambientOcclusionTexture = GetBitmapTex(ambientOcclusionTexMap);

			// Use metallic or roughness texture as a reference for UVs parameters
			IBitmapTex texture = metallicTexture ?? roughnessTexture;
			if (texture == null)
			{
				return null;
			}

		   logger?.RaiseMessage("Export ORM texture", 2);

			string textureID = texture.GetGuid().ToString();
			if (textureMap.ContainsKey(textureID))
			{
				return textureMap[textureID];
			}
			else 
			{
				var babylonTexture = new BabylonTexture(textureID)
				{
					name = ""
				};

				if (ambientOcclusionTexMap != null)
				{
					babylonTexture.name += Path.GetFileNameWithoutExtension(ambientOcclusionTexture.Map.FileName);
				}
				
				if (roughnessTexMap != null)
				{
					babylonTexture.name += Path.GetFileNameWithoutExtension(roughnessTexture.Map.FileName);
				}
				else
				{
					babylonTexture.name += (int)(roughness * 255);
				}

				if (metallicTexMap != null)
				{
					babylonTexture.name += Path.GetFileNameWithoutExtension(metallicTexture.Map.FileName);
				}
				else
				{
					babylonTexture.name += (int)(metallic * 255);
				}

				if (!string.IsNullOrEmpty(babylonTexture.name))
				{
					babylonTexture.name += "jpeg";
				}

				// UVs
				_ = ExportUV(texture.UVGen, babylonTexture);

				// Is cube
				ExportIsCube(texture.Map.FullFilePath, babylonTexture, false);

				// --- Merge metallic and roughness maps ---
				if (!IsTextureOk(metallicTexMap) && !IsTextureOk(roughnessTexMap))
				{
					return null;
				}
				
				textureMap[babylonTexture.Id] = babylonTexture;
				return babylonTexture;
			}
		}
		private BabylonTexture ExportEnvironmnentTexture(ITexmap texMap, BabylonScene babylonScene)
		{
			if (texMap.GetParamBlock(0) == null || texMap.GetParamBlock(0).Owner == null)
			{
				logger?.RaiseWarning("[BABYLON][WARNING][Material][Texture] Failed to export environment texture. Uncheck \"Use Map\" option to fix this warning.");
				return null;
			}

			if (!(texMap.GetParamBlock(0).Owner is IBitmapTex texture))
			{
				logger?.RaiseWarning("[BABYLON][WARNING][Material][Texture] Failed to export environment texture. Uncheck \"Use Map\" option to fix this warning.");
				return null;
			}

			string sourcePath = texture.Map.FullFilePath;
			string fileName = Path.GetFileName(sourcePath);

			// Allow only dds file format
			if (!fileName.EndsWith(".dds"))
			{
				logger?.RaiseWarning("[BABYLON][WARNING][Material][Texture] Failed to export environment texture: only .dds format is supported. Uncheck \"Use map\" to fix this warning.");
				return null;
			}

			string textureID = texture.GetGuid().ToString();
			if (textureMap.ContainsKey(textureID))
			{
				return textureMap[textureID];
			}
			else
			{
				BabylonTexture babylonTexture = new BabylonTexture(textureID)
				{
					name = fileName
				};

				return babylonTexture;
			}
		}
		private BabylonTexture ExportTexture(ITexmap texMap, BabylonScene babylonScene, float amount = 1.0f, bool allowCube = false, bool forceAlpha = false)
		{
			IBitmapTex texture = GetBitmapTex(texMap, false);
			if (texture == null)
			{
				ITexmap specialTexMap = GetSpecialTexmap(texMap, out float specialAmount);
				texture = GetBitmapTex(specialTexMap, false);
				amount *= specialAmount;
			}

			if (texture == null)
			{
				return null;
			}

			string sourcePath = texture.Map.FullFilePath;
			if (sourcePath == null || sourcePath == "")
			{
				logger?.RaiseWarning($"[BABYLON][WARNING][Material][Texture] Path of the texture : {texture.Name} is missing.", 2);
				return null;
			}

			logger?.Print("[BABYLON][Material][Texture] Export texture named: " + Path.GetFileName(sourcePath), Color.Black);

			string validImageFormat = TextureUtilities.GetValidImageFormat(Path.GetExtension(sourcePath));
			if (validImageFormat == null)
			{
				// Image format is not supported by the exporter
				logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] Format of texture {0} is not supported by the exporter. Consider using a standard image format like jpg or png.", Path.GetFileName(sourcePath)), 3);
				return null;
			}
			string textureID = texture.GetGuid().ToString();
			if (textureMap.ContainsKey(textureID))
			{
				return textureMap[textureID];
			}
			else
			{ 
				var babylonTexture = new BabylonTexture(textureID)
				{
					name = Path.GetFileNameWithoutExtension(texture.MapName) + "." + validImageFormat
				};
			   logger?.RaiseMessage($"texture id = {babylonTexture.Id}", 2);

				// Level
				babylonTexture.level = amount;

				// Alpha
				if (forceAlpha)
				{
					babylonTexture.hasAlpha = true;
					babylonTexture.getAlphaFromRGB = (texture.AlphaSource == 2) || (texture.AlphaSource == 3); // 'RGB intensity' or 'None (Opaque)'
				}
				else
				{
					babylonTexture.hasAlpha = (texture.AlphaSource != 3); // Not 'None (Opaque)'
					babylonTexture.getAlphaFromRGB = (texture.AlphaSource == 2); // 'RGB intensity'
				}

				// UVs
				IStdUVGen uvGen = ExportUV(texture.UVGen, babylonTexture);

				// Animations
				List<BabylonAnimation> animations = new List<BabylonAnimation>();
				ExportFloatAnimation("uOffset", animations, key => new[] { uvGen.GetUOffs(key) });
				ExportFloatAnimation("vOffset", animations, key => new[] { -uvGen.GetVOffs(key) });
				ExportFloatAnimation("uScale", animations, key => new[] { uvGen.GetUScl(key) });
				ExportFloatAnimation("vScale", animations, key => new[] { uvGen.GetVScl(key) });
				ExportFloatAnimation("uAng", animations, key => new[] { uvGen.GetUAng(key) });
				ExportFloatAnimation("vAng", animations, key => new[] { uvGen.GetVAng(key) });
				ExportFloatAnimation("wAng", animations, key => new[] { uvGen.GetWAng(key) });
				babylonTexture.animations = animations.ToArray();

				
				babylonTexture.isCube = false;
				babylonTexture.originalPath = sourcePath;

				return babylonTexture;
			}
		}

		// -------------------------
		// -- Export sub methods ---
		// -------------------------

		private ITexmap GetSpecialTexmap(ITexmap texMap, out float amount)
		{
			if (texMap == null)
			{
				amount = 0.0f;
				return null;
			}

#if MAX2016 || MAX2017 || MAX2018 || MAX2019 || MAX2020 || MAX2021
			string className = texMap.ClassName;
#else
			string className = "";
			texMap.GetClassName(ref className);
#endif
			if (className == "Normal Bump")
			{
				IIParamBlock2 block = texMap.GetParamBlockByID(0);        // General Block
				if (block != null)
				{
					amount = block.GetFloat(0, 0, 0);               // Normal texture Mult Spin
					ITexmap map = block.GetTexmap(2, 0, 0);         // Normal texture
					int mapEnabled = block.GetInt(4, 0, 0);         // Normal texture Enable
					if (mapEnabled == 0)
					{
						logger?.RaiseError($"[BABYLON][ERROR][Texture] Only Normal Bump Texture with Normal enabled are supported.", 2);
						return null;
					}

					int method = block.GetInt(6, 0, 0);         // Normal texture mode (Tangent, screen...)
					if (method != 0)
					{
						logger?.RaiseError($"[BABYLON][ERROR][Texture] Only Normal Bump Texture in tangent space are supported.", 2);
						return null;
					}
					int flipR = block.GetInt(7, 0, 0);          // Normal texture Red chanel Flip
					if (flipR != 0)
					{
						logger?.RaiseError($"[BABYLON][ERROR][Texture] Only Normal Bump Texture without R flip are supported.", 2);
						return null;
					}
					int flipG = block.GetInt(8, 0, 0);          // Normal texture Green chanel Flip
					if (flipG != 0)
					{
						logger?.RaiseError($"[BABYLON][ERROR][Texture] Only Normal Bump Texture without G flip are supported.", 2);
						return null;
					}
					int swapRG = block.GetInt(9, 0, 0);         // Normal texture swap R and G channels
					if (swapRG != 0)
					{
						logger?.RaiseError($"[BABYLON][ERROR][Texture] Only Normal Bump Texture without R and G swap are supported.", 2);
						return null;
					}
					int bumpMapEnable = block.GetInt(5, 0, 0);  // Bump texture Enable
					if (bumpMapEnable == 1)
					{
						logger?.RaiseError($"[BABYLON][ERROR][Texture] Only Normal Bump Texture without Bump are supported.", 2);
						return null;
					}
					return map;
				}
			}
			amount = 0.0f;
			logger?.RaiseError($"[BABYLON][ERROR][Texture] Texture type is not supported. Use a Bitmap or Normal Bump map instead.", 2);
			return null;
		}
		private bool IsTextureCube(string filepath)
		{
			try
			{
				byte[] data = File.ReadAllBytes(filepath);
				var intArray = new int[data.Length / 4];

				Buffer.BlockCopy(data, 0, intArray, 0, intArray.Length * 4);

				int width = intArray[4];
				int height = intArray[3];
				int mipmapsCount = intArray[7];

				if ((width >> (mipmapsCount - 1)) > 1)
				{
					int expected = 1;
					int currentSize = Math.Max(width, height);

					while (currentSize > 1)
					{
						currentSize >>= 1;
						expected++;
					}

					logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] Mipmaps chain is not complete: {0} maps instead of {1} (based on texture max size: {2})", mipmapsCount, expected, width), 3);
					logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] You must generate a complete mipmaps chain for .dds)"), 3);
					logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] Mipmaps will be disabled for this texture. If you want automatic texture generation you cannot use a .dds)"), 3);
				}

				bool isCube = (intArray[28] & 0x200) == 0x200;
				return isCube;
			}
			catch
			{
				return false;
			}
		}

		private ITexmap ExportFresnelParameters(ITexmap texMap, out BabylonFresnelParameters fresnelParameters)
		{
			fresnelParameters = null;

#if MAX2016 || MAX2017 || MAX2018 || MAX2019 || MAX2020 || MAX2021
			string className = texMap.ClassName;
#else
			string className = "";
			texMap.GetClassName(ref className);
#endif
			// Fallout
			if (className == "Falloff") // This is the only way I found to detect it. This is crappy but it works
			{
				logger?.RaiseMessage("fresnelParameters", 3);
				fresnelParameters = new BabylonFresnelParameters();

				IIParamBlock2 paramBlock = texMap.GetParamBlock(0);
				IColor color1 = paramBlock.GetColor(0, 0, 0);
				IColor color2 = paramBlock.GetColor(4, 0, 0);

				fresnelParameters.isEnabled = true;
				fresnelParameters.leftColor = color2.ToArray();
				fresnelParameters.rightColor = color1.ToArray();

				if (paramBlock.GetInt(8, 0, 0) == 2)
				{
					fresnelParameters.power = paramBlock.GetFloat(12, 0, 0);
				}
				else
				{
					fresnelParameters.power = 1;
				}

				ITexmap texMap1 = paramBlock.GetTexmap(2, 0, 0);
				int texMap1On = paramBlock.GetInt(3, 0, 0);

				ITexmap texMap2 = paramBlock.GetTexmap(6, 0, 0);
				int texMap2On = paramBlock.GetInt(7, 0, 0);

				if (texMap1 != null && texMap1On != 0)
				{
					texMap = texMap1;
					fresnelParameters.rightColor = new float[] { 1, 1, 1 };

					if (texMap2 != null && texMap2On != 0)
					{
						logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] You cannot specify two textures for falloff. Only one is supported"), 3);
					}
				}
				else if (texMap2 != null && texMap2On != 0)
				{
					fresnelParameters.leftColor = new float[] { 1, 1, 1 };
					texMap = texMap2;
				}
				else
				{
					return null;
				}
			}

			return texMap;
		}
		private IStdUVGen ExportUV(IStdUVGen uvGen, BabylonTexture babylonTexture)
		{
			switch (uvGen.GetCoordMapping(0))
			{
				case 1: //MAP_SPHERICAL
					babylonTexture.coordinatesMode = BabylonTexture.CoordinatesMode.SPHERICAL_MODE;
					break;
				case 2: //MAP_PLANAR
					babylonTexture.coordinatesMode = BabylonTexture.CoordinatesMode.PLANAR_MODE;
					break;
				default:
					babylonTexture.coordinatesMode = BabylonTexture.CoordinatesMode.EXPLICIT_MODE;
					break;
			}

			babylonTexture.coordinatesIndex = uvGen.MapChannel - 1;
			if (uvGen.MapChannel > 2)
			{
				logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] Unsupported map channel, Only channel 1 and 2 are supported."), 3);
			}

			babylonTexture.uOffset = uvGen.GetUOffs(0);
			babylonTexture.vOffset = -uvGen.GetVOffs(0);

			babylonTexture.uScale = uvGen.GetUScl(0);
			babylonTexture.vScale = uvGen.GetVScl(0);

			BabylonVector3 offset = new BabylonVector3(babylonTexture.uOffset, -babylonTexture.vOffset, 0);
			BabylonVector3 scale = new BabylonVector3(babylonTexture.uScale, babylonTexture.vScale, 1);
			BabylonVector3 rotationEuler = new BabylonVector3(uvGen.GetUAng(0), uvGen.GetVAng(0), uvGen.GetWAng(0));
			BabylonQuaternion rotation = BabylonQuaternion.FromEulerAngles(rotationEuler.X, rotationEuler.Y, rotationEuler.Z);
			BabylonVector3 pivotCenter = new BabylonVector3(-0.5f, -0.5f, 0);
			BabylonMatrix transformMatrix = MathUtilities.ComputeTextureTransformMatrix(pivotCenter, offset, rotation, scale);

			transformMatrix.decompose(scale, rotation, offset);
			BabylonVector3 texTransformRotationEuler = rotation.toEulerAngles();

			babylonTexture.uOffset = -offset.X;
			babylonTexture.vOffset = -offset.Y;
			babylonTexture.uScale = scale.X;
			babylonTexture.vScale = -scale.Y;
			babylonTexture.uRotationCenter = 0.0f;
			babylonTexture.vRotationCenter = 0.0f;
			babylonTexture.invertY = false;
			babylonTexture.uAng = texTransformRotationEuler.X;
			babylonTexture.vAng = texTransformRotationEuler.Y;
			babylonTexture.wAng = texTransformRotationEuler.Z;

			if (Path.GetExtension(babylonTexture.name).ToLower() == ".dds")
			{
				babylonTexture.vScale *= -1; // Need to invert Y-axis for DDS texture
			}

			if (babylonTexture.wAng != 0f 
				&& (babylonTexture.uScale != 1f || babylonTexture.vScale != 1f) 
				&& (Math.Abs(babylonTexture.uScale) - Math.Abs(babylonTexture.vScale)) > float.Epsilon)
			{
				logger?.RaiseWarning("[BABYLON][WARNING][Material][Texture] Rotation and non-uniform tiling (scale) on a texture is not supported as it will cause texture shearing. You can use the map UV of the mesh for those transformations.", 3);
			}

			babylonTexture.wrapU = BabylonTexture.AddressMode.CLAMP_ADDRESSMODE; // CLAMP
			if ((uvGen.TextureTiling & 1) != 0) // WRAP
			{
				babylonTexture.wrapU = BabylonTexture.AddressMode.WRAP_ADDRESSMODE;
			}
			else if ((uvGen.TextureTiling & 4) != 0) // MIRROR
			{
				babylonTexture.wrapU = BabylonTexture.AddressMode.MIRROR_ADDRESSMODE;
			}

			babylonTexture.wrapV = BabylonTexture.AddressMode.CLAMP_ADDRESSMODE; // CLAMP
			if ((uvGen.TextureTiling & 2) != 0) // WRAP
			{
				babylonTexture.wrapV = BabylonTexture.AddressMode.WRAP_ADDRESSMODE;
			}
			else if ((uvGen.TextureTiling & 8) != 0) // MIRROR
			{
				babylonTexture.wrapV = BabylonTexture.AddressMode.MIRROR_ADDRESSMODE;
			}

			return uvGen;
		}
		private void ExportIsCube(string absolutePath, BabylonTexture babylonTexture, bool allowCube)
		{
			if (Path.GetExtension(absolutePath).ToLower() != ".dds")
			{
				babylonTexture.isCube = false;
			}
			else
			{
				try
				{
					if (File.Exists(absolutePath))
					{
						babylonTexture.isCube = IsTextureCube(absolutePath);
					}
					else
					{
						logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] Texture {0} not found.", absolutePath), 3);
					}

				}
				catch
				{
					// silently fails
				}

				if (babylonTexture.isCube && !allowCube)
				{
					logger?.RaiseWarning(string.Format("[BABYLON][WARNING][Material][Texture] Cube texture are only supported for reflection channel"), 3);
				}
			}
		}

		// -------------------------
		// --------- Utils ---------
		// -------------------------

		private IBitmapTex GetBitmapTex(ITexmap texMap, bool raiseError = true)
		{
			if (texMap == null || texMap.GetParamBlock(0) == null || texMap.GetParamBlock(0).Owner == null)
			{
				return null;
			}

			IBitmapTex texture = texMap.GetParamBlock(0).Owner as IBitmapTex;
			if (texture == null && raiseError)
			{
				logger?.RaiseError($"[BABYLON][ERROR][Texture] Texture type is not supported. Use a Bitmap instead.", 2);
			}

			return texture;
		}
		private string GetSourcePath(ITexmap texMap)
		{
			IBitmapTex bitmapTex = GetBitmapTex(texMap);
			if (bitmapTex != null)
			{
				return bitmapTex.Map.FullFilePath;
			}
			else
			{
				return null;
			}
		}
		private ITexmap GetTexMap(IIGameMaterial materialNode, int index)
		{
			ITexmap texMap = null;
			if (materialNode.MaxMaterial.SubTexmapOn(index) == 1)
			{
				texMap = materialNode.MaxMaterial.GetSubTexmap(index);

				// No warning displayed because by default, physical material in 3ds Max have all maps on
				// Would be tedious for the user to uncheck all unused maps
			}
			return texMap;
		}
		private ITexmap GetTexMap(IIGameMaterial materialNode, string name)
		{
			for (int i = 0; i < materialNode.MaxMaterial.NumSubTexmaps; i++)
			{
#if MAX2024
				if (materialNode.MaxMaterial.GetSubTexmapSlotName(i, true) == name) return GetTexMap(materialNode, i);
#else
				if (materialNode.MaxMaterial.GetSubTexmapSlotName(i) == name) return GetTexMap(materialNode, i);
#endif
			}
			return null;
		}

		private bool IsTextureOk(ITexmap texMap)
		{
			IBitmapTex texture = GetBitmapTex(texMap);
			if (texture == null)
			{
				return false;
			}

			if (!File.Exists(texture.Map.FullFilePath))
			{
				return false;
			}

			return true;
		}

		private Bitmap LoadTexture(ITexmap texMap)
		{
			IBitmapTex texture = GetBitmapTex(texMap);
			if (texture == null)
			{
				return null;
			}

			return TextureUtilities.LoadTexture(texture.Map.FullFilePath, logger);
		}
	}
}
