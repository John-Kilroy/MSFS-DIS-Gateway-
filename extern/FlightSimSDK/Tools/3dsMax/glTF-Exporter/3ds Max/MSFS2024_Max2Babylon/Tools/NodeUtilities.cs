using Autodesk.Max;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
namespace MSFS2024_Max2Babylon 
{
	public static partial class Tools 
	{
		public static IEnumerable<IINode> DirectChildren(this IINode node)
		{
			List<IINode> children = new List<IINode>();
			for (int i = 0; i < node.NumberOfChildren; ++i)
				if (node.GetChildNode(i) != null)
					children.Add(node.GetChildNode(i));
			return children;
		}

		public static IEnumerable<IINode> Nodes(this IINode node)
		{
			for (int i = 0; i < node.NumberOfChildren; ++i)
				if (node.GetChildNode(i) != null)
					yield return node.GetChildNode(i);
		}

		public static IEnumerable<IINode> SelectedNodes(this IINode node)
		{
			for (int i = 0; i < node.NumberOfChildren; ++i)
				if (node.GetChildNode(i) != null && node.GetChildNode(i).Selected)
					yield return node.GetChildNode(i);
		}

		public static IEnumerable<IINode> SelectedNodeTree(this IINode node)
		{
			foreach (var x in node.SelectedNodes())
			{
				yield return x;
				foreach (var y in x.SelectedNodeTree())
					yield return y;
			}
		}

		public static IEnumerable<IINode> NodeTree(this IINode node)
		{
			foreach (var x in node.Nodes())
			{
				yield return x;
				foreach (var y in x.NodeTree())
					yield return y;
			}
		}

		public static IINodeTab CreateNodeTab() 
		{
#if MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
			IINodeTab nodeTab = Loader.Global.INodeTab.Create();
#else
			IINodeTab nodeTab = Loader.Global.INodeTabNS.Create();
#endif
			return nodeTab;
		}

		public static IINodeTab Join(this IINodeTab nodeTab, IINodeTab other)
		{
			foreach (IINode node in other.ToIEnumerable())
			{
				nodeTab.AppendNode(node,false,0);
			}
			return nodeTab;
		}

		public static IINodeTab GetAncestors(this IINodeTab nodeTab) 
		{
#if MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
			IINodeTab ancestors = Loader.Global.INodeTab.Create();
#else
			IINodeTab ancestors = Loader.Global.INodeTabNS.Create();
#endif
			foreach (IINode node in nodeTab.ToIEnumerable())
			{
				if (!nodeTab.Contains(node.ParentNode)) ancestors.InsertNode(node,0,false);
			}
			return ancestors;
		}

		public static IEnumerable<IINode> NodesListBySuperClass(this IINode rootNode, SClass_ID sid)
		{
			return from n in rootNode.NodeTree() where n.ObjectRef != null && n.EvalWorldState(0, false).Obj.SuperClassID == sid select n;
		}

		public static IEnumerable<IINode> NodesListBySuperClasses(this IINode rootNode, SClass_ID[] sids)
		{
			return from n in rootNode.NodeTree() where n.ObjectRef != null && sids.Any(sid => n.EvalWorldState(0, false).Obj.SuperClassID == sid) select n;
		}

		public static IINode FindChildNode(this IINode node, uint nodeHandle)
		{
			foreach (IINode childNode in node.NodeTree())
				if (childNode.Handle.Equals(nodeHandle))
					return childNode;

			return null;
		}

		public static IINode FindChildNode(this IINode node, string nodeName)
		{
			foreach (IINode childNode in node.NodeTree())
				if (childNode.Name == nodeName)
					return childNode;

			return null;
		}

		public static IINode FindChildNode(this IINode node, Guid nodeGuid)
		{
			foreach (IINode childNode in node.NodeTree())
				if (childNode.GetGuid().Equals(nodeGuid))
					return childNode;

			return null;
		}

		public static bool IsNodeTreeAnimated(this IINode node)
		{
			if (node.IsAnimated) return true;
			foreach (IINode n in node.NodeTree())
			{
				if (n.IsAnimated) return true;
			}

			return false;
		}

