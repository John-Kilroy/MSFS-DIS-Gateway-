using Autodesk.Max;
using BabylonExport.Entities;
using Babylon2GLTF;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;
using Color = System.Drawing.Color;
using Utilities;
using System.Configuration;

namespace MSFS2024_Max2Babylon
{
	public partial class BabylonExporter
	{
		public ILoggingProvider logger;
		public BabylonExporter(ILoggingProvider _logger) 
		{
			logger = _logger;
		}
		public Form callerForm;
		public ExportParameters exportParameters;
		public bool IsCancelled { get; set; }
		public string MaxSceneFileName { get; set; }
		private bool isGltfExported;
		private bool optimizeAnimations = true;
		public float scaleFactor = 1.0f;
		public const int MaxSceneTicksPerSecond = 4800; //https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2016/ENU/MAXScript-Help/files/GUID-141213A1-B5A8-457B-8838-E602022C8798-htm.html
		public static string exporterVersion = ConfigurationValue;


		public static string ConfigurationValue
		{
			get
			{
				string title = "1.0.0.0";
				string dllPath = Assembly.GetExecutingAssembly().Location;
				string dllFolder = Path.GetDirectoryName(dllPath);
				string configPath = Path.Combine(dllFolder, "MSFS2024_Max2Babylon.dll.config");
				if (File.Exists(configPath))
				{
					ExeConfigurationFileMap fileMap = new ExeConfigurationFileMap();
					fileMap.ExeConfigFilename = configPath;
					Configuration config = ConfigurationManager.OpenMappedExeConfiguration(fileMap, ConfigurationUserLevel.None);
					var key = config.AppSettings.Settings["Version"];
					if (key != null)
					{
						title = key.Value;
					}
				}

				return title;
			}
		}

