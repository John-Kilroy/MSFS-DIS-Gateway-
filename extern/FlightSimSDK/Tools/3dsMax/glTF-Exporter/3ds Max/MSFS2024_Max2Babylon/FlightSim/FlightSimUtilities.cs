using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using Autodesk.Max;

namespace MSFS2024_Max2Babylon.FlightSim
{
	static class FlightSimUtilities
	{
		public static bool ExportItemHasClosedContainers(IINode itemRootNode)
		{
			if (itemRootNode == null)
			{
				itemRootNode = Loader.Core.RootNode;
			}

			List<IINode> nodesList = new List<IINode>();
			nodesList.Add(itemRootNode);

			nodesList.AddRange(itemRootNode.NodeTree().ToList());


			foreach (var node in nodesList)
			{
				IIContainerObject containerNode = Loader.Global.ContainerManagerInterface.IsContainerNode(node);

				if (containerNode != null && !containerNode.IsOpen)
				{
					MessageBox.Show("You are tring to export a CLOSED Container\nUse the Container Manager");
					return true;
				}
			}

			return false;
		}
	}

	public static class FlightSimCameraUtilities
	{
		public static readonly MaterialUtilities.ClassIDWrapper class_ID = new MaterialUtilities.ClassIDWrapper(4098, 0);

		public static bool IsMSFSCamera(IINode camera)
		{
			return camera != null && class_ID.Equals(camera.ClassID);
		}
	}

	public static class FlightSimMaterialUtilities
	{
		public static readonly MaterialUtilities.ClassIDWrapper MSFS2020_classID = new MaterialUtilities.ClassIDWrapper(0x5ac74889, 0x27e705cd);
		public static readonly MaterialUtilities.ClassIDWrapper MSFS2024_classID = new MaterialUtilities.ClassIDWrapper(0x627be308, 0x1c79568e);

		public static bool IsMSFS2024Material(IMtl mat)
		{
			return mat != null && MSFS2024_classID.Equals(mat.ClassID);
		}

		public static bool IsMSFS2020Material(IMtl mat)
		{
			return mat != null && MSFS2020_classID.Equals(mat.ClassID);
		}

		public static bool HasMSFS2024Materials(IMtl mat)
		{
			if (mat.IsMultiMtl)
			{
				for (int i = 0; i < mat.NumSubMtls; i++)
				{
					IMtl childMat = mat.GetSubMtl(i);
					if (IsMSFS2024Material(childMat))
					{
						return true;
					}
				}
			}
			else if (IsMSFS2024Material(mat))
			{
				return true;
			}


			return false;
		}

		public static bool HasRuntimeAccess(IMtl mat)
		{
			if (mat.IsMultiMtl)
			{
				for (int i = 0; i < mat.NumSubMtls; i++)
				{
					IMtl childMat = mat.GetSubMtl(i);
					if (IsMSFS2024Material(childMat))
					{
						int p = Tools.GetIntMaterialProperty(childMat, "uniqueInContainer");
						if (Convert.ToBoolean(p))
						{
							return true;
						}
					}
				}
			}
			else if (IsMSFS2024Material(mat))
			{
				int p = Tools.GetIntMaterialProperty(mat, "uniqueInContainer");
				if (Convert.ToBoolean(p))
				{
					return true;
				}
			}
			return false;
		}
	}
}