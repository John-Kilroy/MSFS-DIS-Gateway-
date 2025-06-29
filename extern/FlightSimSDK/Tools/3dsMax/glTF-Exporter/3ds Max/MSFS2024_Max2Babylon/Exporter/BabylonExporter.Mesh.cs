using Autodesk.Max;
using BabylonExport.Entities;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.Linq;
using MSFS2024_Max2Babylon.FlightSim;


namespace MSFS2024_Max2Babylon
{
	public partial class BabylonExporter
	{
		private bool isMaterialDoubleSided;

		private bool IsMeshExportable(IIGameNode meshNode)
		{
			return IsNodeExportable(meshNode);
		}

		private BabylonNode ExportMasterMesh(IIGameScene scene, IIGameNode meshNode, BabylonScene babylonScene)
		{
			IIGameMesh gameMesh = meshNode.IGameObject.AsGameMesh();
			try
			{
				bool initialized = gameMesh.InitializeData; // Needed, the property is in fact a method initializing the exporter that has wrongly been auto 
															// Translated into a property because it has no parameters
			}
			catch (Exception)
			{
				logger?.RaiseWarning($"[BABYLON][WARNING][Mesh] Mesh {meshNode.Name} failed to initialize. Mesh is exported as dummy.", 2);
				return ExportDummy(scene, meshNode, babylonScene);
			}

			var babylonMesh = new BabylonMesh { name = meshNode.Name, id = meshNode.MaxNode.GetGuid().ToString() };

			// Position / rotation / scaling / hierarchy
			ExportNode(babylonMesh, meshNode, scene, babylonScene);

			// Skin
			var isSkinned = gameMesh.IsObjectSkinned;
			var skin = gameMesh.IGameSkin;
			var unskinnedMesh = gameMesh;
			IGMatrix skinInitPoseMatrix = Loader.Global.GMatrix.Create(Loader.Global.Matrix3.Create(true));
			List<int> boneIds = null;
			int maxNbBones = 0;
			List<IIGameNode> skinnedBones = GetSkinnedBones(skin, meshNode) ;
			if (isSkinned && skinnedBones.Count > 0)  // if the mesh has a skin with at least one bone
			{
				var skinAlreadyStored = skins.Find(_skin => IsSkinEqualTo(_skin, skin));
				if (skinAlreadyStored == null)
				{
					skins.Add(skin);
					skinNodeMap.Add(skin,meshNode);
					babylonMesh.skeletonId = skins.IndexOf(skin);
				}
				else
				{
					babylonMesh.skeletonId = skins.IndexOf(skinAlreadyStored);
				}

				skin.GetInitSkinTM(skinInitPoseMatrix);
				boneIds = GetNodeIndices(skin, meshNode);
			}
			else
			{
				skin = null;
			}

			// Mesh
			if (unskinnedMesh.IGameType == Autodesk.Max.IGameObject.ObjectTypes.Mesh && unskinnedMesh.MaxMesh != null)
			{
				if (unskinnedMesh.NumberOfFaces < 1)
				{
					logger?.RaiseError($"[BABYLON][ERROR][Mesh] Mesh {babylonMesh.name} has no face", 2);
				}

				if (unskinnedMesh.NumberOfVerts < 3)
				{
					logger?.RaiseError($"[BABYLON][ERROR][Mesh] Mesh {babylonMesh.name} has not enough vertices", 2);
				}

				if (unskinnedMesh.NumberOfVerts >= 65536)
				{
					logger?.RaiseWarning($"[BABYLON][WARNING][Mesh] Mesh {babylonMesh.name} has more than 65536 vertices which means that it will require specific WebGL extension to be rendered. This may impact portability of your scene on low end devices.", 2);
				}

				if (skin != null)
				{
					for (var vertexIndex = 0; vertexIndex < unskinnedMesh.NumberOfVerts; vertexIndex++)
					{
						maxNbBones = Math.Max(maxNbBones, skin.GetNumberOfBones(vertexIndex));
					}
				}

				// Material
				var mtl = meshNode.NodeMaterial;
				var multiMatsCount = 1;

				// The DirectXShader material is a passthrough to its render material.
				// The shell material is a passthrough to its baked material.
				while (mtl != null && (isShellMaterial(mtl) || isDirectXShaderMaterial(mtl)))
				{
					if (isShellMaterial(mtl))
					{
						// Retrieve the baked material from the shell material.
						mtl = GetBakedMaterialFromShellMaterial(mtl);
					}
					else // isDirectXShaderMaterial(mtl)
					{
						// Retrieve the render material from the directX shader
						mtl = GetRenderMaterialFromDirectXShader(mtl);
					}
				}

				isMaterialDoubleSided = false;
				if (mtl != null)
				{
					IIGameMaterial unsupportedMaterial = IsMaterialSupported(mtl, babylonScene);
					if (unsupportedMaterial == null)
					{
						babylonMesh.materialId = mtl.MaxMaterial.GetGuid().ToString();

						if (!referencedMaterials.Contains(mtl))
						{
							referencedMaterials.Add(mtl);
						}

						multiMatsCount = Math.Max(mtl.SubMaterialCount, 1);

						if (isDoubleSidedMaterial(mtl))
						{
							isMaterialDoubleSided = true;
						}
					}
					else
					{
						if (FlightSimMaterialUtilities.IsMSFS2020Material(mtl.MaxMaterial))
						{
							throw new System.Exception($"[BABYLON][ERROR][Material] Material : '{mtl.MaterialName}' has unsupported Material type 'MSFS2020 : {mtl.MaterialClass}'.");
						}

						throw new System.Exception($"[BABYLON][ERROR][Material] Material : '{mtl.MaterialName}' has unsupported Material type '{mtl.MaterialClass}'.");
					}
				}

				var vertices = new List<GlobalVertex>();
				var indices = new List<int>();
				var mappingChannels = unskinnedMesh.ActiveMapChannelNum;
				bool hasUV = false;
				bool hasUV2 = false;
				for (int i = 0; i < mappingChannels.Count; ++i)
				{
#if MAX2017 || MAX2018 || MAX2019 || MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
					var channelNum = mappingChannels[i];
#else
					var channelNum = mappingChannels[new IntPtr(i)];
#endif
					if (channelNum == 1)
					{
						hasUV = true;
					}
					else if (channelNum == 2)
					{
						hasUV2 = true;
					}
				}
				var hasColor = unskinnedMesh.NumberOfColorVerts > 0;
				var hasAlpha = unskinnedMesh.GetNumberOfMapVerts(-2) > 0;

				var optimizeVertices = true;

				var invertedWorldMatrix = GetInvertWorldTM(meshNode, 0);
				var offsetTM = GetOffsetTM(meshNode, 0);

				// Compute normals
				var subMeshes = new List<BabylonSubMesh>();
				List<int> faceIndexes = null;
				ExtractGeometry(babylonMesh, vertices, indices, subMeshes, boneIds, skin, unskinnedMesh, invertedWorldMatrix, offsetTM, hasUV, hasUV2, hasColor, hasAlpha, optimizeVertices, multiMatsCount, meshNode, ref faceIndexes);

				if (vertices.Count >= 65536)
				{
					logger?.RaiseWarning($"[BABYLON][WARNING][Mesh] Mesh {babylonMesh.name} has {vertices.Count} vertices. This may prevent your scene to work on low end devices where 32 bits indice are not supported", 2);

					if (!optimizeVertices)
					{
						logger?.RaiseError("[BABYLON][ERROR][Mesh] You can try to optimize your object using [Try to optimize vertices] option", 2);
					}
				}

			   logger?.RaiseMessage($"{vertices.Count} vertices, {indices.Count / 3} faces", 2);

				// Buffers
				babylonMesh.positions = vertices.SelectMany(v => new[] { v.Position.X, v.Position.Y, v.Position.Z }).ToArray();
				babylonMesh.normals = vertices.SelectMany(v => new[] { v.Normal.X, v.Normal.Y, v.Normal.Z }).ToArray();

				// Export tangents if option is checked and mesh has tangents
				if (exportParameters.exportTangents)
				{
					babylonMesh.tangents = vertices.SelectMany(v => v.Tangent).ToArray();
				}

				if (hasUV)
				{
					babylonMesh.uvs = vertices.SelectMany(v => new[] { v.UV.X, 1 - v.UV.Y }).ToArray();
				}
				if (hasUV2)
				{
					babylonMesh.uvs2 = vertices.SelectMany(v => new[] { v.UV2.X, 1 - v.UV2.Y }).ToArray();
				}

				if (skin != null)
				{
					babylonMesh.matricesWeights = vertices.SelectMany(v => v.Weights.ToArray()).ToArray();
					babylonMesh.matricesIndices = vertices.Select(v => v.BonesIndices).ToArray();

					//babylonMesh.numBoneInfluencers = maxNbBones;
					if (maxNbBones > 4)
					{
						babylonMesh.matricesWeightsExtra = vertices.SelectMany(
							v => v.WeightsExtra != null ? v.WeightsExtra.ToArray() : new[] { 0.0f, 0.0f, 0.0f, 0.0f }
						).ToArray();
						babylonMesh.matricesIndicesExtra = vertices.Select(v => v.BonesIndicesExtra).ToArray();
					}
				}

				if (hasColor)
				{
					babylonMesh.colors = vertices.SelectMany(v => v.Color.ToArray()).ToArray();
					babylonMesh.hasVertexAlpha = hasAlpha;
				}

				babylonMesh.subMeshes = subMeshes.ToArray();

				// Buffers - Indices
				babylonMesh.indices = indices.ToArray();

				// ------------------------
				// ---- Morph targets -----
				// ------------------------

				// Retreive modifiers with morpher flag
				List<IIGameModifier> modifiers = new List<IIGameModifier>();
				for (int i = 0; i < meshNode.IGameObject.NumModifiers; i++)
				{
					var modifier = meshNode.IGameObject.GetIGameModifier(i);
					if (modifier.ModifierType == Autodesk.Max.IGameModifier.ModType.Morpher)
					{
						modifiers.Add(modifier);
					}
				}

				// Cast modifiers to morphers
				List<IIGameMorpher> morphers = modifiers.ConvertAll(new Converter<IIGameModifier, IIGameMorpher>(modifier => modifier.AsGameMorpher()));

				var hasMorphTarget = false;
				morphers.ForEach(morpher =>
				{
					if (morpher.NumberOfMorphTargets > 0)
					{
						hasMorphTarget = true;
					}
				});

				if (hasMorphTarget)
				{
					logger?.RaiseMessage("Export morph targets", 2);

					// Morph Target Manager
					var babylonMorphTargetManager = new BabylonMorphTargetManager(babylonMesh);
					babylonScene.MorphTargetManagersList.Add(babylonMorphTargetManager);
					babylonMesh.morphTargetManagerId = babylonMorphTargetManager.id;

					// Morph Targets
					var babylonMorphTargets = new List<BabylonMorphTarget>();
					// All morphers are considered identical
					// Their targets are concatenated
					int m = 0;
					morphers.ForEach(morpher =>
					{
						m++;
						for (int i = 0; i < morpher.NumberOfMorphTargets; i++)
						{
							// Morph target
							var maxMorphTarget = GetMorphTarget(scene, babylonMesh, i);
							// here we avoid to extract vertices in an optimize way, du to the fact that the actual optimize process is NOT garanty to keep a one to one relationship
							// with the source and target vertices.
							bool mustRebuildMorphTarget = (maxMorphTarget == null);
							if (mustRebuildMorphTarget)
							{
								string actionStr = exportParameters.rebuildMorphTarget ? $" trying to rebuild {i}." : string.Empty;
								if (maxMorphTarget == null)
								{
									logger?.RaiseWarning($"[BABYLON][WARNING][Mesh][MorphTarget] Morph target [{i}] is not available anymore - ie: has been deleted in max and is baked into the scene.{actionStr}", 3);
								}
								else
								{
									logger?.RaiseWarning($"[BABYLON][WARNING][Mesh][MorphTarget] Morph target [{i}] MUST be rebuilt to avoid artifacts, using the vertices export process.{actionStr}", 3);
									maxMorphTarget = null; // force target to be null anyway ie- when optimize on.
								}
							}

							// Target geometry - this is where we rebuild the target if necessary
							var targetVertices = ExtractMorphTargetVertices(babylonMesh, vertices, offsetTM, i, maxMorphTarget, optimizeVertices, faceIndexes, hasUV, hasColor, hasAlpha);

							if (targetVertices != null && targetVertices.Any())
							{
								var babylonMorphTarget = new BabylonMorphTarget
								{
									// the name is reconstructed if we have to rebuild the target
									name = maxMorphTarget?.Name ?? $"{meshNode.Name}.morpher({m}).target({i})"
								};

								babylonMorphTargets.Add(babylonMorphTarget);
								logger?.Print($"[BABYLON][Mesh][MorphTarget] Morph target {babylonMorphTarget.name} added.", Color.Black);

								// TODO - Influence
								babylonMorphTarget.influence = GetMorphTargetWeight(babylonMesh, i) / 100.0f;

								// Target geometry
								babylonMorphTarget.positions = targetVertices.SelectMany(v => new[] { v.Position.X, v.Position.Y, v.Position.Z }).ToArray();

								if (exportParameters.exportMorphNormals)
								{
									if (mustRebuildMorphTarget)
									{
										// we do not recontruct the normals
										logger?.RaiseWarning("[BABYLON][WARNING][Mesh][MorphTarget] We do not have morph normals when morph target has been rebuilded.", 4);
										babylonMorphTarget.normals = null;
									}
									else
									{
										babylonMorphTarget.normals = targetVertices.SelectMany(v => new[] { v.Normal.X, v.Normal.Y, v.Normal.Z }).ToArray();
									}
								}

								// Tangent
								if (exportParameters.exportTangents && exportParameters.exportMorphTangents)
								{
									if (mustRebuildMorphTarget)
									{
										// we do not recontruct the tangents
										logger?.RaiseWarning("[BABYLON][WARNING][Mesh][MorphTarget] Rebuilt morph targets will not have tangent information.", 4);
										babylonMorphTarget.tangents = null;
									}
									else
									{
										babylonMorphTarget.tangents = targetVertices.SelectMany(v => new[] { v.Tangent[0], v.Tangent[1], v.Tangent[2] }).ToArray();
									}
								}

								// UV
								if(hasUV && exportParameters.exportTargetUVs)
								{
									if (mustRebuildMorphTarget)
									{
										// we do not recontruct the tangents
										logger?.RaiseWarning("[BABYLON][WARNING][Mesh][MorphTarget] Rebuilt morph targets will not have tangent information.", 4);
										babylonMorphTarget.tangents = null;
									}
									else
									{
										babylonMorphTarget.uvs = targetVertices.SelectMany(v => new[] { v.UV.X, 1 - v.UV.Y }).ToArray();
									}
								}

								// Colors
								if (hasColor && exportParameters.exportTargetColors)
								{
									if (mustRebuildMorphTarget)
									{
										// we do not recontruct the tangents
										logger?.RaiseWarning("[BABYLON][WARNING][Mesh][MorphTarget] Rebuilt morph targets will not have tangent information.", 4);
										babylonMorphTarget.tangents = null;
									}
									else
									{
										babylonMorphTarget.hasVertexAlpha = hasAlpha;
										List<float> colors = new List<float>(targetVertices.Count());
										foreach (var vertice in targetVertices)
										{
											var color = vertice.Color;

											if (color != null)
											{
												colors.AddRange(color.ToList());

											}
										}

										babylonMorphTarget.colors = colors.ToArray();
									}

								}

								// Animations
								if (exportParameters.animationExportType == AnimationExportType.Export)
								{
									var animations = new List<BabylonAnimation>();
									var morphWeight = morpher.GetMorphWeight(i);
									ExportFloatGameController(morphWeight, "influence", animations);
									if (animations.Count > 0)
									{
										babylonMorphTarget.animations = animations.ToArray();
									}
								}
							}
						}
					});

					babylonMorphTargetManager.targets = babylonMorphTargets.ToArray();
				}
			}

			// Animations
			// Done last to avoid '0 vertex found' error (unkown cause)
			ExportAnimation(babylonMesh, meshNode);

			if(!babylonScene.MeshesList.Any(x => x.id == babylonMesh.id)) babylonScene.MeshesList.Add(babylonMesh);

			return babylonMesh;
		}
		private BabylonNode ExportInstanceMesh(IIGameScene scene, IIGameNode meshNode, BabylonScene babylonScene, BabylonMesh babylonMasterMesh)
		{
			meshNode.MaxNode.MarkAsInstance();

			BabylonAbstractMesh babylonInstanceMesh = new BabylonAbstractMesh
			{
				id = meshNode.MaxNode.GetGuid().ToString(),
				name = meshNode.Name,
			};

			// Add instance to master mesh
			List<BabylonAbstractMesh> list = babylonMasterMesh.instances != null ? babylonMasterMesh.instances.ToList() : new List<BabylonAbstractMesh>();
			list.Add(babylonInstanceMesh);
			babylonMasterMesh.instances = list.ToArray();

			// Export transform / hierarchy / animations
			ExportNode(babylonInstanceMesh, meshNode, scene, babylonScene);

			// Animations
			ExportAnimation(babylonInstanceMesh, meshNode);

			return babylonInstanceMesh;
		}
		private BabylonNode ExportSubModelExtraNode(IIGameScene scene, IIGameNode meshNode, BabylonScene babylonScene)
		{
			var babylonMesh = new BabylonMesh { 
				name = meshNode.Name, 
				id = meshNode.MaxNode.GetGuid().ToString() 
			};
			//babylonMesh.isDummy = true;

			// Position / rotation / scaling / hierarchy
			ExportNode(babylonMesh, meshNode, scene, babylonScene);

			if (!babylonScene.MeshesList.Any(x => x.id == babylonMesh.id)) babylonScene.MeshesList.Add(babylonMesh);
			return babylonMesh;

		}
		private BabylonNode ExportDummy(IIGameScene scene, IIGameNode meshNode, BabylonScene babylonScene)
		{
			var babylonMesh = new BabylonMesh { 
				name = meshNode.Name, 
				id = meshNode.MaxNode.GetGuid().ToString() 
			};

			// Position / rotation / scaling / hierarchy
			ExportNode(babylonMesh, meshNode, scene, babylonScene);

			// Animations
			ExportAnimation(babylonMesh, meshNode);

			if (!babylonScene.MeshesList.Any(x => x.id == babylonMesh.id)) babylonScene.MeshesList.Add(babylonMesh);
			return babylonMesh;

		}
		private BabylonNode ExportMesh(IIGameScene scene, IIGameNode meshNode, BabylonScene babylonScene)
		{
			if (!exportParameters.keepInstances)
			{
				 return ExportMasterMesh(scene, meshNode, babylonScene);
			}
			else
			{
				// Instances
#if MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
				var tabs = Loader.Global.INodeTab.Create();
#else
				var tabs = Loader.Global.NodeTab.Create();
	#endif
				Loader.Global.IInstanceMgr.InstanceMgr.GetInstances(meshNode.MaxNode, tabs);
				if (tabs.Count > 1)
				{
					IINode Master = TabToList<IINode>(tabs)[tabs.Count - 1];
					List<IINode> Instances = TabToList<IINode>(tabs).FindAll(x => x.Handle != Master.Handle);
					foreach (IINode instanceNode in tabs.ToIEnumerable())
					{
						// This make sure every instance node is indexed in guid dictionary
						Tools.GetGuid(instanceNode);
					}

					BabylonMesh babylonMasterMesh = babylonScene.MeshesList.Find(mesh => mesh.id == Master.GetGuid().ToString());
					if(babylonMasterMesh==null)
					{
						 return ExportMasterMesh(scene, meshNode, babylonScene);
					}
					else
					{  
						return ExportInstanceMesh(scene, meshNode, babylonScene, babylonMasterMesh);
					}
				}
				return ExportMasterMesh(scene, meshNode, babylonScene);
			}
		}