		public static bool IsMeshTree(this IINode node)
		{
			foreach (var y in node.Nodes())
			{
				if (!y.IsMesh()) return false;
			}
			return true;
		}

		public static bool IsSkinned(this IINode node)
		{
			if (!(node.ActualINode.ObjectRef is IIDerivedObject derivedObject))
			{
				return false;
			}

			for (int index = 0; index < derivedObject.NumModifiers; index++)
			{
				IModifier modifier = derivedObject.GetModifier(index);
				if (modifier.ClassID.PartA == 9815843 && modifier.ClassID.PartB == 87654) // Skin
				{
					return true;
				}
			}

			return false;
		}

		public static IISkin GetSkinModifier(this IINode node)
		{
			var obj = node.ObjectRef;

			if (obj.SuperClassID != SClass_ID.GenDerivob)
			{
				return null;
			}

			var derivedObject = obj as IIDerivedObject;

			if (derivedObject == null)
			{
				return null;
			}

			for (var index = 0; index < derivedObject.NumModifiers; index++)
			{
				var modifier = derivedObject.GetModifier(index);

				if (modifier.ClassID.PartA == 9815843 && modifier.ClassID.PartB == 87654) // Skin
				{
					var skin = modifier.GetInterface((InterfaceID)0x00010000) as IISkin;

					return skin;
				}
			}


			return null;
		}

		public static List<IINode> GetINodeSkinnedBones(this IINode node) 
		{
			List<IINode> skinnedNodes = new List<IINode>();
			if (!node.IsSkinned()) return null;
			IISkin skin  = node.GetSkinModifier();
			for (int i = 0; i < skin.NumBones; i++)
			{
				IINode bone = skin.GetBone(i);
				skinnedNodes.Add(bone);
			}
			return skinnedNodes;
		}

		public static IIContainerObject GetContainer(this IList<Guid> guids)
		{
			foreach (Guid guid in guids)
			{
				IINode node = GetINodeByGuid(guid);
				IIContainerObject containerObject = Loader.Global.ContainerManagerInterface.IsInContainer(node);
				if (containerObject != null)
				{
					return containerObject;
				}
			}
			return null;
		}

		public static IIContainerObject GetContainer(this IList<uint> handles)
		{
			foreach (uint handle in handles)
			{
				IINode node = Loader.Core.GetINodeByHandle(handle);
				IIContainerObject containerObject = Loader.Global.ContainerManagerInterface.IsInContainer(node);
				if (containerObject != null)
				{
					return containerObject;
				}
			}
			return null;
		}

		public static List<IIContainerObject> GetContainerInSelection()
		{
#if MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
			IINodeTab selection = Loader.Global.INodeTab.Create();
#else
			IINodeTab selection = Loader.Global.INodeTabNS.Create();
#endif
			Loader.Core.GetSelNodeTab(selection);
			List<IIContainerObject> selectedContainers = new List<IIContainerObject>();

			for (int i = 0; i < selection.Count; i++)
			{
#if MAX2015 || MAX2016
				var selectedNode = selection[(IntPtr)i];
#else
				var selectedNode = selection[i];
#endif

				IIContainerObject containerObject = Loader.Global.ContainerManagerInterface.IsContainerNode(selectedNode);
				if (containerObject != null)
				{
					selectedContainers.Add(containerObject);
				}
			}

			return selectedContainers;
		}

		public static IIContainerObject InSameContainer(this IList<Guid> guids)
		{
			List<IIContainerObject> containers = new List<IIContainerObject>();
			foreach (Guid guid in guids)
			{
				IINode node = GetINodeByGuid(guid);
				IIContainerObject containerObject = Loader.Global.ContainerManagerInterface.IsInContainer(node);
				if (containerObject != null)
				{
					if (!containers.Contains(containerObject))
					{
						containers.Add(containerObject);
					}
				}
			}

			if (containers.Count == 1)
			{
				return containers[0];
			}
			return null;
		}

