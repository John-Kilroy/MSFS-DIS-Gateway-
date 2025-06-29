using BabylonExport.Entities;
using GLTFExport.Entities;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;
using Color = System.Drawing.Color;
using System.Linq;
using System.Diagnostics;
using System.Text.RegularExpressions;
using Utilities;

namespace Babylon2GLTF
{
	public partial class GLTFExporter
	{

		public ExportParameters exportParameters;
		private List<BabylonMaterial> babylonMaterials;
		private List<BabylonNode> babylonNodes;
		private BabylonScene babylonScene;
		public ILoggingProvider logger;
		public bool IsCancelled { get; set; }

		// From BabylonNode to GLTFNode
		public Dictionary<BabylonNode, GLTFNode> nodeToGltfNodeMap;
		public Dictionary<BabylonMaterial, GLTFMaterial> materialToGltfMaterialMap;
		//public Dictionary<BabylonCamera, GLTFCamera> cameraToGltfCameraMap; //todo: fill this

		public bool ExportGltf(ExportParameters exportParameters, BabylonScene babylonScene, bool generateBinary, ILoggingProvider logger, Stopwatch watch)
		{
			this.exportParameters = exportParameters;
			this.logger = logger;

			logger?.Print("[GLTFExporter] Export started", Color.Blue);

			this.babylonScene = babylonScene;
			this.babylonMaterials = new List<BabylonMaterial>();

			var gltf = new GLTF(exportParameters.outputPath)
			{
				// Asset
				asset = new GLTFAsset
				{
					version = "2.0"
					// no minVersion
				}
			};

			FlightSimExtension.FlightSimNormalMapConvention.AddNormalMapConvention(ref gltf, exportParameters);
			
			string softwarePackageName = babylonScene.producer != null ? babylonScene.producer.name : "";
			string softwareVersion = babylonScene.producer != null ? babylonScene.producer.version : "";
			string exporterVersion = babylonScene.producer != null ? babylonScene.producer.exporter_version : "";

			gltf.asset.generator = $"babylon.js glTF exporter for {softwarePackageName} {softwareVersion} v{exporterVersion}";

			// Scene
			gltf.scene = 0;

			// Scenes
			GLTFScene scene = new GLTFScene();
			List<GLTFScene> subScenes = new List<GLTFScene>();

			GLTFScene[] scenes = { scene };
			gltf.scenes = scenes;

			// Initialization
			InitBabylonNodes(babylonScene);

			#region Nodes
			logger?.Print("[GLTFExporter][Nodes] Exporting Nodes", Color.Black);
			List<BabylonNode> babylonRootNodes = new List<BabylonNode>();
			if (exportParameters.exportAsSubmodel)
			{
				gltf.asset.generator += " / Exported as submodel";
				// Get the root nodes intialized from the babylonExporter
				babylonRootNodes = babylonScene.RootNodes;
			}
			else
			{
				babylonRootNodes = babylonNodes.FindAll(node => node.parentId == null);
			}

			nodeToGltfNodeMap = new Dictionary<BabylonNode, GLTFNode>();
			materialToGltfMaterialMap  = new Dictionary<BabylonMaterial, GLTFMaterial>();
			NbNodesByName = new Dictionary<string, int>();

			babylonRootNodes.ForEach(babylonNode =>
			{
				ExportNodeRec(babylonNode, gltf, babylonScene);
			});

			if(gltf.NodesList.Count() == 0)
			{
				return false;
			}

			logger?.RaiseWarning(string.Format("[GLTFExporter][Nodes] Total Nodes exported: {0}", gltf.NodesList.Count), 1);
			double nodesExportTime = watch.ElapsedMilliseconds / 1000.0;
			logger?.Print(string.Format("[GLTFExporter][Nodes] Exported in {0:0.00}s", nodesExportTime), Color.Blue);
			#endregion

			#region Meshes
			logger?.Print("[GLTFExporter][Meshs] Exporting Meshes",Color.Black);
			foreach (var babylonMesh in babylonScene.meshes)
			{
				if (gltf.NodesList.Any(x => x.name == babylonMesh.name))
				{
					ExportMesh(babylonMesh, gltf, babylonScene);
				}
			}

			logger?.RaiseWarning(string.Format("[GLTFExporter][Meshs] Total Meshs exported: {0}", gltf.MeshesList.Count), 1);
			var meshesExportTime = watch.ElapsedMilliseconds / 1000.0 - nodesExportTime;
			logger?.Print(string.Format("[GLTFExporter][Meshs] Exported in {0:0.00}s", meshesExportTime), Color.Blue);
			#endregion

			#region Export Nodes (Mesh Skins, light and Cameras)
			logger?.Print("[GLTFExporter][Skins][Lights][Camera] Exporting Skins, Lights and Cameras", Color.Black);
			babylonRootNodes.ForEach(babylonNode =>
			{
				ExportNodeTypeRec(babylonNode, gltf, babylonScene);
			});
			
			logger?.RaiseWarning(string.Format("[GLTFExporter][Skins] Total Skins exported: {0}", gltf.SkinsList.Count), 1);
			double skinLightCameraExportTime = watch.ElapsedMilliseconds / 1000.0 - meshesExportTime;
			logger?.Print(string.Format("[GLTFExporter][Skins][Lights][Camera] Exported in {0:0.00}s", skinLightCameraExportTime), Color.Blue);
			#endregion

			#region Materials
			logger?.Print("[GLTFExporter][Materials] Exporting Materials",Color.Black);
			foreach (var babylonMaterial in babylonMaterials)
			{
				ExportMaterial(babylonMaterial, gltf);
			};

			logger?.RaiseWarning(string.Format("[GLTFExporter][Materials] Total Materials exported: {0}", gltf.MaterialsList.Count), 1);
			var materialsExportTime = watch.ElapsedMilliseconds / 1000.0 - skinLightCameraExportTime;
			logger?.Print(string.Format("[GLTFExporter][Materials] Exported in {0:0.00}s", materialsExportTime), Color.Blue);
			#endregion

			#region Animations
			if (exportParameters.animationExportType != AnimationExportType.NotExport)
			{
				// Animations
				logger?.Print("[GLTFExporter][Animations] Exporting Animations :", Color.Black);

				if(babylonScene.animationGroups == null)
				{
					logger?.RaiseWarning("[GLTFExporter][WARNING][Animations] There are no animations to export", 1);
				}
				else
				{
					ExportAnimationGroups(gltf, babylonScene);
				}

				logger?.RaiseWarning(string.Format("[GLTFExporter][Animations] Total Animations exported: {0}", gltf.AnimationsList.Count), 1);
				var animationGroupsExportTime = watch.ElapsedMilliseconds / 1000.0 - materialsExportTime;
				logger?.Print(string.Format("[GLTFExporter][Animations] Exported in {0:0.00}s", animationGroupsExportTime),
					Color.Blue);
			}
			#endregion

			// Prepare buffers
			gltf.BuffersList.ForEach(buffer =>
			{
				buffer.BufferViews.ForEach(bufferView =>
				{
					bufferView.Accessors.ForEach(accessor =>
					{
						// Chunk must be padded with trailing zeros (0x00) to satisfy alignment requirements
						accessor.bytesList = new List<byte>(PadChunk(accessor.bytesList.ToArray(), 4, 0x00));

						// Update byte properties
						accessor.byteOffset = bufferView.byteLength;
						bufferView.byteLength += accessor.bytesList.Count;
						// Merge bytes
						bufferView.bytesList.AddRange(accessor.bytesList);
					});
					// Update byte properties
					bufferView.byteOffset = buffer.byteLength;
					buffer.byteLength += bufferView.bytesList.Count;
					// Merge bytes
					buffer.bytesList.AddRange(bufferView.bytesList);
				});
			});

			//remove LOD prefix of node of node:
			//x0_name_left -> name_left
			if (exportParameters.removeLodPrefix)
			{
				foreach (GLTFNode gltfNode in gltf.NodesList)
				{
					string pattern = "(?i)x[0-9]_";
					string result = Regex.Replace(gltfNode.name, pattern,"");
					gltfNode.name = result;
				}
			}

			//remove empty space at end
			foreach (GLTFNode gltfNode in gltf.NodesList)
			{
				gltfNode.name = gltfNode.name.TrimEnd();
			}

			// Add scenes extensions
			ExportGLTFExtension(babylonScene, ref gltf.scenes[0], gltf);

			// Output
			logger?.Print("[GLTFExporter] Saving to output file",Color.Black);
			if (!generateBinary) {

				// Cast lists to arrays
				gltf.Prepare();

				// Write .gltf file
				string outputGltfFile = Path.ChangeExtension(exportParameters.outputPath, "gltf");
				File.WriteAllText(outputGltfFile, GltfToJson(gltf));

				// Write .bin file
				string outputBinaryFile = Path.ChangeExtension(exportParameters.outputPath, "bin");
				using (BinaryWriter writer = new BinaryWriter(File.Open(outputBinaryFile, FileMode.Create)))
				{
					gltf.BuffersList.ForEach(buffer =>
					{
						buffer.bytesList.ForEach(b => writer.Write(b));
					});
				}
			}
			else
			{
				// Export glTF data to binary format .glb

				// Header
				UInt32 magic = 0x46546C67; // ASCII code for glTF
				UInt32 version = 2;
				UInt32 length = 12; // Header length

				// --- JSON chunk ---
				UInt32 chunkTypeJson = 0x4E4F534A; // ASCII code for JSON
				// Remove buffers uri
				foreach (GLTFBuffer gltfBuffer in gltf.BuffersList)
				{
					gltfBuffer.uri = null;
				}
				// Switch images to binary
				var imageBufferViews = SwitchImagesFromUriToBinary(gltf);
				imageBufferViews.ForEach(imageBufferView =>
				{
					imageBufferView.Buffer.bytesList.AddRange(imageBufferView.bytesList);
				});
				gltf.Prepare();
				// Serialize gltf data to JSON string then convert it to bytes
				byte[] chunkDataJson = Encoding.ASCII.GetBytes(GltfToJson(gltf));
				// JSON chunk must be padded with trailing Space chars (0x20) to satisfy alignment requirements 
				chunkDataJson = PadChunk(chunkDataJson, 4, 0x20);
				UInt32 chunkLengthJson = (UInt32)chunkDataJson.Length;
				length += chunkLengthJson + 8; // 8 = JSON chunk header length
				
				// bin chunk
				UInt32 chunkTypeBin = 0x004E4942; // ASCII code for BIN
				UInt32 chunkLengthBin = 0;
				if (gltf.BuffersList.Count > 0)
				{
					foreach (GLTFBuffer gltfBuffer in gltf.BuffersList)
					{
						chunkLengthBin += (uint)gltfBuffer.byteLength;
					}
					length += chunkLengthBin + 8; // 8 = bin chunk header length
				}

				// Write binary file
				string outputGlbFile = Path.ChangeExtension(exportParameters.outputPath, "glb");
				using (BinaryWriter writer = new BinaryWriter(File.Open(outputGlbFile, FileMode.Create)))
				{
					// Header
					writer.Write(magic);
					writer.Write(version);
					writer.Write(length);
					
					// JSON chunk
					writer.Write(chunkLengthJson);
					writer.Write(chunkTypeJson);
					writer.Write(chunkDataJson);

					// bin chunk
					if (gltf.BuffersList.Count > 0)
					{
						writer.Write(chunkLengthBin);
						writer.Write(chunkTypeBin);
						gltf.BuffersList[0].bytesList.ForEach(b => writer.Write(b));
					}
				};
			}

			// Draco compression
			if(exportParameters.dracoCompression) // In our case it's always set to "false"
			{
				logger?.RaiseMessage("[GLTFExporter] Draco compression");

				try
				{
					Process gltfPipeline = new Process();
					gltfPipeline.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;

					string arg;
					if (generateBinary)
					{
						string outputGlbFile = Path.ChangeExtension(exportParameters.outputPath, "glb");
						arg = $" -i {outputGlbFile} -o {outputGlbFile} -d";
					}
					else
					{
						string outputGltfFile = Path.ChangeExtension(exportParameters.outputPath, "gltf");
						arg = $" -i {outputGltfFile} -o {outputGltfFile} -d -s";
					}
					gltfPipeline.StartInfo.FileName = "gltf-pipeline.cmd";
					gltfPipeline.StartInfo.Arguments = arg;

					gltfPipeline.Start();
					gltfPipeline.WaitForExit();
				}
				catch
				{
					logger?.RaiseError("[GLTFExporter][ERROR] gltf-pipeline module not found.", 1);
					logger?.RaiseError("[GLTFExporter][ERROR] The exported file wasn't compressed.");
				}
			}

			return true;
		}