		public void Export(ExportParameters exportParameters)
		{

			Stopwatch watch = new Stopwatch();
			watch.Start();

			// Initialisation
			this.exportParameters = exportParameters;

			IINode exportNode = null;

			string flattenLayerName = "[Temp: delete me] Flatten export layer";

			MaxExportParameters maxExportParameters = null;
			if (exportParameters is MaxExportParameters)
			{
				maxExportParameters = (exportParameters as MaxExportParameters);
				if (logger!= null) logger.LoggerLevel = maxExportParameters.logLevel;
				exportNode = maxExportParameters.exportNode;

				#region Flatten
				if (exportNode != null && maxExportParameters.flattenNodes)
				{
					exportNode = exportNode.CreateMergedMesh(flattenLayerName);
					if (exportNode == null)
					{
						logger?.RaiseError("[BABYLON][ERROR] Flatten Nodes option resulted in empty mesh.");
						return;
					}
				}
				#endregion
			}

			if (exportNode == null && maxExportParameters.ExportLayers == null)
			{
				logger?.RaiseError("[BABYLON][ERROR] Nothing to export! Unexpected error: cleanup your scene to remove any unneeded object may help.");
				return;
			}
			bool fromPresetPanel = maxExportParameters.exportNode == null && maxExportParameters.ExportLayers != null;

			//Set the export path
			string fileExportString = fromPresetPanel ? exportParameters.outputPath : $"{exportNode.NodeName} | {exportParameters.outputPath}";

			// Set Scale factor depending on unit used in the scene
			this.scaleFactor = Tools.GetScaleFactorToMeters();

			// Set the text quality
			long quality = exportParameters.txtQuality;
			try
			{
				if (quality < 0 || quality > 100)
				{
					throw new Exception();
				}
			}
			catch
			{
				logger?.RaiseError("[BABYLON][ERROR] Texture Quality is not a valid number. It should be an integer between 0 and 100.");
				logger?.RaiseError("[BABYLON][ERROR] This parameter sets the quality of jpg compression.");
				return;
			}

			// Set the game scene from 3DSMAX
			IIGameConversionManager gameConversionManger = Loader.Global.ConversionManager;
			gameConversionManger.CoordSystem = Autodesk.Max.IGameConversionManager.CoordSystem.D3d;
			IIGameScene gameScene = Loader.Global.IGameInterface;

			if (fromPresetPanel) // (Preset Panel from the multiexporter view)
			{
				// Select Nodes from selected layers 
				IINodeTab selection = LayerUtilities.GetNodeTabLayersChildren(maxExportParameters.ExportLayers);
				if (selection != null)
				{
					Loader.Core.SelectNodeTab(selection, true, true);
				}
				else
				{
					logger?.RaiseError($"[BABYLON][ERROR] There is nothing to export in the selected layers for : {exportParameters.outputPath}.");
					return;
				}

				// NOTE : we might use gameScene.InitialiseIGame(exportParameters.exportOnlySelected) instead of gameScene.InitialiseIGame(false),
				// but the SDK do NOT return linked object as part of the selection.
				gameScene.InitialiseIGame(false);
			}
			else // Select the hierarchy of a root object given (Object Panel from the multiexporter view)
			{
				Loader.Core.SelectNode(exportNode, true); // Clear selection and select parent node only

				foreach (IINode child in exportNode.NodeTree())
				{
					Loader.Core.SelectNode(child, false); // Add each child to selection
				}

				gameScene.InitialiseIGame(exportNode, true);
			}
			
			// Reset Frame to 0
			gameScene.SetStaticFrame(0);

			// Check ASOBO Unique IDs conflict
			Tools.InitializeGuidsMap();
			if (exportParameters.enableASBUniqueID)
			{
				IEnumerable<IINode> nodes = Loader.Core.RootNode.NodeTree();
				if (Tools.HasUniqueIdConflict(nodes, logger))
				{
					logger?.RaiseMessage("--------------------------------------------------------------------------------------------------------------------------------------------------------");
					Tools.ResolveUniqueIDConflict(nodes, logger);
					logger?.RaiseMessage("--------------------------------------------------------------------------------------------------------------------------------------------------------");
				}
			}

			MaxSceneFileName = gameScene.SceneFileName;
			IsCancelled = false;

			logger?.Print($"[BABYLON] Export started: {fileExportString}", Color.Black, 20);

			// Set directories
			string outputDirectory = Path.GetDirectoryName(exportParameters.outputPath);
			string outputFileName = Path.GetFileName(exportParameters.outputPath);

			// Check directory exists
			if (!Directory.Exists(outputDirectory))
			{
				throw new System.Exception($"[BABYLON][ERROR] Export stopped: Output folder {outputDirectory} does not exist.");
			}


			FileInfo fInfo = new FileInfo(exportParameters.outputPath);
			if (fInfo.Exists && fInfo.IsReadOnly)
			{
				throw new System.Exception($"[BABYLON][ERROR] Export stopped: Output File {exportParameters.outputPath} is ReadOnly.");
			}

			string binFile = Path.ChangeExtension(exportParameters.outputPath, ".bin");
			fInfo = new FileInfo(binFile);
			if (fInfo.Exists && fInfo.IsReadOnly)
			{
				throw new System.Exception($"[BABYLON][ERROR] Export stopped: Output File {binFile} is ReadOnly.");
			}

			// Prepare scene
			BabylonScene babylonScene = new BabylonScene(outputDirectory);
			IINode rootSceneNode = Loader.Core.RootNode;

			string outputFormat = exportParameters.outputFormat;
			isGltfExported = (outputFormat == "gltf" || outputFormat == "glb");

			// Producer
			babylonScene.producer = new BabylonProducer
			{
				name = "3dsmax",
#if MAX2024
				version = "2024",
#elif MAX2023
				version = "2023",
#elif MAX2022
				version = "2022",
#elif MAX2021
				version = "2021",
#elif MAX2020
				version = "2020",
#elif MAX2019
				version = "2019",
#elif MAX2018
				version = "2018",
#elif MAX2017
				version = "2017",
#else
			   version = Loader.Core.ProductVersion.ToString(),
#endif
				exporter_version = exporterVersion,
				file = outputFileName
			};

			// Global
			babylonScene.TimelineStartFrame = Loader.Core.AnimRange.Start / Loader.Global.TicksPerFrame;
			babylonScene.TimelineEndFrame = Loader.Core.AnimRange.End / Loader.Global.TicksPerFrame;
			babylonScene.TimelineFramesPerSecond = MaxSceneTicksPerSecond / Loader.Global.TicksPerFrame;

			// Instantiate custom material exporters
			foreach (Type type in Tools.GetAllLoadableTypes())
			{
				if (type.IsAbstract || type.IsInterface)
					continue;

				if (typeof(IBabylonExtensionExporter).IsAssignableFrom(type))
				{
					IBabylonExtensionExporter exporter = Activator.CreateInstance(type) as IBabylonExtensionExporter;

					if (exporter == null)
						logger?.RaiseWarning("[BABYLON][WARNING] Creating exporter instance failed: " + type.Name, 1);

					ExtendedTypes t = exporter.GetExtendedType();
					babylonScene.BabylonToGLTFExtensions.Add(exporter, t);
				}
			}

			#region Nodes
			// Root nodes
			if (exportParameters.exportAsSubmodel) logger?.RaiseWarning("[BABYLON][WARNING] Exported As SubModel");
			logger?.Print("[BABYLON][Nodes] Exporting Nodes",Color.Black);
			HashSet<IIGameNode> maxRootNodes = GetRootNodes(gameScene);
			
			// Reset referenced scene Materials
			referencedMaterials.Clear();

			// Reseting is optional. It makes each morph target manager export starts from id = 0.
			BabylonMorphTargetManager.Reset();

			List<BabylonNode> rootNodes = new List<BabylonNode>();
			if (exportParameters.exportAsSubmodel)
			{
				rootNodes = SetRootNodesForSubmodel(gameScene, fromPresetPanel, babylonScene, exportParameters, maxRootNodes);
			}
			else
			{
				rootNodes = SetRootNodesForBaseModel(gameScene, exportNode, fromPresetPanel, babylonScene, exportParameters, maxRootNodes);
			}

			if (rootNodes.Count() > 0)
			{
				babylonScene.RootNodes.AddRange(rootNodes);
				logger?.RaiseWarning(string.Format("[BABYLON][Nodes] Total Nodes: {0}", babylonScene.NodeMap.Count), 1);
			}

			var nodesExportTime = watch.ElapsedMilliseconds / 1000.0;
			logger?.Print($"[BABYLON][Nodes] Exported in {nodesExportTime:0.00}s", Color.Blue);
			#endregion

			#region Camera
			// In 3DS Max the default camera look down (in the -z direction for the 3DS Max reference (+y for babylon))
			// In Babylon the default camera look to the horizon (in the +z direction for the babylon reference)
			// In glTF the default camera look to the horizon (in the +Z direction for glTF reference)
			logger?.Print("[BABYLON][Cameras] Exporting Cameras", Color.Black);
			for (int index = 0; index < babylonScene.CamerasList.Count; index++)
			{
				BabylonCamera camera = babylonScene.CamerasList[index];
				logger?.Print($"[BABYLON][Camera] Update rotation and position for camera: {camera.name}", Color.Black);
				FixCamera(ref camera, ref babylonScene);
			}

			// Main camera
			BabylonCamera babylonMainCamera = null;
			ICameraObject maxMainCameraObject = null;
			if (babylonMainCamera == null && babylonScene.CamerasList.Count > 0)
			{
				// Set first camera as main one
				babylonMainCamera = babylonScene.CamerasList[0];
				babylonScene.activeCameraID = babylonMainCamera.id;
				logger?.Print("[BABYLON][Camera] Active camera set to " + babylonMainCamera.name, Color.Green, 1, true);

				// Retrieve camera node with same GUID
				var maxCameraNodesAsTab = gameScene.GetIGameNodeByType(Autodesk.Max.IGameObject.ObjectTypes.Camera);
				var maxCameraNodes = TabToList(maxCameraNodesAsTab);
				var maxMainCameraNode = maxCameraNodes.Find(_camera => _camera.MaxNode.GetGuid().ToString() == babylonMainCamera.id);
				maxMainCameraObject = (maxMainCameraNode.MaxNode.ObjectRef as ICameraObject);
			}
			logger?.RaiseWarning(string.Format("[BABYLON][Cameras] Total Cameras: {0}", babylonScene.CamerasList.Count), 1);
			var cameraExportTime = watch.ElapsedMilliseconds / 1000.0 - nodesExportTime;
			logger?.Print($"[BABYLON][Cameras][Lights] Exported in {cameraExportTime:0.00}s", Color.Blue);
			#endregion

			#region Lights
			// Light for glTF
			logger?.Print("[BABYLON][Lights] Exporting Lights", Color.Black);
			if (isGltfExported)
			{
				for (int index = 0; index < babylonScene.LightsList.Count; index++)
				{
					BabylonNode light = babylonScene.LightsList[index];
					logger?.Print($"[BABYLON][Light] Update rotation for light: {light.name}", Color.Black);
					FixNodeRotation(ref light, ref babylonScene, -Math.PI / 2);
				}
			}
			logger?.RaiseWarning(string.Format("[BABYLON][Lights] Total Lights: {0}", babylonScene.LightsList.Count), 1);

			var lightsExportTime = watch.ElapsedMilliseconds / 1000.0 - cameraExportTime;
			logger?.Print($"[BABYLON][Lights] Exported in {lightsExportTime:0.00}s", Color.Blue);
			#endregion

			#region Scale Nodes (nodes, cameras, lights)
			if (exportParameters.scaleFactor != 1.0f)
			{
				logger?.Print(String.Format("[BABYLON][Node] A root node is added to globally scale the scene by {0}", exportParameters.scaleFactor), Color.Black);

				// Create root node for scaling
				BabylonMesh rootNode = new BabylonMesh { name = "root", id = Guid.NewGuid().ToString() };
				float rootNodeScale = exportParameters.scaleFactor;
				rootNode.scaling = new float[3] { rootNodeScale, rootNodeScale, rootNodeScale };
				rootNode.rotationQuaternion = new float[] { 0, 0, 0, 1 };

				// Update all top nodes
				var babylonNodes = new List<BabylonNode>();
				babylonNodes.AddRange(babylonScene.MeshesList);
				babylonNodes.AddRange(babylonScene.CamerasList);
				babylonNodes.AddRange(babylonScene.LightsList);
				foreach (BabylonNode babylonNode in babylonNodes)
				{
					if (babylonNode.parentId == null)
					{
						babylonNode.parentId = rootNode.id;
					}
				}

				// Store root node
				if (!babylonScene.MeshesList.Any(x => x.id == rootNode.id)) babylonScene.MeshesList.Add(rootNode);
			}
			#endregion
			
			#region Materials
			logger?.Print("[BABYLON][Materials] Exporting Materials",Color.Black);
			if (exportParameters.exportMaterials)
			{
				var matsToExport = referencedMaterials.ToArray(); // Snapshot because multimaterials can export new materials
				foreach (var mat in matsToExport)
				{
					ExportMaterial(mat, babylonScene);
				}
			}
			else
			{
				logger?.RaiseWarning("[BABYLON][WARNING][Materials] Skipping material export.");
			}
			
			var materialsExportTime = watch.ElapsedMilliseconds / 1000.0 - lightsExportTime;
			logger?.Print($"[BABYLON][Materials] Materials exported in {materialsExportTime:0.00}s", Color.Blue);
			#endregion

			#region Skeletons
			if (skins.Count > 0)
			{
				logger?.Print("[BABYLON][Skeletons] Exporting Skeletons", Color.Black);
				foreach (var skin in skins)
				{
					ExportSkin(skin, babylonScene);
				}

				var skeletonsExportTime = watch.ElapsedMilliseconds / 1000.0 - materialsExportTime;
				logger?.Print($"[BABYLON][Skeletons] Skeletons exported in {skeletonsExportTime:0.00}s", Color.Blue);
			}
			#endregion

			#region Animations
			logger?.Print("[BABYLON][Animations] Export Animation Groups", Color.Black);
			babylonScene.animationGroups = new List<BabylonAnimationGroup>();

			if (exportParameters.animationExportType != AnimationExportType.NotExport)
			{
				babylonScene.animationGroups = ExportAnimationGroups(babylonScene);
			}

			logger?.RaiseWarning(string.Format("[BABYLON][Animations] Total Animations: {0}", babylonScene.animationGroups.Count), 1);
			var animationGroupExportTime = watch.ElapsedMilliseconds / 1000.0 - materialsExportTime;
			logger?.Print(string.Format("[BABYLON][Animations] Animation Groups exported in {0:0.00}s", animationGroupExportTime), Color.Blue);
			#endregion

			#region Export
			// Output
			babylonScene.Prepare(false, false);

			bool isExported = false;

			// Export glTF
			if (isGltfExported)
			{
				bool generateBinary = (outputFormat == "glb");

				GLTFExporter gltfExporter = new GLTFExporter();
				isExported = gltfExporter.ExportGltf(this.exportParameters, babylonScene, generateBinary, logger, watch);
			}
			else
			{
				logger?.RaiseError(string.Format("[BABYLON][ERROR] Export failed : Output format should be \"glTF\" or \"glb\" but got : {0}", fileExportString));
			}

			if (isExported)
			{
				if(maxExportParameters.flattenNodes && !fromPresetPanel)
				{
					exportNode.DeleteHierarchyNodes();
					LayerUtilities.DeleteSceneLayer(flattenLayerName);
				}
				logger?.Print(string.Format("[BABYLON] Export done in {0:0.00}s: {1}", watch.ElapsedMilliseconds / 1000.0, fileExportString), Color.Blue);
				IUTF8Str max_notification = Autodesk.Max.GlobalInterface.Instance.UTF8Str.Create("BabylonExportComplete");
				Loader.Global.BroadcastNotification(SystemNotificationCode.PostExport, max_notification);
			}
			else
			{
				logger?.RaiseError(string.Format("[BABYLON][ERROR] Export failed due to empty gltf: {0}", fileExportString));
			}
			#endregion
		}