		public static List<IIContainerObject> GetAllContainers()
		{
			List<IIContainerObject> containersList = new List<IIContainerObject>();
			foreach (IINode node in Loader.Core.RootNode.NodeTree())
			{
				IIContainerObject containerObject = Loader.Global.ContainerManagerInterface.IsContainerNode(node);
				if (containerObject != null)
				{
					containersList.Add(containerObject);
				}
			}
			return containersList;
		}

		public static List<IINode> ContainerNodeTree(this IINode containerNode, bool includeSubContainer)
		{
			List<IINode> containersChildren = new List<IINode>();

			foreach (IINode x in containerNode.Nodes())
			{
				IIContainerObject nestedContainerObject = Loader.Global.ContainerManagerInterface.IsContainerNode(x);
				if (nestedContainerObject != null)
				{
					if (includeSubContainer)
					{
						containersChildren.AddRange(ContainerNodeTree(nestedContainerObject.ContainerNode, includeSubContainer));
					}
				}
				else
				{
					containersChildren.Add(x);
					containersChildren.AddRange(ContainerNodeTree(x, includeSubContainer));
				}
			}

			return containersChildren;
		}

		private static int GetNextAvailableContainerID(this IIContainerObject container)
		{
			int id = 1;
			string guidStr = container.ContainerNode.GetStringProperty("babylonjs_GUID", Guid.NewGuid().ToString());
			List<IIContainerObject> containers = GetAllContainers();
			foreach (IIContainerObject othersContainer in containers)
			{
				if (container.ContainerNode.Handle == othersContainer.ContainerNode.Handle) continue;
				//string compareGuid = iContainerObject.ContainerNode.GetStringProperty("babylonjs_GUID",Guid.NewGuid().ToString());
				string otherName = Regex.Replace(othersContainer.ContainerNode.Name, @"_\d+", "");
				string originalName = Regex.Replace(container.ContainerNode.Name, @"_\d+", "");
				if (otherName == originalName)
				{
					int containerID = 1;
					othersContainer.ContainerNode.GetUserPropInt("babylonjs_ContainerID", ref containerID);
					id = Math.Max(id, containerID + 1);
				}
			}
			return id;
		}

		public static void ResolveContainer(this IIContainerObject container)
		{
			guids = new Dictionary<Guid, IAnimatable>();
			int id = container.GetNextAvailableContainerID();
			container.ContainerNode.SetUserPropInt("babylonjs_ContainerID", id);

		}

		public static IINode BabylonAnimationHelper()
		{
			IINode babylonHelper = null;
			foreach (IINode directChild in Loader.Core.RootNode.DirectChildren())
			{
				if (directChild.IsBabylonAnimationHelper())
				{
					babylonHelper = directChild;
				}
			}

			if (babylonHelper == null)
			{
				IDummyObject dummy = Loader.Global.DummyObject.Create();
				babylonHelper = Loader.Core.CreateObjectNode(dummy, $"BabylonAnimationHelper_{Random.Next(0, 99999)}");
				babylonHelper.SetUserPropBool("babylonjs_AnimationHelper", true);
			}

			return babylonHelper;
		}

		public static IINode BabylonContainerHelper(this IIContainerObject containerObject)
		{
			IINode babylonHelper = null;
			foreach (IINode directChild in containerObject.ContainerNode.DirectChildren())
			{
				if (directChild.IsBabylonContainerHelper())
				{
					babylonHelper = directChild;
				}
			}

			if (babylonHelper == null)
			{
				IDummyObject dummy = Loader.Global.DummyObject.Create();
				babylonHelper = Loader.Core.CreateObjectNode(dummy, $"BabylonContainerHelper_{Random.Next(0, 99999)}");
				babylonHelper.SetUserPropBool("babylonjs_ContainerHelper", true);

				Loader.Core.SetQuietMode(true);
				containerObject.ContainerNode.AttachChild(babylonHelper, false);
				Loader.Core.SetQuietMode(false);
				containerObject.AddNodeToContent(babylonHelper);
			}
			return babylonHelper;
		}