		private List<BabylonNode> InitBabylonNodes(BabylonScene babylonScene)
		{
			babylonNodes = new List<BabylonNode>();
			if (babylonScene.meshes != null)
			{
				int idGroupInstance = 0;
				foreach (var babylonMesh in babylonScene.meshes)
				{
					var babylonAbstractMeshes = new List<BabylonAbstractMesh>
					{
						babylonMesh
					};

					if (babylonMesh.instances != null)
					{
						babylonAbstractMeshes.AddRange(babylonMesh.instances);
					}

					// Add mesh and instances to node list
					babylonNodes.AddRange(babylonAbstractMeshes);

					// Tag mesh and instances with an identifier
					babylonAbstractMeshes.ForEach(babylonAbstractMesh => babylonAbstractMesh.idGroupInstance = idGroupInstance);

					idGroupInstance++;
				}
			}
			if (babylonScene.lights != null)
			{
				babylonNodes.AddRange(babylonScene.lights);
			}
			if (babylonScene.cameras != null)
			{
				babylonNodes.AddRange(babylonScene.cameras);
			}

			if (babylonScene.SkeletonsList != null)
			{
				foreach (BabylonSkeleton babylonSkeleton in babylonScene.SkeletonsList)
				{
					foreach (BabylonBone babylonSkeletonBone in babylonSkeleton.bones)
					{
						if(!babylonNodes.Exists(x => x.id == babylonSkeletonBone.id))
						{
							babylonNodes.Add(BoneToNode(babylonSkeletonBone));
						}
					}
				   
				}
			}

			return babylonNodes;
		}

