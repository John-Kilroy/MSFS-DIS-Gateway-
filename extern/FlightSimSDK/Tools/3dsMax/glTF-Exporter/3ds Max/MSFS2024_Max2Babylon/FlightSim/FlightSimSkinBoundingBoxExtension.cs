using System;
using System.Collections.Generic;
using Autodesk.Max;
using Babylon2GLTF;
using BabylonExport.Entities;
using GLTFExport.Entities;
using MSFS2024_Max2Babylon.FlightSim;

namespace MSFS2024_Max2Babylon.FlightSimExtension
{
	/*
	 * Extension for the sphere Bounding Volume attached to nodes
	 */
	class FlightSimSkinBoundingBoxExtension : IBabylonExtensionExporter
	{
		readonly MaterialUtilities.ClassIDWrapper MSFS20204_old_SphereBoundingVolumeClassID = new MaterialUtilities.ClassIDWrapper(0x4afc6f92, 0x6580db0e);
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_SphereBoundingVolumeClassID = new MaterialUtilities.ClassIDWrapper(0x78ee0ad7, 0x3caa0738);

		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_gizmo_object";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFNode), typeof(GLTFNode));
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public bool IsSphereBoundingVolume(IObject obj)
		{
			bool isMSFS2024_old_SphereBoundingVolume = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS20204_old_SphereBoundingVolumeClassID);
			bool isMSFS2024SphereBoundingVolume = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_SphereBoundingVolumeClassID);
			return isMSFS2024SphereBoundingVolume || isMSFS2024_old_SphereBoundingVolume;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			if (babylonObject is BabylonNode babylonNode)
			{
				GLTFExtensionAsoboGizmo gltfExtensionAsoboGizmo = new GLTFExtensionAsoboGizmo();
				List<GLTFExtensionGizmo> collisions = new List<GLTFExtensionGizmo>();
				gltfExtensionAsoboGizmo.gizmos = collisions;

				Guid.TryParse(babylonNode.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);
				foreach (IINode node in maxNode.DirectChildren())
				{
					IObject obj = node.ObjectRef;
					List<AsoboTag> tags = new List<AsoboTag>();
					GLTFExtensionGizmo gizmo = new GLTFExtensionGizmo();
					if (IsSphereBoundingVolume(obj))
					{
						GLTFExtensionAsoboSphereParams sphereParams = new GLTFExtensionAsoboSphereParams();
						float radius = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "SphereGizmo", "radius");
						gizmo.Translation = FlightSimExtensionUtility.GetTranslation(node, maxNode);
						sphereParams.radius = radius;
						gizmo.Type = "sphere";
						gizmo.Params = sphereParams;

						bool isSkinBoundingVolume = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "SphereCollider", "IsSkinBoundingVolume", IsSubClass: false);

						if (isSkinBoundingVolume) tags.Add(AsoboTag.SkinBoundingVolume);

						ParseTags(ref gizmo, ref gltf, ref tags);
						collisions.Add(gizmo);
					}
				}

				if (collisions.Count > 0)
				{
					return gltfExtensionAsoboGizmo;
				}
			}
			return null;
		}

		void ParseTags(ref GLTFExtensionGizmo gizmo, ref GLTF gltf, ref List<AsoboTag> tags)
		{
			GLTFExtensionAsoboTags asoboTagsExtension = new GLTFExtensionAsoboTags();
			asoboTagsExtension.tags = tags.ConvertAll(x => x.ToString());
			if (tags.Count > 0)
			{
				if (gizmo.extensions == null) gizmo.extensions = new GLTFExtensions();
				gizmo.extensions.Add(GLTFExtensionAsoboTags.SerializedName, asoboTagsExtension);

				if (gltf.extensionsUsed == null) gltf.extensionsUsed = new List<string>();
				if (!gltf.extensionsUsed.Contains(GLTFExtensionAsoboTags.SerializedName))
				{
					gltf.extensionsUsed.Add(GLTFExtensionAsoboTags.SerializedName);
				}
			}
		}

		#endregion
	}
}