		public static bool IsBabylonAnimationHelper(this IINode node)
		{
			return node.GetBoolProperty("babylonjs_AnimationHelper");
		}

		public static bool IsBabylonContainerHelper(this IINode node)
		{
			//to keep retrocompatibility
			if (node.Name == "BabylonAnimationHelper")
			{
				node.Name = $"BabylonContainerHelper_{Random.Next(0, 99999)}";
				node.SetUserPropBool("babylonjs_ContainerHelper", true);
			}

			return node.GetBoolProperty("babylonjs_ContainerHelper");
		}

		public static void UnloadAllContainers()
		{
			foreach (IIContainerObject iContainerObject in GetAllContainers())
			{
				_ = iContainerObject.UnloadContainer;
			}
		}

		public static bool IsNodeSelected(this IINode node)
		{
#if MAX2020 || MAX2021 || MAX2022 || MAX2023 || MAX2024
			IINodeTab selection = Loader.Global.INodeTab.Create();
#else
			IINodeTab selection = Loader.Global.INodeTabNS.Create();
#endif
			Loader.Core.GetSelNodeTab(selection);
			return selection.Contains(node);
		}

		public static bool IsMarkedAsNotFlattenable(this IINode node)
		{
			return node.GetBoolProperty("babylonjs_DoNotFlatten");
		}


		public static bool IsMarkedAsObjectToBakeAnimation(this IINode node)
		{
			return node.GetBoolProperty("babylonjs_BakeAnimation", 0);
		}

		/// <summary>
		/// Converts the ITab to a more convenient IEnumerable.
		/// </summary>
		public static IEnumerable<T> ToIEnumerable<T>(this ITab<T> tab)
		{
#if MAX2015 || MAX2016
					for (int i = 0; i < tab.Count; i++)
					{
						yield return tab[(IntPtr)i];
					}
#else
			for (int i = 0; i < tab.Count; i++)
			{
				yield return tab[i];
			}
#endif

		}

		/// <summary>
		/// Generates a new list with only distinct items preserving original ordering.
		/// </summary>
		/// <typeparam name="T"></typeparam>
		/// <param name="list"></param>
		/// <param name="comparer"></param>
		/// <returns></returns>
		public static IList<T> ToUniqueList<T>(this IList<T> list, IEqualityComparer<T> comparer = null)
		{
			bool Contains(T x) => comparer == null ? list.Contains(x) : list.Contains(x, comparer);

			return list.Where(entity => !Contains(entity)).ToList();
		}

		public static string GetUniqueID(this IINode node) 
		{
			return node.GetStringProperty("flightsim_uniqueID", node.Name);
		}

		public static IINode CreateMergedMesh(this IINode node, string layerName)
		{
			string newNodeName = node.Name + Random.Next(1, 100000);
			
			ScriptsUtilities.ExecuteMaxScriptCommand($"groupNode = maxOps.getNodeByHandle {node.Handle}");
			ScriptsUtilities.ExecuteMaxScriptCommand($@"MSFS2024_Functions.flattenHierarchy groupNode flattenedParentNodeName:""{newNodeName}"" needMeshParent:true layerName:""{layerName}"""); // You can find this function in MSFS2024_Functions.ms
            IINode newNode = Loader.Core.GetINodeByName(newNodeName);

			if (newNode != null)
			{
				string userProps = "";
				node.GetUserPropBuffer(ref userProps);
				newNode.SetUserPropBuffer(userProps);
				newNode.SetUserPropBool("flatten_mergedMesh", true);
				newNode.Name = node.Name;
			}

			return newNode;
		}

		public static void DeleteHierarchyNodes(this IINode node)
		{
			ScriptsUtilities.ExecuteMaxScriptCommand($"groupNode = maxOps.getNodeByHandle {node.Handle}");
			ScriptsUtilities.ExecuteMaxScriptCommand($@"MSFS2024_Functions.deleteHierarchyNodes groupNode"); // You can find this function in MSFS2024_Functions.ms
		}
    }
}