		private void ExportNodeRec(BabylonNode babylonNode, GLTF gltf, BabylonScene babylonScene, GLTFNode gltfParentNode = null)
		{
			GLTFNode gltfNode = null;

			// We check if the node is not already expoted, if true we return the node
			var nodeNodePair = nodeToGltfNodeMap.FirstOrDefault(pair => pair.Key.id.Equals(babylonNode.id));
			if (nodeNodePair.Key != null)
			{
				gltfNode = nodeNodePair.Value;
			}
			else
			{
				gltfNode = ExportNode(babylonNode, gltf, babylonScene, gltfParentNode);
			}
			
			if (gltfNode != null)
			{
				// Export its tag
				if (!string.IsNullOrEmpty(babylonNode.tags))
				{
					if (gltfNode.extras == null)
					{
						gltfNode.extras = new Dictionary<string, object>();
					}
					gltfNode.extras["tags"] = babylonNode.tags;
				}

				if (exportParameters.enableASBUniqueID) 
				{
					ASOBOUniqueIDExtension(ref gltf, ref gltfNode, babylonNode);
				}

				// ...export its children
				List<BabylonNode> babylonDescendants = GetDescendants(babylonNode);
				babylonDescendants.ForEach(descendant => ExportNodeRec(descendant, gltf, babylonScene, gltfNode));
			}
		}
		private void ExportNodeTypeRec(BabylonNode babylonNode, GLTF gltf, BabylonScene babylonScene, GLTFNode gltfParentNode = null)
		{
			var type = babylonNode.GetType();
			logger?.RaiseMessage($"[GLTFExporter] Export Node {babylonNode.name} of Type {type}", 1);

			var nodeNodePair = nodeToGltfNodeMap.FirstOrDefault(pair => pair.Key.id.Equals(babylonNode.id));
			GLTFNode gltfNode = nodeNodePair.Value;

			if (gltfNode != null)
			{
				if (type == typeof(BabylonAbstractMesh) || type.IsSubclassOf(typeof(BabylonAbstractMesh)))
				{
					gltfNode = ExportAbstractMesh(ref gltfNode, babylonNode as BabylonAbstractMesh, gltf, gltfParentNode, babylonScene);
				}
				else if (type == typeof(BabylonCamera))
				{
					GLTFCamera gltfCamera = ExportCamera(ref gltfNode, babylonNode as BabylonCamera, gltf, gltfParentNode);
				}
				else if (type == typeof(BabylonLight) || type.IsSubclassOf(typeof(BabylonLight)))
				{
					if(((BabylonLight)babylonNode).type != 3)
					{
						ExportLight(ref gltfNode, babylonNode as BabylonLight, gltf, gltfParentNode, babylonScene);
					}
				}
				else if (type != typeof(BabylonNode))
				{
					logger?.RaiseError($"[GLTFExporter][ERROR] Node named {babylonNode.name} has no exporter for its type {type}", 1);
				}

				// ...export its children
				List<BabylonNode> babylonDescendants = GetDescendants(babylonNode);
				babylonDescendants.ForEach(descendant => ExportNodeTypeRec(descendant, gltf, babylonScene, gltfNode));
			}
		}

