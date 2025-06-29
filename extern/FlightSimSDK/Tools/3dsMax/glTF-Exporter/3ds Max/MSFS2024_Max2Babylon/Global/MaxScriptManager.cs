using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using BabylonExport.Entities;
using Utilities;
using Autodesk.Max;
using FlightSimExtension;

namespace MSFS2024_Max2Babylon
{
	public class MaxScriptManager
	{
		public static void RunResolveUniqueID()
		{
			BabylonResolveUniqueIDActionItem resolve = new BabylonResolveUniqueIDActionItem();
			resolve.ExecuteAction();
		}

		public static void Export(MaxExportParameters exportParameters, ILoggingProvider _logger)
		{
			if (Loader.Class_ID == null)
			{
				Loader.AssemblyMain();
			}
			// Check output format is valid
			List<string> validFormats = new List<string>(new string[] { "babylon", "binary babylon", "gltf", "glb" });
			if (!validFormats.Contains(exportParameters.outputFormat))
			{
				Autodesk.Max.GlobalInterface.Instance.TheListener.EditStream.Printf("ERROR - Valid output formats are: "+ validFormats.ToArray().ToString(true) + "\n");
				return;
			}
		   
			BabylonExporter exporter = new BabylonExporter(_logger);

			// Start export
			exporter.Export(exportParameters);
		}

		public static void InitializeGuidTable()
		{
			Tools.InitializeGuidsMap();
		}

		//leave the possibility to get the output path from the babylon exporter with all the settings previously-saved
		public static MaxExportParameters InitParameters(string outputPath)
		{
			MaxExportParameters exportParameters = new MaxExportParameters
			{
				outputPath = outputPath,
				outputFormat = Path.GetExtension(outputPath)?.Substring(1),
				exportHiddenObjects = Loader.Core.RootNode.GetBoolProperty("babylonjs_exporthidden"),
				exportAsSubmodel = Loader.Core.RootNode.GetBoolProperty("flightsim_exportAsSubmodel"),
				autoSaveSceneFile = Loader.Core.RootNode.GetBoolProperty("babylonjs_autosave"),
				exportOnlySelected = Loader.Core.RootNode.GetBoolProperty("babylonjs_onlySelected"),
				exportTangents = Loader.Core.RootNode.GetBoolProperty("babylonjs_exporttangents"),
				scaleFactor = float.TryParse(Loader.Core.RootNode.GetStringProperty("babylonjs_txtScaleFactor", "1"), out float scaleFactor) ? scaleFactor : 1,
				txtQuality = long.TryParse(Loader.Core.RootNode.GetStringProperty("babylonjs_txtCompression", "100"), out long txtQuality) ? txtQuality : 100,
				mergeAOwithMR = Loader.Core.RootNode.GetBoolProperty("babylonjs_mergeAOwithMR"),
				dracoCompression = Loader.Core.RootNode.GetBoolProperty("babylonjs_dracoCompression"),
				enableKHRLightsPunctual = Loader.Core.RootNode.GetBoolProperty("babylonjs_khrLightsPunctual"),
				enableKHRTextureTransform = Loader.Core.RootNode.GetBoolProperty("babylonjs_khrTextureTransform"),
				enableKHRMaterialsUnlit = Loader.Core.RootNode.GetBoolProperty("babylonjs_khr_materials_unlit"),
				exportMaterials = Loader.Core.RootNode.GetBoolProperty("babylonjs_export_materials"),

				exportMorphTangents = Loader.Core.RootNode.GetBoolProperty("babylonjs_export_Morph_Tangents"),
				exportMorphNormals = Loader.Core.RootNode.GetBoolProperty("babylonjs_export_Morph_Normals"),
				usePreExportProcess = Loader.Core.RootNode.GetBoolProperty("babylonjs_preproces"),
				mergeContainersAndXRef = Loader.Core.RootNode.GetBoolProperty("babylonjs_mergecontainersandxref"),
				flattenNodes = Loader.Core.RootNode.GetBoolProperty("flightsim_flattenNodes"),
				applyPreprocessToScene = Loader.Core.RootNode.GetBoolProperty("babylonjs_applyPreprocess"),

				pbrFull = Loader.Core.RootNode.GetBoolProperty(ExportParameters.PBRFullPropertyName),
				pbrNoLight = Loader.Core.RootNode.GetBoolProperty(ExportParameters.PBRNoLightPropertyName),
				exportNode = null,

				animationExportType = (AnimationExportType)Loader.Core.RootNode.GetFloatProperty("babylonjs_export_animations_type", 0),
				enableASBUniqueID = Loader.Core.RootNode.GetBoolProperty("flightsim_asb_unique_id", 1),

				removeLodPrefix = Loader.Core.RootNode.GetBoolProperty("flightsim_removelodprefix"),
				tangentSpaceConvention = (TangentSpaceConvention)Loader.Core.RootNode.GetFloatProperty("flightsim_tangent_space_convention", 0),
				bakeAnimationType = (BakeAnimationType)Loader.Core.RootNode.GetFloatProperty("babylonjs_bakeAnimationsType", 0),
				keepInstances = Loader.Core.RootNode.GetBoolProperty("flightsim_keepInstances", 1),

				logLevel = (LogLevel)Loader.Core.RootNode.GetFloatProperty("babylonjs_logLevel", 1)
			};

			return exportParameters;
		}