		private IIGameNode GetMorphTarget(IIGameScene scene, BabylonAbstractMesh babylonAbstractMesh, int morphIndex)
		{
			IIGameNode target = null;
			string script = $"(WM3_MC_GetTarget ${babylonAbstractMesh.name}.morpher {morphIndex}) as string";
#if MAX2022 || MAX2023 || MAX2024
			string str = ManagedServices.MaxscriptSDK.ExecuteStringMaxscriptQuery(script, ManagedServices.MaxscriptSDK.ScriptSource.NotSpecified);
#else
			var str = ManagedServices.MaxscriptSDK.ExecuteStringMaxscriptQuery(script);
#endif
			if (!string.IsNullOrEmpty(str))
			{
				string[] words = str.Split(' ');
				string node = words[0].Split(':')[1];
				var pointHelper = GlobalInterface.Instance.COREInterface.GetINodeByName(node);
				target = scene.GetIGameNode(pointHelper);
			}

			return target;
		}
		private float GetMorphTargetWeight(BabylonAbstractMesh babylonAbstractMesh, int morphIndex)
		{
			var script = $"(WM3_MC_GetValue ${babylonAbstractMesh.name}.morpher {morphIndex + 1}) as string";
#if MAX2022 || MAX2023 || MAX2024
			var str = ManagedServices.MaxscriptSDK.ExecuteStringMaxscriptQuery(script, ManagedServices.MaxscriptSDK.ScriptSource.NotSpecified);
#else
			var str = ManagedServices.MaxscriptSDK.ExecuteStringMaxscriptQuery(script);
#endif
			
			return float.Parse(str, CultureInfo.InvariantCulture.NumberFormat);
		}
		private IEnumerable<GlobalVertex> ExtractMorphTargetVertices(BabylonAbstractMesh babylonAbstractMesh, List<GlobalVertex> vertices, IMatrix3 offsetTM, int morphIndex, IIGameNode maxMorphTarget, bool optimizeVertices, List<int> faceIndexes, bool hasUV, bool hasColor, bool hasAlpha)
		{
			if (maxMorphTarget != null )
			{
				foreach(var v in ExtractVertices(babylonAbstractMesh, maxMorphTarget, optimizeVertices, faceIndexes, hasColor, hasAlpha, hasUV))
				{
					yield return v;
				}
				yield break;
			}
			// rebuild Morph Target
			if (exportParameters.rebuildMorphTarget)
			{
				var points = ExtractMorphTargetPoints(babylonAbstractMesh, morphIndex, offsetTM).ToList();
				for (int i = 0; i != vertices.Count; i++)
				{
					int bi = vertices[i].BaseIndex;
					yield return new GlobalVertex()
					{
						BaseIndex = bi,
						Position = points[bi]
					};
				}
			}
		}
		private IEnumerable<IPoint3> ExtractMorphTargetPoints(BabylonAbstractMesh babylonAbstractMesh, int morphIndex, IMatrix3 offsetTM)
		{
			// this is the place where we reconstruct the vertices. 
			// the needed function is not available on the .net SDK, then we have to use Max Script.
			// TODO : use direct instance instead of manipulate string

			var script = $"with printAllElements on (for k in 0 to (WM3_MC_NumMPts ${babylonAbstractMesh.name}.Morpher {morphIndex}) collect (WM3_MC_GetMorphPoint ${babylonAbstractMesh.name}.morpher {morphIndex} k)) as string";
#if MAX2022 || MAX2023 || MAX2024
			var str = ManagedServices.MaxscriptSDK.ExecuteStringMaxscriptQuery(script, ManagedServices.MaxscriptSDK.ScriptSource.NotSpecified);
#else
			var str = ManagedServices.MaxscriptSDK.ExecuteStringMaxscriptQuery(script);
#endif
			if (!String.IsNullOrEmpty(str))
			{
				// we obtain a list of Point3 as string in a format of #([5.69523,-58.2409,65.1479],...)
				int i = str.IndexOf('[');
				if (i != -1)
				{
					do
					{
						int j = str.IndexOf(']', i++);
						var p3Str = str.Substring(i, j - i);
						var xyz = p3Str.Split(',').Select(s => float.Parse(s, CultureInfo.InvariantCulture)).ToArray();
						// conversion: Max to Directx(Babylon) (swap Y and Z).
						var p = Loader.Global.Point3.Create(xyz[0] * scaleFactor, xyz[2] * scaleFactor, xyz[1] * scaleFactor);
						yield return p;
						i = str.IndexOf('[', j);
					} while (i != -1);
				}
			}
			yield break;
		}