		private List<BabylonNode> GetDescendants(BabylonNode babylonNode)
		{
			return babylonNodes.FindAll(node => node.parentId == babylonNode.id);
		}

		/// <summary>
		/// Return true if node descendant hierarchy has any Mesh or Camera to export
		/// </summary>
		private bool IsNodeRelevantToExport(BabylonNode babylonNode)
		{
			var type = babylonNode.GetType();
			if (type == typeof(BabylonAbstractMesh) ||
				type.IsSubclassOf(typeof(BabylonAbstractMesh)) ||
				type == typeof(BabylonCamera))
			{
				return true;
			}

			// Descandant recursivity
			List<BabylonNode> babylonDescendants = GetDescendants(babylonNode);
			int indexDescendant = 0;
			while (indexDescendant < babylonDescendants.Count) // while instead of for to stop as soon as a relevant node has been found
			{
				if (IsNodeRelevantToExport(babylonDescendants[indexDescendant]))
				{
					return true;
				}
				indexDescendant++;
			}

			// No relevant node found in hierarchy
			return false;
		}

		private string GltfToJson(GLTF gltf)
		{
			var jsonSerializer = JsonSerializer.Create(new JsonSerializerSettings());
			var sb = new StringBuilder();
			var sw = new StringWriter(sb, CultureInfo.InvariantCulture);

			// Do not use the optimized writer because it's not necessary to truncate values
			// Use the bounded writer in case some values are infinity ()
			using (var jsonWriter = new JsonTextWriterBounded(sw))
			{
#if DEBUG
				jsonWriter.Formatting = Formatting.Indented;
#else
				jsonWriter.Formatting = Formatting.None;
#endif
				jsonSerializer.Serialize(jsonWriter, gltf);
			}
			return sb.ToString();
		}