		private BabylonNode ExportNodeRec(IIGameNode maxGameNode, BabylonScene babylonScene, IIGameScene maxGameScene, bool fromPresetPanel, bool setAsNewRoot = false, BabylonMatrix parentTransform = null)
		{
			BabylonNode babylonNode = null;

			bool isNodeExportable = IsNodeRelevantToExport(maxGameNode);

			if (!babylonScene.NodeMap.ContainsKey(maxGameNode.MaxNode.GetGuid().ToString()))
			{
				if (isNodeExportable)
				{
					try
					{
						switch (maxGameNode.IGameObject.IGameType)
						{
							case Autodesk.Max.IGameObject.ObjectTypes.Mesh:
								babylonNode = ExportMesh(maxGameScene, maxGameNode, babylonScene);
								break;
							case Autodesk.Max.IGameObject.ObjectTypes.Camera:
								babylonNode = ExportCamera(maxGameScene, maxGameNode, babylonScene);
								break;
							case Autodesk.Max.IGameObject.ObjectTypes.Light:
								babylonNode = ExportLight(maxGameScene, maxGameNode, babylonScene);
								break;
							default:
								// The type of node is not exportable (helper, spline, xref...)
								babylonNode = ExportDummy(maxGameScene, maxGameNode, babylonScene);
								break;
						}
					}
					catch (Exception E)
					{
						throw new System.Exception(E.Message);
					};

					if (babylonNode != null)
					{
						if (setAsNewRoot)
						{
							babylonNode.parentId = null;
							if (parentTransform != null)
							{
								MoveNodeTransform(ref babylonNode, parentTransform);
							}
						}

						#region KeepTransform Node
						bool exportTransform = maxGameNode.MaxNode.GetBoolProperty("flightsim_export_transform", 1);
						bool exportPosition = maxGameNode.MaxNode.GetBoolProperty("flightsim_export_position", Convert.ToInt16(exportTransform));
						bool exportRotation = maxGameNode.MaxNode.GetBoolProperty("flightsim_export_rotation", Convert.ToInt16(exportTransform));
						bool exportScale = maxGameNode.MaxNode.GetBoolProperty("flightsim_export_scale", Convert.ToInt16(exportTransform));

						if (!exportPosition && !exportRotation && !exportScale)
						{
							SetNodeTransform(ref babylonNode, BabylonMatrix.Identity());
						}
						else if (!exportPosition || !exportRotation || !exportScale)
						{
							var newPos = babylonNode.position;
							var newRotQuat = babylonNode.rotationQuaternion;
							var newScale = babylonNode.scaling;
							if (!exportPosition)
							{
								newPos = new float[] { 0, 0, 0 };
							}
							if (!exportRotation)
							{
								newRotQuat = new float[] { 0, 0, 0, 1 };
							}
							if (!exportScale)
							{
								newScale = new float[] { 1, 1, 1 };
							}
							var newTransform = BabylonMatrix.Compose(
								BabylonVector3.FromArray(newScale),
								BabylonQuaternion.FromArray(newRotQuat),
								BabylonVector3.FromArray(newPos)
							);
							SetNodeTransform(ref babylonNode, newTransform);
						}
						#endregion

						string tag = maxGameNode.MaxNode.GetStringProperty("babylonjs_tag", "");
						if (tag != "")
						{
							babylonNode.tags = tag;
						}

						babylonNode.UniqueID = maxGameNode.MaxNode.GetUniqueID();
						babylonScene.NodeMap[babylonNode.id] = babylonNode;
					}
					
					setAsNewRoot = false;
				}
			}
			else
			{
				babylonNode = babylonScene.NodeMap[maxGameNode.MaxNode.GetGuid().ToString()];

			}

			if (fromPresetPanel || isNodeExportable) // From objects panel: dont need to try to export children if parent is not exported
			{
				if (setAsNewRoot)
				{
					if (parentTransform == null)
					{
						parentTransform = BabylonMatrix.Identity();
					}
					parentTransform *= GetMaxNodeTransform(ref maxGameNode);
				}

				// Export its children
				for (int i = 0; i < maxGameNode.ChildCount; i++)
				{
					var descendant = maxGameNode.GetNodeChild(i);
					ExportNodeRec(descendant, babylonScene, maxGameScene, fromPresetPanel, setAsNewRoot, parentTransform);
				}
			}

			return babylonNode;
		}