		private List<GlobalVertex> ExtractVertices(BabylonAbstractMesh babylonAbstractMesh, IIGameNode maxMorphTarget, bool optimizeVertices, List<int> faceIndexes, bool hasColor, bool hasAlpha, bool hasUv)
		{
			IIGameMesh gameMesh = maxMorphTarget.IGameObject.AsGameMesh();
			IIGameMaterial mtl = maxMorphTarget.NodeMaterial;
			int multiMatsCount = 1;

			if (mtl != null)
			{
				multiMatsCount = Math.Max(mtl.SubMaterialCount, 1);
			}
			IMatrix3 invertedWorldMatrix = GetInvertWorldTM(maxMorphTarget, 0);
			IMatrix3 offsetTM = GetOffsetTM(maxMorphTarget, 0);

			List<GlobalVertex> vertices = new List<GlobalVertex>();
			ExtractGeometry(babylonAbstractMesh, vertices, new List<int>(), new List<BabylonSubMesh>(), null, null, gameMesh, invertedWorldMatrix, offsetTM, hasUv, false, hasColor, hasAlpha, optimizeVertices, multiMatsCount, maxMorphTarget, ref faceIndexes);
			return vertices;
		}
		private void ExtractGeometry(BabylonAbstractMesh babylonAbstractMesh, List<GlobalVertex> vertices, List<int> indices, List<BabylonSubMesh> subMeshes, List<int> boneIds, IIGameSkin skin, IIGameMesh unskinnedMesh, IMatrix3 invertedWorldMatrix, IMatrix3 offsetTM, bool hasUV, bool hasUV2, bool hasColor, bool hasAlpha, bool optimizeVertices, int multiMatsCount, IIGameNode meshNode, ref List<int> faceIndexes)
		{
			Dictionary<GlobalVertex, List<GlobalVertex>> verticesAlreadyExported = null;

			if (optimizeVertices)
			{
				verticesAlreadyExported = new Dictionary<GlobalVertex, List<GlobalVertex>>();
			}

			int indexStart = 0;
			// Whether or not to store order in which faces are exported
			// Storage is used when exporting Morph Targets geometry
			// To ensure face order is identical, especially with multimaterials involved
			bool storeFaceIndexes = faceIndexes == null;
			if (storeFaceIndexes)
			{
				faceIndexes = new List<int>();
			}
			int indexInFaceIndexesArray = 0;
			for (int i = 0; i < multiMatsCount; ++i)
			{
				int materialId = i;
				int indexCount = 0;
				int minVertexIndex = int.MaxValue;
				int maxVertexIndex = int.MinValue;
				BabylonSubMesh subMesh = new BabylonSubMesh { indexStart = indexStart, materialIndex = i };

				if (multiMatsCount == 1)
				{
					for (int j = 0; j < unskinnedMesh.NumberOfFaces; ++j)
					{
						IFaceEx face = null;
						if (storeFaceIndexes)
						{
							face = unskinnedMesh.GetFace(j);
							// Store face index (j = face.MeshFaceIndex)
							faceIndexes.Add(j);
						}
						else
						{
							face = unskinnedMesh.GetFace(faceIndexes[indexInFaceIndexesArray++]);
						}
						ExtractFace(skin, unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, vertices, indices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, ref indexCount, ref minVertexIndex, ref maxVertexIndex, face, boneIds);
					}
				}
				else
				{
					if (i == 0 || isMaterialDoubleSided == false)
					{
						ITab<IFaceEx> materialFaces = unskinnedMesh.GetFacesFromMatID(materialId);
						for (int j = 0; j < materialFaces.Count; ++j)
						{
							IFaceEx face = null;
							if (storeFaceIndexes)
							{
								// Retreive face
#if MAX2017 || MAX2018 || MAX2019 || MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
								face = materialFaces[j];
#else
								face = materialFaces[new IntPtr(j)];
#endif

								// Store face index
								faceIndexes.Add(face.MeshFaceIndex);
							}
							else
							{
								face = unskinnedMesh.GetFace(faceIndexes[indexInFaceIndexesArray++]);
							}
							ExtractFace(skin, unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, vertices, indices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, ref indexCount, ref minVertexIndex, ref maxVertexIndex, face, boneIds);
						}
					}
					else
					{
						// It's a double sided material
						// The back faces are created at runtime

						// WARNING - Nested multimaterial and double sided material are not supported
						minVertexIndex = vertices.Count;
						maxVertexIndex = vertices.Count * 2 - 1;

						// Vertices
						int nbVertices = vertices.Count;
						for (int index = 0; index < nbVertices; index++)
						{
							GlobalVertex vertexOrg = vertices[index];

							// Duplicate vertex
							GlobalVertex vertexNew = new GlobalVertex(vertexOrg);

							// Inverse back vertices normal
							vertexNew.Normal = vertexNew.Normal.MultiplyBy(-1);
							vertexNew.Tangent = vertexNew.Tangent.MultiplyBy(-1);

							vertices.Add(vertexNew);
						}

						// Faces
						int nbIndices = indices.Count;
						for (int index = 0; index < nbIndices; index += 3)
						{
							// Duplicate and flip faces
							indices.Add(indices[index + 2] + nbIndices);
							indices.Add(indices[index + 1] + nbIndices);
							indices.Add(indices[index] + nbIndices);

							indexCount += 3;
						}
					}
				}

				if (indexCount != 0)
				{

					subMesh.indexCount = indexCount;
					subMesh.verticesStart = minVertexIndex;
					subMesh.verticesCount = maxVertexIndex - minVertexIndex + 1;

					indexStart += indexCount;

					subMeshes.Add(subMesh);
				}
			}
		}
		private void ExtractFace(IIGameSkin skin, IIGameMesh unskinnedMesh, BabylonAbstractMesh babylonAbstractMesh, IMatrix3 invertedWorldMatrix, IMatrix3 offsetTM, List<GlobalVertex> vertices, List<int> indices, bool hasUV, bool hasUV2, bool hasColor, bool hasAlpha, Dictionary<GlobalVertex, List<GlobalVertex>> verticesAlreadyExported, ref int indexCount, ref int minVertexIndex, ref int maxVertexIndex, IFaceEx face, List<int> boneIds)
		{
			int a, b, c;
			// Parity is TRUE, if determinant negative ( counter-intuitive convention of 3ds max, see docs... :/ )

			// For threejs and babylonjs (handle negative scales correctly (reversed winding order expected)
			if (invertedWorldMatrix.Parity)
			{
				// Flipped case: reverse winding order
				a = CreateGlobalVertex(unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, face, 0, vertices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, skin, boneIds);
				b = CreateGlobalVertex(unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, face, 1, vertices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, skin, boneIds);
				c = CreateGlobalVertex(unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, face, 2, vertices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, skin, boneIds);
			}
			else
			{
				// normal case
				a = CreateGlobalVertex(unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, face, 0, vertices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, skin, boneIds);
				b = CreateGlobalVertex(unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, face, 2, vertices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, skin, boneIds);
				c = CreateGlobalVertex(unskinnedMesh, babylonAbstractMesh, invertedWorldMatrix, offsetTM, face, 1, vertices, hasUV, hasUV2, hasColor, hasAlpha, verticesAlreadyExported, skin, boneIds);
			}

			indices.Add(a);
			indices.Add(b);
			indices.Add(c);

			if (a < minVertexIndex)
			{
				minVertexIndex = a;
			}

			if (b < minVertexIndex)
			{
				minVertexIndex = b;
			}

			if (c < minVertexIndex)
			{
				minVertexIndex = c;
			}

			if (a > maxVertexIndex)
			{
				maxVertexIndex = a;
			}

			if (b > maxVertexIndex)
			{
				maxVertexIndex = b;
			}

			if (c > maxVertexIndex)
			{
				maxVertexIndex = c;
			}

			indexCount += 3;
		}