		private List<GLTFBufferView> SwitchImagesFromUriToBinary(GLTF gltf)
		{
			var imageBufferViews = new List<GLTFBufferView>();

			foreach (GLTFImage gltfImage in gltf.ImagesList)
			{
				var path = Path.Combine(gltf.OutputFolder, gltfImage.uri);
				byte[] imageBytes = File.ReadAllBytes(path);

				// Chunk must be padded with trailing zeros (0x00) to satisfy alignment requirements
				imageBytes = PadChunk(imageBytes, 4, 0x00);

				// BufferView - Image
				var buffer = gltf.buffer;
				var bufferViewImage = new GLTFBufferView
				{
					name = "bufferViewImage",
					buffer = buffer.index,
					Buffer = buffer,
					byteOffset = buffer.byteLength
				};
				bufferViewImage.index = gltf.BufferViewsList.Count;
				gltf.BufferViewsList.Add(bufferViewImage);
				imageBufferViews.Add(bufferViewImage);


				gltfImage.uri = null;
				gltfImage.bufferView = bufferViewImage.index;
				gltfImage.mimeType = "image/" + gltfImage.FileExtension;

				bufferViewImage.bytesList.AddRange(imageBytes);
				bufferViewImage.byteLength += imageBytes.Length;
				bufferViewImage.Buffer.byteLength += imageBytes.Length;
			}
			return imageBufferViews;
		}
		private byte[] PadChunk(byte[] chunk, int padding, byte trailingChar)
		{
			var chunkModuloPadding = chunk.Length % padding;
			var nbCharacterToAdd = chunkModuloPadding == 0 ? 0 : (padding - chunkModuloPadding);
			var chunkList = new List<byte>(chunk);
			for (int i = 0; i < nbCharacterToAdd; i++)
			{
				chunkList.Add(trailingChar);
			}
			return chunkList.ToArray();
		}