		private void CalculateSkeletonList(IIGameNode maxGameNode, BabylonScene babylonScene, IIGameScene maxGameScene )
		{
			if (maxGameNode.IGameObject.IGameType is Autodesk.Max.IGameObject.ObjectTypes.Mesh)
			{
				var gameMesh = maxGameNode.IGameObject.AsGameMesh();
				// Skin
				var isSkinned = gameMesh.IsObjectSkinned;
				var skin = gameMesh.IGameSkin;
				IGMatrix skinInitPoseMatrix = Loader.Global.GMatrix.Create(Loader.Global.Matrix3.Create(true));

				if (isSkinned && GetSkinnedBones(skin, maxGameNode).Count > 0)  // if the mesh has a skin with at least one bone
				{
					var skinAlreadyStored = skins.Find(_skin => IsSkinEqualTo(_skin, skin));
					if (skinAlreadyStored == null)
					{
						skins.Add(skin);
						skinNodeMap.Add(skin,maxGameNode);
					}

					skin.GetInitSkinTM(skinInitPoseMatrix);
				}
			}
			else
			{
				if (IsNodeExportable(maxGameNode))
				{
					BabylonNode babylonNode = ExportDummy(maxGameScene, maxGameNode, babylonScene);
					babylonScene.NodeMap[babylonNode.id] = babylonNode;
				}
			}

			for (int i = 0; i < maxGameNode.ChildCount; i++)
			{
				var descendant = maxGameNode.GetNodeChild(i);
				CalculateSkeletonList(descendant,babylonScene,maxGameScene);
			}

			
		}
		private List<IIGameNode> CalculateSubModelSkinsDependencies(IIGameNode maxGameNode, BabylonScene babylonScene, IIGameScene maxGameScene)
		{
			List<IIGameNode> subModelDeps = new List<IIGameNode>();
			if (maxGameNode.IGameObject.IGameType is Autodesk.Max.IGameObject.ObjectTypes.Mesh)
			{
				var gameMesh = maxGameNode.IGameObject.AsGameMesh();
				// Skin
				var isSkinned = gameMesh.IsObjectSkinned;
				var skin = gameMesh.IGameSkin;

				if (isSkinned && maxGameNode.MaxNode.Selected) subModelDeps = GetSubModelSkinHierarchy(skin, maxGameNode); // if the mesh has a skin with at least one bone
			}

			for (int i = 0; i < maxGameNode.ChildCount; i++)
			{
				var descendant = maxGameNode.GetNodeChild(i);
				subModelDeps.AddRange(CalculateSubModelSkinsDependencies(descendant, babylonScene, maxGameScene));
			}

			return subModelDeps;
		}
		private BabylonNode CalculateSubModelBonesDependencies(IIGameNode maxGameNode, BabylonScene babylonScene, IIGameScene maxGameScene) 
		{
			BabylonNode subModelRoot = null;
			List<IIGameNode> subModelDeps = CalculateSubModelSkinsDependencies(maxGameNode, babylonScene, maxGameScene);

			foreach (IIGameNode subModelDep in subModelDeps)
			{
				if (!subModelDep.MaxNode.Selected)
				{
					BabylonNode babylonNode = ExportSubModelExtraNode(maxGameScene, subModelDep, babylonScene);
					babylonNode.extraNode = true;
					if (!subModelDeps.Contains(subModelDep.NodeParent)) subModelRoot = babylonNode;
					babylonScene.NodeMap[babylonNode.id] = babylonNode;
				}

			}
			return subModelRoot;
		}