		int CreateGlobalVertex(IIGameMesh mesh, BabylonAbstractMesh babylonAbstractMesh, IMatrix3 invertedWorldMatrix, IMatrix3 offsetTM, IFaceEx face, int facePart, List<GlobalVertex> vertices, bool hasUV, bool hasUV2, bool hasColor, bool hasAlpha, Dictionary<GlobalVertex, List<GlobalVertex>> verticesAlreadyExported, IIGameSkin skin, List<int> boneIds)
		{
			int vertexIndex = (int)face.Vert[facePart];

			// Position can by retrieved in world space or object space
			// Unfortunately, this value can't be retrieved in local space
			GlobalVertex vertex = new GlobalVertex
			{
				BaseIndex = vertexIndex,
				Position = mesh.GetVertex(vertexIndex, true), // retrieve in object space to keep precision
				Normal = mesh.GetNormal((int)face.Norm[facePart], true) // object space (world space was somehow bugged for normal)
			};
			// System.Diagnostics.Debug.WriteLine("vertex normal: " + string.Join(", ", vertex.Normal.ToArray().Select(v => Math.Round(v, 3))));

			// Convert from object to local/node space
			vertex.Position = offsetTM.PointTransform(vertex.Position);

			// normal (from object to local/node space)
			vertex.Normal = offsetTM.VectorTransform(vertex.Normal).Normalize;

			// tangent
			if (exportParameters.exportTangents)
			{
				int indexTangentBinormal = mesh.GetFaceVertexTangentBinormal(face.MeshFaceIndex, facePart, 1);
				IPoint3 normal = vertex.Normal.Normalize;
				IPoint3 tangent = mesh.GetTangent(indexTangentBinormal, 1).Normalize;
				IPoint3 bitangent = mesh.GetBinormal(indexTangentBinormal, 1).Normalize;
				int w = GetW(normal, tangent, bitangent);
				vertex.Tangent = new float[] { tangent.X, tangent.Y, tangent.Z, w };
			}

			if (hasUV)
			{
				int[] indices = new int[3];
				unsafe
				{
					fixed (int* indicesPtr = indices)
					{
						mesh.GetMapFaceIndex(1, face.MeshFaceIndex, new IntPtr(indicesPtr));
					}
				}
				IPoint3 texCoord = mesh.GetMapVertex(1, indices[facePart]);
				vertex.UV = Loader.Global.Point2.Create(texCoord.X, 1-texCoord.Y);
			}

			if (hasUV2)
			{
				int[] indices = new int[3];
				unsafe
				{
					fixed (int* indicesPtr = indices)
					{
						mesh.GetMapFaceIndex(2, face.MeshFaceIndex, new IntPtr(indicesPtr));
					}
				}
				IPoint3 texCoord = mesh.GetMapVertex(2, indices[facePart]);
				vertex.UV2 = Loader.Global.Point2.Create(texCoord.X, 1-texCoord.Y);
			}

			if (hasColor)
			{
				int vertexColorIndex = (int)face.Color[facePart];
				IPoint3 vertexColor = mesh.GetColorVertex(vertexColorIndex);
				float alpha = 1.0f;
				if (hasAlpha)
				{
					int[] indices = new int[3];
					unsafe
					{
						fixed (int* indicesPtr = indices)
						{
							mesh.GetMapFaceIndex(-2, face.MeshFaceIndex, new IntPtr(indicesPtr));
						}
					}
					IPoint3 color = mesh.GetMapVertex(-2, indices[facePart]);
					alpha = color.X;
				}
				vertex.Color = new[] { vertexColor.X, vertexColor.Y, vertexColor.Z, alpha };
			}

			if (skin != null)
			{
				float[] weight = new float[4] { 0, 0, 0, 0 };
				int[] bone = new int[4] { 0, 0, 0, 0 };
				int nbBones = skin.GetNumberOfBones(vertexIndex);

				int currentVtxBone = 0;
				int currentSkinBone = 0;

				// process skin bones until we have 4 bones for this vertex or we run out of skin bones
				for (currentSkinBone = 0; currentSkinBone < nbBones && currentVtxBone < 4; ++currentSkinBone)
				{
					float boneWeight = skin.GetWeight(vertexIndex, currentSkinBone);
					if (boneWeight <= 0)
						continue;

					bone[currentVtxBone] = boneIds.IndexOf(skin.GetIGameBone(vertexIndex, currentSkinBone).NodeID);
					weight[currentVtxBone] = skin.GetWeight(vertexIndex, currentSkinBone);
					++currentVtxBone;
				}

				// if we didnt have any bones with a weight > 0
				if (currentVtxBone == 0)
				{
					weight[0] = 1.0f;
					bone[0] = 0;
				}

				vertex.Weights = Loader.Global.Point4.Create(weight);

				if (bone[3] > 255 || bone[2] > 255 || bone[1] > 255 || bone[0] > 255)
				{
					throw new System.Exception($"[BABYLON][ERROR][Bone] Too many bones, the vertex with id {vertexIndex} is influenced by a bone with an id greater than 255.");
				}

				vertex.BonesIndices = (bone[3] << 24) | (bone[2] << 16) | (bone[1] << 8) | bone[0];

				if (currentVtxBone >= 4 && currentSkinBone < nbBones)
				{
					weight = new float[4] { 0, 0, 0, 0 };
					bone = new int[4] { 0, 0, 0, 0 };

					// process remaining skin bones until we have a total of 8 bones for this vertex or we run out of skin bones
					for (; currentSkinBone < nbBones && currentVtxBone < 8; ++currentSkinBone)
					{
						float boneWeight = skin.GetWeight(vertexIndex, currentSkinBone);
						if (boneWeight <= 0)
							continue;

						if (isGltfExported)
						{
							logger?.RaiseError("[BABYLON][ERROR][Mesh] Too many bone influences per vertex for vertexIndex: " + vertexIndex + ". glTF only supports up to 4 bone influences per vertex.", 2);
							break;
						}

						bone[currentVtxBone - 4] = boneIds.IndexOf(skin.GetIGameBone(vertexIndex, currentSkinBone).NodeID);
						weight[currentVtxBone - 4] = skin.GetWeight(vertexIndex, currentSkinBone);
						++currentVtxBone;
					}

					// if we have any extra bone weights
					if (currentVtxBone > 4)
					{
						vertex.WeightsExtra = Loader.Global.Point4.Create(weight);
						vertex.BonesIndicesExtra = (bone[3] << 24) | (bone[2] << 16) | (bone[1] << 8) | bone[0];

						if (currentSkinBone < nbBones)
						{
							// if we have more skin bones left, this means we have used up all our bones for this vertex
							// check if any of the remaining bones has a weight > 0
							for (; currentSkinBone < nbBones; ++currentSkinBone)
							{
								float boneWeight = skin.GetWeight(vertexIndex, currentSkinBone);
								if (boneWeight <= 0)
									continue;
								logger?.RaiseError("[BABYLON][ERROR][Mesh] Too many bone influences per vertex for vertexIndex: " + vertexIndex + ". Babylon.js only supports up to 8 bone influences per vertex.", 2);
								break;
							}
						}
					}
				}
			}

			// if we are optimizing our exported vertices, check that a hash-equivalent vertex was already exported.
			if (verticesAlreadyExported != null)
			{
				if (verticesAlreadyExported.ContainsKey(vertex))
				{
					verticesAlreadyExported[vertex].Add(vertex);
					return verticesAlreadyExported[vertex].ElementAt(0).CurrentIndex;
				}
				else
				{
					verticesAlreadyExported[vertex] = new List<GlobalVertex>();
					GlobalVertex modifiedVertex = new GlobalVertex(vertex)
					{
						CurrentIndex = vertices.Count
					};
					verticesAlreadyExported[vertex].Add(modifiedVertex);
					vertex = modifiedVertex;
				}
			}

			vertices.Add(vertex);

			return vertices.Count - 1;
		}