		public static void DisableBabylonAutoSave()
		{
			Loader.Core.RootNode.SetUserPropBool("babylonjs_autosave",false);
		}

		public static void ImportAnimationGroups(string jsonPath)
		{
			AnimationGroupList animationGroups = new AnimationGroupList();
			var fileStream = File.Open(jsonPath, FileMode.Open);

			using (StreamReader reader = new StreamReader(fileStream))
			{
				string jsonContent = reader.ReadToEnd();
				animationGroups.LoadFromJson(jsonContent);
			}
		}

		public static void MergeAnimationGroups(string jsonPath)
		{
			AnimationGroupList animationGroups = new AnimationGroupList();
			var fileStream = File.Open(jsonPath, FileMode.Open);

			using (StreamReader reader = new StreamReader(fileStream))
			{
				string jsonContent = reader.ReadToEnd();
				animationGroups.LoadFromJson(jsonContent,true);
			}
		}

		public static void MergeAnimationGroups(string jsonPath, string old_root, string new_root)
		{
			AnimationGroupList animationGroups = new AnimationGroupList();
			var fileStream = File.Open(jsonPath, FileMode.Open);

			using (StreamReader reader = new StreamReader(fileStream))
			{
				string jsonContent = reader.ReadToEnd();
				string textToFind = string.Format(@"\b{0}\b", old_root);
				string overridedJsonContent = Regex.Replace(jsonContent, textToFind, new_root);
				animationGroups.LoadFromJson(overridedJsonContent, true);
			}
		}

		public AnimationGroup GetAnimationGroupByName(string name)
		{
			AnimationGroupList animationGroupList = new AnimationGroupList();
			animationGroupList.LoadFromData();

			foreach (AnimationGroup animationGroup in animationGroupList)
			{
				if (animationGroup.Name == name)
				{
					return animationGroup;
				}
			}

			return null;
		}

		public void AutoAssignLodInAnimationGroup()
		{
			AnimationGroupList animationGroupList = new AnimationGroupList();
			animationGroupList.LoadFromData();

			var nodes = Loader.Core.RootNode.NodeTree();

			List<IINode> nodeToAdd = new List<IINode>();
			foreach (AnimationGroup anim in animationGroupList)
			{
				nodeToAdd.Clear();
				foreach (Guid guid in anim.NodeGuids)
				{
					IINode n = Tools.GetINodeByGuid(guid);
					if (n == null) continue;    
					if(!Regex.IsMatch(n.Name, "(?i)x[0-9]_")) continue;
					string noLodName = n.Name.Substring(3);
					foreach (IINode node in nodes)
					{
						if(Regex.IsMatch(node.Name,$"(?i)x[0-9]_{noLodName}$"))
						{
							nodeToAdd.Add(node);
						}
					}
				}

				foreach (IINode n in nodeToAdd)
				{
					List<Guid> newGuids = anim.NodeGuids.ToList();
					newGuids.Add(n.GetGuid());
					anim.NodeGuids = newGuids;
				}
				anim.SaveToData();
			}
		}

