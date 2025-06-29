using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Runtime.Serialization;
using Autodesk.Max;
using Babylon2GLTF;
using BabylonExport.Entities;
using GLTFExport.Entities;

namespace Babylon2GLTF
{
	#region Serializable glTF Objects

	[DataContract]
	class GLTFExtensionAsoboSoftBodies : GLTFProperty
	{
		[DataMember(EmitDefaultValue = false)]
		public string type { get; set; }
	}

	#endregion
}

namespace MSFS2024_Max2Babylon.FlightSimExtension
{
	class FlightSimSoftBodiesExtension : IBabylonExtensionExporter
	{
		#region Implementation of IBabylonExtensionExporter

		public ReadOnlyCollection<string> Types { get { return new List<string> { "balloon" }.AsReadOnly(); } }

		public string GetGLTFExtensionName()
		{
			return "ASOBO_softbody_mesh";
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

		public object ExportGLTFExtension<T1, T2>(T1 babylonObject, ref T2 gltfObject, ref GLTF gltf, GLTFExporter exporter, ExtensionInfo extInfo)
		{
			if (babylonObject is BabylonMesh babylonMesh)
			{
				Guid.TryParse(babylonMesh.id, out Guid guid);
				IINode maxNode = Tools.GetINodeByGuid(guid);

				string userProp = string.Empty;
				if (maxNode != null && maxNode.GetUserPropString("IsSoftBody", ref userProp))
				{
					string AsoboSoftBodyExtension = GetGLTFExtensionName();
					GLTFExtensionAsoboSoftBodies gltfExtensionAsoboSoftBody = new GLTFExtensionAsoboSoftBodies();
					if (Types.Contains(userProp.ToLower()))
					{
						gltfExtensionAsoboSoftBody.type = userProp; // Other than balloons to be added to the Types list
					}
					else
						gltfExtensionAsoboSoftBody.type = "balloon";

					if (gltf.extensionsUsed == null)
					{
						gltf.extensionsUsed = new List<string>();
					}

					if (!gltf.extensionsUsed.Contains(AsoboSoftBodyExtension))
					{
						gltf.extensionsUsed.Add(AsoboSoftBodyExtension);
					}

					return gltfExtensionAsoboSoftBody;
				}
			}
			return null;
		}

		#endregion
	}
}