		/// <summary>
		/// Create a gltf node from the babylon node.
		/// </summary>
		/// <param name="babylonNode"></param>
		/// <param name="gltf"></param>
		/// <param name="babylonScene"></param>
		/// <param name="gltfParentNode">The parent of the glTF node that will be created.</param>
		/// <returns>The gltf node created.</returns>
		private GLTFNode ExportNode(BabylonNode babylonNode, GLTF gltf, BabylonScene babylonScene, GLTFNode gltfParentNode)
		{
			// Node
			GLTFNode gltfNode = new GLTFNode
			{
				//GetUniqueNodeName(babylonNode.name))
				name = babylonNode.name,
				index = gltf.NodesList.Count
			};

			// User Custom Attributes
			if (babylonNode.metadata != null && babylonNode.metadata.Count != 0)
			{
				gltfNode.extras = babylonNode.metadata;
			}

			logger?.Print($"[GLTFExporter][Node] Exporting node : {babylonNode.name}", Color.Black);
			gltf.NodesList.Add(gltfNode);   // Add the node to the gltf list
			nodeToGltfNodeMap.Add(babylonNode, gltfNode);   // add the node to the global map


			// Hierarchy
			if (gltfParentNode != null)
			{
				logger?.RaiseMessage("GLTFExporter.Node| Add " + babylonNode.name + " as child to " + gltfParentNode.name, 2);
				gltfParentNode.ChildrenList.Add(gltfNode.index);
				gltfNode.parent = gltfParentNode;
			}
			else
			{
				// It's a root node
				// Only root nodes are listed in a gltf scene
				logger?.RaiseMessage("GLTFExporter.Node | Add " + babylonNode.name + " as root node to scene", 2);

				gltf.scenes[0].NodesList.Add(gltfNode.index);
			}

			// Transform
			// Position
			gltfNode.translation = babylonNode.position;

			// Rotation
			if (babylonNode.rotationQuaternion != null)
			{
				gltfNode.rotation = babylonNode.rotationQuaternion;
			}
			else
			{
				// Convert rotation vector to quaternion
				BabylonVector3 rotationVector3 = new BabylonVector3
				{
					X = babylonNode.rotation[0],
					Y = babylonNode.rotation[1],
					Z = babylonNode.rotation[2]
				};
				gltfNode.rotation = rotationVector3.toQuaternion().ToArray();
				}

			// Scale
			gltfNode.scale = babylonNode.scaling;

			// Switch coordinate system at object level
			gltfNode.translation[2] *= -1;
			gltfNode.translation[0] *= exportParameters.scaleFactor;
			gltfNode.translation[1] *= exportParameters.scaleFactor;
			gltfNode.translation[2] *= exportParameters.scaleFactor;
			gltfNode.rotation[0] *= -1;
			gltfNode.rotation[1] *= -1;

			ExportGLTFExtension(babylonNode, ref gltfNode, gltf);
			
			return gltfNode;
		}

		private void ExportGLTFExtension<T1,T2>(T1 babylonObject, ref T2 gltfObject, GLTF gltf, ExtensionInfo extInfo = null) where T2:GLTFProperty
		{
			GLTFExtensions nodeExtensions = gltfObject.extensions ?? new GLTFExtensions();
			foreach (var extensionExporter in babylonScene.BabylonToGLTFExtensions)
			{
				if (extensionExporter.Value.gltfType == typeof(T2))
				{
					string extensionName = extensionExporter.Key.GetGLTFExtensionName();
					object extensionObject = extensionExporter.Key.ExportGLTFExtension(babylonObject,ref gltfObject, ref gltf,this,extInfo);
					if (extensionObject != null && !string.IsNullOrEmpty(extensionName) && !nodeExtensions.ContainsKey(extensionName))
					{
						nodeExtensions.Add(extensionName,extensionObject);
					}
				}
			}
			if (nodeExtensions.Count > 0)
			{
				gltfObject.extensions = nodeExtensions;

				if (gltf.extensionsUsed == null)
				{
					gltf.extensionsUsed = new List<string>();
				}

				foreach (KeyValuePair<string, object> extension in gltfObject.extensions)
				{
					if (!gltf.extensionsUsed.Contains(extension.Key))
					{
						gltf.extensionsUsed.Add(extension.Key);
					}
				}
			}
		}
	}
}
