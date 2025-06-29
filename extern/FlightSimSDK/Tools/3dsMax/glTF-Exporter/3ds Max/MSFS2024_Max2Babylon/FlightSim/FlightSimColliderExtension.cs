using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using Autodesk.Max;
using Babylon2GLTF;
using BabylonExport.Entities;
using GLTFExport.Entities;
using MSFS2024_Max2Babylon.FlightSim;

namespace MSFS2024_Max2Babylon.FlightSimExtension
{
	enum AsoboTag
	{
		Collision,
		Road,
		SkinBoundingVolume
	}

	[DataContract]
	class GLTFExtensionAsoboTags : GLTFProperty
	{
		public const string SerializedName = "ASOBO_tags";
		[DataMember]
		public List<string> tags { get; set; }
	}

	[DataContract]
	class GLTFExtensionAsoboGizmo : GLTFProperty
	{
		[DataMember(Name = "gizmo_objects")]
		public List<GLTFExtensionGizmo> gizmos { get; set; }
	}

	[DataContract]
	class GLTFExtensionGizmo : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false, Name = "type")] public string Type { get; set; }
		[DataMember(EmitDefaultValue = false, Name = "translation")] public object Translation;
		[DataMember(EmitDefaultValue = false, Name = "rotation")] public object Rotation;
		[DataMember(Name = "params")] public object Params { get; set; }
	}

	[DataContract]
	class GLTFExtensionAsoboBoxParams : GLTFProperty
	{

		[DataMember(EmitDefaultValue = false)] public float? width;
		[DataMember(EmitDefaultValue = false)] public float? height;
		[DataMember(EmitDefaultValue = false)] public float? length;
	}

	[DataContract]
	class GLTFExtensionAsoboSphereParams : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false)] public float? radius;
	}

	[DataContract]
	class GLTFExtensionAsoboCylinderParams : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false)] public float? radius;
		[DataMember(EmitDefaultValue = false)] public float? height;
	}


	class FlightSimColliderExtension : IBabylonExtensionExporter
	{
		readonly MaterialUtilities.ClassIDWrapper MSFS2020_BoxColliderClassID = new MaterialUtilities.ClassIDWrapper(0x231f3b1a, 0x5a974704);
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_BoxColliderClassID = new MaterialUtilities.ClassIDWrapper(0x5ea2c852, 0x69be16a0);

		readonly MaterialUtilities.ClassIDWrapper MSFS2020_CylinderColliderClassID = new MaterialUtilities.ClassIDWrapper(0x7c242166, 0x5dbf7d08);
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_CylinderColliderClassID = new MaterialUtilities.ClassIDWrapper(0x53759d0f, 0x661b0fbd);

		readonly MaterialUtilities.ClassIDWrapper MSFS2020_SphereColliderClassID = new MaterialUtilities.ClassIDWrapper(0x736e21e7, 0x45da3199);
		readonly MaterialUtilities.ClassIDWrapper MSFS2024_SphereColliderClassID = new MaterialUtilities.ClassIDWrapper(0x72af43fb, 0x6b664a01);

		#region Implementation of IBabylonExtensionExporter

		public string GetGLTFExtensionName()
		{
			return "ASOBO_gizmo_object";
		}

		public ExtendedTypes GetExtendedType()
		{
			return new ExtendedTypes(typeof(GLTFMesh));
		}

		public bool ExportBabylonExtension<T>(T babylonObject, ref BabylonScene babylonScene, BabylonExporter exporter)
		{
			// just skip this extension is ment only for GLTF
			return false;
		}

		public bool IsMSFS2024BoxCollider(IObject obj)
		{
			bool isMSFS2024BoxCollider = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_BoxColliderClassID);
			return isMSFS2024BoxCollider;
		}

		public bool IsMSFS2024CylinderCollider(IObject obj)
		{
			bool isMSFS2024CylinderCollider = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_CylinderColliderClassID);
			return isMSFS2024CylinderCollider;
		}

		public bool IsMSFS2024SphereCollider(IObject obj)
		{
			bool isMSFS2024SphereCollider = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2024_SphereColliderClassID);
			return isMSFS2024SphereCollider;
		}

		public bool IsMSFS2020BoxCollider(IObject obj)
		{
			bool isMSFS2020BoxCollider = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2020_BoxColliderClassID);
			return isMSFS2020BoxCollider;
		}

		public bool IsMSFS2020CylinderCollider(IObject obj)
		{
			bool isMSFS2020CylinderCollider = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2020_CylinderColliderClassID);
			return isMSFS2020CylinderCollider;
		}

		public bool IsMSFS2020SphereCollider(IObject obj)
		{
			bool isMSFS2020SphereCollider = new MaterialUtilities.ClassIDWrapper(obj.ClassID).Equals(MSFS2020_SphereColliderClassID);
			return isMSFS2020SphereCollider;
		}

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			var logger = exporter.logger;
			if (babylonObject is BabylonMesh babylonMesh)
			{
				GLTFExtensionAsoboGizmo gltfExtensionAsoboGizmo = new GLTFExtensionAsoboGizmo();
				List<GLTFExtensionGizmo> collisions = new List<GLTFExtensionGizmo>();
				gltfExtensionAsoboGizmo.gizmos = collisions;

				Guid.TryParse(babylonMesh.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);
				foreach (IINode node in maxNode.DirectChildren())
				{
					IObject obj = node.ObjectRef;
					List<AsoboTag> tags = new List<AsoboTag>();
					GLTFExtensionGizmo gizmo = new GLTFExtensionGizmo();

					if (IsMSFS2024BoxCollider(obj))
					{
						GLTFExtensionAsoboBoxParams boxParams = new GLTFExtensionAsoboBoxParams();
						float height = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "BoxGizmo", "height");
						float width = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "BoxGizmo", "width");
						float length = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "BoxGizmo", "length");
						gizmo.Translation = FlightSimExtensionUtility.GetTranslation(node, maxNode);
						float[] rotation = FlightSimExtensionUtility.GetRotation(node, maxNode);
						if (!FlightSimExtensionUtility.IsDefaultRotation(rotation))
						{
							gizmo.Rotation = rotation;
						}

						boxParams.width = width;
						boxParams.height = height;
						boxParams.length = length;

						gizmo.Params = boxParams;
						gizmo.Type = "box";

						bool isRoad = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "BoxCollider", "IsRoad", IsSubClass: false);
						bool isCollision = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "BoxCollider", "IsCollider", IsSubClass: false);

						if (isCollision) tags.Add(AsoboTag.Collision);
						if (isRoad) tags.Add(AsoboTag.Road);

						ParseTags(ref gizmo, ref gltf, ref tags);
						collisions.Add(gizmo);

					}
					else if (IsMSFS2024CylinderCollider(obj))
					{
						GLTFExtensionAsoboCylinderParams cylinderParams = new GLTFExtensionAsoboCylinderParams();
						float radius = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "CylGizmo", "radius");
						float height = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "CylGizmo", "height");
						gizmo.Translation = FlightSimExtensionUtility.GetTranslation(node, maxNode);
						float[] rotation = FlightSimExtensionUtility.GetRotation(node, maxNode);
						if (!FlightSimExtensionUtility.IsDefaultRotation(rotation))
						{
							gizmo.Rotation = rotation;
						}
						cylinderParams.height = height;
						cylinderParams.radius = radius;
						gizmo.Params = cylinderParams;
						gizmo.Type = "cylinder";

						bool isRoad = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "CylCollider", "IsRoad", IsSubClass: false);
						bool isCollision = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "CylCollider", "IsCollider", IsSubClass: false);

						if (isCollision) tags.Add(AsoboTag.Collision);
						if (isRoad) tags.Add(AsoboTag.Road);

						ParseTags(ref gizmo, ref gltf, ref tags);
						collisions.Add(gizmo);
					}
					else if (IsMSFS2024SphereCollider(obj))
					{
						GLTFExtensionAsoboSphereParams sphereParams = new GLTFExtensionAsoboSphereParams();
						float radius = FlightSimExtensionUtility.GetGizmoParameterFloat(node, "SphereGizmo", "radius");
						gizmo.Translation = FlightSimExtensionUtility.GetTranslation(node, maxNode);
						sphereParams.radius = radius;
						gizmo.Type = "sphere";
						gizmo.Params = sphereParams;

						bool isRoad = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "SphereCollider", "IsRoad", IsSubClass: false);
						bool isCollision = FlightSimExtensionUtility.GetGizmoParameterBoolean(node, "SphereCollider", "IsCollider", IsSubClass: false);

						if (isCollision) tags.Add(AsoboTag.Collision);
						if (isRoad) tags.Add(AsoboTag.Road);

						ParseTags(ref gizmo, ref gltf, ref tags);
						collisions.Add(gizmo);
					}
					else if (IsMSFS2020BoxCollider(obj) || IsMSFS2020CylinderCollider(obj) || IsMSFS2020SphereCollider(obj))
					{
						string message = $"[GLTFExporter][ERROR][Collisions] Object class of {node.Name} has been set up with MSFS2020 tools.";
						throw new System.Exception(message);
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
			GLTFExtensionAsoboTags asoboTagsExtension = new GLTFExtensionAsoboTags
			{
				tags = tags.ConvertAll(x => x.ToString())
			};

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