		private void ExportNode(BabylonAbstractMesh babylonAbstractMesh, IIGameNode maxGameNode, IIGameScene maxGameScene, BabylonScene babylonScene)
		{
			// Position / rotation / scaling
			ExportTransform(babylonAbstractMesh, maxGameNode);

			// Hierarchy
			if (maxGameNode.NodeParent != null)
			{
				babylonAbstractMesh.parentId = maxGameNode.NodeParent.MaxNode.GetGuid().ToString();
			}
		}
		private void ExportTransform(BabylonNode babylonAbstractMesh, IIGameNode maxGameNode)
		{
			// Position / rotation / scaling
			IGMatrix localTM = maxGameNode.GetLocalTM(0);

			// Use babylon decomposition, as 3ds max built-in values are no correct
			BabylonMatrix tm_babylon = new BabylonMatrix
			{
				m = localTM.ToArray()
			};

			BabylonVector3 s_babylon = new BabylonVector3();
			BabylonQuaternion q_babylon = new BabylonQuaternion();
			BabylonVector3 t_babylon = new BabylonVector3();

			tm_babylon.decompose(s_babylon, q_babylon, t_babylon);

			// Normalize quaternion
			BabylonQuaternion q = q_babylon;
			float q_length = (float)Math.Sqrt(q.X * q.X + q.Y * q.Y + q.Z * q.Z + q.W * q.W);
			babylonAbstractMesh.rotationQuaternion = new[] { 
				q_babylon.X / q_length, 
				q_babylon.Y / q_length, q_babylon.Z / q_length, 
				q_babylon.W / q_length 
			};

			babylonAbstractMesh.scaling = new[] { s_babylon.X, s_babylon.Y, s_babylon.Z };
			babylonAbstractMesh.position = new[] { t_babylon.X, t_babylon.Y, t_babylon.Z };
		}