		/// <summary>
		/// Return true if node descendant hierarchy has any exportable Mesh, Camera or Light
		/// </summary>
		private bool IsNodeRelevantToExport(IIGameNode maxGameNode)
		{
			bool isRelevantToExport;
			switch (maxGameNode.IGameObject.IGameType)
			{
				case Autodesk.Max.IGameObject.ObjectTypes.Mesh:
					isRelevantToExport = IsMeshExportable(maxGameNode);
					break;
				case Autodesk.Max.IGameObject.ObjectTypes.Camera:
					isRelevantToExport = IsCameraExportable(maxGameNode);
					break;
				case Autodesk.Max.IGameObject.ObjectTypes.Light:
					isRelevantToExport = IsLightExportable(maxGameNode);
					break;
				default:
					isRelevantToExport = IsNodeExportable(maxGameNode);
					break;
			}

			return isRelevantToExport;
		}

		private bool IsNodeExportable(IIGameNode gameNode)
		{
			if (exportParameters is MaxExportParameters)
			{
				MaxExportParameters maxExporterParameters = (exportParameters as MaxExportParameters);
				if (maxExporterParameters.ExportLayers !=null && maxExporterParameters.ExportLayers.Count > 0)
				{
					if (!maxExporterParameters.ExportLayers.HaveNode(gameNode.MaxNode))
					{
						return false;
					}
				}
			}

			if ((exportParameters.exportOnlySelected || exportParameters.exportAsSubmodel) && !gameNode.MaxNode.Selected)
			{
				return false;
			}

			if (gameNode.MaxNode.GetBoolProperty("babylonjs_noexport"))
			{
				return false;
			}

			if (gameNode.MaxNode.IsBabylonContainerHelper() || gameNode.MaxNode.IsBabylonAnimationHelper())
			{
				return false;
			}

			
			if (!exportParameters.exportHiddenObjects && gameNode.MaxNode.IsHidden(NodeHideFlags.None, false))
			{
				return false;
			}

			return true;
		}

		BabylonNode GetRootParent(BabylonNode node, BabylonScene scene)
		{
			if (node.parentId == null)
				return node;

			if (scene.NodeMap.ContainsKey(node.parentId))
				return GetRootParent(scene.NodeMap[node.parentId], scene);

			return null;
		}

		string GetRootParentID(string parentId, Dictionary<string, IIGameNode> allSceneNodes)
		{
			if (parentId == null)
				return null;

			if (allSceneNodes.ContainsKey(parentId))
			{
				if (allSceneNodes[parentId].NodeParent == null)
					return allSceneNodes[parentId].MaxNode.GetGuid().ToString();

				string newParentId = allSceneNodes[parentId].NodeParent.MaxNode.GetGuid().ToString();
				return GetRootParentID(newParentId, allSceneNodes);
			}

			return null;
		}

		private List<IIGameNode> GetDescendants(IIGameNode maxGameNode)
		{
			var maxDescendants = new List<IIGameNode>();
			for (int i = 0; i < maxGameNode.ChildCount; i++)
			{
				maxDescendants.Add(maxGameNode.GetNodeChild(i));
			}
			return maxDescendants;
		}