		public AnimationGroup CreateAnimationGroup()
		{
			AnimationGroupList animationGroupList = new AnimationGroupList();
			animationGroupList.LoadFromData();

			AnimationGroup info = new AnimationGroup();

			// get a unique name and guid
			string baseName = info.Name;
			int i = 0;
			bool hasConflict = true;
			while (hasConflict)
			{
				hasConflict = false;
				foreach (AnimationGroup animationGroup in animationGroupList)
				{
					if (info.Name.Equals(animationGroup.Name))
					{
						info.Name = baseName + i.ToString();
						++i;
						hasConflict = true;
						break;
					}
					if (info.SerializedId.Equals(animationGroup.SerializedId))
					{
						info.SerializedId = Guid.NewGuid();
						hasConflict = true;
						break;
					}
				}
			}

			// save info and animation list entry
			animationGroupList.Add(info);
			animationGroupList.SaveToData();
			Loader.Global.SetSaveRequiredFlag(true, false);
			return info;
		}

		public string RenameAnimationGroup(AnimationGroup info,string name)
		{
			AnimationGroupList animationGroupList = new AnimationGroupList();
			animationGroupList.LoadFromData();

			AnimationGroup animGroupToRename = animationGroupList.GetAnimationGroupByName(info.Name);

			string baseName = name;
			int i = 0;
			bool hasConflict = true;
			while (hasConflict)
			{
				hasConflict = false;
				foreach (AnimationGroup animationGroup in animationGroupList)
				{
					if (baseName.Equals(animationGroup.Name))
					{
						baseName = name + i.ToString();
						++i;
						hasConflict = true;
						break;
					}
				}
			}

			animGroupToRename.Name = baseName;

			// save info and animation list entry
			animationGroupList.SaveToData();
			Loader.Global.SetSaveRequiredFlag(true, false);
			return baseName;
		}

		public void AddNodeInAnimationGroup(AnimationGroup info, uint nodeHandle)
		{
			if (info == null)
				return;

			IINode node = Loader.Core.GetINodeByHandle(nodeHandle);
			if (node == null)
			{
				return;
			}

			List<Guid> newGuids = info.NodeGuids.ToList();
			newGuids.Add(node.GetGuid());
			info.NodeGuids = newGuids;
			info.SaveToData();
		}

		public int GetTimeRange(AnimationGroup info)
		{
			return Tools.CalculateEndFrameFromAnimationGroupNodes(info);
		}

		public void SetAnimationGroupTimeRange(AnimationGroup info, int start,int end)
		{
			if (info == null)
				return;

			info.FrameStart = start;
			info.FrameEnd = end;
			info.SaveToData();
		}

		public void RemoveAllNodeFromAnimationGroup(AnimationGroup info)
		{
			if (info == null)
				return;

			info.NodeGuids = new List<Guid>();
			info.SaveToData();
		}

		public void RemoveNodeFromAnimationGroup(AnimationGroup info, uint nodeHandle)
		{
			if (info == null)
				return;

			IINode node = Loader.Core.GetINodeByHandle(nodeHandle);
			if (node == null)
			{
				return;
			}

			List<Guid> newGuids = info.NodeGuids.ToList();
			newGuids.Remove(node.GetGuid());
			info.NodeGuids = newGuids;
			info.SaveToData();
		}

		public void ExecuteLoadAnimationAction()
		{
			var loadAnimationAction = new BabylonLoadAnimations();
			loadAnimationAction.ExecuteAction();
		}

		public void InitGUID(IntPtr matHandle)
		{
			try
			{
				IAnimatable mat = Loader.Global.Animatable.GetAnimByHandle((UIntPtr)(int)matHandle);
				Guid uid = Guid.NewGuid();
				Tools.SetMaterialProperty((IMtl)mat, "guid", uid.ToString());
			}
			catch (System.Exception ex)
			{
				Autodesk.Max.GlobalInterface.Instance.TheListener.EditStream.Printf(ex.Message);
			}
			
		}
	}
}