		private void ExportAnimation(BabylonNode babylonNode, IIGameNode maxGameNode)
		{
			if (!maxGameNode.MaxNode.IsAnimated) return;
			List<BabylonAnimation> animations = new List<BabylonAnimation>();

			GenerateCoordinatesAnimations(maxGameNode, animations);

			if (!ExportFloatController(maxGameNode.MaxNode.VisController, "visibility", animations))
			{
				ExportFloatAnimation("visibility", animations, key => new[] { maxGameNode.MaxNode.GetVisibility(key, Tools.Forever) });
			}

			babylonNode.animations = animations.ToArray();

			//if (maxGameNode.MaxNode.GetBoolProperty("babylonjs_autoanimate", 1))
			//{
			//	babylonNode.autoAnimate = true;
			//	babylonNode.autoAnimateFrom = (int)maxGameNode.MaxNode.GetFloatProperty("babylonjs_autoanimate_from");
			//	babylonNode.autoAnimateTo = (int)maxGameNode.MaxNode.GetFloatProperty("babylonjs_autoanimate_to", 100);
			//	babylonNode.autoAnimateLoop = maxGameNode.MaxNode.GetBoolProperty("babylonjs_autoanimateloop", 1);
			//}
		}
		public void GenerateCoordinatesAnimations(IIGameNode meshNode, List<BabylonAnimation> animations)
		{
			GeneratePositionAnimation(meshNode, animations);
			GenerateRotationAnimation(meshNode, animations);
			GenerateScalingAnimation(meshNode, animations);
		}

		/// <summary>
		/// get the w of the tangent
		/// </summary>
		/// <param name="normal"></param>
		/// <param name="tangent"></param>
		/// <param name="bitangent"></param>
		/// <returns>
		/// -1 when the normal is not flipped
		/// 1 when the normal is flipped
		/// </returns>
		private int GetW(IPoint3 normal, IPoint3 tangent, IPoint3 bitangent)
		{
			//Cross product bitangent = w * normal ^ tangent
			float x = normal.Y * tangent.Z - normal.Z * tangent.Y;
			float y = normal.Z * tangent.X - normal.X * tangent.Z;
			float z = normal.X * tangent.Y - normal.Y * tangent.X;

			int w = Math.Sign(bitangent.X * x);
			if (w == 0)
			{
				w = Math.Sign(bitangent.Y * y);
			}
			if (w == 0)
			{
				w = Math.Sign(bitangent.Z * z);
			}

			return w;
		}
	}
}
