using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using Autodesk.Max;
using Babylon2GLTF;
using BabylonExport.Entities;
using GLTFExport.Entities;

namespace BabylonExport.Entities
{
	public partial class BabylonNode
	{
		private string _uniqueId;
		public string UniqueID
		{
			get
			{
				if (string.IsNullOrWhiteSpace(_uniqueId))
				{
					return name;
				}

				return _uniqueId;
			}
			set => _uniqueId = value;
		}
	}

}

namespace Babylon2GLTF
{
	#region Serializable glTF Objects

	[DataContract]
	class GLTFExtensionASBUniqueID : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false)]
		public string id { get; set; }
	}

	#endregion

	public partial class GLTFExporter
	{
		private const string AsoboUniqueID = "ASOBO_unique_id";

		public void ASOBOUniqueIDExtension(ref GLTF gltf, ref GLTFNode gltfNode, BabylonNode babylonNode)
		{
			GLTFExtensionASBUniqueID extensionObject = new GLTFExtensionASBUniqueID
			{
				id = babylonNode.UniqueID
			};

			if (gltfNode != null)
			{
				if (gltfNode.extensions == null)
				{
					gltfNode.extensions = new GLTFExtensions();
				}
				gltfNode.extensions[AsoboUniqueID] = extensionObject;
			}

			if (gltf.extensionsUsed == null)
			{
				gltf.extensionsUsed = new List<string>();
			}
			if (!gltf.extensionsUsed.Contains(AsoboUniqueID))
			{
				gltf.extensionsUsed.Add(AsoboUniqueID);
			}
		}
	}

}


namespace MSFS2024_Max2Babylon.FlightSimExtension
{
	class AsoboUniqueIDExtension : IBabylonExtensionExporter
	{
		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_unique_id";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFScene));
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			if (!exporter.exportParameters.exportAsSubmodel) return null;

			BabylonScene babylonScene = babylonObject as BabylonScene;
			GLTFScene gltfScene = gltfObject as GLTFScene;
			Dictionary<string, GLTFScene> scenes = new Dictionary<string, GLTFScene>();

			GLTFExtensionASBUniqueID uniqueIDext = null;
			foreach (BabylonNode rootNode in babylonScene.RootNodes)
			{
				GLTFNode subSceneGltfRoot = exporter.nodeToGltfNodeMap.First(n => n.Key.id == rootNode.id).Value;
				int subSceneRootIndex = subSceneGltfRoot.index;

				GLTFScene subScene = new GLTFScene();
				subScene.NodesList.Add(subSceneRootIndex);

				Guid subSceneRootGUID = new Guid(rootNode.id);
				IINode maxNode = Tools.GetINodeByGuid(subSceneRootGUID);

				if (!maxNode.IsRootNode)
				{
					string subSceneParentId = maxNode.ParentNode.GetUniqueID();
					uniqueIDext = new GLTFExtensionASBUniqueID
					{
						id = subSceneParentId
					};

					if (!uniqueIDext.id.Equals("Scene Root"))
						subScene.extensions.Add(GetGLTFExtensionName(), uniqueIDext);
				};

				if (uniqueIDext != null)
				{
					if (scenes.ContainsKey(uniqueIDext.id))
					{
						if (scenes[uniqueIDext.id] == null)
						{
							scenes[uniqueIDext.id] = new GLTFScene
							{
								extensions = subScene.extensions
							};
						}

						scenes[uniqueIDext.id].NodesList.AddRange(subScene.NodesList);

					}
					else
					{
						scenes.Add(uniqueIDext.id, subScene);
					}
				}
			}

			GLTFScene[] subScenes = new GLTFScene[scenes.Count()];
			int i = 0;
			foreach (var key in scenes.Keys)
			{
				subScenes[i] = scenes[key];
				i++;
			}

			if (subScenes.Length > 0) gltf.scenes = subScenes;

			return uniqueIDext;

		}
		#endregion

	}
}