		private HashSet<IIGameNode> GetRootNodes(IIGameScene maxGameScene)
		{
			HashSet<IIGameNode> maxGameNodes = new HashSet<IIGameNode>();

			Func<IIGameNode, IIGameNode> getMaxRootNode = delegate (IIGameNode maxGameNode)
			{
				while (maxGameNode.NodeParent != null)
				{
					maxGameNode = maxGameNode.NodeParent;
				}
				return maxGameNode;
			};

			Action<Autodesk.Max.IGameObject.ObjectTypes> addMaxRootNodes = delegate (Autodesk.Max.IGameObject.ObjectTypes type)
			{
				ITab<IIGameNode> maxGameNodesOfType = maxGameScene.GetIGameNodeByType(type);
				if (maxGameNodesOfType != null)
				{
					TabToList(maxGameNodesOfType).ForEach(maxGameNode =>
					{
						var maxRootNode = getMaxRootNode(maxGameNode);
						maxGameNodes.Add(maxRootNode);
					});
				}
			};

			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Mesh);
			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Light);
			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Camera);
			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Helper);

			return maxGameNodes;
		}
		private HashSet<IIGameNode> GetSubModelsRootNodes(IIGameScene maxGameScene)
		{
			HashSet<IIGameNode> maxGameNodes = new HashSet<IIGameNode>();

			Func<IIGameNode, IIGameNode> getMaxRootNode = delegate (IIGameNode maxGameNode)
			{
				while (maxGameNode.NodeParent != null && maxGameNode.NodeParent.MaxNode.Selected == true)
				{
					maxGameNode = maxGameNode.NodeParent;
				}
				return maxGameNode;
			};

			Action<Autodesk.Max.IGameObject.ObjectTypes> addMaxRootNodes = delegate (Autodesk.Max.IGameObject.ObjectTypes type)
			{
				ITab<IIGameNode> maxGameNodesOfType = maxGameScene.GetIGameNodeByType(type);
				if (maxGameNodesOfType != null)
				{
					TabToList(maxGameNodesOfType).ForEach(maxGameNode =>
					{
						if (maxGameNode.MaxNode.Selected) 
						{
							var maxRootNode = getMaxRootNode(maxGameNode);
							maxGameNodes.Add(maxRootNode);
						}
						
					});
				}
			};

			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Mesh);
			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Light);
			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Camera);
			addMaxRootNodes(Autodesk.Max.IGameObject.ObjectTypes.Helper);

			return maxGameNodes;
		}

		private static List<T> TabToList<T>(ITab<T> tab)
		{
			if (tab == null)
			{
				return null;
			}
			else
			{
				List<T> list = new List<T>();
				for (int i = 0; i < tab.Count; i++)
				{
#if MAX2017 || MAX2018 || MAX2019 || MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
					var item = tab[i];
#else
					var item = tab[new IntPtr(i)];
#endif
					list.Add(item);
				}
				return list;
			}
		}

		private IMatrix3 GetInvertWorldTM(IIGameNode gameNode, int key)
		{
			var worldMatrix = gameNode.GetWorldTM(key);
			var invertedWorldMatrix = worldMatrix.ExtractMatrix3();
			invertedWorldMatrix.Invert();
			return invertedWorldMatrix;
		}
		private IMatrix3 GetOffsetTM(IIGameNode gameNode, int key)
		{
			IPoint3 objOffsetPos = gameNode.MaxNode.ObjOffsetPos;
			IQuat objOffsetQuat = gameNode.MaxNode.ObjOffsetRot;
			IPoint3 objOffsetScale = gameNode.MaxNode.ObjOffsetScale.S;

			// conversion: LH vs RH coordinate system (swap Y and Z)
			var tmpSwap = objOffsetPos.Y;
			objOffsetPos.Y = objOffsetPos.Z;
			objOffsetPos.Z = tmpSwap;

			tmpSwap = objOffsetQuat.Y;
			objOffsetQuat.Y = objOffsetQuat.Z;
			objOffsetQuat.Z = tmpSwap;
			var objOffsetRotMat = Tools.Identity;
			objOffsetQuat.MakeMatrix(objOffsetRotMat, true);

			tmpSwap = objOffsetScale.Y;
			objOffsetScale.Y = objOffsetScale.Z;
			objOffsetScale.Z = tmpSwap;

			// build the offset transform; equivalent in maxscript: 
			// offsetTM = (scaleMatrix $.objectOffsetScale) * ($.objectOffsetRot as matrix3) * (transMatrix $.objectOffsetPos)
			IMatrix3 offsetTM = Tools.Identity;
			offsetTM.Scale(objOffsetScale, false);
			offsetTM.MultiplyBy(objOffsetRotMat);
			offsetTM.Translate(objOffsetPos); 

			return offsetTM;
		}

		/// <summary>
		/// In 3DS Max default element can look in different direction than the same default element in Babylon or in glTF.
		/// This function correct the node rotation.
		/// </summary>
		/// <param name="node"></param>
		/// <param name="babylonScene"></param>
		/// <param name="angle"></param>
		private void FixNodeRotation(ref BabylonNode node, ref BabylonScene babylonScene, double angle)
		{
			string id = node.id;
			IList<BabylonNode> childs = babylonScene.NodeMap.Values.ToList<BabylonNode>().FindAll(sceneNode => sceneNode.parentId == null ? false : sceneNode.parentId.Equals(id));

			logger?.Print($"Fix node rotation for: {node.name}", Color.Black);

			// fix the vue
			// Rotation around the axis X of PI / 2 in the indirect direction for camera
			// double angle = Math.PI / 2; // for camera
			// double angle = -Math.PI / 2; // for light

			if (node.rotation != null)
			{
				node.rotation[0] += (float)angle;
			}
			if (node.rotationQuaternion != null)
			{
				BabylonQuaternion rotationQuaternion = FixCameraQuaternion(node, angle);

				node.rotationQuaternion = rotationQuaternion.ToArray();
				node.rotation = rotationQuaternion.toEulerAngles().ToArray();
			}

			// animation
			List<BabylonAnimation> animations = new List<BabylonAnimation>(node.animations);
			BabylonAnimation animationRotationQuaternion = animations.Find(animation => animation.property.Equals("rotationQuaternion"));
			if (animationRotationQuaternion != null)
			{
				foreach (BabylonAnimationKey key in animationRotationQuaternion.keys)
				{
					key.values = FixCameraQuaternion(key.values, angle);
				}
			}
			else   // if the camera has a lockedTargetId, it is the extraAnimations that stores the rotation animation
			{
				if (node.extraAnimations != null)
				{
					List<BabylonAnimation> extraAnimations = new List<BabylonAnimation>(node.extraAnimations);
					animationRotationQuaternion = extraAnimations.Find(animation => animation.property.Equals("rotationQuaternion"));
					if (animationRotationQuaternion != null)
					{
						foreach (BabylonAnimationKey key in animationRotationQuaternion.keys)
						{
							key.values = FixCameraQuaternion(key.values, angle);
						}
					}
				}
			}

			// fix direct children
			// Rotation around the axis X of -PI / 2 in the direct direction for camera children
			angle = -angle;
			foreach (var child in childs)
			{
				logger?.RaiseVerbose($"{child.name}", 3);
				child.position = new float[] { child.position[0], -child.position[2], child.position[1] };

				// Add a rotation of PI/2 axis X in direct direction
				if (child.rotationQuaternion != null)
				{
					// Rotation around the axis X of -PI / 2 in the direct direction
					BabylonQuaternion quaternion = FixChildQuaternion(child, angle);

					child.rotationQuaternion = quaternion.ToArray();
				}
				if (child.rotation != null)
				{
					child.rotation[0] += (float)angle;
				}


				// Animations
				if (child.animations != null)
				{
					animations = new List<BabylonAnimation>(child.animations);
					// Position
					BabylonAnimation animationPosition = animations.Find(animation => animation.property.Equals("position"));
					if (animationPosition != null)
					{
						foreach (BabylonAnimationKey key in animationPosition.keys)
						{
							key.values = new float[] { key.values[0], -key.values[2], key.values[1] };
						}
					}
				}

				// Rotation
				animationRotationQuaternion = animations.Find(animation => animation.property.Equals("rotationQuaternion"));
				if (animationRotationQuaternion != null)
				{
					foreach (BabylonAnimationKey key in animationRotationQuaternion.keys)
					{
						key.values = FixChildQuaternion(key.values, angle);
					}
				}
			}

		}
		// This is a duplicate from ExportTransform() in BabylonExporter.Mesh.cs
		private BabylonMatrix GetMaxNodeTransform(ref IIGameNode maxGameNode)
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
			var newQ = new[] { q_babylon.X / q_length, q_babylon.Y / q_length, q_babylon.Z / q_length, q_babylon.W / q_length };
			q_babylon.X = newQ[0];
			q_babylon.Y = newQ[1];
			q_babylon.Z = newQ[2];
			q_babylon.W = newQ[3];

			return BabylonMatrix.Compose(s_babylon, q_babylon, t_babylon);
		}
		private BabylonMatrix GetNodeTransform(ref BabylonNode node)
		{
			var nodeTransform = BabylonMatrix.Compose(
				BabylonVector3.FromArray(node.scaling),
				BabylonQuaternion.FromArray(node.rotationQuaternion),
				BabylonVector3.FromArray(node.position)
			);
			return nodeTransform;
		}
		// Move
		private void MoveNodeTransform(ref BabylonNode node, BabylonMatrix transform)
		{
			var nodeTransform = GetNodeTransform(ref node);
			var newTransform = nodeTransform * transform;

			var translationBabylon = new BabylonVector3();
			var rotationQuatBabylon = new BabylonQuaternion();
			var scaleBabylon = new BabylonVector3();
			newTransform.decompose(scaleBabylon, rotationQuatBabylon, translationBabylon);

			node.scaling = scaleBabylon.ToArray();
			node.rotationQuaternion = rotationQuatBabylon.ToArray();
			node.position = translationBabylon.ToArray();

			if (node.animations == null) return;
	
			List<BabylonAnimation> animations = new List<BabylonAnimation>(node.animations);
			BabylonAnimation animationMatrix = animations.Find(animation => animation.property.Equals("_matrix"));
			if (animationMatrix != null)
			{
				foreach (BabylonAnimationKey key in animationMatrix.keys)
				{
					var keyTransform = new BabylonMatrix();
					keyTransform.m = key.values;
					key.values = (keyTransform * transform).m;
				}
			}
			BabylonAnimation animationPosition = animations.Find(animation => animation.property.Equals("position"));
			if (animationPosition != null)
			{
				foreach (BabylonAnimationKey key in animationPosition.keys)
				{
					var keyPosition = new BabylonVector3(
						key.values[0],
						key.values[1],
						key.values[2]);
					var keyTransform = BabylonMatrix.Translation(keyPosition);
					keyTransform = keyTransform * transform;
					BabylonVector3 s_babylon = new BabylonVector3();
					BabylonQuaternion q_babylon = new BabylonQuaternion();
					BabylonVector3 t_babylon = new BabylonVector3();
					keyTransform.decompose(s_babylon, q_babylon, t_babylon);
					key.values = new float[] {
						t_babylon.X,
						t_babylon.Y,
						t_babylon.Z };
				}
			}
			BabylonAnimation animationRotation = animations.Find(animation => animation.property.Equals("rotationQuaternion"));
			if (animationRotation != null)
			{
				foreach (BabylonAnimationKey key in animationRotation.keys)
				{
					var keyRotation = new BabylonQuaternion(
						key.values[0],
						key.values[1],
						key.values[2],
						key.values[3]);
					var keyTransform = BabylonMatrix.Compose(new BabylonVector3(1, 1, 1), keyRotation, new BabylonVector3(0, 0, 0));
					keyTransform = keyTransform * transform;
					BabylonVector3 s_babylon = new BabylonVector3();
					BabylonQuaternion q_babylon = new BabylonQuaternion();
					BabylonVector3 t_babylon = new BabylonVector3();
					keyTransform.decompose(s_babylon, q_babylon, t_babylon);
					key.values = new float[] {
						q_babylon.X,
						q_babylon.Y,
						q_babylon.Z,
						q_babylon.W };
				}
			}
			BabylonAnimation animationScale = animations.Find(animation => animation.property.Equals("scaling"));
			if (animationScale != null)
			{
				foreach (BabylonAnimationKey key in animationScale.keys)
				{
					var keyScale = new BabylonVector3(
						key.values[0],
						key.values[1],
						key.values[2]);
					var keyTransform = BabylonMatrix.Compose(keyScale, new BabylonQuaternion(0, 0, 0, 1), new BabylonVector3(0, 0, 0));
					keyTransform = keyTransform * transform;
					BabylonVector3 s_babylon = new BabylonVector3();
					BabylonQuaternion q_babylon = new BabylonQuaternion();
					BabylonVector3 t_babylon = new BabylonVector3();
					keyTransform.decompose(s_babylon, q_babylon, t_babylon);
					key.values = new float[] {
						s_babylon.X,
						s_babylon.Y,
						s_babylon.Z };
				}
			}
		}
		// Set
		private void SetNodeTransform(ref BabylonNode node, BabylonMatrix newTransform)
		{
			var translationBabylon = new BabylonVector3();
			var rotationQuatBabylon = new BabylonQuaternion();
			var scaleBabylon = new BabylonVector3();
			newTransform.decompose(scaleBabylon, rotationQuatBabylon, translationBabylon);

			var nodeTransform = GetNodeTransform(ref node);

			node.scaling = scaleBabylon.ToArray();
			node.rotationQuaternion = rotationQuatBabylon.ToArray();
			node.position = translationBabylon.ToArray();

			if (node.animations == null) return;

			var nodeTransformInvert = nodeTransform.invert();

			List<BabylonAnimation> animations = new List<BabylonAnimation>(node.animations);
			BabylonAnimation animationMatrix = animations.Find(animation => animation.property.Equals("_matrix"));
			if (animationMatrix != null)
			{
				foreach (BabylonAnimationKey key in animationMatrix.keys)
				{
					var keyTransform = new BabylonMatrix();
					keyTransform.m = key.values;
					key.values = (keyTransform * nodeTransformInvert * newTransform).m;
				}
			}
			BabylonAnimation animationPosition = animations.Find(animation => animation.property.Equals("position"));
			if (animationPosition != null)
			{
				foreach (BabylonAnimationKey key in animationPosition.keys)
				{
					var keyPosition = new BabylonVector3(
						key.values[0],
						key.values[1],
						key.values[2] );
					var keyTransform = BabylonMatrix.Translation(keyPosition);
					keyTransform = keyTransform * nodeTransformInvert * newTransform;
					BabylonVector3 s_babylon = new BabylonVector3();
					BabylonQuaternion q_babylon = new BabylonQuaternion();
					BabylonVector3 t_babylon = new BabylonVector3();
					keyTransform.decompose(s_babylon, q_babylon, t_babylon);
					key.values = new float[] {
						t_babylon.X,
						t_babylon.Y,
						t_babylon.Z };
				}
			}
			BabylonAnimation animationRotation = animations.Find(animation => animation.property.Equals("rotationQuaternion"));
			if (animationRotation != null)
			{
				foreach (BabylonAnimationKey key in animationRotation.keys)
				{
					var keyRotation = new BabylonQuaternion(
						key.values[0],
						key.values[1],
						key.values[2],
						key.values[3] );
					var keyTransform = BabylonMatrix.Compose(new BabylonVector3(1, 1, 1), keyRotation, new BabylonVector3(0, 0, 0));
					keyTransform = keyTransform * nodeTransformInvert * newTransform;
					BabylonVector3 s_babylon = new BabylonVector3();
					BabylonQuaternion q_babylon = new BabylonQuaternion();
					BabylonVector3 t_babylon = new BabylonVector3();
					keyTransform.decompose(s_babylon, q_babylon, t_babylon);
					key.values = new float[] {
						q_babylon.X,
						q_babylon.Y,
						q_babylon.Z,
						q_babylon.W };
				}
			}
			BabylonAnimation animationScale = animations.Find(animation => animation.property.Equals("scaling"));
			if (animationScale != null)
			{
				foreach (BabylonAnimationKey key in animationScale.keys)
				{
					var keyScale = new BabylonVector3(
						key.values[0],
						key.values[1],
						key.values[2] );
					var keyTransform = BabylonMatrix.Compose(keyScale, new BabylonQuaternion(0, 0, 0, 1), new BabylonVector3(0, 0, 0));
					keyTransform = keyTransform * nodeTransformInvert * newTransform;
					BabylonVector3 s_babylon = new BabylonVector3();
					BabylonQuaternion q_babylon = new BabylonQuaternion();
					BabylonVector3 t_babylon = new BabylonVector3();
					keyTransform.decompose(s_babylon, q_babylon, t_babylon);
					key.values = new float[] {
						s_babylon.X,
						s_babylon.Y,
						s_babylon.Z };
				}
			}
		}
		private void SetNodePosition(ref BabylonNode node, float[] newPosition)
		{
			float[] offset = new float[] { newPosition[0] - node.position[0], newPosition[1] - node.position[1], newPosition[2] - node.position[2] };
			node.position = newPosition;

			if (node.animations == null) return;

			List<BabylonAnimation> animations = new List<BabylonAnimation>(node.animations);
			BabylonAnimation animationPosition = animations.Find(animation => animation.property.Equals("position"));
			if (animationPosition != null)
			{
				foreach (BabylonAnimationKey key in animationPosition.keys)
				{
					key.values = new float[] {
						key.values[0] + offset[0],
						key.values[1] + offset[1],
						key.values[2] + offset[2] };
				}
			}
		}

		private List<BabylonNode> SetRootNodesForBaseModel(IIGameScene gameScene, IINode exportNode, bool fromPresetPanel, BabylonScene babylonScene, ExportParameters exportParameters, HashSet<IIGameNode> maxRootNodes)
		{
			List<BabylonNode> result = new List<BabylonNode>();
			foreach (IIGameNode maxRootNode in maxRootNodes)
			{
				if(isGltfExported && exportParameters.animationExportType == AnimationExportType.ExportOnly)
				{
					CalculateSkeletonList(maxRootNode, babylonScene, gameScene);
				}
				else
				{
					BabylonNode node = ExportNodeRec(maxRootNode, babylonScene, gameScene, fromPresetPanel, true);
					if (node != null) result.Add(node);
				}
			}
			return result;
		}
		private List<BabylonNode> SetRootNodesForSubmodel(IIGameScene gameScene, bool fromPresetPanel, BabylonScene babylonScene, ExportParameters exportParameters, HashSet<IIGameNode> maxRootNodes)
		{
			List<BabylonNode> result = new List<BabylonNode>();

			// Calculate a map containing id of node and associated maxnode
			Dictionary<string, IIGameNode> allSceneNodes = new Dictionary<string, IIGameNode>();
			foreach (IIGameNode maxRootNode in maxRootNodes)
			{
				CreateBabylonSceneNodesRec(maxRootNode, allSceneNodes, fromPresetPanel);
			}

			//Init root nodes
			List<BabylonNode> copyRootNodes = new List<BabylonNode>();
			maxRootNodes = GetSubModelsRootNodes(gameScene);

			foreach (IIGameNode maxRootNode in maxRootNodes)
			{
				if (isGltfExported && exportParameters.animationExportType == AnimationExportType.ExportOnly)
				{
					CalculateSkeletonList(maxRootNode, babylonScene, gameScene);
				}
				else
				{
					// In case the skin has one or more bones that are not part of the submodel hierarchy
					BabylonNode subModelRoot = CalculateSubModelBonesDependencies(maxRootNode, babylonScene, gameScene);
					BabylonNode node = ExportNodeRec(maxRootNode, babylonScene, gameScene, fromPresetPanel);

					if (node != null)
					{
						if (subModelRoot == null)
						{
							// in case the skin has all the skinned nodes in the submodel child hierarchy
							// in case it is not a mesh 
							// in case it is not skinned
							subModelRoot = node;
						}

						if (!result.Any(x => x.id == subModelRoot.id)) result.Add(subModelRoot);
					}
				}
			}

			copyRootNodes.AddRange(result);

			// If exported as submodel and we need to keep only the common ancesstor for the skin meshs
			foreach (BabylonNode node in copyRootNodes)
			{
				if (result.Any(x => x.id == node.id))
				{
					List<BabylonNode> childRootNodes = new List<BabylonNode>();
					foreach (var root in result)
					{
						if (root.parentId != null)
						{
							string newParentId = GetRootParentID(root.parentId, allSceneNodes);

							if (newParentId != null && newParentId == node.id)
							{
								childRootNodes.Add(root);
							}
						}
					}
					if (childRootNodes.Count > 0)
					{
						foreach (var child in childRootNodes)
						{
							result.Remove(child);
						}
					}
				}
			}
			return result;
		}

		private void CreateBabylonSceneNodesRec(IIGameNode maxRootNode, Dictionary<string, IIGameNode> allSceneNodes, bool fromPresetPanel = false)
		{
			if (fromPresetPanel && !allSceneNodes.ContainsKey(maxRootNode.MaxNode.GetGuid().ToString()))
			{
				allSceneNodes.Add(maxRootNode.MaxNode.GetGuid().ToString(), maxRootNode);
				// add the children
				for (int i = 0; i < maxRootNode.ChildCount; i++)
				{
					var descendant = maxRootNode.GetNodeChild(i);
					CreateBabylonSceneNodesRec(descendant, allSceneNodes, fromPresetPanel);
				}
			}
		}

		private bool ExportBabylonExtension<T1>(T1 sceneObject,Type babylonType, ref BabylonScene babylonScene)
		{
			foreach (var extensionExporter in babylonScene.BabylonToGLTFExtensions)
			{
				if (extensionExporter.Value.babylonType == babylonType)
				{
				   if(extensionExporter.Key.ExportBabylonExtension(sceneObject,ref babylonScene,this)) return true;
				}
			}

			return false;
		}
	}

	
}
